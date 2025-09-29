import sys

n = int(sys.stdin.readline())
a = list(map(int, sys.stdin.readline().split()))
diffs = [a[i + 1] - a[i] for i in range(n - 1)]
print(min(diffs))
