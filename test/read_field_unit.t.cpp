#include "CppUTest/TestHarness.h"
#include "register.hpp"
#include "test_register.hpp"

TestReg test_register;

TEST_GROUP(ReadFieldFromRegister)
{
    void setup() { register_view(test_register) = 0u; };
};

TEST(ReadFieldFromRegister, ReadSingleClearedBit)
{
    CHECK_EQUAL(F0{0u}, test_register.read<F0>());
}

TEST(ReadFieldFromRegister, ReadSingleSetBit)
{
    test_register.write(F0{1});
    const F0 output_field = test_register.extract();
    CHECK_EQUAL(F0{1u}, output_field);
}


TEST(ReadFieldFromRegister, ReadsFieldWithNonZeroLsb)
{
    test_register.write(F1{2});
    const F1 output_field = test_register.extract();
    CHECK_EQUAL(F1{2}, output_field);
}

TEST(ReadFieldFromRegister, ReadsOnlyReturnBitsForOneField)
{
    test_register.write(F1{2}, F0{1});
    const F1 output_field = test_register.extract();
    CHECK_EQUAL(F1{2}, output_field);
}