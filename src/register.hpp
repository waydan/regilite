#ifndef REGILITE_REGISTER_HPP
#define REGILITE_REGISTER_HPP

#include <cstdint>
#include <type_traits>

#include "field.hpp"
#include "utility.hpp"

namespace regilite {

template <typename UInt>
class Register
{
    static_assert(std::is_unsigned<UInt>::value
                      and not std::is_same<UInt, bool>::value,
                  "Register<> type requires an unsigned integral as its "
                  "underlying representation.");

    UInt state_;

  public:
    class Snapshot
    {
        UInt state_;

        struct FieldExtractor {
            UInt state_;

            template <UInt mask, typename ValType>
            constexpr operator Field<UInt, mask, ValType>() const noexcept
            {
                return Field<UInt, mask, ValType>{(state_ & mask)
                                                  >> detail::lsb(mask)};
            }
        };

        template <UInt mask>
        auto match(detail::BitField<UInt, mask> f) const noexcept -> bool
        {
            return f.value == state_ & mask;
        }


      public:
        explicit constexpr Snapshot(UInt s) : state_{s} {};

        constexpr auto raw() const noexcept -> UInt { return state_; }

        template <UInt mask, typename ValType, UInt... masks,
                  typename... ValTypes>
        auto modify(Field<UInt, mask, ValType> f,
                    Field<UInt, masks, ValTypes>... fs) noexcept -> Snapshot&
        {
            const auto fields = detail::fold_fields(f, fs...);
            state_ = detail::insert_bits(state_, fields);
            return *this;
        }


        constexpr auto extract() const noexcept
        {
            return FieldExtractor{state_};
        }


        template <UInt mask, typename ValType>
        auto match(Field<UInt, mask, ValType> f) const noexcept -> bool
        {
            return f == decltype(f){extract()};
        }


        template <UInt mask, typename ValType, UInt... masks,
                  typename... ValTypes>
        auto match_all(Field<UInt, mask, ValType> f,
                       Field<UInt, masks, ValTypes>... fs) const noexcept
            -> bool
        {
            const auto fields = detail::fold_fields(f, fs...);
            return match(fields);
        }

#ifndef __cpp_fold_expressions
        template <UInt mask, typename ValType>
        auto match_any(Field<UInt, mask, ValType> f) const noexcept -> bool
        {
            return match(f);
        }
#endif

        template <UInt mask, typename ValType, UInt... masks,
                  typename... ValTypes>
        auto match_any(Field<UInt, mask, ValType> f,
                       Field<UInt, masks, ValTypes>... fs) const noexcept
            -> bool
        {

#ifndef __cpp_fold_expressions
            return match_any(f) or match_any(fs...);
#else
            return (match(f) or ... or match(fs));
#endif
        };
    };
    auto write(Snapshot s) noexcept -> void
    {
        detail::make_volatile_ref(state_) = s.raw();
    }


    template <UInt mask, typename ValType, UInt... masks, typename... ValTypes>
    auto write(Field<UInt, mask, ValType> f,
               Field<UInt, masks, ValTypes>... fs) noexcept -> void
    {
        write(read().modify(f, fs...));
    }


    auto read() const noexcept -> Snapshot
    {
        return Snapshot{detail::make_volatile_ref(state_)};
    }


    constexpr auto extract() const noexcept { return read().extract(); }


    template <UInt mask, typename ValType>
    auto match(Field<UInt, mask, ValType> f) const noexcept -> bool
    {
        return read().match(f);
    }


    template <UInt mask, typename ValType, UInt... masks, typename... ValTypes>
    auto match_all(Field<UInt, mask, ValType> f,
                   Field<UInt, masks, ValTypes>... fs) const noexcept -> bool
    {
        return read().match_all(f, fs...);
    }

    template <UInt mask, typename ValType, UInt... masks, typename... ValTypes>
    auto match_any(Field<UInt, mask, ValType> f,
                   Field<UInt, masks, ValTypes>... fs) const noexcept -> bool
    {
        return read().match_any(f, fs...);
    }
};

} // namespace regilite


#endif // REGILITE_REGISTER_HPP