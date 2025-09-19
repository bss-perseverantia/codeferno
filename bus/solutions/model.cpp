#include <bits/stdc++.h>

int main() {
  auto _int = []() { int x; std::cin >> x; return x; };
  std::vector<int> a(_int());
  for (int &i : a) i += _int();
  for (int &i : a) i -= _int();
  int c = _int();
  std::cout << *std::ranges::max_element((std::partial_sum(a.begin(), a.end(), a.begin(), [c](int x, int y) { return std::min(x + y,  c); }), a)) << '\n';
}