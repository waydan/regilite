#include <type_traits>

#include "CppUTest/TestHarness.h"
#include "test_registers.hpp"


PartableReg test_register;


TEST_GROUP(PartitionRegisterAccess)
{
    void setup() { test_register.raw_write(0u); };
};

TEST(PartitionRegisterAccess, WriteBitInLowestByte)
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

TEST(PartitionRegisterAccess, WriteOnlyUpperByte)
{
    const auto access_audit = test_register.write(F3{F3Val::D});
    static_assert(
        regilite::traits::match_unqualified<decltype(access_audit),
                                            regilite::Write<std::uint8_t>>,
        "Access the smallest aligned span which covers all fields.");
    REGISTER_EQUALS(0x800, test_register);

    LONGS_EQUAL(reinterpret_cast<std::uintptr_t>(&test_register) + 1u,
                access_audit.address());
}
