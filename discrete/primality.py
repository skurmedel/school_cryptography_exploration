from random import randint
from math import log, ceil


def miller_rabin(a: int, n: int) -> bool:
    """
    The Miller-Rabin probabilistic test, using potential witness a to test n for compositeness.

    This is a stronger test than Fermat's test, as it does not suffer from Carmichael-numbers.

    Returns True if n is definitely composite. False means n might be prime.
    """
    a, n = abs(a), abs(n)
    if n <= 2:
        raise ValueError("n must be greater than 2.")
    if n % 2 == 0:
        return True

    # n - 1 is even, so we can factor it as 2^k q for some k
    k = 0
    q = n - 1
    while True:
        s, r = divmod(q, 2)
        if r == 0:
            k += 1
            q = s
        else:
            break

    # Now we'll use the fact that IF n is an odd prime:
    #
    #   a^(n-1) = 1  (mod n)
    #
    # And x^2 - 1 = (x - 1)(x + 1) so if
    #
    #   x^2 - 1 = 0  (mod n)
    #
    # then n | (x - 1)(x + 1) divides either (x - 1) or (x + 1) so x is congruent to one of them.
    #
    # Now the terms in  a^q, a^(2 q), a^(2^2 q), ..., a^(2^k q) are square roots of the previous term,
    # and 2^k q = p - 1 so the last one is 1.
    #
    # Thus for any 1 <= a < n, either the a^q = 1 (mod n) or one of the terms are congruent -1 (mod n)
    # (as that would then get squared to 1).

    min1 = (-1) % n
    b = pow(a, q, n)
    if b == 1 or b == min1:
        return False
    i = 0
    while i < k:
        b = pow(b, 2, n)
        if b == min1:
            return False
        i += 1

    return True


def miller_rabin_samples(n: int) -> int:
    """
    Computes the number of random potential witnesses we should use to test n for primality.

    The target is 99.9999% probability of it being prime.

    If n is even and not 2, this returns 0, as it is guaranteed to be a composite.

    This function uses a theorem that states the following:
        if n is an odd composite, ~75% of the numbers between 1 and n-1 are Miller-Rabin witnesses to it being
        composite.

    Together with the prime number theorem we can estimate the number of samples we'll have to take.
    """
    n = abs(n)
    if n == 1:
        return 1

    res = log(log(n), 4) - log(1.0 - 0.9999, 4)
    return 1 if res < 1 else int(ceil(res))


def miller_rabin_test(n: int, k: int):
    """
    Run k rounds of the Miller-Rabin-test, using random integers chosen as potential witnesses.

    Like miller_rabin, returns True when composite. If k rounds show probable primality, returns False.

    n is taken as its absolute. k must be at least 1. If k > n - 1, k is clamped to n - 1.
    """
    n = abs(n)
    if n == 1:
        return True
    if k < 1:
        raise ValueError("k must be equal or greater than 1")
    k = k if k < n else n - 1
    for i in range(0, k):
        if miller_rabin(randint(1, n - 1), n):
            return True
    return False


def random_prime(start: int, end: int) -> int:
    if end < start:
        raise ValueError("end < start")
    i = 0
    while i < end - start + 1:
        candidate = randint(start, end)
        if candidate == 2:
            return candidate
        if not miller_rabin_test(candidate, miller_rabin_samples(candidate)):
            return candidate
        i += 1
    raise ValueError("found no probable primes in range")


# OEIS A000040
FIRST_PRIMES = [
    2,
    3,
    5,
    7,
    11,
    13,
    17,
    19,
    23,
    29,
    31,
    37,
    41,
    43,
    47,
    53,
    59,
    61,
    67,
    71,
    73,
    79,
    83,
    89,
    97,
    101,
    103,
    107,
    109,
    113,
    127,
    131,
    137,
    139,
    149,
    151,
    157,
    163,
    167,
    173,
    179,
    181,
    191,
    193,
    197,
    199,
    211,
    223,
    227,
    229,
    233,
    239,
    241,
    251,
    257,
    263,
    269,
    271,
]

# Carmichael Numbers n, a^(n-1) = 1 for every coprime a.
# These numbers make the "trivial" test for primality using Fermat's little theorem fraught with danger.
# For most numbers a^n = a only when n is prime, but these are exceptions. Crucially, Miller-Rabin doesn't
# have such numbers.
# OEIS A002997
CARMICHAEL_NUMBERS = [
    561,
    1105,
    1729,
    2465,
    2821,
    6601,
    8911,
    10585,
    15841,
    29341,
    41041,
    46657,
    52633,
    62745,
    63973,
    75361,
    101101,
    115921,
    126217,
    162401,
    172081,
    188461,
    252601,
    278545,
]
