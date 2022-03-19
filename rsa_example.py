from discrete import rsa

# Order of this ~120 bits, so we should be able to fit about 15 ASCII chars.
p, q = 1905621573238457983, 3206147249787367099
n = p * q
e = 11

_, d, _ = rsa.egcd(e, rsa._order(p, q))
pkey = rsa.PrivateKey(n, d)
pubkey = rsa.PublicKey(n, e)

msg = "Riemann Rocks"
assert len(msg) <= 15
plaintext = int.from_bytes(msg.encode("utf-8"), "big")
print(f"Message: {msg}\nPlaintext: {plaintext}")
enc = rsa.encrypt(plaintext, pubkey)
print(f"Encrypted: {enc}")
dec = rsa.decrypt(enc, pkey)
print(f"Decrypted: {dec}")
print("Decrypted (UTF-8): " + dec.to_bytes(len(msg), "big").decode("utf-8"))
