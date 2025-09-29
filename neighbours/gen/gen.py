#!/usr/bin/env python3
import os
import random

N_MAX = 1000
X_MAX = 10**6

# Directory structure (relative to gen/)
INPUT_DIR = "../input"
OUTPUT_DIR = "../output"

def ensure_dirs():
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def write_case(idx, n, positions):
    in_path = os.path.join(INPUT_DIR, f"input{idx}.txt")
    out_path = os.path.join(OUTPUT_DIR, f"output{idx}.txt")

    # Write input
    with open(in_path, "w") as f:
        f.write(f"{n}\n")
        f.write(" ".join(map(str, positions)) + "\n")

    # Write output
    diffs = [positions[i+1] - positions[i] for i in range(n-1)]
    with open(out_path, "w") as f:
        f.write(str(min(diffs)) + "\n")

def gen_cases():
    ensure_dirs()
    idx = 0

    # Group 1: 2 sample cases
    samples = [
        (5, [1, 4, 7, 12, 14]),
        (4, [10, 20, 25, 40]),
    ]
    for n, pos in samples:
        write_case(idx, n, pos)
        idx += 1

    # Group 2: 5 small random cases (N ≤ 100, X ≤ 1000)
    for _ in range(5):
        n = random.randint(2, 100)
        positions = sorted(random.sample(range(0, 1001), n))
        write_case(idx, n, positions)
        idx += 1

    # Group 3: 5 larger random cases (N ≤ 1000, X ≤ 10^6)
    for _ in range(5):
        n = random.randint(500, 1000)  # big stress test
        positions = sorted(random.sample(range(0, X_MAX+1), n))
        write_case(idx, n, positions)
        idx += 1

if __name__ == "__main__":
    random.seed(42)
    gen_cases()
