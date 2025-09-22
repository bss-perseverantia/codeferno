import itertools

_int = lambda: int(next(tokens))
tokens = iter(open(0).read().split())
n = _int()
a = [0] * n
for i in range(n):
    a[i] += _int()
for i in range(n):
    a[i] -= _int()
c = _int()
a[0] = min(a[0], c)
s = list(itertools.accumulate(a, lambda x, y: min(x + y, c)))
maxval = max(s)
idx = s.index(maxval) + 1
print(maxval, idx)