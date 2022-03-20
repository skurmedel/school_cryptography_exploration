from math import log2, ceil
from typing import Tuple, Union
from dataclasses import dataclass
from ..euclidean import extended as egcd
from ..primality import random_prime


class BadEncryptionExponent(BaseException):
    def __init__(self, msg):
        super().__init__()
        self._msg = msg

    def __repr__(self) -> str:
        return f"BadEncryptionExponent: {self._msg}"


def _order(p: int, q: int):
    """Eulers totient function, special cased for two primes p and q."""
    return (p - 1) * (q - 1)


@dataclass
class PublicKey:
    n: int
    # Encryption exponent.
    e: int

    def __str__(self) -> str:
        return f"<PublicKey: n={self.n:x}, e={self.e}>"


@dataclass
class PrivateKey:
    n: int
    # Decryption exponent. Inverse of the public key exponent e in the (p-1)(q-1) finite field.
    d: int

    def __str__(self) -> str:
        return f"<PrivateKey: n={self.n:x}, d={self.d}>"


def encrypt(plaintext: int, public_key: PublicKey) -> int:
    """
    Encrypt plaintext using the RSA algorithm with the given public key. Note that values of the
    plaintext larger than n will wrap around, so to get a bijective mapping the inputs should be
    less than n.

    RSA without padding is vulnerable to chosen ciphertext attacks. This function currently does
    not do padding.

    Returns the ciphertext.
    """
    return pow(plaintext, public_key.e, public_key.n)


def decrypt(ciphertext: int, private_key: PrivateKey) -> int:
    """
    Decrypts some ciphertext using the private key. If this cannot be done (usually because of a bad key),
    an exception will be raised.

    Note that decrypt(encrypt(k, pubkey), privkey) = k, which is a defining property of a public key
    crypto-system.

    Returns the plaintext.
    """
    return pow(ciphertext, private_key.d, private_key.n)


def generate_keys(
    min_bits: int = 1024, e: int = 2**16 + 1
) -> Tuple[PrivateKey, PublicKey]:
    """
    Generates a key pair for the RSA system. Two random primes (p, q) are generated (in a not very secure
    fashion), such that their product n uses more bits than min_bits.

    The encryption exponent e can be specified, but it needs to be "less" or equal to min_bits. An exception
    will be raised if e is not co-prime to (p - 1)(q - 1).
    """
    if min_bits < 1:
        raise ValueError("min_bits must be at least 1.")
    if e < 1:
        raise BadEncryptionExponent(
            "exponent must be 1 or larger (negative congruences are not supported.)"
        )
    e_bits = int(ceil(log2(e)))
    if e_bits > min_bits:
        raise BadEncryptionExponent("e uses more bits than n can be guaranteed.")

    prime_bits = ceil(min_bits / 2)

    range = (2 ** (prime_bits - 1), 2**prime_bits - 1)
    p = random_prime(*range)
    q = random_prime(*range)
    while p == q:
        q = random_prime(*range)

    order = (p - 1) * (q - 1)  # Eulers totient for prime product
    n = p * q
    gcd, d, _ = egcd(e, order)
    if gcd != 1:
        raise BadEncryptionExponent("e is not coprime to the generated order.")
    pkey = PrivateKey(n, d)
    pubkey = PublicKey(n, e)

    return pkey, pubkey
