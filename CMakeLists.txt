cmake_minimum_required(VERSION 3.16)
project(regilite CXX)

enable_testing()

option(REGILITE_BUILD_TESTS "Build tests" ON)

# Register manipulation header library
add_subdirectory(regilite)

# Register header generator utility
add_subdirectory(regenerator)