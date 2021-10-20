find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

add_test(NAME regenerator-unit-tests COMMAND ${Python3_EXECUTABLE} -m unittest discover -p test_*.py
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})