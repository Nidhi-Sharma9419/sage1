r"""
Tutorial: Using free modules and vector spaces

AUTHOR: Jason Bandlow

In this tutorial, we show how to construct and manipulate free modules
and vector spaces and their elements.

Sage currently provides two implementations of free modules:
:class:`FreeModule` and :class:`CombinatorialFreeModule`. The
distinction between the two is mostly an accident in history. The
latter allows for the basis to be indexed by any kind of objects,
instead of just `0,1,2,...`. They also differ by feature set and
efficiency. Eventually, both implementations will be merged under the
name :class:`FreeModule`. In the mean time, we focus here on
:class:`CombinatorialFreeModule`. We recommend to start by browsing
its documentation::

    sage: CombinatorialFreeModule?                # not tested

Construction, arithmetic, and basic usage
=========================================

We begin with a minimal example::

    sage: G = Zmod(5)
    sage: F = CombinatorialFreeModule(ZZ, G)
    sage: F.an_element()
    2*B[0] + 2*B[1] + 3*B[2]


`F` is the free module over the ring integers `\ZZ` whose canonical
basis is indexed by the set of integers modulo 5.

We can use any set, finite or not, to index the basis, as long as its
elements are immutable. Here are some `\ZZ`-free modules; what is the
indexing set for the basis in each example below?

::

    sage: F = CombinatorialFreeModule(ZZ, CC); F.an_element()
    B[1.00000000000000*I]
    sage: F = CombinatorialFreeModule(ZZ, Partitions(NonNegativeIntegers(),             # needs sage.combinat
    ....:                                            max_part=3)); F.an_element()
    2*B[[]] + 2*B[[1]] + 3*B[[2]]
    sage: F = CombinatorialFreeModule(ZZ, ['spam', 'eggs', '42']); F.an_element()
    3*B['42'] + 2*B['eggs'] + 2*B['spam']

Note that we use '42' (and not the number 42) in order to ensure that
all objects are comparable in a deterministic way, which allows the
elements to be printed in a predictable manner. It is not mandatory
that indices have such a stable ordering, but if they do not, then the
elements may be displayed in some random order.

Lists are not hashable, and thus cannot be used to index the basis;
instead one can use tuples::

    sage: F = CombinatorialFreeModule(ZZ, ([1],[2],[3])); F.an_element()
    Traceback (most recent call last):
    ...
    TypeError: unhashable type: 'list'

    sage: F = CombinatorialFreeModule(ZZ, ((1,), (2,), (3,))); F.an_element()
    2*B[(1,)] + 2*B[(2,)] + 3*B[(3,)]

The name of the basis can be customized::

    sage: F = CombinatorialFreeModule(ZZ, Zmod(5), prefix='a'); F.an_element()
    2*a[0] + 2*a[1] + 3*a[2]

Let us do some arithmetic with elements of `A`::

    sage: f = F.an_element(); f
    2*a[0] + 2*a[1] + 3*a[2]

    sage: 2*f
    4*a[0] + 4*a[1] + 6*a[2]

    sage: 2*f - f
    2*a[0] + 2*a[1] + 3*a[2]

Inputing elements as they are output does not work by default::

    sage: a[0] + 3*a[1]
    Traceback (most recent call last):
    ...
    NameError: name 'a' is not defined

To enable this, we must first get the *canonical basis* for the
module::

    sage: a = F.basis(); a
    Lazy family (Term map from Ring of integers modulo 5
                 to Free module generated by Ring of integers modulo 5
                 over Integer Ring(i))_{i in Ring of integers modulo 5}

This gadget models the :class:`family <Family>` `(B_i)_{i \in \ZZ_5}`.
In particular, one can run through its elements::

    sage: list(a)
    [a[0], a[1], a[2], a[3], a[4]]

recover its indexing set::

    sage: a.keys()
    Ring of integers modulo 5

or construct an element from the corresponding index::

    sage: a[2]
    a[2]

So now we can do::

    sage: a[0] + 3*a[1]
    a[0] + 3*a[1]

which enables copy-pasting outputs as long as the prefix matches the
name of the basis::

    sage: 2*a[0] + 2*a[1] + 3*a[2] == f
    True

Be careful that the input is currently *not* checked::

    sage: a['is'] + a['this'] + a['a'] + a['bug']
    a['a'] + a['bug'] + a['is'] + a['this']

Manipulating free module elements
=================================

The elements of our module come with many methods for exploring and
manipulating them::

    sage: f.<tab>                                 # not tested

Some definitions:

 * A *monomial* is an element of the basis `B_i`;
 * A *term* is an element of the basis multiplied by a non zero
   *coefficient*: `c B_i`;
 * The support of that term is `i`.
 * The corresponding *item* is the :class:`tuple` ``(i, c)``.
 * The *support* of an element `f` is the collection of indices `i`
   such that `B_i` appears in `f` with non zero coefficient.
 * The *monomials*, *terms*, *items*, and *coefficients* of an element
   `f` are defined accordingly.
 * *Leading*/*trailing* refers to the *greatest*/*least* index.
   Elements are printed starting with the *least* index (for
   lexicographic order by default).

Let us investigate those definitions on our example::

    sage: f
    2*a[0] + 2*a[1] + 3*a[2]
    sage: f.leading_term()
    3*a[2]
    sage: f.leading_monomial()
    a[2]
    sage: f.leading_support()
    2
    sage: f.leading_coefficient()
    3
    sage: f.leading_item()
    (2, 3)

    sage: f.support()
    SupportView({0: 2, 1: 2, 2: 3})
    sage: f.monomials()
    [a[0], a[1], a[2]]
    sage: f.coefficients()
    [2, 2, 3]

We can iterate through the items of an element::

    sage: for index, coeff in f:
    ....:     print("The coefficient of a_{%s} is %s"%(index, coeff))
    The coefficient of a_{0} is 2
    The coefficient of a_{1} is 2
    The coefficient of a_{2} is 3

This element can be thought of as a dictionary index-->coefficient::

    sage: f[0], f[1], f[2]
    (2, 2, 3)

This dictionary can be accessed explicitly with the monomial_coefficients method::

    sage: f.monomial_coefficients()
    {0: 2, 1: 2, 2: 3}

The ``map`` methods are useful to transform elements::

    sage: f
    2*a[0] + 2*a[1] + 3*a[2]
    sage: f.map_support(lambda i: i+1)
    2*a[1] + 2*a[2] + 3*a[3]
    sage: f.map_coefficients(lambda c: c-3)
    -a[0] - a[1]
    sage: f.map_item(lambda i,c: (i+1,c-3))
    -a[1] - a[2]

Note: this last function should be called ``map_items``!

Manipulating free modules
=========================

The free module itself (`A` in our example) has several utility
methods for constructing elements::

    sage: F.zero()
    0
    sage: F.term(1)
    a[1]
    sage: F.sum_of_monomials(i for i in Zmod(5) if i > 2)
    a[3] + a[4]
    sage: F.sum_of_terms((i+1,i) for i in Zmod(5) if i > 2)
    4*a[0] + 3*a[4]
    sage: F.sum(ZZ(i)*a[i+1] for i in Zmod(5) if i > 2)  # Note coeff is not (currently) implicitly coerced
    4*a[0] + 3*a[4]

Is safer to use ``F.sum()`` than to use ``sum()``: in case the input
is an empty iterable, it makes sure the zero of `A` is returned, and
not a plain `0`::

    sage: F.sum([]), parent(F.sum([]))
    (0, Free module generated by Ring of integers modulo 5 over Integer Ring)
    sage: sum([]),   parent(sum([]))
    (0, <... 'int'>)


.. TODO::

    Introduce echelon forms, submodules, quotients in the finite dimensional case

Review
======

In this tutorial we have seen how to construct vector spaces and free
modules with a basis indexed by any kind of objects.

To learn how to endow such free modules with additional structure,
define morphisms, or implement modules with several distinguished
basis, see the :ref:`Implementing Algebraic Structures
<tutorial-implementing-algebraic-structures>`_
thematic tutorial.
"""
