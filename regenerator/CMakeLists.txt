find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

function(add_python_test testFile)
    add_test(NAME ${testFile} COMMAND ${Python3_EXECUTABLE} -m unittest ${testFile}
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
endfunction()

add_python_test(tests.cmsis_svd_parser.test_parse_register)
add_python_test(tests.cmsis_svd_parser.test_parse_array)
add_python_test(tests.cmsis_svd_parser.test_parse_member)
add_python_test(tests.cmsis_svd_parser.test_parse_field)
add_python_test(tests.cmsis_svd_parser.test_parse_enum)
add_python_test(tests.cmsis_svd_parser.test_join_register_register)
add_python_test(tests.cmsis_svd_parser.test_join_struct_register)