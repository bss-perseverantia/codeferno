import java.io.*;
import java.util.*;

public class bus {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st;
        Iterator<String> tokens = Arrays.asList(br.readLine().trim().split("\\s+")).iterator();
        int N = Integer.parseInt(tokens.next());
        int[] a = new int[N];
        st = new StringTokenizer(br.readLine());
        for (int i = 0; i < N; i++) {
            a[i] += Integer.parseInt(st.nextToken());
        }
        st = new StringTokenizer(br.readLine());
        for (int i = 0; i < N; i++) {
            a[i] -= Integer.parseInt(st.nextToken());
        }
        int C = Integer.parseInt(br.readLine().trim());
        for (int i = 1; i < N; i++) {
            a[i] = Math.min(a[i - 1] + a[i], C);
        }
        int maxVal = Math.min(a[0], C), idx = 0;
        for (int i = 1; i < N; i++) {
            if (a[i] > maxVal) {
                maxVal = a[i];
                idx = i;
            }
        }
        System.out.println(maxVal + " " + (idx + 1));
    }
}
