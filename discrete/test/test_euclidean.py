import math
from ..euclidean import FIRST_PRIMES, division, extended


def test_division_simple():
    assert division(0, 0) == None

    p, q, r = 547, 709, 37  # some random primes
    cases = [
        (-5, 0, 5),
        (0, -5, 5),
        (1, 1, 1),
        (1, 2, 1),
        (-1, 2, 1),
        (1, -2, 1),
        (-1, -2, 1),
        (10, 2, 2),
        (2, 10, 2),
        (15, 10, 5),
        (10, 15, 5),
        (p * q, q * r, q),
        (p, q, 1),
        (p * r, q, 1),
    ]

    for a, b, d_expected in cases:
        d_result, steps = division(a, b)
        assert d_result == d_expected


def test_division_steps():
    a, b = 2 * 3 * 3 * 5, 5 * 7
    assert math.gcd(a, b) == 5  # just to guard against me being stupid

    d, steps = division(a, b)
    assert d == 5

    assert steps == [(a, b, 2, 20), (b, 20, 1, 15), (20, 15, 1, 5)]


def test_extended():
    assert extended(0, 0) == None

    # For these, the GCD is 1
    prime_cases = [(1, FIRST_PRIMES[i], FIRST_PRIMES[i + 1]) for i in range(0, 10)]

    cases = [
        (5, 90, 35),
        (5, -90, 35),
        (3, 3, 6),
        (10, 10, 30),
        (10, 10, -30),
        (3, -375, 633),
        (1, 762, -541),
        (1, 97384, 7941),
        (2, -98524, 3426),
        (6, 53322, 55152),
        (2, 51717466, -10284014),
    ] + prime_cases

    for d_expected, a, b in cases:
        d_result, u, v = extended(a, b)
        assert d_expected == d_result
        assert a * u + b * v == d_expected


def test_extended_edges():
    assert extended(0, 0) is None

    d, u, v = extended(5, 0)
    assert u == 1 and v == 0 and d == 5

    d, u, v = extended(0, 5)
    assert u == 0 and v == 1 and d == 5
