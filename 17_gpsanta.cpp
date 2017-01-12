// this is for emacs file handling -*- mode: c++; indent-tabs-mode: nil -*-
// -- BEGIN LICENSE BLOCK ----------------------------------------------
// -- END LICENSE BLOCK ------------------------------------------------
//----------------------------------------------------------------------
/*!\file
 *
 * \author  Christoph Rist <rist.christoph@gmail.com>
 * \date    2016-12-28
 *
 */
//----------------------------------------------------------------------
/***********************************
 * IEEE SB Passau Adventskalender
 * Problem 17
 */

#include <memory>
#include <iostream>
#include <iomanip>
#include <vector>
#include <set>
#include <map>
#include <stack>
#include <cmath>
#include <algorithm>

//#define TEST
#ifdef TEST
#include "io_redirect.h"
#endif

using namespace std;


class Graph
{
public:
  using Node = pair<uint8_t, uint8_t>;

  void addEdge(const Node& first_node, const Node& second_node)
  {
    addNode(first_node);
    addNode(second_node);
    nodes_[first_node].insert(second_node);
  }

  uint32_t nbSimplePaths(const Node& start, const Node& end)
  {
    set<Node> visited{};
    uint32_t nb_paths = 0;

    stack<pair<Node, set<Node>::const_iterator>> s;
    s.emplace(start, nodes_[start].cbegin());

    while(!s.empty())
    {
      auto& n = s.top();

      if (n.first == end || n.second == nodes_[n.first].cend())
      {
        if (n.first == end)
          ++nb_paths;
        visited.erase(n.first);
        s.pop();
      }
      else
      {
        const Node& v = *n.second;
        ++n.second;

        if (visited.find(v) == visited.cend())
        {
          s.emplace(v, nodes_.at(v).cbegin());
          visited.insert(v);
        }
      }

    }

    return nb_paths;
  }
private:
  void addNode(const Node& n)
  {
    if (nodes_.find(n) == nodes_.cend())
    {
      nodes_.emplace(n, set<Node>{});
    }
  }

  map<Node, set<Node>> nodes_;
};

Graph buildGraph(uint8_t size)
{
  Graph g{};
  for (uint8_t x = 1; x < size; ++x)
  {
    for (uint8_t y = 0; y < x; ++y)
    {
      g.addEdge({x - 1, y}, {x, y});
      g.addEdge({x, y}, {x, y + 1});
    }
  }
  return g;
}

int main(int argc, char* argv[])
{
#ifdef TEST
  //////////////////////// INPUT/OUTPUT //////////////////////////
  if (!redirect_io(argc, argv))
    return 0;
#endif

  uint32_t nb_testcases;
  cin >> nb_testcases;
  vector<uint8_t> sizes{};
  // parse
  string l;
  getline(cin, l);
  for (uint32_t i = 0; i < nb_testcases; ++i)
  {
    getline(cin, l);
    const auto it = std::find(l.cbegin(), l.cend(), 'x');
    if (it == l.cend())
      throw runtime_error("Invalid input");

    const int32_t first = stoi(string(l.cbegin(), it));
    const int32_t second = stoi(string(it + 1, l.cend()));

    if (first < 0 || first != second || first > 255)
      throw runtime_error("Invalid input");

    sizes.push_back(static_cast<uint8_t>(first));
  }

  for (uint8_t s : sizes)
  {
    auto g = buildGraph(s + 1);
    cout <<g.nbSimplePaths({0, 0}, {s, s}) <<endl;
  }


#ifdef TEST
  cleanup_io();
#endif

  return 0;
}
