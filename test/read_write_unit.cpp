#include "CppUTest/TestHarness.h"

#include "register.hpp"
#include <cstdint>

std::uint32_t virtual_register;

using Enable = registex::Field<
    registex::make_addr<virtual_register>>;

TEST_GROUP(WriteToRegister)
{
    void setup() { virtual_register = 0u; };
};

TEST(WriteToRegister, WriteSingleBit)
{
    write(Enable{1});
    CHECK_EQUAL(1u, virtual_register);
};
