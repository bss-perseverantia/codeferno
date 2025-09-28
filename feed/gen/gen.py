#!/usr/bin/env python3
# gen.py — Offthentic Feed test generator
#
# Creates:
#   ../input/input0.txt, ../input/input1.txt, ...
#   ../output/output0.txt, ../output/output1.txt, ...
#
# Coverage:
# - Subtask 1: n ≤ 100, k = 1 (min/max, all-same-timestamp, equal-like + increasing-time to catch wrong timestamp tie)
# - Subtask 2: n ≤ 2000, k ≤ 10 (dense equal timestamps; decreasing-likes to cause many "never appear"; equal-likes increasing t)
# - Subtask 3: n ≤ 1e5, k ≤ 100 (single large stress with clustered ties)
# - Subtask 4: general (k = n case; big same-timestamp adversarial; full max n,k)
#
# Notes:
# - Deterministic via fixed seeds
# - Ensures (u, t, l) are within problem constraints
# - Reference solution uses global-rank + Fenwick, O(n log n)

import os
import random
from typing import List, Tuple

# ------------------------
# Reference solver
# ------------------------

class Fenwick:
    def __init__(self, n: int):
        self.n = n
        self.fw = [0] * (n + 1)
    def add(self, i: int, v: int):
        i += 1
        while i <= self.n:
            self.fw[i] += v
            i += i & -i
    def sum_prefix(self, i: int) -> int:
        i += 1
        s = 0
        while i > 0:
            s += self.fw[i]
            i -= i & -i
        return s

def solve_reference(posts: List[Tuple[int,int,int,int]], k: int) -> List[int]:
    n = len(posts)

    # Global rank by (likes desc, time desc, user asc, idx asc)
    order_rank = sorted(posts, key=lambda x: (-x[2], -x[1], x[0], x[3]))
    rank_of = {p[3]: r for r, p in enumerate(order_rank)}

    # Process by time asc; within same time, better-first
    posts_time = sorted(posts, key=lambda x: (x[1], -x[2], x[0], x[3]))

    ft = Fenwick(n)
    ans = []
    for (u, t, l, idx1) in posts_time:
        r = rank_of[idx1]
        ft.add(r, 1)
        if ft.sum_prefix(r) <= k:
            ans.append(idx1)
    return ans

# ------------------------
# Utilities
# ------------------------

def ensure_dirs():
    os.makedirs("../input", exist_ok=True)
    os.makedirs("../output", exist_ok=True)

def write_case(case_id: int, posts: List[Tuple[int,int,int,int]], k: int):
    n = len(posts)
    inp_path = f"../input/input{case_id}.txt"
    out_path = f"../output/output{case_id}.txt"

    with open(inp_path, "w") as f:
        f.write(f"{n} {k}\n")
        posts_by_idx = sorted(posts, key=lambda x: x[3])
        for (u, t, l, idx1) in posts_by_idx:
            f.write(f"{u} {t} {l}\n")

    ans = solve_reference(posts, k)
    with open(out_path, "w") as f:
        f.write(" ".join(map(str, ans)).strip() + "\n")

def unique_users(n: int, rng: random.Random) -> List[int]:
    # generate n unique user IDs within [1, 1e9]
    return rng.sample(range(1, 10**9), n)

def make_posts_from_arrays(u_list, t_list, l_list) -> List[Tuple[int,int,int,int]]:
    n = len(u_list)
    seen = set()
    posts = []
    for i in range(n):
        u, t, l = u_list[i], t_list[i], l_list[i]
        # ensure (u,t) uniqueness
        if (u, t) in seen:
            u = min(u + 1, 10**9)
        seen.add((u, t))
        posts.append((u, t, l, i + 1))
    return posts

# ------------------------
# Generators per case
# ------------------------

def sample1(case_id: int) -> int:
    posts = [
        (10,1,5,1),
        (7,2,5,2),
        (3,2,8,3),
        (5,3,5,4),
        (2,5,10,5),
    ]
    write_case(case_id, posts, k=2)
    return case_id + 1

def sample2(case_id: int) -> int:
    posts = [
        (1,1,100,1),
        (2,2,50,2),
        (3,3,100,3),
        (4,4,200,4),
    ]
    write_case(case_id, posts, k=2)
    return case_id + 1

def subtask1_min(case_id: int) -> int:
    posts = [(42, 0, 0, 1)]
    write_case(case_id, posts, k=1)
    return case_id + 1

def subtask1_all_same_t_k1(case_id: int) -> int:
    rng = random.Random(1001)
    n, k = 100, 1
    u = unique_users(n, rng)
    t = [0]*n
    l = [rng.randint(0, 100000) for _ in range(n)]
    posts = make_posts_from_arrays(u, t, l)
    write_case(case_id, posts, k)
    return case_id + 1

def subtask1_equal_likes_increasing_t_k1(case_id: int) -> int:
    rng = random.Random(1002)
    n, k = 50, 1
    u = unique_users(n, rng)
    t = list(range(1, n+1))
    l = [777]*n
    posts = make_posts_from_arrays(u, t, l)
    write_case(case_id, posts, k)
    return case_id + 1

def subtask2_dense_random(case_id: int) -> int:
    rng = random.Random(2001)
    n, k = 2000, 10
    u = unique_users(n, rng)
    t = [rng.randint(0, 200) for _ in range(n)]
    l = [rng.randint(0, 100000) for _ in range(n)]
    posts = make_posts_from_arrays(u, t, l)
    write_case(case_id, posts, k)
    return case_id + 1

def subtask2_decreasing_likes(case_id: int) -> int:
    rng = random.Random(2002)
    n, k = 1500, 10
    u = unique_users(n, rng)
    t = list(range(n))
    # likes descending but capped at 1e5
    l = [min(100000, n - i) for i in range(n)]
    posts = make_posts_from_arrays(u, t, l)
    write_case(case_id, posts, k)
    return case_id + 1

def subtask2_equal_likes_increasing_t(case_id: int) -> int:
    rng = random.Random(2003)
    n, k = 1800, 10
    u = unique_users(n, rng)
    t = list(range(n))
    l = [50000]*n
    posts = make_posts_from_arrays(u, t, l)
    write_case(case_id, posts, k)
    return case_id + 1

def subtask3_large_clustered(case_id: int) -> int:
    rng = random.Random(3001)
    n, k = 100000, 100
    u = unique_users(n, rng)
    clusters = 50
    t, l = [], []
    for i in range(n):
        c = rng.randint(0, clusters - 1)
        t.append(c * 2000 + rng.randint(0, 999))
        l.append(rng.randint(min(c * 2000, 100000), min(c * 2000 + 999, 100000)))
    posts = make_posts_from_arrays(u, t, l)
    write_case(case_id, posts, k)
    return case_id + 1

def subtask4_k_equals_n(case_id: int) -> int:
    rng = random.Random(4001)
    n = 5000
    k = n
    u = unique_users(n, rng)
    t = [rng.randint(0, 10**6) for _ in range(n)]
    l = [rng.randint(0, 100000) for _ in range(n)]
    posts = make_posts_from_arrays(u, t, l)
    write_case(case_id, posts, k)
    return case_id + 1

def subtask4_big_same_time(case_id: int) -> int:
    rng = random.Random(4002)
    n, k = 12000, 75
    u = unique_users(n, rng)
    t = [123456789] * n
    l = [rng.randint(0, 100000) for _ in range(n)]
    posts = make_posts_from_arrays(u, t, l)
    write_case(case_id, posts, k)
    return case_id + 1

def subtask4_full_max(case_id: int) -> int:
    rng = random.Random(4003)
    n, k = 100000, 100000
    u = unique_users(n, rng)
    t = [rng.randint(0, 10**9) for _ in range(n)]
    l = [rng.randint(0, 100000) for _ in range(n)]
    posts = make_posts_from_arrays(u, t, l)
    write_case(case_id, posts, k)
    return case_id + 1

# ------------------------
# Main
# ------------------------

def main():
    ensure_dirs()
    cid = 0
    # Samples
    cid = sample1(cid)
    cid = sample2(cid)
    # Subtask 1
    cid = subtask1_min(cid)
    cid = subtask1_all_same_t_k1(cid)
    cid = subtask1_equal_likes_increasing_t_k1(cid)
    # Subtask 2
    cid = subtask2_dense_random(cid)
    cid = subtask2_decreasing_likes(cid)
    cid = subtask2_equal_likes_increasing_t(cid)
    # Subtask 3
    cid = subtask3_large_clustered(cid)
    # Subtask 4
    cid = subtask4_k_equals_n(cid)
    cid = subtask4_big_same_time(cid)
    cid = subtask4_full_max(cid)
    print(f"Generated {cid} test cases in ../input and ../output")

if __name__ == "__main__":
    main()
