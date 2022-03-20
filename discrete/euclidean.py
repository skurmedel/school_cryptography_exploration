from collections import namedtuple
from typing import Union, SupportsInt, Tuple, List, NewType

DivModResult = NewType("DivModResult", Tuple[int, int, int, int])


def division(
    a: SupportsInt, b: SupportsInt
) -> Union[Tuple[int, List[DivModResult]], None]:
    """
    The Euclidean division algorithm. This finds the GCD of two integers a and b, but the main
    purpose of this function is to return a list of the steps taken in the algorithm. This is
    useful for validation, and sometimes other algorithms.

    The built-in gcd function (module math) is probably heaps quicker than calling this; it
    likely uses a quicker algorithm (binary or Lehmer's) and is most likely implemented in C.

    Negative numbers are treated as their absolute values.

    In most cases, extended() will suffice or be preferable as it is much faster and you'll want
    the Bezout coefficients anyway.

    Edge cases:
        if |a| + |b| > 0 and min(|a|, |b|) = 0 then this will return max(|a|, |b|)
        if both are zero, this will return None
    """
    x, y = abs(a), abs(b)
    if x == 0 and y == 0:
        return None
    if min(x, y) == 0:
        return (max(x, y), [])
    r = b
    d = None
    steps = []
    while True:
        d = r
        q, r = divmod(x, y)
        if r == 0:
            break
        steps.append((x, y, q, r))
        x, y = y, r

    return d, steps


def extended(a: SupportsInt, b: SupportsInt) -> Union[Tuple[int, int, int], None]:
    """
    The extended Euclidean division algorithm. It gives the integers in Bezout's identity, u, v, d such that:

        a u + b v = d

    where d = gcd(a, b). This is guaranteed a solution unless a and b are both zero.

    Note that it can be shown that a u + b v = 1 if and only if gcd(a, b) == 1.

    The GCD will always be reported positive.

    The extended Euclidean division algorithm is useful for finding inverses in multiplicative finite groups.

    Edge cases:
        if both are zero, this will return None

    Returns gcd, u, v
    """
    if a == 0:
        if b == 0:
            return None
        else:
            return (b, 0, 1)
    elif b == 0:
        return (a, 1, 0)

    # This version calculates u in: a u + b v = d by calculating u and d. We can solve for v when we know
    # these. The sequence for u is found by doing the "school" version on paper and observing that u can be
    # calculated as u = u_prev2 - q u_prev1.

    # u calculated for previous two steps. We assume we start at step 1, and step -1 = a, step 0 = b.
    u_p2, u_p1 = 1, 0
    q, r2, r1 = 1, a, b
    # loop until we get a remainder of 0, this means that he previous step calculated the GCD and also
    # u and v.
    while r1 != 0:
        q, r = divmod(r2, r1)
        u_p1, u_p2 = u_p2 - q * u_p1, u_p1
        r1, r2 = r, r1

    d, u = r2, u_p2
    v = (d - u * a) // b

    # We want a positive GCD, it's just neater.
    if d < 0:
        d, u, v = -d, -u, -v

    return d, u, v
