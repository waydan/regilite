#include "CppUTest/TestHarness.h"
#include "test_register.hpp"

TestReg test_register;

TEST_GROUP(MatchFieldValues)
{
    void setup() { register_view(test_register) = 0u; };
};

TEST(MatchFieldValues, RegisterStateMatchesFieldArgument)
{
    CHECK(test_register.match(F0{0}));
}

TEST(MatchFieldValues, RegisterStateDoesNotMatchFieldArgument)
{
    CHECK(not test_register.match(F0{1}));
}

TEST(MatchFieldValues, RegisterStateMatchesAllFields)
{
    test_register.write(F1{1}, F0{1});
    CHECK(test_register.match_all(F1{1}, F0{1}));
}

TEST(MatchFieldValues, RegisterStateDoesNotMatchAllFields)
{
    test_register.write(F1{3}, F0{1});
    CHECK(not test_register.match_all(F1{1}, F0{1}));
}

TEST(MatchFieldValues, RegisterStateMatchesAnyField)
{
    test_register.write(F1{3}, F0{1});
    CHECK(test_register.match_any(F1{1}, F0{1}));
}

TEST(MatchFieldValues, RegisterStateMatchesNoFields)
{
    test_register.write(F1{3}, F0{1});
    CHECK(not test_register.match_any(F1{1}, F1{2}));
}
