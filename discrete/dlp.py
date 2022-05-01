from typing import Union, Tuple

from pyrsistent import rex
from .euclidean import extended as egcd

# TODO move Shanks in to this.


def pollard_rho(g: int, h: int, p: int, max_iter: int = None) -> Union[None, int]:
    """Pollard's rho collision algorithm for solving the DLP:

        g^x = h  (mod p)

    p should be a prime. To guarantee an answer, g should be a generator of F_p (primitive root).
    """
    x, y = 1, 1
    max_iter = p

    p_by_3 = p // 3
    p_min_1 = p - 1

    # x = g^x h^b
    a, b = 0, 0
    # y = g^c h^d
    c, d = 0, 0

    def rexp(v):
        return v % p_min_1

    # Each step we "advance" x once, and y twice. This is done with the scrambling function
    # f, which is chosen such that after a number of steps, we enter a cycle.
    # The map can be expressed in terms of the exponents (and so mod p-1).
    def f_g(z, a):
        v = 0
        if 0 <= z < p_by_3:
            v = a + 1
        elif p_by_3 <= z < 2 * p_by_3:
            v = 2 * a
        else:
            v = a
        return rexp(v)

    def f_h(z, b):
        v = 0
        if 0 <= z < p_by_3:
            v = b
        elif p_by_3 <= z < 2 * p_by_3:
            v = 2 * b
        else:
            v = b + 1
        return rexp(v)

    def step():
        nonlocal x, y, a, b, c, d
        a, b = f_g(x, a), f_h(x, b)
        x = (pow(g, a, p) * pow(h, b, p)) % p

        for _ in range(0, 2):
            c, d = f_g(y, c), f_h(y, d)
            y = (pow(g, c, p) * pow(h, d, p)) % p

    step()
    i = 1
    while x != y and 1 <= i < max_iter:
        step()
        i += 1

    if x != y:
        return None

    # Now we know g^(a-c) = h(d-b)  (mod p)
    A = rexp(a - c)
    B = rexp(d - b)
    d, u, v = egcd(B, p_min_1)

    s = rexp((u * A) // d)
    # We now have s * A = d * log_g(h)   mod (p - 1)
    # We also now know d divides the left hand side, and so log_g(h) should have d many solutions.
    # The solutions to log_g(h) (if g generator) is now somewhere among s + k * (p - 1) / d
    possible_dlogs = [rexp(s + k * (p_min_1 // d)) for k in range(0, d)]
    solutions = sorted(dlog for dlog in possible_dlogs if pow(g, dlog, p) == h)
    # This usually happens when g does not generate F_p.
    if not solutions:
        return None
    return solutions[0]
