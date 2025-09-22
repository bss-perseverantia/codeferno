import os
import random
import sys
sys.setrecursionlimit(1 << 25)

def generate_tree(n):
    """Generates a valid binary tree rooted at node 1."""
    nodes = list(range(2, n + 1))
    random.shuffle(nodes)
    tree = [[] for _ in range(n + 1)]

    for i, u in enumerate(nodes):
        # pick a valid parent from already attached nodes (1 always exists)
        possible_parents = nodes[:i] + [1]
        parent = random.choice(possible_parents)
        tree[parent].append(u)

    return tree

def build_edges(tree):
    edges = []
    for u in range(1, len(tree)):
        for v in tree[u]:
            edges.append((u, v))
    return edges

def dfs_traversals(tree):
    inorder, preorder, postorder = [], [], []

    def dfs(u):
        preorder.append(u)
        children = sorted(tree[u])
        left = children[0] if len(children) >= 1 else None
        right = children[1] if len(children) == 2 else None

        if left is not None:
            dfs(left)
        inorder.append(u)
        if right is not None:
            dfs(right)
        postorder.append(u)

    dfs(1)
    return inorder, preorder, postorder

def write_case(index, n, edges, inorder, preorder, postorder):
    with open(f"../input/input{index}.txt", "w") as f:
        f.write(f"{n}\n")
        for u, v in edges:
            f.write(f"{u} {v}\n")

    with open(f"../output/output{index}.txt", "w") as f:
        f.write(" ".join(map(str, inorder)) + "\n")
        f.write(" ".join(map(str, preorder)) + "\n")
        f.write(" ".join(map(str, postorder)) + "\n")

def generate():
    os.makedirs("../input", exist_ok=True)
    os.makedirs("../output", exist_ok=True)

    index = 0

    # Subtask 1: n = 1
    n = 1
    tree = [[] for _ in range(n + 1)]
    inorder = preorder = postorder = [1]
    write_case(index, n, [], inorder, preorder, postorder)
    index += 1

    # Subtask 2: n = 3 (5 test cases)
    for _ in range(5):
        n = 3
        tree = generate_tree(n)
        edges = build_edges(tree)
        inorder, preorder, postorder = dfs_traversals(tree)
        write_case(index, n, edges, inorder, preorder, postorder)
        index += 1

    # Subtask 3: 20 test cases, n up to 10^5 (adjusted to lower for dev)
    for _ in range(20):
        n = random.randint(10, 500)  # For real tests: change 500 → 10**5
        tree = generate_tree(n)
        edges = build_edges(tree)
        inorder, preorder, postorder = dfs_traversals(tree)
        write_case(index, n, edges, inorder, preorder, postorder)
        index += 1

    print(f"✅ Generated {index} testcases.")

if __name__ == "__main__":
    generate()
