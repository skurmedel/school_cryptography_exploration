from dataclasses import dataclass
from ..euclidean import extended as egcd


def _order(p: int, q: int):
    """Eulers totient function, special cased for two primes p and q."""
    return (p - 1) * (q - 1)


@dataclass
class PublicKey:
    n: int
    # Encryption exponent.
    e: int


@dataclass
class PrivateKey:
    n: int
    # Decryption exponent. Inverse of the public key exponent e in the (p-1)(q-1) finite field.
    d: int


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

    