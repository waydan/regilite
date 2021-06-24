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
    const F0 output_field = test_register.extract_field();
    CHECK_EQUAL(F0{0u}, output_field);
}

TEST(ReadFieldFromRegister, ReadSingleSetBit)
{
    test_register.write(F0{1});
    const F0 output_field = test_register.extract_field();
    CHECK_EQUAL(F0{1u}, output_field);
}


TEST(ReadFieldFromRegister, ReadsFieldWithNonZeroLsb)
{
    test_register.write(F1{2});
    const F1 output_field = test_register.extract_field();
    CHECK_EQUAL(F1{2}, output_field);
}

TEST(ReadFieldFromRegister, ReadsOnlyReturnBitsForOneField)
{
    test_register.write(F1{2}, F0{1});
    const F1 output_field = test_register.extract_field();
    CHECK_EQUAL(F1{2}, output_field);
}

TEST(ReadFieldFromRegister, DirectComparisonPossible)
{
    test_register.write(F1{2}, F0{1});
    CHECK(F1{2} == test_register.extract_field());
    CHECK(test_register.extract_field() == F0{1});
}

TEST(ReadFieldFromRegister, DirectNegativeComparisonPossible)
{
    test_register.write(F1{2}, F0{1});
    CHECK(F1{1} != test_register.extract_field());
    CHECK(test_register.extract_field() != F0{0});
}

TEST(ReadFieldFromRegister, CannotSaveFieldExtractor)
{
    // This expression will not compile. Register<>::Snapshot<>::FieldExtractor
    // is unnameable and can only be move constructed by friend classes

    // auto extractor = test_register.extract_field();
    // (void)extractor;
}