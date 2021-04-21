#include "CppUTest/TestHarness.h"

#include "register.hpp"

TEST_GROUP(WriteFields){};

TEST(WriteFields, Pass) {
  struct DummyRegister : registex::Register {};
}
