
from .getlocal import getconfig


async def strdec(en, session) -> str:
    config = await getconfig(session)
    n = 0
    org_n = 0
    org = ''
    start = 0
    llen = 0
    readchilen = True

    for ch in en:
        print('start', start, 'n', n, 'org_n', org_n)
        if(ch == ' '):
            llen = n - start
            if(readchilen):
                chilen = llen
                print('chilen', chilen)
                readchilen = False
                start = n
            else:
                org_n = org_n+1
                org = org + \
                    chr((int(en[start:n]) - (config['code'] %
                                             (10**chilen))) // org_n)
                readchilen = True
                start = n+1
        n = n+1
    org_n = org_n+1
    org = org + \
        chr((int(en[start:n]) - (config['code'] % (10**chilen))) // org_n)
    return org
