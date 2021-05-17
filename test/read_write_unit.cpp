#include "CppUTest/TestHarness.h"
#include "register.hpp"

#include <type_traits>

regilite::Register test_register;

static_assert(std::is_standard_layout<decltype(test_register)>::value,
              "Register<> type must always be standard layout.");

TEST_GROUP(EmptyFirstTest){};

TEST(EmptyFirstTest, RunTest) {}