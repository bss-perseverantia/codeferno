#include <limits.h>
#include <stdio.h>

int main() {
  int n;
  scanf("%d", &n);
  int ans = INT_MAX;
  int prev;
  scanf("%d", &prev);
  for (int i = 1, cur; i < n; ++i) {
    scanf("%d", &cur);
    ans = ans < cur - prev ? ans : cur - prev;
    prev = cur;
  }
  printf("%d\n", ans);
}