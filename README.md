# school_cryptography_exploration
Some computational number theory stuff and cryptography implementations for self-learning. Could serve as a reference for others.

## Algorithm roadmap:

### Modular arithmetic and GCD
- [x] Extended Euclidean division (GCD)
- [ ] Chinese Remainder Theorem

### Primes and RSA
- [x] Miller-Rabin test
- [x] Random Prime generator
- [x] RSA
- [x] A RSA trival key generator
- [ ] RSA secure prime generation (2q + 1)

### Discrete log
- [x] Shanks Babystep-Giantstep
- [ ] Pohlig-Hellman
- [x] Pollard's rho for logarithms
- [ ] Diffie-Hellman
- [ ] Elgamal crypto

### Factorisation
- [ ] Quadratic Sieve
- [x] Pollard p - 1
- [ ] Pollard's rho

### Elliptic Curves
*TBD*

## Do Not Ever Use For Security
These methods are implemented by a math undergrad with a subpar knowledge of cryptography. It should be evident that never ever should the code in this repository be used for any production code. It will have flaws, sometimes they are even documented.
