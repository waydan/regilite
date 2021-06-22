#include <cstdint>
#include <type_traits>

#include "CppUTest/TestHarness.h"
#include "register.hpp"
#include "test_register.hpp"


TEST_GROUP(CompileTimeChecks){};

using NonMemberF = regilite::Field<std::uint32_t, 0x1, std::uint32_t>;

template <typename Register, typename Field, typename = void>
struct WriteNonMemberField {};

template <typename Register, typename Field>
struct WriteNonMemberField<Register, Field,
                           decltype(std::declval<Register>().write(
                               std::declval<Field>()))> {
    WriteNonMemberField()
    {
        FAIL("Writing a non-member field must fail compilation");
    }
};


TEST(CompileTimeChecks, CannotWriteNonmemberField)
{
    WriteNonMemberField<TestReg, NonMemberF>{};
}