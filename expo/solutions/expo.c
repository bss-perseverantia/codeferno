#include <stdio.h>

int main() {
  int t;
  scanf("%d", &t);
  while (t--) {
    long long a, b, m;
    scanf("%lld%lld%lld", &a, &b, &m);
    long long ans = 1, p = a;
    for (int bt = 0; bt < 30; ++bt) {
      if (b & (1 << bt)) {
        ans = (ans * p) % m;
      }
      p = (p * p) % m;
    }
    printf("%lld\n", ans);
  }
}