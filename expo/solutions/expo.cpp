#include <cstdint>
#include <iostream>

int main() {
  std::ios::sync_with_stdio(false);
  std::cin.tie(nullptr);
  int t;
  std::cin >> t;
  while (t--) {
    int64_t a, b, m;
    std::cin >> a >> b >> m;
    int64_t ans = 1, p = a;
    for (int bt = 0; bt < 30; ++bt) {
      if (b & (1 << bt)) {
        ans = (ans * p) % m;
      }
      p = (p * p) % m;
    }
    std::cout << ans << '\n';
  }
}