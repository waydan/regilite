cmake_minimum_required(VERSION 3.16)

project(registex CXX)

set(CMAKE_CXX_STANDARD 20)

option(BUILD_TESTS "Build tests" ON)
if(BUILD_TESTS)
enable_testing()
find_package(CppUTest REQUIRED)
add_subdirectory(test)
endif()

set(SRC_PATH ${CMAKE_CURRENT_SOURCE_DIR}/src CACHE STRING "")