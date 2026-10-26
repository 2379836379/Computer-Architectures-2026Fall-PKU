#!/usr/bin/env python3
"""Evaluate my_perceptron inside an existing ChampSim environment.

Cache bimodal baseline/<trace-name>.json files; simulate only missing/stale entries.
Build the candidate once, run traces concurrently, and print {"score": ...}.
Uses only Python's standard library. See auto-run.README.md for data layout.
"""
from __future__ import annotations

import argparse
import copy
from contextlib import contextmanager
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

WARMUP_INSTRUCTIONS = 2_000_000
SIMULATION_INSTRUCTIONS = 100_000_000
EPSILON = 1e-12
BRANCH_TRACES = (
    "pred-1-1.champsimtrace.xz", "pred-1-2.champsimtrace.xz",
    "pred-2-1.champsimtrace.xz", "pred-2-2.champsimtrace.xz",
    "pred-2-3.champsimtrace.xz", "pred-2-4.champsimtrace.xz",
    "pred-2-5.champsimtrace.xz", "pred-2-6.champsimtrace.xz",
    "pred-3-1.champsimtrace.xz", "pred-4.champsimtrace.xz",
    "pred-5.champsimtrace.xz", "pred-6.champsimtrace.xz",
    "403.gcc-48B.champsimtrace.xz", "657.xz_s-56B.champsimtrace.xz",
)
NUMBER = r"[0-9.+\-eE]+"


def progress(message):
    print(message, file=sys.stderr, flush=True)


def nonnegative_mpki(value, source):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"MPKI must be numeric: {source}")
    value = float(value)
    if not math.isfinite(value) or value < 0:
        raise ValueError(f"MPKI must be finite and nonnegative: {source}")
    return value


def parse_branch_mpki(output):
    """Read the last simulation ROI, not warmup or intermediate statistics."""
    if "ChampSim completed all CPUs" not in output:
        raise ValueError("ChampSim did not report completion")
    if "Region of Interest Statistics" not in output:
        raise ValueError("Missing Region of Interest Statistics")
    roi = output.rsplit("Region of Interest Statistics", 1)[1]
    matches = re.findall(
        rf"CPU\s+0\s+Branch Prediction Accuracy:[^\n]*?MPKI:\s*({NUMBER})", roi
    )
    if not matches:
        raise ValueError("Cannot find CPU 0 branch MPKI in the final ROI")
    return nonnegative_mpki(float(matches[-1]), "candidate ROI")


@contextmanager
def file_lock(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def digest_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix="." + path.name, dir=path.parent)
    try:
        with os.fdopen(fd, "w") as handle:
            json.dump(data, handle, indent=2, allow_nan=False)
            handle.write("\n")
        Path(name).replace(path)
    finally:
        Path(name).unlink(missing_ok=True)


def configuration(args, predictor):
    path = args.config
    if path is None:
        path = next((args.root / name for name in ("lab2_config.json", "branch_config.json")
                     if (args.root / name).is_file()), None)
    if path:
        config = json.loads(path.read_text())
    else:
        config = {"ooo_cpu": [{"frequency": 4000, "rob_size": 352,
                               "btb": "basic_btb", "mispredict_penalty": 15}]}
    if not isinstance(config, dict):
        raise ValueError("Configuration must contain one JSON object")
    config = copy.deepcopy(config)
    cores = config.setdefault("ooo_cpu", [{}])
    if config.get("num_cores", 1) != 1 or not isinstance(cores, list) or len(cores) != 1 or not isinstance(cores[0], dict):
        raise ValueError("Evaluation requires a single-core configuration")
    cores[0]["branch_predictor"] = predictor
    if "branch_predictor" in config:
        config["branch_predictor"] = predictor
    config.pop("executable_name", None)
    return config


def baseline_source_digest(root):
    # Candidate BP edits must never invalidate the bimodal baseline cache.
    digest = hashlib.sha256()
    files = []
    for name in ("inc", "src", "config", "branch/bimodal", "btb", "prefetcher", "replacement"):
        folder = root / name
        if folder.is_dir():
            files.extend(p for p in folder.rglob("*") if p.is_file() and p.suffix in (".h", ".cc", ".py", ".options"))
    files.extend(root / n for n in ("Makefile", "global.options", "module.options", "vcpkg.json", "config.sh") if (root / n).is_file())
    for path in sorted(files):
        digest.update(str(path.relative_to(root)).encode())
        digest.update(b"\0")
        digest.update(bytes.fromhex(digest_file(path)))
    digest.update(os.environ.get("CXX", "g++").encode())
    return digest.hexdigest()


def baseline_metadata(args, config):
    common = {"version": 1, "predictor": "bimodal", "warmup_instructions": args.warmup,
              "simulation_instructions": args.simulation, "configuration": config,
              "source_sha256": baseline_source_digest(args.root)}
    return {trace: dict(common, trace_sha256=digest_file(args.trace_dir / trace)) for trace in args.traces}


def cached_mpki(path, metadata, trust_legacy=False):
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text())
        if not isinstance(data, dict):
            return None
        value = nonnegative_mpki(data["mpki"], path)
        if data.get("metadata") == metadata:
            return value
        # Preserve compatibility with files from the supplied original generator.
        if "metadata" not in data and trust_legacy:
            for key in ("warmup_instructions", "simulation_instructions"):
                if key in data and data[key] != metadata[key]:
                    return None
            progress(f"[BASELINE] Reusing legacy baseline without fingerprint: {path.name}")
            return value
    except (OSError, ValueError, KeyError, TypeError):
        pass
    return None


def prepare_baselines(args, run_dir, processes):
    config = configuration(args, "bimodal")
    metadata = baseline_metadata(args, config)
    # Recheck under the lock: overlapping invocations must not both build baselines.
    with file_lock(args.baseline_dir / ".baseline.lock"):
        values, missing = {}, []
        for trace in args.traces:
            value = cached_mpki(args.baseline_dir / f"{trace}.json", metadata[trace], args.trust_legacy_baseline)
            if value is None:
                missing.append(trace)
            else:
                values[trace] = value
        if not missing:
            progress(f"[BASELINE] Reusing all {len(values)} cached results; no baseline build or simulation")
            return values
        progress(f"[BASELINE] Generating {len(missing)} missing/stale bimodal results; reusing {len(values)}")
        binary = build_predictor(args, run_dir, processes, "bimodal", config)

        def one(trace):
            log = run_dir / f"baseline-{trace}.log"
            progress(f"[BASELINE START] {trace}")
            processes.run([str(binary), "--warmup-instructions", str(args.warmup),
                           "--simulation-instructions", str(args.simulation),
                           str(args.trace_dir / trace)], args.root, log)
            value = parse_branch_mpki(log.read_text(errors="replace"))
            atomic_json(args.baseline_dir / f"{trace}.json", {"mpki": value, "metadata": metadata[trace]})
            progress(f"[BASELINE DONE] {trace}: MPKI={value:g}")
            return value

        values.update(parallel_traces(args, missing, one, processes))
        return values


def calculate_branch_score(results):
    """Keep 100 * GM(baseline/candidate), including the original EPSILON rule."""
    if not results:
        raise ValueError("No benchmark results")
    logs = []
    zero_ratio = False
    for result in results:
        baseline = nonnegative_mpki(result["baseline_mpki"], "baseline")
        candidate = nonnegative_mpki(result["candidate_mpki"], "candidate")
        if baseline <= EPSILON and candidate <= EPSILON:
            logs.append(0.0)
        elif baseline == 0:
            zero_ratio = True
        else:
            logs.append(math.log(baseline) - math.log(max(candidate, EPSILON)))
    score = 0.0 if zero_ratio else 100.0 * math.exp(math.fsum(logs) / len(results))
    if not math.isfinite(score):
        raise ValueError("Score is not finite")
    return score


class Processes:
    """Own only this run's build/simulation process groups, including children."""
    def __init__(self):
        self.lock = threading.Lock()
        self.active = set()
        self.stopped = False

    def run(self, command, cwd, log_path):
        with log_path.open("w") as log:
            with self.lock:
                if self.stopped:
                    raise RuntimeError("Evaluation cancelled")
                process = subprocess.Popen(command, cwd=cwd, stdout=log,
                                           stderr=subprocess.STDOUT, start_new_session=True)
                self.active.add(process)
            try:
                status = process.wait()
            except BaseException:
                try:
                    os.killpg(process.pid, signal.SIGTERM)
                    process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
                except ProcessLookupError:
                    pass
                raise
            finally:
                with self.lock:
                    self.active.discard(process)
        if status:
            raise RuntimeError(f"Command failed (exit {status}); see {log_path}")

    def stop(self):
        with self.lock:
            self.stopped = True
            active = list(self.active)
        for process in active:
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
        for process in active:
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                process.wait()


def build_predictor(args, run_dir, processes, predictor, config=None):
    config = copy.deepcopy(config if config is not None else configuration(args, predictor))
    name = "auto-run-" + predictor + "-" + run_dir.name
    config["executable_name"] = name
    config_file = run_dir / f"{predictor}-config.json"
    config_file.write_text(json.dumps(config, indent=2) + "\n")
    progress(f"[BUILD] Configuring and compiling {predictor} once")
    # ChampSim's generated build files are shared, even with unique binary names.
    with file_lock(args.root / ".auto-run/build.lock"):
        processes.run([sys.executable, str(args.root / "config.sh"), "--no-compile-all-modules",
                       str(config_file)], args.root, run_dir / f"{predictor}-configure.log")
        processes.run(["make", "-j", str(args.build_jobs), f"bin/{name}"],
                      args.root, run_dir / f"{predictor}-build.log")
    binary = args.root / "bin" / name
    if not binary.is_file() or not os.access(binary, os.X_OK):
        raise RuntimeError(f"Build did not produce executable {binary}")
    return binary


def build_candidate(args, run_dir, processes):
    if args.binary:
        binary = args.binary.resolve()
        if not binary.is_file() or not os.access(binary, os.X_OK):
            raise ValueError(f"Candidate executable not found or not executable: {binary}")
        return binary
    return build_predictor(args, run_dir, processes, "my_perceptron")


def parallel_traces(args, traces, worker, processes):
    executor = ThreadPoolExecutor(max_workers=args.workers)
    futures, results = {}, {}
    try:
        futures = {executor.submit(worker, trace): trace for trace in traces}
        for future in as_completed(futures):
            results[futures[future]] = future.result()
    except BaseException:
        processes.stop()
        for future in futures:
            future.cancel()
        raise
    finally:
        executor.shutdown(wait=True)
    return results


def evaluate(args, binary, run_dir, baselines, processes):
    def one(trace):
        log = run_dir / f"{trace}.log"
        progress(f"[START] {trace}")
        processes.run([str(binary), "--warmup-instructions", str(args.warmup),
                       "--simulation-instructions", str(args.simulation),
                       str(args.trace_dir / trace)], args.root, log)
        mpki = parse_branch_mpki(log.read_text(errors="replace"))
        progress(f"[DONE] {trace}: MPKI={mpki:g}")
        return {"trace": trace, "baseline_mpki": baselines[trace], "candidate_mpki": mpki}

    results = parallel_traces(args, args.traces, one, processes)
    return [results[trace] for trace in args.traces]


def positive(value):
    value = int(value)
    if value <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return value


def arguments(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--champsim-root", dest="root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--baseline-dir", type=Path, help="Bimodal baseline cache; default: <root>/baseline")
    parser.add_argument("--trace-dir", type=Path, help="Default: <root>/traces")
    parser.add_argument("--trust-legacy-baseline", action="store_true", help="Explicitly trust old MPKI-only JSON files without fingerprints")
    parser.add_argument("--config", type=Path, help="Candidate configuration; default: lab2_config.json, then branch_config.json")
    parser.add_argument("--binary", type=Path, help="Use an already-built candidate executable instead of compiling")
    parser.add_argument("--max-worker", "--max-workers", dest="workers", type=positive, default=4)
    parser.add_argument("--build-jobs", type=positive, default=min(8, os.cpu_count() or 1))
    parser.add_argument("--trace", action="append", dest="traces", help="Evaluate only these filenames (repeatable); default: 14 course branch traces")
    parser.add_argument("--warmup-instructions", dest="warmup", type=int, default=WARMUP_INSTRUCTIONS)
    parser.add_argument("--simulation-instructions", dest="simulation", type=positive, default=SIMULATION_INSTRUCTIONS)
    parser.add_argument("--output-file", type=Path, help="Optional detailed JSON result file")
    args = parser.parse_args(argv)
    args.root = args.root.resolve()
    args.baseline_dir = (args.baseline_dir or args.root / "baseline").resolve()
    args.trace_dir = (args.trace_dir or args.root / "traces").resolve()
    args.config = args.config.resolve() if args.config else None
    args.traces = args.traces or list(BRANCH_TRACES)
    if args.warmup < 0:
        parser.error("--warmup-instructions must be nonnegative")
    if len(set(args.traces)) != len(args.traces):
        parser.error("Duplicate trace filenames")
    if any(Path(t).name != t or t in (".", "..") for t in args.traces):
        parser.error("--trace requires a filename, not a path")
    return args


def main(argv=None):
    args = arguments(argv)
    processes = Processes()
    previous = {}
    run_dir = None

    def interrupted(signum, _frame):
        signal.signal(signum, signal.SIG_IGN)
        raise KeyboardInterrupt(f"signal {signum}")

    try:
        if not args.root.is_dir():
            raise ValueError(f"ChampSim root does not exist: {args.root}")
        for trace in args.traces:
            if not (args.trace_dir / trace).is_file():
                raise ValueError(f"Missing trace: {args.trace_dir / trace}")
        if not args.binary and not (args.root / "branch/my_perceptron").is_dir():
            raise ValueError(f"Missing predictor directory: {args.root / 'branch/my_perceptron'}")
        workspace = args.root / ".auto-run"
        workspace.mkdir(exist_ok=True)
        run_dir = Path(tempfile.mkdtemp(prefix="run-", dir=workspace))
        progress(f"[LOGS] {run_dir}")
        for sig in (signal.SIGINT, signal.SIGTERM):
            previous[sig] = signal.signal(sig, interrupted)
        baselines = prepare_baselines(args, run_dir, processes)
        binary = build_candidate(args, run_dir, processes)
        results = evaluate(args, binary, run_dir, baselines, processes)
        score = round(calculate_branch_score(results), 6)
        detail = {"score": score, "warmup_instructions": args.warmup,
                  "simulation_instructions": args.simulation, "binary": str(binary),
                  "results": results}
        (run_dir / "results.json").write_text(json.dumps(detail, indent=2, allow_nan=False) + "\n")
        if args.output_file:
            args.output_file.parent.mkdir(parents=True, exist_ok=True)
            args.output_file.write_text(json.dumps(detail, indent=2, allow_nan=False) + "\n")
        print(json.dumps({"score": score}, allow_nan=False), flush=True)
        return 0
    except KeyboardInterrupt:
        progress("[ERROR] Evaluation interrupted")
        return 130
    except (OSError, ValueError, RuntimeError, OverflowError) as exc:
        progress(f"[ERROR] {exc}")
        return 1
    finally:
        # Prevent repeated signals from interrupting process-group cleanup.
        for sig in previous:
            signal.signal(sig, signal.SIG_IGN)
        processes.stop()
        for sig, handler in previous.items():
            signal.signal(sig, handler)


if __name__ == "__main__":
    sys.exit(main())
