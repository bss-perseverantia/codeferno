import sys

data = list(map(int, sys.stdin.buffer.read().split()))
it = iter(data)
n = next(it)
adj = [[] for _ in range(n + 1)]
for _ in range(n - 1):
  u = next(it)
  v = next(it)
  adj[u].append(v)
  adj[v].append(u)
for neighbours in adj:
  neighbours.sort()

sys.setrecursionlimit(max(1000000, 2 * n + 10))

_in, pre, post = [], [], []

def dfs(u, p):
  pre.append(u)
  vis = 0
  for v in adj[u]:
    if v == p:
      continue
    if vis == 1:
      _in.append(u)
    vis += 1
    dfs(v, u)
  if vis == 0:
    _in.append(u)
  post.append(u)

dfs(1, 0)

out = [
  ' '.join(map(str, _in)),
  ' '.join(map(str, pre)),
  ' '.join(map(str, post)),
]
sys.stdout.write('\n'.join(out))