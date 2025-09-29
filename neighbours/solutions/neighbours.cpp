#include <bits/stdc++.h>

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(nullptr);

  int n;
  std::cin >> n;
  std::vector<int> a(n);
  for (int &i : a) {
    std::cin >> i;
  }
  std::adjacent_difference(a.begin(), a.end(), a.begin());
  std::cout << *std::min_element(a.begin() + 1, a.end()) << '\n';
}