from ..primality import *
from pytest import raises

def test_miller_rabin_known_primes():
    # We know these are primes, so it should never answer "composite" for these.
    for p in FIRST_PRIMES[1:]:
        for a in range(1, p - 1):
            assert miller_rabin(a, p) == False


def test_miller_rabin_even():
    # Even numbers except 2 are trivially composite.
    for n in (4, 6, 22, 2 * 31):
        for a in range(1, n - 1):
            assert miller_rabin(a, n) == True


def test_miller_rabin_odd_composites():
    for c in ODD_COMPOSITES:
        assert any(miller_rabin(a, c) for a in range(1, c - 1))


def test_miller_rabin_test():
    for p in FIRST_PRIMES[1:]:
        assert not miller_rabin_test(p, 20)

    for c in ODD_COMPOSITES:
        assert miller_rabin_test(c, 50)

def test_random_prime():
    # We'll begin by testing in the range of FIRST_PRIMES.
    start, end = 1, FIRST_PRIMES[-1] + 1

    res = set()
    while len(res) < len(FIRST_PRIMES):
        res.add(random_prime(start, end))
    
    assert sorted(res) == FIRST_PRIMES


def test_random_prime_none_in_range():
    with raises(ValueError):
        random_prime(8, 9)

# Generated with Mathematica.
ODD_COMPOSITES = [
    55045,
    77627,
    54665,
    15963,
    20529,
    97753,
    15931,
    98231,
    50127,
    72021,
    85943,
    58113,
    75095,
    6065,
    5979,
    5809,
    97759,
    29635,
    25179,
    24089,
    80417,
    25395,
    99769,
    77355,
    40893,
    43979,
    19131,
    96623,
    73809,
    20243,
    23901,
    44245,
    64649,
    54399,
    28115,
    84955,
    65977,
    72565,
    58957,
    50771,
    80383,
    65611,
    5553,
    28239,
    84893,
    77087,
    36975,
    30993,
    29555,
    69927,
    77443,
    43837,
    27789,
    56619,
    36703,
    73915,
    70431,
    45835,
    99387,
    16601,
    9331,
    21969,
    35333,
    83283,
    22577,
    17019,
    59155,
    61419,
    22387,
    17297,
    27843,
    19343,
    27593,
    10365,
    28203,
    46213,
    15673,
    67703,
]
