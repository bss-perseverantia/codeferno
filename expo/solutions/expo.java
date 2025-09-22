import java.util.Scanner;

public class expo {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int t = sc.nextInt();
        for (int i = 0; i < t; ++i) {
            long a = sc.nextLong(), b = sc.nextLong(), m = sc.nextLong();
            long ans = 1, p = a;
            for (int bt = 0; bt < 30; ++bt) {
                if ((b & (1 << bt)) != 0) {
                    ans = (ans * p) % m;
                }
                p = (p * p) % m;
            }
            System.out.print(ans + "\n");
        }
        sc.close();
    }
}