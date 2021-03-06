#include <cstdint>
#include <type_traits>

#include "CppUTest/TestHarness.h"
#include "test_registers.hpp"

template <typename>
using sink = void;

TEST_GROUP(CompileTimeChecks){};

// This field is the same as F0 except for `NonMember` shadow type
using NonMemberF = regilite::Field<std::uint16_t, 0x1, struct NonMember>;


template <typename R, typename F, typename = void>
struct WriteNonMemberField {};

template <typename R, typename F>
struct WriteNonMemberField<
    R, F, decltype(std::declval<R>().write(std::declval<F>()))> {
    WriteNonMemberField()
    {
        FAIL("Writing a non-member field must fail compilation");
    }
};


TEST(CompileTimeChecks, CannotWriteNonmemberField)
{
    WriteNonMemberField<TestReg, NonMemberF>{};
}

// Types overlap at bit position 3
using Fa = regilite::Field<std::uint32_t, 0x0F>;
using Fb = regilite::Field<std::uint32_t, 0xF8>;
using RegAB = regilite::DefaultRegister<std::uint32_t, 0, Fa, Fb>;

template <typename R, typename F1, typename F2, typename = void>
struct WriteOverlappingFields {};

template <typename R, typename F1, typename F2>
struct WriteOverlappingFields<R, F1, F2,
                              sink<decltype(std::declval<R>().write(
                                  std::declval<F1>(), std::declval<F2>()))>> {
    WriteOverlappingFields()
    {
        FAIL("Writing overlapping member fields must fail compilation");
    }
};

TEST(CompileTimeChecks, CannotWriteOverlappingFields)
{
    WriteOverlappingFields<RegAB, Fa, Fb>{};
}

template <typename R, typename F1, typename F2, typename = void>
struct MatchAnyOverlappingFields {};

template <typename R, typename F1, typename F2>
struct MatchAnyOverlappingFields<
    R, F1, F2,
    sink<decltype(
        std::declval<R>().match_all(std::declval<F1>(), std::declval<F2>()))>> {
    MatchAnyOverlappingFields()
    {
        FAIL("Matching overlapping member fields must fail compilation");
    }
};

TEST(CompileTimeChecks, CannotMatchOverlappingFields)
{
    MatchAnyOverlappingFields<RegAB, Fa, Fb>{};
}