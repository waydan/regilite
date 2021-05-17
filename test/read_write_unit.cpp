#include "CppUTest/TestHarness.h"
#include "register.hpp"

#include <cstdint>
#include <type_traits>

regilite::Register test_register;

static_assert(std::is_standard_layout<decltype(test_register)>::value,
              "Register<> type must always be standard layout.");

std::uint32_t& register_view{*reinterpret_cast<std::uint32_t*>(&test_register)};

TEST_GROUP(WriteToRegister)
{
    void setup() { register_view = 0u; };
};

TEST(WriteToRegister, SetOneBit)
{
    test_register.write(regilite::Field{1});
    LONGS_EQUAL(0x1, register_view);
}

TEST(WriteToRegister, ClearOneBit)
{
    register_view = 1u;
    test_register.write(regilite::Field{0});
    LONGS_EQUAL(0x0, register_view);
}

TEST(WriteToRegister, SetTwoAdjacentFields)
{
    register_view = 1u;
    test_register.write(regilite::Field{0});
    LONGS_EQUAL(0x0, register_view);
}