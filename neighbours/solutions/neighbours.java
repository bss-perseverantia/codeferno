import java.util.Scanner;

public class neighbours {
  public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);
    int n = sc.nextInt();
    int ans = Integer.MAX_VALUE;
    int prev = sc.nextInt();
    for (int i = 1; i < n; ++i) {
      int cur = sc.nextInt();
      ans = Math.min(ans, cur - prev);
      prev = cur;
    }
    System.out.print(ans + "\n");
  }  
}
