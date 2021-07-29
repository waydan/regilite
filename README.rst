.. default-role:: code

.. role:: c-code(code)
    :language: C

.. role:: cpp-code(code)
    :language: Cpp

.. include:: <isonum.txt>

Introduction
------------

**Regilite** provides concise, robust abstractions for interacting with memory-mapped hardware registers. It's goals are to:

- Lighten user burden and improve readability with a simple, expressive interface
- Flag most programming errors at compile-time
- Generate assebly at-least as efficient as hand-written C code

Example
--------
The most common operation for a memory-mapped hardware register is probably read-modify-write. This is expressed idiomatically in C as :c-code:`register = (register & ~mask) | value;` (assuming `mask` and `value` are both appropriately shifted and `register` has been declared :c-code:`volatile`).

Read-modify-write, however, is actually an implementation detail. Usually a user just wants to update one or more fields in a register. In Regilite, this is expressed as :cpp-code:`register.write(field)`. Here, `field` is an object of some `Field`-like type defined in the library, and it carries metadata to perform all bit-shifting and masking behind the scenes.


.. code-block:: Cpp

    UART0->C1.write(PE{ParityEnable::Disable}, M{Mode::Bits8});

What does the above line of code do? It clearly disables parity *and* configures the UART for 8-bit transmissions. The register names are taken from the `Kinetis KV1x`_ peripheral definition and they set the UART to `8-N-1`_ mode.

.. _`Kinetis KV1x`: https://www.nxp.com/files-static/32bit/doc/ref_manual/KV11P64M75RM.pdf

.. _`8-N-1`: https://en.wikipedia.org/wiki/8-N-1

+-+-----------+-----------+---+---+
|R|           |           |ERR|   |
+-+   GIBBLE  |    Res.   +---+EN |
|W|           |           |w1c|   |
+-+---+---+---+---+---+---+---+---+
| | 7 | 6 | 5 | 4 | 3 | 3 | 1 | 0 |
+-+---+---+---+---+---+---+---+---+

.. code-block:: Cpp

    FROB.write(EN::Enable);

    Or perhaps we want to update GIBBLE at the same time. Then we'd just write

.. code-block:: Cpp

    FROB.write(EN::Enable, GIBBLE{2});


Notes
-----

Rationale
---------
Traditional C-style access and manipulation of hardware registers is manual, tedeous, and error prone. There are well documented patterns to reduce errors and make code more obvious, e.g. `Barr Group`_.

.. _`Barr Group`: https://barrgroup.com/embedded-systems/books/programming-embedded-systems/peripherals-device-drivers

Often silicon vendors will provide a headder file which groups registers into a struct and ``#define``\ s pointers and constants to ease access.

.. code-block:: C

    typedef struct {
        uint8_t volatile CONFIG;
        uint8_t volatile MISSILE_COMMAND;
    } FROB;

    #define FROB0 ((FROB* const)(0x1000))
    #define GIBBLE_SHIFT    (5)
    #define GIBBLE_MASK     ((uint8_t)(7u << GIBBLE_SHIFT))
    #define GIBBLE(x)       ((uint8_t)((x) << GIBBLE_SHIFT))


A function in the hardware abstraction layer may then contain code which looks like:

.. code-block:: C

        FROB0->CONFIG = (FROB0->CONFIG & ~GIBBLE_MASK) | GIBBLE(2u);

Prior Art
---------
This library is not breaking new ground; others have also used the expressive power of C++ to simplify register access and reduce errors.

- Kvasir_
- regbits_

.. _Kvasir: https://github.com/kvasir-io/Kvasir
.. _regbits: https://github.com/thanks4opensource/regbits

These libraries are interesting and readers should take a look to consider which option is the best fit for their application or usecase.

- Write a single field to a register
- Write multiple fields to a register
- Read a single field from a register
- Read multiple fields from a register

Reduce Errors
+++++++++++++

- Only Predefined ``Field``\ s may be written to a ``Register``
- Overlapping ``Field``\ s can be detected at compile-time

Interface
=========

Copyright |copy| 2021 by Daniel Way