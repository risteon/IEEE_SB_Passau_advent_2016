//
#include "io_redirect.h"

#include <fstream>
#include <iostream>
#include <sys/stat.h>

std::streambuf* coutbuf = nullptr;
std::streambuf* cinbuf = nullptr;
std::ifstream in{};
std::ofstream out{};

bool redirect_io(int argc, char* argv[])
{
  if (argc < 2)
  {
    std::cerr <<"Set input file as Argument! jam.out B-sample.in" <<std::endl;
    return false;
  }
  struct stat buffer;
  if (stat (argv[1], &buffer) != 0)
  {
    std::cerr <<"Make sure input exists: " <<argv[1] <<std::endl;
    return false;
  }
  coutbuf = nullptr;
  cinbuf = nullptr;
  in.open(argv[1]);
  cinbuf = std::cin.rdbuf(in.rdbuf());
  if (argc > 2)     //< write to output file
  {
    out.open(argv[2]);
    coutbuf = std::cout.rdbuf(out.rdbuf());
  }

  return true;
}

void cleanup_io()
{
  if (coutbuf)
    std::cout.rdbuf(coutbuf);
  if (cinbuf)
    std::cin.rdbuf(cinbuf);
}