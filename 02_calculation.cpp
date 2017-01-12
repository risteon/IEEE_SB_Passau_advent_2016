// this is for emacs file handling -*- mode: c++; indent-tabs-mode: nil -*-
// -- BEGIN LICENSE BLOCK ----------------------------------------------
// -- END LICENSE BLOCK ------------------------------------------------
//----------------------------------------------------------------------
/*!\file
 *
 * \author  Christoph Rist <rist.christoph@gmail.com>
 * \date    2016-12-03
 *
 */
//----------------------------------------------------------------------

#include <algorithm>
#include <iostream>
#include <iomanip>
#include <string>
#include <stdexcept>
#include <vector>
#include <array>
#include <stack>

#define TEST

#ifdef TEST
#undef NDEBUG
#include <assert.h>
#endif

using namespace std;

using Int = int64_t;
using UInt = u_int64_t;

enum class Operator
{
  ADD = 0,
  SUB = 1,
  MUL = 2,
  DIV = 3,
  NEG = 4,
  MOD = 5,
  LSHIFT = 6,
  RSHIFT = 7,
  AND = 8,
  OR = 9,
  COMP = 10,
  XOR = 11,
  COUNT = 12
};

uint8_t getOperationOperandCount(Operator op)
{
  if (op == Operator::COUNT)
    throw logic_error("Invalid use");
  else if (op == Operator::NEG || op == Operator::COMP)
    return 1;
  else
    return 2;
}

Int calculate(Operator op, stack<Int>& operands)
{
  const uint8_t num_op = getOperationOperandCount(op);
  // sanity check
  if (operands.size() < num_op)
    throw runtime_error("Invalid expression: not enough operands.");

  // create vector, pop from stack
  vector<Int> ops(num_op);
  for (uint8_t i = num_op; i; --i)
  {
    ops[i-1] = operands.top();
    operands.pop();
  }

  switch(op)
  {
    case Operator::ADD: return ops[0] + ops[1];
    case Operator::SUB: return ops[0] - ops[1];
    case Operator::MUL: return ops[0] * ops[1];
    case Operator::DIV: return ops[0] / ops[1];
    case Operator::NEG: return -ops[0];
    case Operator::MOD: return (ops[0] % ops[1]) * (ops[1] >= 0 ? 1 : -1);
    case Operator::LSHIFT:
      if (ops[1] < 0)
        throw runtime_error("Lshift undefined behavior.");
      if (abs(ops[1]) >= sizeof(Int) * 8)
        return 0;
      else
        return static_cast<Int>(static_cast<UInt>(ops[0]) << ops[1]);
    case Operator::RSHIFT:
      if (ops[1] < 0)
        throw runtime_error("Rshift undefined behavior.");
      //if (abs(ops[1]) >= sizeof(Int) * 8)
      //  return 0;
      else
        //return static_cast<Int>(static_cast<UInt>(ops[0]) >> ops[1]);
        return ops[0] >> ops[1];
    case Operator::AND: return ops[0] & ops[1];
    case Operator::OR: return ops[0] | ops[1];
    case Operator::COMP: return ~ops[0];
    case Operator::XOR: return ops[0] ^ ops[1];
    default: throw runtime_error("Unknown operator");
  }
}

//! Hold either an operand or an operator. Parse from input string.
class Op
{
public:
  static const array<string, static_cast<uint8_t>(Operator::COUNT)> OP_NAMES;

  Op() = delete;
  //! Create from input string
  Op(const string& s)
  {
    if (s.empty())
      throw std::runtime_error("empty operator or operand");

    try
    {
      operand_ = stoi(s);
      operator_ = Operator::COUNT;
    }
    catch (invalid_argument&)
    {
      // conversion to integer failed, treat as operator
      const auto pos = std::find(OP_NAMES.cbegin(), OP_NAMES.cend(), s);
      if (pos == OP_NAMES.cend())
        throw std::runtime_error("unknown operator");
      operator_ = static_cast<Operator>(std::distance(OP_NAMES.cbegin(), pos));
      operand_ = std::numeric_limits<decltype(operand_)>::max();
    }
  }
  bool isOperand() const               { return operator_ == Operator::COUNT; }
  Int get() const                      { return operand_; }
  Operator getOperator() const         { return operator_; }

private:
  Operator operator_;
  Int operand_;
};

const array<string, static_cast<uint8_t>(Operator::COUNT)> Op::OP_NAMES =
{
  "add",
  "sub",
  "mul",
  "div",
  "neg",
  "mod",
  "lshift",
  "rshift",
  "and",
  "or",
  "comp",
  "xor"
};

Int getResult(const vector<string>& input)
{
  // Parse input strings and put as Op objects into container
  vector<Op> operations{};
  std::transform(input.cbegin(), input.cend(), std::back_inserter(operations), [](const string& s){return Op(s);});

  stack<Int> operands{};
  for (vector<Op>::const_iterator op = operations.cbegin(); op != operations.cend(); ++op)
  {
    if (op->isOperand())
    {
      // push new operand on stack
      operands.push(op->get());
    }
    else
    {
      // calculate using stack values
      operands.push(calculate(op->getOperator(), operands));
    }
  }
  return operands.top();
}

#ifndef TEST
int main()
{
  // Read input line into word vector
  vector<string> input{};
  string tmp;
  while (cin >> tmp)
    input.push_back(tmp);

  const auto res = getResult(input);
  cout <<res <<endl;

  return 0;
}
#else
int main()
{
  assert(getResult({"0"}) == 0);
  assert(getResult({"42"}) == 42);
  assert(getResult({"-42"}) == -42);
  assert(getResult({"6", "3", "add", "42", "9", "mul", "sub", "3", "div", "neg"}) == 123);
  assert(getResult({"2", "2", "2", "2", "2", "2", "add", "add", "add", "add", "add"}) == 12);
  assert(getResult({"-1", "6", "2", "3", "add", "mul", "5", "7", "sub", "div", "add"}) == -16);
  assert(getResult({"111", "neg"}) == -111);
  assert(getResult({"10", "4", "neg", "mod"}) == -2);
  assert(getResult({"10", "4", "mod"}) == 2);
  assert(getResult({"12", "-8", "mod"}) == -4);
  assert(getResult({"2", "2", "lshift"}) == 8);
  assert(getResult({"8", "2", "rshift"}) == 2);
  assert(getResult({"2", "4", "and"}) == 0);
  assert(getResult({"72", "184", "and"}) == 8);
  assert(getResult({"72", "184", "or"}) == 248);
  assert(getResult({"2", "4", "or"}) == 6);
  assert(getResult({"222", "comp"}) == -223);
  assert(getResult({"0", "comp"}) == -1);
  assert(getResult({"114", "170", "xor"}) == 216);
  assert(getResult({"123456789", "neg", "neg"}) == 123456789);
  assert(getResult({"-123456789", "neg", "neg"}) == -123456789);
  assert(getResult({"123456", "3", "lshift", "3", "rshift"}) == 123456);
  assert(getResult({"-1", "1", "lshift"}) == -2);
  assert(getResult({"1", "32", "lshift"}) == 4294967296);
  assert(getResult({"1", "64", "lshift"}) == 18446744073709551616);
  //assert(getResult({"-1", "32", "lshift"}) == 0);
  assert(getResult({"-1", "32", "lshift"}) == -4294967296);
  //assert(getResult({"-1", "32", "rshift"}) == 0);
  assert(getResult({"1", "32", "rshift"}) == 0);
  assert(getResult({"-1", "32", "rshift"}) == -1);

  return 0;
}
#endif
