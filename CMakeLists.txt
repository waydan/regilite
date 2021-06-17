cmake_minimum_required(VERSION 3.16)

project(regilite CXX)

add_library(regilite INTERFACE)
target_include_directories(regilite INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}/src)
target_compile_features(regilite INTERFACE cxx_std_14)

option(REGILITE_BUILD_TESTS "Build tests" ON)
if(REGILITE_BUILD_TESTS)
enable_testing()
find_package(CppUTest REQUIRED)
add_subdirectory(test)
endif()
