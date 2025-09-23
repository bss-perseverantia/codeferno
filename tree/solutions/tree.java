import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class tree {
  private static List<Integer>[] adj;
  private static final List<Integer> in = new ArrayList<>();
  private static final List<Integer> pre = new ArrayList<>();
  private static final List<Integer> post = new ArrayList<>();

  public static void main(String[] args) {
    new Thread(null, () -> {
      try {
        run();
      } catch (IOException e) {
        throw new RuntimeException(e);
      }
    }, "", 1 << 26).start();
  }

  private static void run() throws IOException {
    FastScanner fs = new FastScanner(System.in);
    int n = fs.nextInt();
    if (n <= 0) {
      return;
    }
    adj = new ArrayList[n + 1];
    for (int i = 0; i <= n; ++i) {
      adj[i] = new ArrayList<>();
    }
    for (int i = 0; i < n - 1; ++i) {
      int u = fs.nextInt();
      int v = fs.nextInt();
      adj[u].add(v);
      adj[v].add(u);
    }
    for (int i = 0; i <= n; ++i) {
      Collections.sort(adj[i]);
    }

    dfs(1, 0);

    StringBuilder sb = new StringBuilder();
    appendList(sb, in);
    appendList(sb, pre);
    appendList(sb, post);
    System.out.print(sb);
  }

  private static void dfs(int u, int p) {
    pre.add(u);
    int vis = 0;
    for (int v : adj[u]) {
      if (v == p) {
        continue;
      }
      if (vis == 1) {
        in.add(u);
      }
      vis++;
      dfs(v, u);
    }
    if (vis == 0) {
      in.add(u);
    }
    post.add(u);
  }

  private static void appendList(StringBuilder sb, List<Integer> values) {
    for (int value : values) {
      sb.append(value).append(' ');
    }
    sb.append('\n');
  }

  private static class FastScanner {
    private final InputStream in;
    private final byte[] buffer = new byte[1 << 16];
    private int ptr = 0;
    private int len = 0;

    FastScanner(InputStream in) {
      this.in = in;
    }

    int nextInt() throws IOException {
      int c;
      while ((c = read()) <= ' ') {
        if (c == -1) {
          return -1;
        }
      }
      int sign = 1;
      if (c == '-') {
        sign = -1;
        c = read();
      }
      int val = 0;
      while (c > ' ') {
        val = val * 10 + c - '0';
        c = read();
      }
      return val * sign;
    }

    private int read() throws IOException {
      if (ptr >= len) {
        len = in.read(buffer);
        ptr = 0;
        if (len <= 0) {
          return -1;
        }
      }
      return buffer[ptr++];
    }
  }
}
