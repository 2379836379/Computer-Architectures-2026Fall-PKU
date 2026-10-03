# Please include the following in your report:
## Part 1:
1. A screenshot that shows you can successfully configure and compile ChampSim .
(./screenshot of the successful compilation.png)

2. A screenshot of the output showing that your ChampSim executable can
successfully run an instruction trace and generate simulation statistics.
(./screenshot of the successful execution.png)

3. Use the provided basic configuration to build ChampSim successfully.

```
root@aaefef21d69a:/champsim# ./config.sh                 
No configuration specified. Building default ChampSim with no prefetching.
root@aaefef21d69a:/champsim# make -j $(nproc)
g++ @global.options @absolute.options -MM -MT .csconfig/f45bff292054888f_main.d -MT .csconfig/f45bff292054888f_main.o -I.csconfig -DCHAMPSIM_BUILD=0xf45bff292054888f -MF .csconfig/f45bff292054888f_main.d src/main.cc
g++ @global.options @absolute.options -MM -MT .csconfig/generated_environment.d -MT .csconfig/generated_environment.o -I.csconfig -MF .csconfig/generated_environment.d src/generated_environment.cc
g++ @global.options @absolute.options -MM -MT .csconfig/TEST_main.d -MT .csconfig/TEST_main.o -I.csconfig -DCHAMPSIM_BUILD=0xTEST -MF .csconfig/TEST_main.d src/main.cc
g++ @global.options @absolute.options -I.csconfig  -c -o .csconfig/generated_environment.o src/generated_environment.cc
g++ @global.options @absolute.options -I.csconfig -DCHAMPSIM_BUILD=0xf45bff292054888f  -c -o .csconfig/f45bff292054888f_main.o src/main.cc
g++ -L/champsim/vcpkg_installed/x64-linux/lib -L/champsim/vcpkg_installed/x64-linux/lib/manual-link -o bin/champsim .csconfig/address.o .csconfig/bandwidth.o .csconfig/cache.o .csconfig/cache_stats.o .csconfig/champsim.o .csconfig/channel.o .csconfig/chrono.o .csconfig/core_stats.o .csconfig/dram_controller.o .csconfig/dram_stats.o .csconfig/extent.o .csconfig/generated_environment.o .csconfig/json_printer.o .csconfig/f45bff292054888f_main.o .csconfig/modules.o .csconfig/ooo_cpu.o .csconfig/operable.o .csconfig/plain_printer.o .csconfig/ptw.o .csconfig/ptw_builder.o .csconfig/register_allocator.o .csconfig/tracereader.o .csconfig/vmem.o .csconfig/modules/branch/bimodal/bimodal.o .csconfig/modules/branch/gshare/gshare.o .csconfig/modules/branch/hashed_perceptron/hashed_perceptron.o .csconfig/modules/branch/local_bp/local_bp.o .csconfig/modules/branch/my_perceptron/my_perceptron.o .csconfig/modules/branch/tournament/tournament.o .csconfig/modules/btb/basic_btb/basic_btb.o .csconfig/modules/btb/basic_btb/direct_predictor.o .csconfig/modules/btb/basic_btb/indirect_predictor.o .csconfig/modules/btb/basic_btb/return_stack.o .csconfig/modules/prefetcher/ip_stride/ip_stride.o .csconfig/modules/prefetcher/my_prefetcher/my_prefetcher.o .csconfig/modules/prefetcher/next_line/next_line.o .csconfig/modules/prefetcher/no/no.o .csconfig/modules/prefetcher/spp_dev/spp_dev.o .csconfig/modules/prefetcher/va_ampm_lite/va_ampm_lite.o .csconfig/modules/replacement/drrip/drrip.o .csconfig/modules/replacement/lru/lru.o .csconfig/modules/replacement/random/random.o .csconfig/modules/replacement/ship/ship.o .csconfig/modules/replacement/srrip/srrip.o  -lCLI11 -llzma -lz -lbz2 -lfmt
```

4. Use binary_search instruction traces to run the generated ChampSim
executable. You may first use a small number of warmup and simulation
instructions to verify that the simulator works correctly.
```small
root@aaefef21d69a:/champsim# ./bin/champsim --warmup-instructions 1000000 --simulation-instructions 10000000 traces/binary_search.champsimtrace.xz | tee results-part1.txt
[VMEM] WARNING: physical memory size is smaller than virtual memory size.

*** ChampSim Multicore Out-of-Order Simulator ***
Warmup Instructions: 1000000
Simulation Instructions: 10000000
Number of CPUs: 1
Page size: 4096

Off-chip DRAM Size: 16 GiB Channels: 1 Width: 64-bit Data Rate: 3205 MT/s
Warmup finished CPU 0 instructions: 1000001 cycles: 507661 cumulative IPC: 1.97 (Simulation time: 00 hr 00 min 13 sec)
Warmup complete CPU 0 instructions: 1000001 cycles: 507661 cumulative IPC: 1.97 (Simulation time: 00 hr 00 min 13 sec)
Heartbeat CPU 0 instructions: 10000003 cycles: 17141781 heartbeat IPC: 0.5834 cumulative IPC: 0.5411 (Simulation time: 00 hr 03 min 43 sec)
Simulation finished CPU 0 instructions: 10000001 cycles: 18417731 cumulative IPC: 0.543 (Simulation time: 00 hr 04 min 02 sec)
Simulation complete CPU 0 instructions: 10000001 cycles: 18417731 cumulative IPC: 0.543 (Simulation time: 00 hr 04 min 02 sec)

ChampSim completed all CPUs

=== Simulation ===
CPU 0 runs traces/binary_search.champsimtrace.xz

Region of Interest Statistics

CPU 0 cumulative IPC: 0.543 instructions: 10000001 cycles: 18417731
CPU 0 Branch Prediction Accuracy: 85.77% MPKI: 15.69 Average ROB Occupancy at Mispredict: 36.61
Branch type MPKI
BRANCH_DIRECT_JUMP: 0
BRANCH_INDIRECT: 0
BRANCH_CONDITIONAL: 15.69
BRANCH_DIRECT_CALL: 0
BRANCH_INDIRECT_CALL: 0
BRANCH_RETURN: 0

cpu0->LLC TOTAL        ACCESS:      99903 HIT:      35762 MISS:      64141 MISS_MERGE:          0
cpu0->LLC LOAD         ACCESS:      97160 HIT:      33116 MISS:      64044 MISS_MERGE:          0
cpu0->LLC RFO          ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->LLC PREFETCH     ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->LLC WRITE        ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->LLC TRANSLATION  ACCESS:       2743 HIT:       2646 MISS:         97 MISS_MERGE:          0
cpu0->LLC PREFETCH REQUESTED:          0 ISSUED:          0 USEFUL:          0 USELESS:          0
cpu0->LLC AVERAGE MISS LATENCY: 175 cycles
cpu0->cpu0_DTLB TOTAL        ACCESS:    3068656 HIT:    2841745 MISS:     226911 MISS_MERGE:     113739
cpu0->cpu0_DTLB LOAD         ACCESS:    3068656 HIT:    2841745 MISS:     226911 MISS_MERGE:     113739
cpu0->cpu0_DTLB RFO          ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_DTLB PREFETCH     ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_DTLB WRITE        ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_DTLB TRANSLATION  ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_DTLB PREFETCH REQUESTED:          0 ISSUED:          0 USEFUL:          0 USELESS:          0
cpu0->cpu0_DTLB AVERAGE MISS LATENCY: 7.989 cycles
cpu0->cpu0_ITLB TOTAL        ACCESS:        972 HIT:        972 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_ITLB LOAD         ACCESS:        972 HIT:        972 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_ITLB RFO          ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_ITLB PREFETCH     ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_ITLB WRITE        ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_ITLB TRANSLATION  ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_ITLB PREFETCH REQUESTED:          0 ISSUED:          0 USEFUL:          0 USELESS:          0
cpu0->cpu0_ITLB AVERAGE MISS LATENCY: - cycles
cpu0->cpu0_L1D TOTAL        ACCESS:    3083062 HIT:    2797452 MISS:     285610 MISS_MERGE:     143943
cpu0->cpu0_L1D LOAD         ACCESS:    2367522 HIT:    2087482 MISS:     280040 MISS_MERGE:     143482
cpu0->cpu0_L1D RFO          ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_L1D PREFETCH     ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_L1D WRITE        ACCESS:     701134 HIT:     701134 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_L1D TRANSLATION  ACCESS:      14406 HIT:       8836 MISS:       5570 MISS_MERGE:        461
cpu0->cpu0_L1D PREFETCH REQUESTED:          0 ISSUED:          0 USEFUL:          0 USELESS:          0
cpu0->cpu0_L1D AVERAGE MISS LATENCY: 97.58 cycles
cpu0->cpu0_L1I TOTAL        ACCESS:        972 HIT:        972 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_L1I LOAD         ACCESS:        972 HIT:        972 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_L1I RFO          ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_L1I PREFETCH     ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_L1I WRITE        ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_L1I TRANSLATION  ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_L1I PREFETCH REQUESTED:          0 ISSUED:          0 USEFUL:          0 USELESS:          0
cpu0->cpu0_L1I AVERAGE MISS LATENCY: - cycles
cpu0->cpu0_L2C TOTAL        ACCESS:     141667 HIT:      41764 MISS:      99903 MISS_MERGE:          0
cpu0->cpu0_L2C LOAD         ACCESS:     136558 HIT:      39398 MISS:      97160 MISS_MERGE:          0
cpu0->cpu0_L2C RFO          ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_L2C PREFETCH     ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_L2C WRITE        ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_L2C TRANSLATION  ACCESS:       5109 HIT:       2366 MISS:       2743 MISS_MERGE:          0
cpu0->cpu0_L2C PREFETCH REQUESTED:          0 ISSUED:          0 USEFUL:          0 USELESS:          0
cpu0->cpu0_L2C AVERAGE MISS LATENCY: 126 cycles
cpu0->cpu0_STLB TOTAL        ACCESS:     113172 HIT:     105969 MISS:       7203 MISS_MERGE:          0
cpu0->cpu0_STLB LOAD         ACCESS:     113172 HIT:     105969 MISS:       7203 MISS_MERGE:          0
cpu0->cpu0_STLB RFO          ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_STLB PREFETCH     ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_STLB WRITE        ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_STLB TRANSLATION  ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_STLB PREFETCH REQUESTED:          0 ISSUED:          0 USEFUL:          0 USELESS:          0
cpu0->cpu0_STLB AVERAGE MISS LATENCY: 61.68 cycles

DRAM Statistics

Channel 0 RQ ROW_BUFFER_HIT:         50
  ROW_BUFFER_MISS:      64091
  AVG DBUS CONGESTED CYCLE: 2.468
Channel 0 WQ ROW_BUFFER_HIT:          0
  ROW_BUFFER_MISS:          0
  FULL:          0
Channel 0 REFRESHES ISSUED:       1535
```

```full
[VMEM] WARNING: physical memory size is smaller than virtual memory size.

*** ChampSim Multicore Out-of-Order Simulator ***
Warmup Instructions: 100000000
Simulation Instructions: 500000000
Number of CPUs: 1
Page size: 4096

Off-chip DRAM Size: 16 GiB Channels: 1 Width: 64-bit Data Rate: 3205 MT/s
Heartbeat CPU 0 instructions: 10000002 cycles: 4084436 heartbeat IPC: 2.448 cumulative IPC: 2.448 (Simulation time: 00 hr 01 min 35 sec)
Heartbeat CPU 0 instructions: 20000002 cycles: 7940788 heartbeat IPC: 2.593 cumulative IPC: 2.519 (Simulation time: 00 hr 03 min 05 sec)
Heartbeat CPU 0 instructions: 30000003 cycles: 11798237 heartbeat IPC: 2.592 cumulative IPC: 2.543 (Simulation time: 00 hr 04 min 37 sec)
Heartbeat CPU 0 instructions: 40000003 cycles: 15656243 heartbeat IPC: 2.592 cumulative IPC: 2.555 (Simulation time: 00 hr 06 min 10 sec)
Heartbeat CPU 0 instructions: 50000003 cycles: 19513157 heartbeat IPC: 2.593 cumulative IPC: 2.562 (Simulation time: 00 hr 07 min 51 sec)
Heartbeat CPU 0 instructions: 60000005 cycles: 23370057 heartbeat IPC: 2.593 cumulative IPC: 2.567 (Simulation time: 00 hr 09 min 37 sec)
Heartbeat CPU 0 instructions: 70000005 cycles: 27227684 heartbeat IPC: 2.592 cumulative IPC: 2.571 (Simulation time: 00 hr 11 min 22 sec)
Heartbeat CPU 0 instructions: 80000009 cycles: 31084553 heartbeat IPC: 2.593 cumulative IPC: 2.574 (Simulation time: 00 hr 13 min 15 sec)
Heartbeat CPU 0 instructions: 90000013 cycles: 34943254 heartbeat IPC: 2.592 cumulative IPC: 2.576 (Simulation time: 00 hr 15 min 25 sec)
Warmup finished CPU 0 instructions: 100000003 cycles: 38799674 cumulative IPC: 2.577 (Simulation time: 00 hr 17 min 15 sec)
Warmup complete CPU 0 instructions: 100000003 cycles: 38799674 cumulative IPC: 2.577 (Simulation time: 00 hr 17 min 15 sec)
Heartbeat CPU 0 instructions: 100000013 cycles: 38799676 heartbeat IPC: 2.593 cumulative IPC: 5 (Simulation time: 00 hr 17 min 15 sec)
Heartbeat CPU 0 instructions: 110000014 cycles: 56739482 heartbeat IPC: 0.5574 cumulative IPC: 0.5574 (Simulation time: 00 hr 21 min 00 sec)
Heartbeat CPU 0 instructions: 120000016 cycles: 74685197 heartbeat IPC: 0.5572 cumulative IPC: 0.5573 (Simulation time: 00 hr 25 min 28 sec)
Heartbeat CPU 0 instructions: 130000016 cycles: 92616294 heartbeat IPC: 0.5577 cumulative IPC: 0.5574 (Simulation time: 00 hr 29 min 16 sec)
Heartbeat CPU 0 instructions: 140000019 cycles: 110557992 heartbeat IPC: 0.5574 cumulative IPC: 0.5574 (Simulation time: 00 hr 32 min 53 sec)
Heartbeat CPU 0 instructions: 150000021 cycles: 128543286 heartbeat IPC: 0.556 cumulative IPC: 0.5571 (Simulation time: 00 hr 36 min 01 sec)
Heartbeat CPU 0 instructions: 160000021 cycles: 146491865 heartbeat IPC: 0.5571 cumulative IPC: 0.5571 (Simulation time: 00 hr 39 min 24 sec)
Heartbeat CPU 0 instructions: 170000021 cycles: 164480197 heartbeat IPC: 0.5559 cumulative IPC: 0.557 (Simulation time: 00 hr 42 min 32 sec)
Heartbeat CPU 0 instructions: 180000021 cycles: 182375032 heartbeat IPC: 0.5588 cumulative IPC: 0.5572 (Simulation time: 00 hr 45 min 47 sec)
Heartbeat CPU 0 instructions: 190000022 cycles: 200319799 heartbeat IPC: 0.5573 cumulative IPC: 0.5572 (Simulation time: 00 hr 48 min 57 sec)
Heartbeat CPU 0 instructions: 200000023 cycles: 218338486 heartbeat IPC: 0.555 cumulative IPC: 0.557 (Simulation time: 00 hr 52 min 07 sec)
Heartbeat CPU 0 instructions: 210000026 cycles: 236258194 heartbeat IPC: 0.558 cumulative IPC: 0.5571 (Simulation time: 00 hr 55 min 20 sec)
Heartbeat CPU 0 instructions: 220000028 cycles: 254180844 heartbeat IPC: 0.558 cumulative IPC: 0.5572 (Simulation time: 00 hr 58 min 50 sec)
Heartbeat CPU 0 instructions: 230000030 cycles: 272171446 heartbeat IPC: 0.5558 cumulative IPC: 0.5571 (Simulation time: 01 hr 01 min 58 sec)
Heartbeat CPU 0 instructions: 240000031 cycles: 290143332 heartbeat IPC: 0.5564 cumulative IPC: 0.557 (Simulation time: 01 hr 05 min 06 sec)
*** Reached end of trace: (0, "traces/binary_search.champsimtrace.xz")
Heartbeat CPU 0 instructions: 250000031 cycles: 308073797 heartbeat IPC: 0.5577 cumulative IPC: 0.5571 (Simulation time: 01 hr 08 min 36 sec)
Heartbeat CPU 0 instructions: 260000035 cycles: 325988131 heartbeat IPC: 0.5582 cumulative IPC: 0.5571 (Simulation time: 01 hr 12 min 58 sec)
Heartbeat CPU 0 instructions: 270000035 cycles: 343856524 heartbeat IPC: 0.5596 cumulative IPC: 0.5573 (Simulation time: 01 hr 17 min 18 sec)
Heartbeat CPU 0 instructions: 280000035 cycles: 361781109 heartbeat IPC: 0.5579 cumulative IPC: 0.5573 (Simulation time: 01 hr 20 min 36 sec)
Heartbeat CPU 0 instructions: 290000037 cycles: 379749375 heartbeat IPC: 0.5565 cumulative IPC: 0.5573 (Simulation time: 01 hr 23 min 43 sec)
Heartbeat CPU 0 instructions: 300000040 cycles: 397633297 heartbeat IPC: 0.5592 cumulative IPC: 0.5574 (Simulation time: 01 hr 26 min 50 sec)
Heartbeat CPU 0 instructions: 310000040 cycles: 415503875 heartbeat IPC: 0.5596 cumulative IPC: 0.5575 (Simulation time: 01 hr 30 min 03 sec)
Heartbeat CPU 0 instructions: 320000042 cycles: 433543262 heartbeat IPC: 0.5543 cumulative IPC: 0.5573 (Simulation time: 01 hr 33 min 21 sec)
Heartbeat CPU 0 instructions: 330000042 cycles: 451551143 heartbeat IPC: 0.5553 cumulative IPC: 0.5572 (Simulation time: 01 hr 36 min 29 sec)
Heartbeat CPU 0 instructions: 340000043 cycles: 469522455 heartbeat IPC: 0.5564 cumulative IPC: 0.5572 (Simulation time: 01 hr 39 min 36 sec)
Heartbeat CPU 0 instructions: 350000046 cycles: 487486622 heartbeat IPC: 0.5567 cumulative IPC: 0.5572 (Simulation time: 01 hr 43 min 07 sec)
Heartbeat CPU 0 instructions: 360000047 cycles: 505419054 heartbeat IPC: 0.5576 cumulative IPC: 0.5572 (Simulation time: 01 hr 47 min 13 sec)
Heartbeat CPU 0 instructions: 370000048 cycles: 523345612 heartbeat IPC: 0.5578 cumulative IPC: 0.5572 (Simulation time: 01 hr 50 min 31 sec)
Heartbeat CPU 0 instructions: 380000048 cycles: 541260670 heartbeat IPC: 0.5582 cumulative IPC: 0.5573 (Simulation time: 01 hr 53 min 33 sec)
Heartbeat CPU 0 instructions: 390000051 cycles: 559208086 heartbeat IPC: 0.5572 cumulative IPC: 0.5573 (Simulation time: 01 hr 56 min 49 sec)
Heartbeat CPU 0 instructions: 400000051 cycles: 577161017 heartbeat IPC: 0.557 cumulative IPC: 0.5572 (Simulation time: 02 hr 00 min 16 sec)
Heartbeat CPU 0 instructions: 410000051 cycles: 595103715 heartbeat IPC: 0.5573 cumulative IPC: 0.5572 (Simulation time: 02 hr 03 min 40 sec)
Heartbeat CPU 0 instructions: 420000051 cycles: 613067288 heartbeat IPC: 0.5567 cumulative IPC: 0.5572 (Simulation time: 02 hr 08 min 16 sec)
Heartbeat CPU 0 instructions: 430000055 cycles: 630937404 heartbeat IPC: 0.5596 cumulative IPC: 0.5573 (Simulation time: 02 hr 11 min 50 sec)
Heartbeat CPU 0 instructions: 440000056 cycles: 648830829 heartbeat IPC: 0.5589 cumulative IPC: 0.5573 (Simulation time: 02 hr 15 min 07 sec)
Heartbeat CPU 0 instructions: 450000059 cycles: 666824035 heartbeat IPC: 0.5558 cumulative IPC: 0.5573 (Simulation time: 02 hr 18 min 14 sec)
Heartbeat CPU 0 instructions: 460000060 cycles: 684735851 heartbeat IPC: 0.5583 cumulative IPC: 0.5573 (Simulation time: 02 hr 21 min 21 sec)
Heartbeat CPU 0 instructions: 470000063 cycles: 702649873 heartbeat IPC: 0.5582 cumulative IPC: 0.5574 (Simulation time: 02 hr 24 min 28 sec)
Heartbeat CPU 0 instructions: 480000063 cycles: 720639575 heartbeat IPC: 0.5559 cumulative IPC: 0.5573 (Simulation time: 02 hr 27 min 13 sec)
Heartbeat CPU 0 instructions: 490000063 cycles: 738586952 heartbeat IPC: 0.5572 cumulative IPC: 0.5573 (Simulation time: 02 hr 29 min 58 sec)
*** Reached end of trace: (0, "traces/binary_search.champsimtrace.xz")
Heartbeat CPU 0 instructions: 500000065 cycles: 756482843 heartbeat IPC: 0.5588 cumulative IPC: 0.5573 (Simulation time: 02 hr 32 min 50 sec)
Heartbeat CPU 0 instructions: 510000066 cycles: 774377458 heartbeat IPC: 0.5588 cumulative IPC: 0.5574 (Simulation time: 02 hr 35 min 34 sec)
Heartbeat CPU 0 instructions: 520000066 cycles: 792221078 heartbeat IPC: 0.5604 cumulative IPC: 0.5575 (Simulation time: 02 hr 38 min 18 sec)
Heartbeat CPU 0 instructions: 530000066 cycles: 810134164 heartbeat IPC: 0.5583 cumulative IPC: 0.5575 (Simulation time: 02 hr 41 min 02 sec)
Heartbeat CPU 0 instructions: 540000067 cycles: 828115165 heartbeat IPC: 0.5561 cumulative IPC: 0.5574 (Simulation time: 02 hr 44 min 14 sec)
Heartbeat CPU 0 instructions: 550000067 cycles: 846008114 heartbeat IPC: 0.5589 cumulative IPC: 0.5575 (Simulation time: 02 hr 47 min 05 sec)
Heartbeat CPU 0 instructions: 560000068 cycles: 863866184 heartbeat IPC: 0.56 cumulative IPC: 0.5575 (Simulation time: 02 hr 49 min 50 sec)
Heartbeat CPU 0 instructions: 570000069 cycles: 881882222 heartbeat IPC: 0.5551 cumulative IPC: 0.5575 (Simulation time: 02 hr 52 min 35 sec)
Heartbeat CPU 0 instructions: 580000069 cycles: 899883682 heartbeat IPC: 0.5555 cumulative IPC: 0.5574 (Simulation time: 02 hr 55 min 22 sec)
Heartbeat CPU 0 instructions: 590000070 cycles: 917848274 heartbeat IPC: 0.5567 cumulative IPC: 0.5574 (Simulation time: 02 hr 58 min 14 sec)
Simulation finished CPU 0 instructions: 500000001 cycles: 897024804 cumulative IPC: 0.5574 (Simulation time: 03 hr 01 min 11 sec)
Simulation complete CPU 0 instructions: 500000001 cycles: 897024804 cumulative IPC: 0.5574 (Simulation time: 03 hr 01 min 11 sec)

ChampSim completed all CPUs

=== Simulation ===
CPU 0 runs traces/binary_search.champsimtrace.xz

Region of Interest Statistics

CPU 0 cumulative IPC: 0.5574 instructions: 500000001 cycles: 897024804
CPU 0 Branch Prediction Accuracy: 85.84% MPKI: 15.62 Average ROB Occupancy at Mispredict: 36.77
Branch type MPKI
BRANCH_DIRECT_JUMP: 0
BRANCH_INDIRECT: 0
BRANCH_CONDITIONAL: 15.62
BRANCH_DIRECT_CALL: 0
BRANCH_INDIRECT_CALL: 0
BRANCH_RETURN: 0

cpu0->LLC TOTAL        ACCESS:    5018495 HIT:    1969817 MISS:    3048678 MISS_MERGE:          0
cpu0->LLC LOAD         ACCESS:    4879635 HIT:    1836491 MISS:    3043144 MISS_MERGE:          0
cpu0->LLC RFO          ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->LLC PREFETCH     ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->LLC WRITE        ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->LLC TRANSLATION  ACCESS:     138860 HIT:     133326 MISS:       5534 MISS_MERGE:          0
cpu0->LLC PREFETCH REQUESTED:          0 ISSUED:          0 USEFUL:          0 USELESS:          0
cpu0->LLC AVERAGE MISS LATENCY: 174.8 cycles
cpu0->cpu0_DTLB TOTAL        ACCESS:  153839227 HIT:  142494691 MISS:   11344536 MISS_MERGE:    5680180
cpu0->cpu0_DTLB LOAD         ACCESS:  153839227 HIT:  142494691 MISS:   11344536 MISS_MERGE:    5680180
cpu0->cpu0_DTLB RFO          ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_DTLB PREFETCH     ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_DTLB WRITE        ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_DTLB TRANSLATION  ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_DTLB PREFETCH REQUESTED:          0 ISSUED:          0 USEFUL:          0 USELESS:          0
cpu0->cpu0_DTLB AVERAGE MISS LATENCY: 5.862 cycles
cpu0->cpu0_ITLB TOTAL        ACCESS:      47350 HIT:      47350 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_ITLB LOAD         ACCESS:      47350 HIT:      47350 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_ITLB RFO          ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_ITLB PREFETCH     ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_ITLB WRITE        ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_ITLB TRANSLATION  ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_ITLB PREFETCH REQUESTED:          0 ISSUED:          0 USEFUL:          0 USELESS:          0
cpu0->cpu0_ITLB AVERAGE MISS LATENCY: - cycles
cpu0->cpu0_L1D TOTAL        ACCESS:  154555499 HIT:  140296832 MISS:   14258667 MISS_MERGE:    7179029
cpu0->cpu0_L1D LOAD         ACCESS:  118783653 HIT:  104805976 MISS:   13977677 MISS_MERGE:    7156163
cpu0->cpu0_L1D RFO          ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_L1D PREFETCH     ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_L1D WRITE        ACCESS:   35055574 HIT:   35055574 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_L1D TRANSLATION  ACCESS:     716272 HIT:     435282 MISS:     280990 MISS_MERGE:      22866
cpu0->cpu0_L1D PREFETCH REQUESTED:          0 ISSUED:          0 USEFUL:          0 USELESS:          0
cpu0->cpu0_L1D AVERAGE MISS LATENCY: 93.65 cycles
cpu0->cpu0_L1I TOTAL        ACCESS:      47350 HIT:      47350 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_L1I LOAD         ACCESS:      47350 HIT:      47350 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_L1I RFO          ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_L1I PREFETCH     ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_L1I WRITE        ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_L1I TRANSLATION  ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_L1I PREFETCH REQUESTED:          0 ISSUED:          0 USEFUL:          0 USELESS:          0
cpu0->cpu0_L1I AVERAGE MISS LATENCY: - cycles
cpu0->cpu0_L2C TOTAL        ACCESS:    7079638 HIT:    2061143 MISS:    5018495 MISS_MERGE:          0
cpu0->cpu0_L2C LOAD         ACCESS:    6821514 HIT:    1941879 MISS:    4879635 MISS_MERGE:          0
cpu0->cpu0_L2C RFO          ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_L2C PREFETCH     ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_L2C WRITE        ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_L2C TRANSLATION  ACCESS:     258124 HIT:     119264 MISS:     138860 MISS_MERGE:          0
cpu0->cpu0_L2C PREFETCH REQUESTED:          0 ISSUED:          0 USEFUL:          0 USELESS:          0
cpu0->cpu0_L2C AVERAGE MISS LATENCY: 119.8 cycles
cpu0->cpu0_STLB TOTAL        ACCESS:    5664356 HIT:    5306220 MISS:     358136 MISS_MERGE:          0
cpu0->cpu0_STLB LOAD         ACCESS:    5664356 HIT:    5306220 MISS:     358136 MISS_MERGE:          0
cpu0->cpu0_STLB RFO          ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_STLB PREFETCH     ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_STLB WRITE        ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_STLB TRANSLATION  ACCESS:          0 HIT:          0 MISS:          0 MISS_MERGE:          0
cpu0->cpu0_STLB PREFETCH REQUESTED:          0 ISSUED:          0 USEFUL:          0 USELESS:          0
cpu0->cpu0_STLB AVERAGE MISS LATENCY: 28.46 cycles

DRAM Statistics

Channel 0 RQ ROW_BUFFER_HIT:       1728
  ROW_BUFFER_MISS:    3046950
  AVG DBUS CONGESTED CYCLE: 2.433
Channel 0 WQ ROW_BUFFER_HIT:          0
  ROW_BUFFER_MISS:          0
  FULL:          0
Channel 0 REFRESHES ISSUED:      74752

```

5. A screenshot of the successful execution of the ChampSim executable with a
provided trace.
(./screenshot of the successful execution.png)

6. Briefly describe the complete workflow of ChampSim , including
configuration, compilation, trace execution, and statistics collection.
You DO NOT need to submit your trace files in this project.