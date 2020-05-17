

from .getlocal import getconfig

import math
import random


async def strenc(raw, session) -> str:
    config = await getconfig(session)
    n = 0
    en = ''
    for ch in raw:
        n = n+1
        chi = ord(ch)*n
        chilen = math.floor(math.log(chi, 10)+1)
        i = 0
        while i < chilen:
            i = i+1
            en = en + chr(random.randint(33, 126))
        en = en + ' {} '.format(chi + (config['code'] % (10**chilen)))
    return en
