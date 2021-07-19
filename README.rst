Introduction
------------

**Regilite** provides concise, robust abstractions for interacting with memory-mapped hardware registers. It's goals are:

- To reduce programming errors by restricting register interaction to preset fields; automating bit shifting and masking; and avoiding unintentional modification of special fields like "write-1-to-clear"
- Affecting volatile access without obstructing the user
- Generate assebly at-least as efficient as hand-written C code.

Traditional C-style access and manipulation of hardware registers is manual, tedeous, and error prone.

.. code-block:: C

    typedef struct {
        uint8_t volatile CONFIG;
        /* etc. */
    } UART;

    #define UART0 ((UART* const)(0x1000))

    void configurize(void)
    {
        UART0->CONFIG = (UART0->CONFIG & ~(7u << 5)) | (2u << 5);
    }

The magic numbers are often abstracted with macros to make code more readable.

.. code-block:: C

    #define PARITY_SHIFT    (5)
    #define PARITY_MASK     ((uint8_t)(7u << PARITY_SHIFT))
    #define PARITY(x)       ((uint8_t)((x) << PARITY_SHIFT))

    void configurize(void)
    {
        UART0->CONFIG = (UART0->CONFIG & ~PARITY_MASK) | PARITY(2u);
    }

Examples
--------

A simple 8-bit register

+-+-----------+---+-------+---+---+
|R|           |   |  ERRF |   |   |
+-+   PARITY  |Res+-------+Res| EN|
|W|           |   |       |   |   |
+-+---+---+---+---+---+---+---+---+
| | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
+-+---+---+---+---+---+---+---+---+


Notes
-----

Rationale
---------

References
----------
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
