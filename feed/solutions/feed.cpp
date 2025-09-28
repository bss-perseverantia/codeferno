#include <bits/stdc++.h>

class segment_tree {
public:
  int n;
  std::vector<int> seg;

  segment_tree(int n) : n(n), seg(2 * n) {}

  void set(int idx, int x) {
    for (seg[idx += n] = x, idx /= 2; idx > 0; idx /= 2) {
      seg[idx] = seg[2 * idx] + seg[2 * idx + 1];
    }
  }

  int query(int l, int r) {
    int ans = 0;
    for (l += n, r += n + 1; l < r; l /= 2, r /= 2) {
      if (l & 1)
        ans += seg[l++];
      if (r & 1)
        ans += seg[--r];
    }
    return ans;
  }
};

int main() {
  std::ios::sync_with_stdio(false);
  std::cin.tie(nullptr);

  int n, k;
  std::cin >> n >> k;
  struct post {
    int u, t, l, i, rank;
  };
  std::vector<post> a(n);
  for (int i = 0; i < n; ++i) {
    std::cin >> a[i].u >> a[i].t >> a[i].l;
    a[i].i = i;
  }
  std::sort(a.begin(), a.end(), [](post a, post b) {
    if (a.l != b.l) {
      return a.l > b.l;
    }
    if (a.t != b.t) {
      return a.t > b.t;
    }
    return a.u < b.u;
  });
  for (int i = 0; i < n; ++i) {
    a[i].rank = i;
  }
  std::sort(a.begin(), a.end(), [](post a, post b) {
    if (a.t != b.t) {
      return a.t < b.t;
    }
    if (a.l != b.l) {
      return a.l > b.l;
    }
    return a.u < b.u;
  });
  std::vector<int> ans;
  segment_tree st(n);
  for (auto &i : a) {
    st.set(i.rank, 1);
    if (st.query(0, i.rank) <= k) {
      ans.push_back(i.i);
    }
  }
  for (int &i : ans) {
    std::cout << i + 1 << ' ';
  }
  std::cout << '\n';
}