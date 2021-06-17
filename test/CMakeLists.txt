add_executable(test-write-fields write_field_unit.t.cpp test_main.cpp)
target_link_libraries(test-write-fields PRIVATE CppUTest regilite)
add_test(NAME test-write-fields COMMAND test-write-fields)

add_executable(test-read-fields read_field_unit.t.cpp test_main.cpp)
target_link_libraries(test-read-fields PRIVATE CppUTest regilite)
add_test(NAME test-read-fields COMMAND test-read-fields)

add_executable(test-match-fields match_field_unit.t.cpp test_main.cpp)
target_link_libraries(test-match-fields PRIVATE CppUTest regilite)
add_test(NAME test-match-fields COMMAND test-match-fields)

add_executable(test-read-snapshot read_snapshot_unit.t.cpp test_main.cpp)
target_link_libraries(test-read-snapshot PRIVATE CppUTest regilite)
add_test(NAME test-read-snapshot COMMAND test-read-snapshot)

add_executable(test-enum-field enum_field_unit.t.cpp test_main.cpp)
target_link_libraries(test-enum-field PRIVATE CppUTest regilite)
add_test(NAME test-enum-field COMMAND test-enum-field)
