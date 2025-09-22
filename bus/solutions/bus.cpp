#include <bits/stdc++.h>

int main() {
  std::ios::sync_with_stdio(false);
  std::cin.tie(nullptr);
  auto _int = []() { int x; std::cin >> x; return x; };
  std::vector<int> a(_int());
  for (int &i : a) i += _int();
  for (int &i : a) i -= _int();
  int c = _int();
  a[0] = std::min(a[0], c);
  auto it = std::ranges::max_element((std::partial_sum(a.begin(), a.end(), a.begin(), [c](int x, int y) { return std::min(x + y,  c); }), a));
  std::cout << *it << ' ' <<  it - a.begin() + 1 << '\n';
}