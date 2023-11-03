from sage.libs.gmp.types cimport __mpz_struct, mpz_t, mpz_ptr
from sage.libs.gmp.mpz cimport mpz_set

from sage.structure.element cimport EuclideanDomainElement, RingElement
from sage.categories.morphism cimport Morphism

cdef class Integer(EuclideanDomainElement):
    # This is really of type mpz_t, but we don't use the mpz_t typedef
    # to work around Cython bug
    # https://github.com/cython/cython/issues/1984
    cdef __mpz_struct value[1]

    cdef void set_from_mpz(self, mpz_t value) noexcept
    cdef hash_c(self) noexcept

    cpdef __pari__(self) noexcept

    cpdef _shift_helper(Integer self, y, int sign) noexcept
    cpdef _add_(self, other) noexcept
    cpdef _mul_(self, other) noexcept
    cpdef _pow_(self, other) noexcept
    cdef _and(Integer self, Integer other) noexcept
    cdef _or(Integer self, Integer other) noexcept
    cdef _xor(Integer self, Integer other) noexcept

    cpdef size_t _exact_log_log2_iter(self,Integer m) noexcept
    cpdef size_t _exact_log_mpfi_log(self,m) noexcept
    cpdef RingElement _valuation(Integer self, Integer p) noexcept
    cdef object _val_unit(Integer self, Integer p) noexcept
    cdef Integer _divide_knowing_divisible_by(Integer self, Integer right) noexcept
    cdef bint _is_power_of(Integer self, Integer n) noexcept

    cdef bint _pseudoprime_is_prime(self, proof) except -1

cdef int mpz_set_str_python(mpz_ptr z, char* s, int base) except -1

cdef Integer smallInteger(long value) noexcept

cdef bint _small_primes_table[500]

cdef inline Integer _Integer_from_mpz(mpz_t e) noexcept:
    cdef Integer z = Integer.__new__(Integer)
    mpz_set(z.value, e)
    return z

cdef class int_to_Z(Morphism):
    pass
