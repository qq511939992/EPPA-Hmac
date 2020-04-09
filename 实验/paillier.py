import math
import primes_gmpy2
import random
from pypbc import get_random_prime

def invmod(a, p, maxiter=1000000):
    """The multiplicitive inverse of a in the integers modulo p:
         a * b == 1 mod p
       Returns b.
       (http://code.activestate.com/recipes/576737-inverse-modulo-p/)"""
    if a == 0:
        raise ValueError('0 has no inverse mod %d' % p)
    r = a
    d = 1
    for i in range(min(p, maxiter)):
        d = ((p // r + 1) * d) % p
        r = (d * a) % p
        if r == 1:
            break
    else:
        raise ValueError('%d has no inverse mod %d' % (a, p))
    return d

def modpow(base, exponent, modulus):
    """Modular exponent:
         c = b ^ e mod m
       Returns c.
       (http://www.programmish.com/?p=34)"""
    result = 1
    while exponent > 0:
        if exponent & 1 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result

class PrivateKey(object):

    def __init__(self, p, q, n,a1,a2,a3):
        self.l = (p-1) * (q-1)
        self.m = invmod(self.l, n)
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
    def __repr__(self):
        return '<PrivateKey: %s %s>' % (self.l, self.m)

class PublicKey(object):

    @classmethod
    def from_n(cls, n):
        return cls(n)

    def __init__(self, n,a1,a2,a3):
        self.n = n
        self.n_sq = n * n
        self.g1 = pow(n+1,a1,self.n_sq)
        self.g2 = pow(n+1,a2,self.n_sq)
        self.g3 = pow(n+1,a3,self.n_sq)

    def __repr__(self):
        return '<PublicKey: %s>' % self.n

def generate_keypair(bits,N,d):
    p = primes_gmpy2.generate_prime(bits / 2)
    q = primes_gmpy2.generate_prime(bits / 2)
    n = p * q
    a1 = 1
    #a2 = n//(2*N*d)-N*d
    #a3 = n//(2*N*d)+N*d
    a2 = random.randrange(max(N*d,p,q),n//((N*d)*(N*d+1))-1)
    a3 = random.randrange((a1+a2)*N*d,n//(N*d)-a1-a2)
    if a1+a2+a3>=n:
        print("wrong")
    return PrivateKey(p, q, n,a1,a2,a3), PublicKey(n,a1,a2,a3)

def encrypt(pub, plain1,plain2,plain3):
    while True:
        r = primes_gmpy2.generate_prime(round(math.log(pub.n, 2)))
        if r > 0 and r < pub.n:
            break
    x = pow(r, pub.n, pub.n_sq)
    cipher = (pow(pub.g1, plain1, pub.n_sq)*pow(pub.g2, plain2, pub.n_sq)*pow(pub.g3, plain3, pub.n_sq) * x) % pub.n_sq
    return cipher

def e_add(pub, a, b):
    """Add one encrypted integer to another"""
    return a * b % pub.n_sq

def e_add_const(pub, a, n):
    """Add constant n to an encrypted integer"""
    return a * modpow(pub.g, n, pub.n_sq) % pub.n_sq

def e_mul_const(pub, a, n):
    """Multiplies an ancrypted integer by a constant"""
    return modpow(a, n, pub.n_sq)

def decrypt(priv, pub, cipher):
    x = pow(cipher, priv.l, pub.n_sq) - 1
    plain0 = ((x // pub.n) * priv.m) % pub.n
    return plain0

def huifu(plain0,priv):
    x3 = plain0
    x2 = plain0 % priv.a3
    x1 = x2 % priv.a2
    D3 = (x3-x2)//priv.a3
    D2 = (x2-x1)//priv.a2
    D1 = x1
    return D1,D2,D3