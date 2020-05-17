
from sympy import prime
import random
import time


async def gen(code) -> int:
    code = code * prime(random.randint(10**4, 10**5)) + \
        time.time()*prime(random.randint(10**7, 3*10**7))
    return int(code % (10**9))
