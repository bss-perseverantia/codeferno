#include <stdio.h>

#define N 100000

int adj[N + 1][3], size[N + 1], in[N], pre[N], post[N], a, b, c;

void dfs(int u, int p) {
  pre[a++] = u;
  int vis = 0;
  for (int i = 0; i < size[u]; ++i) {
    if (adj[u][i] == p) {
      continue;
    }
    if (vis++ == 1) {
      in[b++] = u;
    }
    dfs(adj[u][i], u);
  }
  if (!vis) {
    in[b++] = u;
  }
  post[c++] = u;
}

int main() {
  int n;
  scanf("%d", &n);
  for (int i = 0, u, v; i < n - 1; ++i) {
    scanf("%d%d", &u, &v);
    adj[u][size[u]++] = v;
    adj[v][size[v]++] = u;
  }
  for (int i = 1; i <= n; ++i) {
    for (int j = 0; j < size[i]; ++j) {
      for (int k = j + 1; k < size[i]; ++k) {
        if (adj[i][j] > adj[i][k]) {
          int t = adj[i][j];
          adj[i][j] = adj[i][k];
          adj[i][k] = t;
        }
      }
    }
  }

  dfs(1, 0);

  for (int i = 0; i < n; ++i) {
    printf("%d ", in[i]);
  }
  printf("\n");
  for (int i = 0; i < n; ++i) {
    printf("%d ", pre[i]);
  }
  printf("\n");
  for (int i = 0; i < n; ++i) {
    printf("%d ", post[i]);
  }
  printf("\n");
}