from ..factor import pollardpmin1
from ..primality import FIRST_PRIMES
from pytest import raises


def test_pollardpmin1_bad_input():
    with raises(ValueError):
        pollardpmin1(13 * 11, -1)


def test_pollardpmin1_easy_cases():
    cases = [
        (0, 0),
        (1, 1),
        (11 * 11, 11),
        (13 * FIRST_PRIMES[-1], 13),
        (17 * FIRST_PRIMES[-2], 17),
        (23 * FIRST_PRIMES[-2], 23),
    ]

    for n, expected in cases:
        actual = pollardpmin1(n)
        assert expected == actual
