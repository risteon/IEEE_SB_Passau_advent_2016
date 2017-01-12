// this is for emacs file handling -*- mode: c++; indent-tabs-mode: nil -*-
// -- BEGIN LICENSE BLOCK ----------------------------------------------
// -- END LICENSE BLOCK ------------------------------------------------
//----------------------------------------------------------------------
/*!\file
 *
 * \author  Christoph Rist <rist.christoph@gmail.com>
 * \date    2016-12-04
 *
 */
//----------------------------------------------------------------------
/***********************************
 * IEEE SB Passau Adventskalender
 * Problem 04
 */

#include <memory>
#include <algorithm>
#include <iostream>
#include <iomanip>
#include <string>
#include <stdexcept>
#include <vector>
#include <array>
#include <map>
#include <set>

//#define TEST
#ifdef TEST
#include "io_redirect.h"
#endif

using namespace std;


enum class Direction
{
  UP = 0,
  RIGHT = 1,
  DOWN = 2,
  LEFT = 3,
  NB_NEIGHBORS = 4
};

string directionToStr(const vector<Direction>& dirs)
{
  string s;
  for (Direction d : dirs)
  {
    char c;
    switch (d)
    {
      case Direction::UP: c = 'N'; break;
      case Direction::RIGHT: c = 'O'; break;
      case Direction::LEFT: c = 'W'; break;
      case Direction::DOWN: c = 'S'; break;
      default: throw logic_error("Invalid value.");
    }
    s += c;
  }
  return s;
}

// (0,0) ---> x
//   |
//   y

//! Simple x, y coordinates. Unsigned, (0,0) is upper-right
struct Pos
{
  //! create invalid position
  Pos()
          : x(std::numeric_limits<decltype(x)>::max())
  {}
  //! create position from coordinates
  Pos(uint32_t x, uint32_t y)
          : x(x)
          , y(y)
  {}

  //! define strict weak ordering to use as map key
  bool operator< (const Pos& other) const
  {
    if (y != other.y)
      return y < other.y;
    return x < other.x;
  }
  bool operator== (const Pos& other) const  { return x == other.x && y == other.y; }
  bool invalid() const                      { return x == std::numeric_limits<decltype(x)>::max(); }

  uint32_t x;
  uint32_t y;
};
// all adjacent positions
using AdjacentPositionArray = array<Pos, static_cast<uint32_t>(Direction::NB_NEIGHBORS)>;

//! Represent a graph node. This is an accessible field at a unique position.
struct Node
{
  Node(const Pos& p, bool exit)
          : p(p)
          , exit(exit)
          , cost(numeric_limits<decltype(cost)>::max())
          , fscore(numeric_limits<decltype(cost)>::max())
  {}

  using Ptr = shared_ptr<Node>;
  using WPtr = weak_ptr<Node>;
  using Adjacency = array<Node::WPtr, static_cast<uint32_t>(Direction::NB_NEIGHBORS)>;

  Pos p;
  bool exit;
  //! Adjacent nodes
  Adjacency adj;
  //! Cost aka gscore
  uint32_t cost;
  //! Reach goal passing this node aka fscore
  uint32_t fscore;
  //! Node from where this node is reached from
  WPtr came_from;
  //! Direction from where this node is reached from
  Direction came_from_direction;

  //! strict weak ordering using fscore, same fscore returns a comparison by unique positions
  bool operator< (const Node& other) const
  {
    if (fscore != other.fscore)
      return fscore < other.fscore;
    return p < other.p;
  }
  //! Positions are unique, so check for equality by positions
  bool operator== (const Node& other) const
  {
    return p == other.p;
  }
};
//! Overloads for shared ptr of Node
bool operator< (const Node::Ptr& a, const Node::Ptr& b)     { return *a < *b; }
bool operator== (const Node::Ptr& a, const Node::Ptr& b)    { return *a == *b; }

//! Spatial grid layout
struct Grid
{
  Pos start_pos;
  uint32_t width;
  uint32_t height;
  vector<bool> grid;

  AdjacentPositionArray getAdjacent(const Pos& pos) const
  {
    AdjacentPositionArray adj{};
    if (pos.x > 0 && atPos(Pos(pos.x - 1, pos.y)))
      adj[static_cast<uint32_t>(Direction::LEFT)] = Pos(pos.x - 1, pos.y);
    if (pos.y > 0 && atPos(Pos(pos.x, pos.y - 1)))
      adj[static_cast<uint32_t>(Direction::UP)] = Pos(pos.x, pos.y - 1);
    if (pos.x < width - 1 && atPos(Pos(pos.x + 1, pos.y)))
      adj[static_cast<uint32_t>(Direction::RIGHT)] = Pos(pos.x + 1, pos.y);
    if (pos.y < height - 1 && atPos(Pos(pos.x, pos.y + 1)))
      adj[static_cast<uint32_t>(Direction::DOWN)] = Pos(pos.x, pos.y + 1);
    return adj;
  }
  Pos indexToPos(uint32_t index) const         { return Pos(index % width, index / width); }
  uint32_t posToIndex(const Pos& pos) const    { return pos.y * width + pos.x; }
  bool atPos(const Pos& pos) const             { return grid[posToIndex(pos)]; }
  bool isExit(const Pos& pos) const            { return pos.x == 0 || pos.x == width - 1 ||
                                                        pos.y == 0 || pos.y == height -1 ;}

  static Grid fromInput()
  {
    Grid grid{};
    cin >> grid.height >> grid.width;
    grid.grid.reserve(grid.height * grid.width);

    string line;
    // read line break
    getline(cin, line);
    uint32_t counter = 0;
    for (uint32_t i = 0; i < grid.height; ++i)
    {
      getline(cin, line);
      if (line.size() != grid.width)
        throw runtime_error("Invalid input.");

      for (char c : line)
      {
        switch (c)
        {
          case '#':
            grid.grid.push_back(false);
            break;
          case 'X':
            grid.start_pos = grid.indexToPos(counter);
          case '.':
            grid.grid.push_back(true);
            break;
          default:
            throw runtime_error("Invalid input character.");

        }
        ++counter;
      }
    }
    return grid;
  }

private:
  Grid() {}
};

//! The graph for path search. Keeps information about start and exits
class Graph
{
public:
  Graph() = delete;
  Graph(const Grid& grid)
  {
    // create Node for every accessible field
    for (uint32_t i = 0; i < grid.grid.size(); ++i)
    {
      if (grid.grid[i])
      {
        const Pos p = grid.indexToPos(i);
        const bool exit = grid.isExit(p);
        Node::Ptr n = make_shared<Node>(p, exit);
        nodes_.emplace(p, n);
        if (exit)
        {
          exits_.push_back(n);
        }
        if (p == grid.start_pos)
        {
          if (start_ != nullptr)
            throw runtime_error("Two start positions!");
          start_ = n;
        }
      }
    }
    // connect nodes
    for (const pair<Pos, Node::Ptr>& p : nodes_)
    {
      const AdjacentPositionArray adj_pos = grid.getAdjacent(p.first);
      for (uint32_t d = 0; d < static_cast<uint32_t>(Direction::NB_NEIGHBORS); ++d)
      {
        if (!adj_pos[d].invalid())
        {
          p.second->adj[d] = nodes_.at(adj_pos[d]);
        }
      }
    }
    // sanity check
    if (exits_.empty() || start_ == nullptr)
      throw runtime_error("Invalid input");

  }
  //! A* shortest path search
  Node::Ptr searchShortest() const
  {
    // sets are sorted not sorted by fscore if nodes fscore gets updated
    set<Node::Ptr> closed{};
    set<Node::Ptr> open{start_};
    start_->cost = 0;
    start_->fscore = costEstimate(start_->p);

    while (!open.empty())
    {
      // node with lowest fscore, explicit search in set is necessary
      const Node::Ptr n = *min_element(open.cbegin(), open.cend(),
                                       [](const Node::Ptr& a, const Node::Ptr& b) {return *a < *b;});

      // check if this is an exit
      for (const Node::Ptr& e : exits_)
      {
        if (n == e)
          return e;
      }

      open.erase(n);
      closed.insert(n);
      // check neighbors
      for (uint32_t d = 0; d < static_cast<uint32_t>(Direction::NB_NEIGHBORS); ++d)
      {
        // no neighbor...
        if (n->adj[d].expired())
          continue;
        Node::Ptr neighbor = n->adj[d].lock();
        if (closed.find(neighbor) != closed.cend())
          continue;

        // start to neighbor, distance between a node and its neighbor is always 1
        const uint32_t tentative_cost = n->cost + 1;

        // discover new node (if not in open set)
        if (open.find(neighbor) == open.cend())
          open.insert(neighbor);
        // abort if this is no better path
        else if (tentative_cost >= neighbor->cost)
          continue;

        // is best path
        neighbor->cost = tentative_cost;
        neighbor->fscore = tentative_cost + costEstimate(neighbor->p);
        neighbor->came_from = n;
        neighbor->came_from_direction = static_cast<Direction>(d);
      }

    }
    return nullptr;
  }

  vector<Direction> outputPath(const Node::Ptr& from) const
  {
    vector<Direction> d{};
    Node::Ptr current = from;
    while (current != start_)
    {
      d.push_back(current->came_from_direction);
      current = current->came_from.lock();
    }
    return d;
  }

private:
  //! Manhattan distance
  uint32_t manhattanDistance(const Pos& from, const Pos& to) const
  {
    return static_cast<uint32_t>(abs(static_cast<int64_t>(from.x) - static_cast<int64_t>(to.x)))
           + static_cast<uint32_t>(abs(static_cast<int64_t>(from.y) - static_cast<int64_t>(to.y)));
  }

  //! Heuristic
  uint32_t costEstimate(const Pos& from) const
  {
    uint32_t best = numeric_limits<uint32_t>::max();
    for (const Node::Ptr& n : exits_)
    {
      uint32_t dist = manhattanDistance(from, n->p);
      if (dist < best)
        best = dist;
    }
    return best;
  }

  Node::Ptr start_;
  map<Pos, Node::Ptr> nodes_;
  vector<Node::Ptr> exits_;
};

int main(int argc, char* argv[])
{
#ifdef TEST
  //////////////////////// INPUT/OUTPUT //////////////////////////
  if (!redirect_io(argc, argv))
    return 0;
#endif

  const Grid grid = Grid::fromInput();
  const Graph graph(grid);
  const Node::Ptr& exit = graph.searchShortest();
  if (exit == nullptr)
    throw runtime_error("No solution, input invalid.");

  vector<Direction> dirs = graph.outputPath(exit);
  // walking from exit to start, need to reverse
  reverse(dirs.begin(), dirs.end());
  // if on exit tile, one step out of the grid is needed, must be same as last direction, so repeat last direction
  dirs.push_back(dirs.back());
  cout <<directionToStr(dirs) <<endl;

#ifdef TEST
  cleanup_io();
#endif

  return 0;
}
