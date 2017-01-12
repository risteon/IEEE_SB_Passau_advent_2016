// this is for emacs file handling -*- mode: c++; indent-tabs-mode: nil -*-
// -- BEGIN LICENSE BLOCK ----------------------------------------------
// -- END LICENSE BLOCK ------------------------------------------------
//----------------------------------------------------------------------
/*!\file
 *
 * \author  Christoph Rist <rist.christoph@gmail.com>
 * \date    2016-12-05
 *
 */
//----------------------------------------------------------------------
/***********************************
 * IEEE SB Passau Adventskalender
 * Problem 05
 */

#include <iostream>
#include <string>
#include <ctime>
#include <iomanip>
#include <stdexcept>


std::string getWeekdayString(int wday)
{
  switch (wday)
  {
    case 0: return "Montag";
    case 1: return "Dienstag";
    case 2: return "Mittwoch";
    case 3: return "Donnerstag";
    case 4: return "Freitag";
    case 5: return "Samstag";
    case 6: return "Sonntag";
    default: throw std::runtime_error("Invalid wday");
  }
}

/**
 * Solve this problem most fast, easy and error-proof
 * by making use of standard library functionality.
 * ... don't reinvent the wheel ...
 */

int main(int argc, char* argv[])
{
  uint32_t nb_testcases;
  std::cin >> nb_testcases;

  int y, m, d;
  for (uint32_t i = 0; i < nb_testcases; ++i)
  {
    std::cin >> y >> m >> d;
    std::tm t = {0, 0, 12, d, m - 1, y - 1990, 0, 0, 0};
    std::mktime(&t);
    std::cout <<getWeekdayString(t.tm_wday) <<std::endl;
  }

  return 0;
}
