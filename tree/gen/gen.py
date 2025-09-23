#!/usr/bin/env python3
# Deterministic generator for full binary trees (each node has 0 or 2 children when rooted at 1).
# Produces exactly 26 testcases: index 0..25
# - 1 testcase n=1
# - 1 testcase n=3
# - 24 other testcases with odd n <= 1e5 (no duplicates)
#
# Each testcase produces:
#  - ../input/input{index}.txt  (n, followed by n-1 undirected edges)
#  - ../output/output{index}.txt (inorder, preorder, postorder traversals, each on its own line)
#
# Reproducible: fixed seed.

import random
import os
import sys
from collections import deque

random_seed = 2025
random.seed(random_seed)

sys.setrecursionlimit(1 << 25)

def ensure_dirs():
    os.makedirs("../input", exist_ok=True)
    os.makedirs("../output", exist_ok=True)

def write_case(index, n, edges, inorder, preorder, postorder):
    inp_path = f"../input/input{index}.txt"
    out_path = f"../output/output{index}.txt"
    with open(inp_path, "w") as f:
        f.write(f"{n}\n")
        for u, v in edges:
            f.write(f"{u} {v}\n")
    with open(out_path, "w") as f:
        f.write(" ".join(map(str, inorder)) + "\n")
        f.write(" ".join(map(str, preorder)) + "\n")
        f.write(" ".join(map(str, postorder)) + "\n")

def traversals_from_edges(n, edges):
    # build adjacency
    adj = [[] for _ in range(n+1)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    inorder = []
    preorder = []
    postorder = []
    def dfs(u, p):
        preorder.append(u)
        children = [v for v in adj[u] if v != p]
        children.sort()  # smaller child is left
        left = children[0] if len(children) >= 1 else None
        right = children[1] if len(children) == 2 else None
        if left is not None:
            dfs(left, u)
        inorder.append(u)
        if right is not None:
            dfs(right, u)
        postorder.append(u)
    dfs(1, 0)
    return inorder, preorder, postorder

def canonical_edge_signature(edges):
    # canonical normalized sorted tuple of edges to check duplicates
    normalized = tuple(sorted(tuple(sorted(e)) for e in edges))
    return normalized

# Generate a full binary tree of size n = 1 + 2*t (t expansions).
# shape controls which leaf we expand next:
#  - 'balanced' : BFS expansion (queue) -> near-perfect
#  - 'left-skew' : always expand the oldest leaf (simulate deep-left)
#  - 'right-skew' : always expand the newest leaf (deep-right)
#  - 'random' : pick a random current leaf to expand
#  - 'comb' : alternate expanding a deep path and then shallow leaf -> comb-like
def generate_full_binary_tree(n, shape='random'):
    assert n % 2 == 1 and n >= 1
    if n == 1:
        return [[] for _ in range(2)]  # nodes 1..1, but we return list sized n+1 (indexing convenience)
    total_nodes = n
    # We'll maintain:
    # nodes: integer labels from 1..n assigned as we create them
    # parent -> children mapping: children_list
    children = [[] for _ in range(n + 1)]
    # start with root node 1 as a leaf
    next_label = 2  # next node id to assign
    # leaves list: store node ids that are leaves (available to be expanded)
    # We'll use deque for 'balanced', list for 'right-skew' (stack-like), etc.
    if shape == 'balanced':
        leaves = deque([1])
    else:
        leaves = [1]

    expansions_needed = (n - 1) // 2
    # for comb shape we use a toggle
    comb_toggle = True

    for i in range(expansions_needed):
        # pick which leaf to expand
        if shape == 'balanced':
            leaf = leaves.popleft()
        elif shape == 'left-skew':
            # expand the left-most leaf (the earliest added) -> use pop(0)
            leaf = leaves.pop(0)
        elif shape == 'right-skew':
            # expand the most recently added leaf -> stack behavior
            leaf = leaves.pop()
        elif shape == 'comb':
            if comb_toggle:
                leaf = leaves.pop()  # deep path
            else:
                leaf = leaves.pop(0)  # shallow
            comb_toggle = not comb_toggle
        elif shape == 'random':
            idx = random.randrange(len(leaves))
            leaf = leaves.pop(idx)
        else:
            # default fallback: random
            idx = random.randrange(len(leaves))
            leaf = leaves.pop(idx)

        # create two children and attach to leaf
        left_child = next_label
        right_child = next_label + 1
        next_label += 2
        # we will not reorder labels: left_child will be smaller than right_child by construction
        # but when interpreting children for traversal we sort children ascending anyway.
        children[leaf].extend([left_child, right_child])
        # add new leaves into leaves structure
        if shape == 'balanced':
            leaves.append(left_child)
            leaves.append(right_child)
        elif shape == 'left-skew':
            # to make deep-left, add new children so left stays at front
            leaves.insert(0, left_child)
            leaves.insert(0, right_child)
        elif shape == 'right-skew':
            leaves.append(left_child)
            leaves.append(right_child)
        elif shape == 'comb':
            # add both but order matters for comb effect
            leaves.append(left_child)
            leaves.append(right_child)
        else:  # random or fallback
            leaves.append(left_child)
            leaves.append(right_child)
    # Build edges (parent-child)
    edges = []
    for u in range(1, n+1):
        for v in children[u]:
            edges.append((u, v))
    # final sanity: next_label should be n+1
    assert next_label == n+1, f"label mismatch next_label={next_label} expected {n+1}"
    return children, edges

def make_unique_testcases():
    # We'll build exactly 26 testcases.
    # Index 0 -> n=1
    # Index 1 -> n=3 (only valid tree)
    # Index 2..25 -> 24 other odd sizes <= 1e5 (no duplicates)
    testcases = []

    # Test 0: n = 1
    testcases.append((1, 'trivial'))

    # Test 1: n = 3 (unique valid tree: root 1 with children 2 and 3)
    testcases.append((3, 'tiny'))

    # Now 24 more sizes (odd, <= 100000), diverse:
    # chosen deterministically but varied: small, moderate, large, near-max
    sizes_24 = [
        5, 7, 9, 11, 15, 21, 31, 33, 47, 63, 65, 127,
        255, 511, 1023, 2047, 4095, 8191, 16383, 32767, 50001, 65535, 99997, 99999
    ]
    assert len(sizes_24) == 24

    # choose an assortment of shapes, cycle through them to ensure variety
    shapes = ['balanced', 'left-skew', 'right-skew', 'random', 'comb']
    for i, s in enumerate(sizes_24):
        shape = shapes[i % len(shapes)]
        testcases.append((s, shape))

    assert len(testcases) == 26
    return testcases

def main():
    ensure_dirs()
    testcases = make_unique_testcases()
    seen_signatures = set()
    index = 0
    for (n, shape) in testcases:
        if n == 1:
            # trivial single node
            edges = []
        elif n == 3:
            # unique full binary tree
            edges = [(1,2), (1,3)]
        else:
            # generate children and edges using our generator
            children, edges = generate_full_binary_tree(n, shape=shape)
            # edges returned are directed parent->child (u,v). ok for input (undirected)
        # canonical signature to ensure we don't accidentally repeat structure
        sig = canonical_edge_signature(edges)
        if sig in seen_signatures:
            print(f"Warning: duplicate detected for n={n}, shape={shape}. Regenerating with random shuffle.")
            # regenerate as random shape and different labelling
            children, edges = generate_full_binary_tree(n, shape='random')
            sig = canonical_edge_signature(edges)
            if sig in seen_signatures:
                raise RuntimeError("Couldn't produce unique testcase for n=%d" % n)
        seen_signatures.add(sig)

        # compute traversals
        inorder, preorder, postorder = traversals_from_edges(n, edges)

        # Quick validity check: each node must have 0 or 2 children when rooted at 1.
        adj = [[] for _ in range(n+1)]
        for u,v in edges:
            adj[u].append(v)
            adj[v].append(u)
        def child_count_rooted():
            counts = [0]*(n+1)
            stack = [(1,0)]
            while stack:
                u,p = stack.pop()
                cnt = 0
                for v in adj[u]:
                    if v == p: continue
                    cnt += 1
                    stack.append((v,u))
                counts[u] = cnt
            return counts
        counts = child_count_rooted()
        for u in range(1, n+1):
            if counts[u] not in (0,2):
                raise AssertionError(f"Node {u} in tree n={n} has {counts[u]} children (not 0 or 2). Test generation bug.")

        write_case(index, n, edges, inorder, preorder, postorder)
        print(f"Written testcase {index}: n={n}, shape={shape}, edges={len(edges)}")
        index += 1

    assert index == 26
    print(f"Generated {index} unique testcases (seed={random_seed}).")

if __name__ == "__main__":
    main()
