import math
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
