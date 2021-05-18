#include "CppUTest/TestHarness.h"
#include "register.hpp"
#include "test_register.hpp"

#include <cstdint>
#include <type_traits>

TestReg test_register;


TEST_GROUP(WriteToRegister)
{
    void setup() { register_view(test_register) = 0u; };
};

TEST(WriteToRegister, SetOneBit)
{
    test_register.write(F0{1});
    LONGS_EQUAL(0x1, register_view(test_register));
}

TEST(WriteToRegister, SetTwoAdjacentFields)
{
    test_register.write(F0{1}, F1{2});
    LONGS_EQUAL(0b101, register_view(test_register));
}

TEST(WriteToRegister, WritesOnlyModifyBitsInField)
{
    register_view(test_register) = 0b100u;
    test_register.write(F0{1});
    LONGS_EQUAL(0b101, register_view(test_register));
}

TEST(WriteToRegister, FieldUnsetBitsAreCleared)
{
    register_view(test_register) = 0b1111;
    test_register.write(F1{1}, F0{0});
    LONGS_EQUAL(0b1010, register_view(test_register));
}