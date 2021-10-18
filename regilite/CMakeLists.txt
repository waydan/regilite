add_library(regilite INTERFACE)
target_include_directories(regilite INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}/src)
target_compile_features(regilite INTERFACE cxx_std_14)

if(REGILITE_BUILD_TESTS)
find_package(CppUTest REQUIRED)
add_subdirectory(test)
endif()