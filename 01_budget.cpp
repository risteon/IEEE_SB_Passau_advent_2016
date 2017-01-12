#include <algorithm>
#include <iostream>
#include <iomanip>
#include <string>
#include <sstream>
#include <stdexcept>
#include <vector>


using namespace std;

using UInt = uint64_t;
using Int = int64_t;

int main()
{
  size_t num_test_cases;
  cin >> num_test_cases;

  string line;
  // read only \n
  getline(cin, line);

  UInt total_sum = 0;

  for (size_t i = 0; i < num_test_cases; i++)
  {
    getline(cin, line);

    istringstream ss(line);
    string num;
    UInt sum = 0;

    while (ss >> num)
    {
      reverse(num.begin(), num.end());

      try
      {
        sum += static_cast<UInt>(stoi(num));

      }
      catch(invalid_argument& e)
      {
        return -1;
      }
    }

    total_sum += sum;

    string result = std::to_string(sum);
    reverse(result.begin(), result.end());
    cout <<result <<endl;
  }

  cout <<"Totale Summe: " <<total_sum <<endl;

  return 0;
}
