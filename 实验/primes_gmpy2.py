import random
import sys
from gmpy2 import mpz, powmod, invert, is_prime, random_state, mpz_urandomb
import time

def timing(f, c=0):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        clocktime=time2-time1
        if c==0:
            return ret
        else:
            return ret, clocktime
    return wrap

rand=random_state(random.randrange(sys.maxsize))

def generate_prime(bits):
    """Will generate an integer of b bits that is prime
    using the gmpy2 library  """
    bits=int(bits)
    while True:
        possible =  mpz(2)**(bits-1)   + mpz_urandomb(rand,bits-1)
        if is_prime(possible):
            return possible

if __name__ == '__main__':
    #testing
    p=generate_prime(1024)
    t_generate_prime=timing(generate_prime,1)
    clocktime_avg=0
    for x in range(10):
        p, clocktime =t_generate_prime(1024)
        clocktime_avg+=clocktime
#        print p
#        print p.bit_length()