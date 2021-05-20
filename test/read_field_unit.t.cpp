#include "CppUTest/TestHarness.h"
#include "register.hpp"
#include "test_register.hpp"

TestReg test_register;

TEST_GROUP(ReadFieldFromRegister){
    void setup(){register_view(test_register) = 0u;
}
}
;

TEST(ReadFieldFromRegister, ReadSingleClearedBit)
{
    // CHECK_EQUAL(F0{0u}, test_register.read<F0>());
    CHECK_EQUAL(F0{0u}, test_register.read<F0>());
}

TEST(ReadFieldFromRegister, ReadSingleSetBit)
{
    test_register.write(F0{1});
    CHECK_EQUAL(F0{1u}, test_register.read<F0>());
}


TEST(ReadFieldFromRegister, ReadsFieldWithNonZeroLsb)
{
    test_register.write(F1{2});
    CHECK_EQUAL(F1{2}, test_register.read<F1>());
}

TEST(ReadFieldFromRegister, ReadsOnlyReturnBitsForOneField)
{
    test_register.write(F1{2}, F0{1});
    CHECK_EQUAL(F1{2}, test_register.read<F1>());
}