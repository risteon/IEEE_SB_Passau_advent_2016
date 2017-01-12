#!/usr/bin/env sh

if [ ! -e build ]; then
  mkdir build
fi

cd build
cmake ..
cmake --build . -- -j4


