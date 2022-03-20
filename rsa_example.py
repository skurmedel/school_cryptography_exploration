from discrete import rsa

print("Generating keypair of at least 256 bits: ")
pkey, pubkey = rsa.generate_keys(min_bits=256)
print(pkey)
print(pubkey)

msg = "Riemann Rocks 😊"
msg_bytes = msg.encode("utf-8")
plaintext = int.from_bytes(msg_bytes, "big")
print(f"Message: {msg}\nPlaintext: {plaintext}")
enc = rsa.encrypt(plaintext, pubkey)
print(f"Encrypted: {enc}")
dec = rsa.decrypt(enc, pkey)
print(f"Decrypted: {dec}")
print("Decrypted (UTF-8): " + dec.to_bytes(len(msg_bytes), "big").decode("utf-8"))
