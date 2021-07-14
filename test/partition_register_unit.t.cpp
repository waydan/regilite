#include <type_traits>

#include "CppUTest/TestHarness.h"
#include "test_registers.hpp"


PartableReg test_register;


TEST_GROUP(PartitionRegisterAccess)
{
    void setup() { register_view(test_register) = 0u; };
};

TEST(PartitionRegisterAccess, WriteSingleBit)
{
    auto write_type = test_register.write(F0{1});
    static_assert(
        std::is_same<decltype(write_type), regilite::Write<std::uint8_t>>{},
        "Should only access the lowest byte");
    REGISTER_EQUALS(0x1, test_register);
}

TEST(PartitionRegisterAccess, WriteSpans16Bits)
{
    auto write_type = test_register.write(F3{F3Val::A}, F0{1});
    static_assert(
        std::is_same<decltype(write_type), regilite::Write<std::uint16_t>>{},
        "Access the smallest aligned span which covers all fields.");
    REGISTER_EQUALS(0x101, test_register);
}
