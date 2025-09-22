#!/usr/bin/env python3
# gen/gen_bus.py
#
# Generates Bus Stops tests in ../input and ../output:
# - input{1..39}.txt and output{1..39}.txt
#
# Subtasks:
#  S1: 5 tests  (T1–T5)
#  S2: 7 tests  (T6–T12)
#  S3: 5 tests  (T13–T17)
#  S4: 10 tests (T18–T27)  [capacity enforced]
#  S5: 12 tests (T28–T39)  [print index of first max]
#
# Input format:
#   N
#   on_1 ... on_N
#   off_1 ... off_N
#   C
#
# Output format:
#   Subtasks 1–4:  max_students
#   Subtask 5:     max_students stop_index   (1-based first index of the max)

import os
import random
from typing import List, Tuple

# --------------------- Global parameters ---------------------
BIG_C = 10**9         # "infinite" capacity for S1–S3 & S5
MAXV_SMALL = 100      # Subtask 2 bounds
MAXV_BIG   = 10**4    # Subtasks 3–5 bounds
SEED_BASE  = 20250919 # reproducible

# Directories relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IN_DIR  = os.path.join(SCRIPT_DIR, "..", "input")
OUT_DIR = os.path.join(SCRIPT_DIR, "..", "output")

os.makedirs(IN_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

# --------------------- Helpers ---------------------

def write_case(idx: int, n: int, on: List[int], off: List[int], C: int,
               need_index: bool):
    """Write input and output files for one case."""
    assert len(on) == n and len(off) == n
    inp_path = os.path.join(IN_DIR,  f"input{idx - 1}.txt")
    out_path = os.path.join(OUT_DIR, f"output{idx - 1}.txt")

    with open(inp_path, "w") as f:
        f.write(str(n) + "\n")
        f.write(" ".join(map(str, on)) + "\n")
        f.write(" ".join(map(str, off)) + "\n")
        f.write(str(C) + "\n")

    ans_line = solve(on, off, C, need_index)
    with open(out_path, "w") as f:
        f.write(ans_line + "\n")


def solve(on: List[int], off: List[int], C: int, need_index: bool) -> str:
    """Judge solution (reference). Off happens before on; boarding limited by C."""
    cur = 0
    best = 0
    best_idx = 1
    n = len(on)
    for i in range(n):
        # Off first (guaranteed valid by generator)
        cur -= off[i]
        if cur < 0:
            # Should never happen if generator is correct
            cur = 0
        # On with capacity cap
        space = C - cur
        if space > 0:
            take = min(space, on[i])
            cur += take
        # Track first occurrence of maximum
        if cur > best:
            best = cur
            best_idx = i + 1
    return f"{best} {best_idx}" if need_index else f"{best}"


def normalize_nonnegative(on: List[int], off: List[int], C: int) -> Tuple[List[int], List[int]]:
    """
    Adjust off[i] so that off[i] <= current occupancy BEFORE off,
    with occupancy evolving under capacity C.
    We do NOT clamp 'on' itself; capacity applies at runtime.
    """
    cur = 0
    n = len(on)
    off2 = off[:]
    for i in range(n):
        if off2[i] > cur:
            off2[i] = cur
        cur -= off2[i]
        # Board (with capacity limit)
        space = C - cur
        take = min(space, on[i])
        cur += take
    return on, off2


def build_from_occupancy(O: List[int]) -> Tuple[List[int], List[int]]:
    """Given O[1..N] with O[0]=0 and O[i]>=0, produce (on, off) that realize exactly O."""
    n = len(O) - 1
    on = [0]*n
    off = [0]*n
    for i in range(1, n+1):
        delta = O[i] - O[i-1]
        if delta >= 0:
            on[i-1] = delta
            off[i-1] = 0
        else:
            on[i-1] = 0
            off[i-1] = -delta
    return on, off


def bounded_random_case(n: int, maxv: int, C: int, rng: random.Random) -> Tuple[List[int], List[int], int]:
    """Random on/off in [0, maxv], normalized so off never exceeds current (under capacity C)."""
    on = [rng.randint(0, maxv) for _ in range(n)]
    off = [rng.randint(0, maxv) for _ in range(n)]
    on, off = normalize_nonnegative(on, off, C)
    return on, off, C


# --------------------- Subtask builders ---------------------

def subtask1_cases() -> List[Tuple[int,List[int],List[int],int,bool]]:
    """5 tests, C = BIG_C, small N & values."""
    cases = []

    # T1: N=1, no one on/off
    on = [0]; off = [0]
    cases.append((1, on, off, BIG_C, False))

    # T2: N=2, board then off
    on = [5, 0]; off = [0, 5]
    cases.append((2, on, off, BIG_C, False))

    # T3: N=3, always empty
    on = [0, 0, 0]; off = [0, 0, 0]
    cases.append((3, on, off, BIG_C, False))

    # T4: N=3, max occupancy at last stop
    on = [1, 2, 5]; off = [0, 0, 0]
    cases.append((3, on, off, BIG_C, False))

    # T5: N=3, oscillating on/off (max at first)
    on = [5, 0, 5]; off = [0, 5, 0]
    on, off = normalize_nonnegative(on, off, BIG_C)
    cases.append((3, on, off, BIG_C, False))

    return cases


def subtask2_cases(rng: random.Random) -> List[Tuple[int,List[int],List[int],int,bool]]:
    """7 tests, N up to 100, on/off up to 100, C = BIG_C."""
    cases = []

    # T6: N=10, all on=1, off=0
    n = 10
    cases.append((n, [1]*n, [0]*n, BIG_C, False))

    # T7: N=50, alternating +1/-1 (wave 1,0,1,0,...)
    n = 50
    on = [1 if i % 2 == 0 else 0 for i in range(n)]
    off = [0 if i % 2 == 0 else 1 for i in range(n)]
    on, off = normalize_nonnegative(on, off, BIG_C)
    cases.append((n, on, off, BIG_C, False))

    # T8: N=100, big burst of 100 at once
    n = 100
    on = [0]*n
    on[49] = 100
    off = [0]*n
    cases.append((n, on, off, BIG_C, False))

    # T9: N=100, increasing then all off at end
    n = 100
    on = [1 if i < 80 else 0 for i in range(n)]
    off = [0]*n
    off[-1] = 80
    on, off = normalize_nonnegative(on, off, BIG_C)
    cases.append((n, on, off, BIG_C, False))

    # T10: N=100, edge values=100: load then unload
    n = 100
    on = [100 if i < 50 else 0 for i in range(n)]
    off = [0 if i < 50 else 100 for i in range(n)]
    on, off = normalize_nonnegative(on, off, BIG_C)
    cases.append((n, on, off, BIG_C, False))

    # T11: N=100, random small values
    n = 100
    on, off, C = bounded_random_case(n, MAXV_SMALL, BIG_C, rng)
    cases.append((n, on, off, C, False))

    # T12: N=100, another random (different seed effect)
    on, off, C = bounded_random_case(n, MAXV_SMALL, BIG_C, rng)
    cases.append((n, on, off, C, False))

    return cases


def subtask3_cases(rng: random.Random) -> List[Tuple[int,List[int],List[int],int,bool]]:
    """5 tests, N up to 1000, on/off up to 1e4, C = BIG_C."""
    cases = []

    # T13: all zeros
    n = 1000
    cases.append((n, [0]*n, [0]*n, BIG_C, False))

    # T14: one massive group boards at stop 500
    on = [0]*n
    on[499] = 9999
    off = [0]*n
    cases.append((n, on, off, BIG_C, False))

    # T15: wave pattern: +x, -x repeated
    x = 200
    on = []; off = []
    cur = 0
    for i in range(n):
        if i % 4 in (0, 1):   # two steps up
            on.append(x); off.append(0); cur += x
        else:                 # two steps down (won't go negative)
            down = min(x, cur)
            on.append(0); off.append(down); cur -= down
    cases.append((n, on, off, BIG_C, False))

    # T16: max values 1e4: load first half, unload second half
    on  = [MAXV_BIG if i < n//2 else 0 for i in range(n)]
    off = [0 if i < n//2 else MAXV_BIG for i in range(n)]
    on, off = normalize_nonnegative(on, off, BIG_C)
    cases.append((n, on, off, BIG_C, False))

    # T17: random with high peaks
    on, off, C = bounded_random_case(n, MAXV_BIG, BIG_C, rng)
    cases.append((n, on, off, C, False))

    return cases


def subtask4_cases(rng: random.Random) -> List[Tuple[int,List[int],List[int],int,bool]]:
    """10 tests with capacity enforced (various C)."""
    cases = []

    # T18: C=1, on>1, off=0
    n = 10; C = 1
    on = [5]*n; off = [0]*n
    on, off = normalize_nonnegative(on, off, C)
    cases.append((n, on, off, C, False))

    # T19: C=5, exactly fills then more try to board
    n = 8; C = 5
    on  = [5, 5, 5, 0, 0, 0, 0, 0]
    off = [0, 0, 0, 0, 0, 0, 0, 0]
    on, off = normalize_nonnegative(on, off, C)
    cases.append((n, on, off, C, False))

    # T20: C=1000, large N=1000, small C
    n = 1000; C = 1000
    on, off, _ = bounded_random_case(n, MAXV_BIG, C, rng)
    cases.append((n, on, off, C, False))

    # T21: C=1e4, just fits in one go
    n = 6; C = 10**4
    on  = [10**4, 10**4, 0, 0, 0, 0]  # attempts more later, but remains at cap
    off = [0]*n
    on, off = normalize_nonnegative(on, off, C)
    cases.append((n, on, off, C, False))

    # T22–T27: random cases with medium C
    for _ in range(6):
        n = rng.randint(200, 1000)
        C = rng.choice([50, 100, 200, 500, 2000, 5000])
        on, off, _ = bounded_random_case(n, MAXV_BIG, C, rng)
        cases.append((n, on, off, C, False))

    return cases


def subtask5_cases(rng: random.Random) -> List[Tuple[int,List[int],List[int],int,bool]]:
    """12 tests requiring (max, first_index). Build many from occupancy O."""
    cases = []

    # Helper: add case from occupancy O (with C=BIG_C)
    def add_O(O: List[int]):
        on, off = build_from_occupancy([0] + O)
        cases.append((len(O), on, off, BIG_C, True))

    # T28: simple tie at multiple stops
    # O: 1,3,1,3,0 -> max=3 occurs at i=2 and i=4 -> answer index 2
    add_O([1,3,1,3,0])

    # T29: tie at beginning vs later (first is at stop 1)
    # O: 5,4,3,5,2,0 -> max=5 at i=1 and i=4 -> index 1
    add_O([5,4,3,5,2,0])

    # T30: big N=1000, peak early
    n = 1000
    O = [0]*n
    cur = 0
    for i in range(10):
        cur += 800  # ramp quickly
        O[i] = cur
    for i in range(10, n):
        # drift around but never exceed first peak
        cur = max(0, cur - (1 if i % 3 else 2))
        O[i] = cur
    # Ensure first few are maximized to the same peak a couple of times
    M = max(O)
    O[5] = M; O[20] = min(M, O[20])  # keep first peak early
    add_O(O)

    # T31: big N=1000, peak late
    O = [0]*n; cur = 0
    for i in range(n-20):
        cur = max(0, cur - (1 if i % 5 == 0 else 0))
        O[i] = cur
    for i in range(n-20, n):
        cur += 600
        O[i] = cur
    add_O(O)

    # T32: wave pattern with repeated equal peaks
    O = []
    cur = 0
    peak = 2000
    for rep in range(5):
        # up
        for _ in range(10):
            cur += peak // 10
            O.append(cur)
        # down
        for _ in range(10):
            cur = max(0, cur - peak // 10)
            O.append(cur)
    add_O(O[:1000])  # trim to 1000 if longer

    # T33–T36: random with forced ties at known indices
    for tie_case in range(4):
        n = 300 + tie_case*100
        O = [0]*n
        cur = 0
        # random walk up and down
        for i in range(n):
            step = rng.randint(-50, 80)
            cur = max(0, cur + step)
            O[i] = cur
        M = max(O)
        # Force another M later if not already repeated
        first = O.index(M)
        # choose a later index and set to M
        later = min(n-1, first + 50 + rng.randint(0, 100))
        O[later] = M
        # smooth around later to avoid exceeding M
        for j in range(later+1, min(n, later+6)):
            O[j] = min(O[j], M - rng.randint(0, 5))
        add_O(O)

    # T37–T38: crafted unique peak late/early with long tails
    # Early unique peak
    O = [0]*600
    cur = 0
    for i in range(50):
        cur += 300
        O[i] = cur
    peak = cur
    for i in range(50, 600):
        cur = max(0, cur - 1)
        O[i] = min(cur, peak - 1)  # never reach peak again
    add_O(O)

    # Late unique peak
    O = [0]*800
    for i in range(799):
        O[i] = i % 200  # keep low
    O[799] = 5000     # single late spike
    add_O(O)

    # T39: edge with large values and a tie
    O = []
    cur = 0
    for i in range(100):
        cur += 10000
        O.append(cur)
    # drop and re-peak to same M
    M = cur
    for _ in range(50):
        cur = max(0, cur - 5000)
        O.append(cur)
    for _ in range(50):
        cur += 5000
        O.append(min(cur, M))  # cap at M to tie
    add_O(O[:1000])

    return cases


# --------------------- Main orchestrator ---------------------

def main():
    rng = random.Random(SEED_BASE)
    index = 1

    # Subtask 1
    for n, on, off, C, need_idx in subtask1_cases():
        write_case(index, n, on, off, C, need_idx)
        print(f"[S1]  input{index - 1}.txt  N={n}")
        index += 1

    # Subtask 2
    for n, on, off, C, need_idx in subtask2_cases(rng):
        write_case(index, n, on, off, C, need_idx)
        print(f"[S2]  input{index - 1}.txt  N={n}")
        index += 1

    # Subtask 3
    for n, on, off, C, need_idx in subtask3_cases(rng):
        write_case(index, n, on, off, C, need_idx)
        print(f"[S3]  input{index - 1}.txt  N={n}")
        index += 1

    # Subtask 4
    for n, on, off, C, need_idx in subtask4_cases(rng):
        write_case(index, n, on, off, C, need_idx)
        print(f"[S4]  input{index - 1}.txt  N={n}, C={C}")
        index += 1

    # Subtask 5
    for n, on, off, C, need_idx in subtask5_cases(rng):
        write_case(index, n, on, off, C, need_idx)
        print(f"[S5]  input{index - 1}.txt  N={n} (index required)")
        index += 1

    total = index - 1
    assert total == 39, f"Expected 39 tests, produced {total}"
    print(f"\nDone. Generated {total} tests into:\n  {IN_DIR}\n  {OUT_DIR}")

if __name__ == "__main__":
    main()
