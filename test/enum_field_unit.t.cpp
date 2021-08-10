#include "CppUTest/TestHarness.h"
#include "test_registers.hpp"


TestReg test_register;


TEST_GROUP(EnumTypeField)
{
    void setup() { test_register.raw_write(0u); };
};

TEST(EnumTypeField, CreateEnumField) { F3 enum_field{F3Val::A}; }

TEST(EnumTypeField, NakedValueIsEnum)
{
    CHECK(F3{F3Val::C}.value() == F3Val::C);
}

TEST(EnumTypeField, ExtractingEnum)
{
    test_register.write(F3{F3Val::B});
    CHECK(F3{F3Val::B} == test_register.extract_field());
}

TEST(EnumTypeField, EnumFieldJoinsWithNonEnum)
{
    test_register.write(F3{F3Val::D}, F0{1});
    REGISTER_EQUALS(0x0801, test_register);
}