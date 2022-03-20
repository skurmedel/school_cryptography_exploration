import math
from pytest import raises
from .. import rsa
from ...euclidean import extended


def test_encrypt_decrypt_basic():
    p, q = 193, 701
    n = p * q
    e = 11

    _, d, _ = extended(e, rsa._order(p, q))
    pkey = rsa.PrivateKey(n, d)
    pubkey = rsa.PublicKey(n, e)

    msg = 431

    ciphertext = rsa.encrypt(msg, pubkey)
    assert ciphertext == pow(msg, e, n)

    plaintext = rsa.decrypt(ciphertext, pkey)
    assert plaintext == msg


def test_generate_keys():
    with raises(rsa.BadEncryptionExponent):
        # e can't really fit into min_bits without wrap-around.
        rsa.generate_keys(min_bits=32, e=2**33)
    with raises(rsa.BadEncryptionExponent):
        # Since n will be an odd number, n - 1 will be even and so 2 will not be coprime.
        rsa.generate_keys(min_bits=32, e=2)
    with raises(rsa.BadEncryptionExponent):
        # 0 has no multiplicative inverse.
        rsa.generate_keys(min_bits=32, e=0)
    with raises(ValueError):
        rsa.generate_keys(min_bits=-1)
    with raises(ValueError):
        rsa.generate_keys(min_bits=0)

    privkey, pubkey = rsa.generate_keys(min_bits=512)

    ciphertext = rsa.encrypt(131, pubkey)
    assert rsa.decrypt(ciphertext, privkey) == 131

    with raises(ValueError):
        # Bits are too few to guarantee two primes
        rsa.generate_keys(min_bits=2, e=1)
