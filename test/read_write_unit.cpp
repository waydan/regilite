#include "CppUTest/TestHarness.h"

#include "register.hpp"
#include <cstdint>

std::uint32_t test_register;

TEST_GROUP(WriteFields)
{
    void setup() { test_register = 0u; };
};

TEST(WriteFields, Pass)
{
    class DummyRegister : registex::Register {};
};
