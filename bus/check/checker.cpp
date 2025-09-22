#include <bits/stdc++.h>
using namespace std;

/*
CMS runs checker as:
  checker <input> <correct_output> <contestant_output>

Contract:
  - Print a floating-point score to stdout (e.g. "1.0", "0.0").
  - Print messages for contestants/admins to stderr.
  - Always return 0.
*/

int main(int argc, char *argv[]) {
  if (argc < 4) {
    cerr << "Usage: checker <in> <out> <user_out>\n";
    printf("0.0\n");
    return 0;
  }

  ifstream fin(argv[1]);  // problem input
  ifstream fans(argv[2]); // correct output
  ifstream fout(argv[3]); // contestant output

  if (!fin || !fans || !fout) {
    cerr << "File open error\n";
    printf("0.0\n");
    return 0;
  }

  int N;
  fin >> N;
  vector<int> on(N), off(N);
  for (int i = 0; i < N; i++)
    fin >> on[i];
  for (int i = 0; i < N; i++)
    fin >> off[i];
  long long C;
  fin >> C;

  long long correct_max;
  fans >> correct_max;

  long long user_max;
  if (!(fout >> user_max)) {
    cerr << "Contestant output missing first number\n";
    printf("0.0\n");
    return 0;
  }

  if (user_max != correct_max) {
    cerr << "Expected max=" << correct_max << " but got " << user_max << "\n";
    printf("0.0\n");
    return 0;
  }

  long long correct_index;
  if (fans >> correct_index) {
    long long user_index;
    if (!(fout >> user_index)) {
      cerr << "Expected an index in output\n";
      printf("0.0\n");
      return 0;
    }
    if (user_index != correct_index) {
      cerr << "Expected index=" << correct_index
           << " but got " << user_index << "\n";
      printf("0.0\n");
      return 0;
    }
  }

  // If we reach here, everything matched
  cerr << "Output correct\n";
  printf("1.0\n");
  return 0;
}