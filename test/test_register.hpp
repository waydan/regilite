#ifndef TEST_REGISTER_HPP
#define TEST_REGISTER_HPP

#include "CppUTest/TestHarness.h"
#include "basic_register.hpp"
#include "field.hpp"
#include "traits.hpp"

template <typename ValType, regilite::mask_t mask>
SimpleString StringFrom(regilite::Field<ValType, mask> f)
{
    return SimpleString{"Field value: "}
           + StringFrom(regilite::traits::as_uint(f.value()));
}

template <typename Impl, typename... Fields>
auto register_view(regilite::RegisterProxy<Impl, Fields...>& reg) ->
    typename Impl::storage_type&
{
    return *reinterpret_cast<typename Impl::storage_type*>(&reg);
}

template <typename Impl, typename... Fields>
auto REGISTER_EQUALS(typename Impl::storage_type value,
                     regilite::RegisterProxy<Impl, Fields...>& reg) -> void
{
    LONGS_EQUAL(value, register_view(reg));
}


// TestReg layout
// +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
// |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
// +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
//  31 30 29 28 27 26 25 24 23 22 21 20 19 18 17 16
// +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
// |  |  |  |  |     F3    |  |   F2   |  |  F1 |F0|
// +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
//  15 14 13 12 11 10  9  8  7  6  5  4  3  2  1  0

enum class F3Val : std::uint32_t
{
    A = 1,
    B = 2,
    C = 4,
    D = 8
};

using F0 = regilite::Field<std::uint16_t, regilite::Mask<0>{}>;
using F1 = regilite::Field<std::uint16_t, regilite::Mask<2, 1>{}>;
using F2 = regilite::Field<std::uint16_t, regilite::Mask<6, 4>{}>;
using F3 = regilite::Field<F3Val, regilite::Mask<11, 8>{}>;


using TestReg = regilite::BasicRegister<std::uint32_t, F0, F1, F2, F3>;

static_assert(std::is_standard_layout<TestReg>{},
              "BasicRegister<> type must be standard layout.");

static_assert(
    std::is_standard_layout<TestReg::Snapshot>{},
    "Unnameable type RegisterProxy<>::Snapshot must be standard layout.");

#endif // TEST_REGISTER_HPP