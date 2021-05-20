include_directories(${SRC_PATH})

add_executable(test-write-fields write_field_unit.t.cpp test_main.cpp)
target_link_libraries(test-write-fields PRIVATE CppUTest)
add_test(NAME test-write-fields COMMAND test-write-fields)

add_executable(test-read-fields read_field_unit.t.cpp test_main.cpp)
target_link_libraries(test-read-fields PRIVATE CppUTest)
add_test(NAME test-read-fields COMMAND test-read-fields)
