#include "CppUTest/TestHarness.h"
#include "bitmask.hpp"
#include "field.hpp"
#include "test_registers.hpp"

template <typename ValType, regilite::mask_t mask, typename Access,
          typename Shadow>
SimpleString StringFrom(regilite::Field<ValType, mask, Access, Shadow> f)
{
    return SimpleString{"Field value: "}
           + StringFrom(static_cast<regilite::mask_t>(f.value()));
}

TestReg test_register;

TEST_GROUP(ReadFieldFromRegister)
{
    void setup() override { test_register.raw_write(0u); };
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