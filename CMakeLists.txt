#
cmake_minimum_required (VERSION 2.8)
project (advent)

SET(CMAKE_CXX_FLAGS "-std=c++0x")
SET(CMAKE_BUILD_TYPE "Debug")

add_executable (01_budget 01_budget.cpp)
add_executable (02_calculation 02_calculation.cpp)
add_executable (04_party_preparations 04_party_preparations.cpp io_redirect.cpp)
add_executable (05_weekday 05_weekday.cpp)
add_executable (07_christmas_illumination 07_christmas_illumination.cpp)
add_executable (17_gpsanta 17_gpsanta.cpp io_redirect.cpp)
add_executable (21_collision_ahead 21_collision_ahead.cpp io_redirect.cpp)
