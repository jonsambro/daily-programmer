#include <iostream>

struct Count{
  long ones, twos;
};

Count Naive(int n){
  auto seq = new char[n+1];
  seq[1] = 1;
  seq[2] = 2;
  seq[3] = 2;
  int count[] = {0,1,2};

  auto i = 3, x = 4;
  while (x <= n){
    auto out = static_cast<char>((i+1) % 2 + 1);
    auto upper_bound = x + seq[i];
    for (; x < upper_bound && x <= n; x++){
      seq[x] = out;
    }
    count[out] += upper_bound <= n ? seq[i] : n - upper_bound + seq[i] + 1;
    i++;
  }
  delete [] seq;
  return {.ones = count[1], .twos = count[2]};
}

int main() {
  int n;
  std::cin >> n;

  auto count = Naive(n);

  std::cout << count.ones << ":" << count.twos << std::endl;

  return 0;
}