#include <cstdint>

#include "CppUTest/TestHarness.h"
#include "field.hpp"
#include "field_access.hpp"
#include "test_registers.hpp"


using Fx =
    regilite::Field<std::uint8_t, regilite::Mask<0>{}, regilite::RW, void>;
using Flag = regilite::Field<bool, regilite::Mask<7>{}, regilite::W1C, void>;

regilite::BasicRegister<std::uint8_t, Fx, Flag> special_reg;

TEST_GROUP(WriteSpecialFields)
{
    void setup() { register_view(special_reg) = 0u; };
};

TEST(WriteSpecialFields, ImplicitlyWrite1ToW1C)
{
    register_view(special_reg) = 0x80;
    special_reg.write(Fx{1});
    REGISTER_EQUALS(0x01, special_reg);
}

TEST(WriteSpecialFields, ExplicitWritePreventsImplicitWrite)
{
    special_reg.write(Fx{1}, Flag{true});
    REGISTER_EQUALS(0x81, special_reg);
}