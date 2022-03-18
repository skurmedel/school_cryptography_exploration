from math import floor, sqrt


def shanks_n(p):
    """Gives the n used for the algorithm for a given p. The actual storage used is 2n.
    
    >>> shanks_n(17)
    5
    """
    return floor(sqrt(p-1)) + 1

def shanks(g, h, p):
    """
    "Solves" the Discrete Logarithm Problem g^x = h mod p using Shank's Babystep-Gianstep algorithm.

    p is in general a prime, or a prime power, which guarantees that we have a group F_p* and generators 
    (primitive roots), if g is a generator, this is guaranteed a solution. In other cases, this might 
    fail.

    >>> shanks(11, 21, 71)
    37
    >>> shanks(2, 3, 5)
    3
    >>> pow(156, shanks(156, 116, 593), 593)
    116

    The solution might not be the "best", for example:
    >>> shanks(156, 116, 593)
    503

    >>> shanks(2, 3, 6) is None
    True

    But 59 is also a solution.
    """
    n = shanks_n(p)
    list1 = {pow(g, k, p): k for k in range(0, n+1)}
    list2 = {h * pow(g, -n*k, p) % p: k for k in range(0, n+1)}
    print(list1, list2)
    
    x = None
    for gpow, k1 in list1.items():
        if gpow in list2:
            k2 = list2[gpow]
            tmp = (k1 + k2 * n) % (p-1)
            if x is None or tmp < x:
                x = tmp
            break
    
    return x        

if __name__ == "__main__":
    import doctest  
    doctest.testmod()

    print(shanks(156, 116, 593))
    print(pow(156, shanks(156, 116, 593), 593))
    print(shanks(650, 2213, 3571))