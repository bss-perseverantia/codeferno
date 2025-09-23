#include <bits/stdc++.h>

int main() {
  std::ios::sync_with_stdio(false);
  std::cin.tie(nullptr);

  int n;
  std::cin >> n;
  std::vector<std::vector<int>> adj(n + 1);
  for (int i = 0, u, v; i < n - 1; ++i) {
    std::cin >> u >> v;
    adj[u].push_back(v);
    adj[v].push_back(u);
  }
  for (auto &i : adj) {
    std::sort(i.begin(), i.end());
  }

  std::vector<int> in, pre, post;
  auto dfs = [&](auto &&self, int u, int p) -> void {
    pre.push_back(u);
    int vis = 0;
    for (int &i : adj[u]) {
      if (i == p) {
        continue;
      }
      if (vis++ == 1) {
        in.push_back(u);
      }
      self(self, i, u);
    }
    if (!vis) {
      in.push_back(u);
    }
    post.push_back(u);
  };
  dfs(dfs, 1, 0);

  for (int &i : in) {
    std::cout << i << ' ';
  }
  std::cout << '\n';
  for (int &i : pre) {
    std::cout << i << ' ';
  }
  std::cout << '\n';
  for (int &i : post) {
    std::cout << i << ' ';
  }
  std::cout << '\n';
}