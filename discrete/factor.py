from typing import Union
from .euclidean import extended as egcd


def pollardpmin1(n: int, max_factorial: int = 100, a: int = 2) -> Union[None, int]:
    """Tries to find a factor of n by Pollard's p - 1 method. This can be an effective
    algorithm for composite numbers like pq where p and q are prime, and p - 1 or q - 1
    consists of small primes factors.

    Such numbers can arise in weak RSA key generators.

    Tries to run until max_factorial is hit. Returns a factor if found (note: not all).

    If no factor is found within the bounds given, returns None.

    Note: 
        factorial is calculated modulo n, so it should be viewed more as an iteration 
        count.
    """
    n = abs(int(n))
    max_factorial = int(max_factorial)
    if n == 0:
        return 0
    if n == 1:
        return 1

    if max_factorial < 0:
        raise ValueError("max_factorial must be 0 or greater.")

    # The main idea:
    #   Assume n = p q, p some prime.
    #   Now if p - 1 factors as "small primes", then it should divide a reasonably small k!
    #   From Fermat's little theorem we then know that
    #       a^(k!)      = 1  mod p      (as p has order p - 1)
    #       a^(k!) - 1  = 0  mod p
    #   Which means p divides a^(k!) - 1, and so gcd(a^(k!) - 1, n) = p (or even more).
    #
    # Pollard's optimisation:
    #   We only care about primes a^(k!) < n (it wouldn't be a factor of n otherwise),
    #   so by the above, we can work modulo n.

    a_ = a
    for i in range(1, max_factorial+1):
        a_ = pow(a_, i, n)
        d, _, _ = egcd(a_ - 1, n)
        if d != 1:
            return d
    
    return None

