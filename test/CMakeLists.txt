include_directories(${SRC_PATH})

add_executable(read_write_unit read_write_unit.cpp test_main.cpp)
target_link_libraries(read_write_unit PRIVATE CppUTest)
add_test(NAME read_write_unit COMMAND read_write_unit)
