// this is for emacs file handling -*- mode: c++; indent-tabs-mode: nil -*-
// -- BEGIN LICENSE BLOCK ----------------------------------------------
// -- END LICENSE BLOCK ------------------------------------------------
//----------------------------------------------------------------------
/*!\file
 *
 * \author  Christoph Rist <rist.christoph@gmail.com>
 * \date    2016-12-25
 *
 */
//----------------------------------------------------------------------
/***********************************
 * IEEE SB Passau Adventskalender
 * Problem 21
 */

#include <memory>
#include <algorithm>
#include <iostream>
#include <iomanip>
#include <vector>

//#define TEST
#ifdef TEST
#include "io_redirect.h"
#endif

using namespace std;

struct AABBRectangle
{
  AABBRectangle(double left, double right, double bottom, double top)
  : left(left), right(right), bottom(bottom), top(top)
  {}
  double left, right, bottom, top;

  bool collision(const AABBRectangle& other)
  {
    return bottom < other.top && top > other.bottom && left < other.right && right > other.left;
  }
};


int main(int argc, char* argv[])
{
#ifdef TEST
  //////////////////////// INPUT/OUTPUT //////////////////////////
  if (!redirect_io(argc, argv))
    return 0;
#endif

  uint32_t nb_rect;
  cin >> nb_rect;

  vector<AABBRectangle> rects;
  rects.reserve(nb_rect);

  for (uint32_t i = 0; i < nb_rect; ++i)
  {
    double left, right, bottom, top;
    cin >> left >> right >> bottom >> top;
    rects.emplace_back(left, right, bottom, top);
  }

  for (uint32_t i = 0; i < nb_rect; ++i)
  {
    cout <<i <<" with [";
    bool first = true;
    for (uint32_t j = 0; j < nb_rect; ++j)
    {
      if (j == i)
        continue;
      if (rects[i].collision(rects[j]))
      {
        if (first)
          first = false;
        else
        {
          cout <<", ";
        }
        cout <<j;
      }
    }
    cout <<"]" <<endl;
  }

#ifdef TEST
  cleanup_io();
#endif

  return 0;
}
