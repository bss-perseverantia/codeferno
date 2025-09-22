#include <stdio.h>

#define N 1000

int a[N];

int main() {
  int n;
  scanf("%d", &n);
  for (int i = 0, x; i < n; ++i) {
    scanf("%d", &x);
    a[i] += x;
  }
  for (int i = 0, x; i < n; ++i) {
    scanf("%d", &x);
    a[i] -= x;
  }
  int c;
  scanf("%d", &c);
  int ans = 0, idx = 0;
  for (int i = 0, sum = 0; i < n; ++i) {
    sum = c < sum + a[i] ? c : sum + a[i];
    if (sum > ans) {
      ans = sum;
      idx = i;
    }
  }
  printf("%d %d\n", ans, idx + 1);
}