#include <cstdint>
#include <type_traits>

#include "CppUTest/TestHarness.h"
#include "field.hpp"
#include "field_traits.hpp"
#include "test_registers.hpp"


// +----+--+--+--+--+--+--+--+
// |Flag|     Reserved    |Fx|
// +----+--+--+--+--+--+--+--+
//   7    6  5  4  3  2  1  0

using Fx =
    regilite::Field<std::uint8_t, regilite::Mask<0>{}, regilite::RW, void>;
using Flag = regilite::Field<bool, regilite::Mask<7>{}, regilite::W1C, void>;

regilite::BasicRegister<std::uint8_t, 0, Fx, Flag> special_reg;

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

TEST(WriteSpecialFields, ResetValueIsPreservedInReservedFields)
{
    register_view(special_reg) = 0b01111110;
    const auto audit = special_reg.write(Fx{1});
    static_assert(regilite::traits::match_unqualified<decltype(audit),
                                                      regilite::Overwrite>,
                  "Whole field should be overwritten");
    REGISTER_EQUALS(0x01, special_reg);
}