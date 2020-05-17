
from nonebot import on_command, CommandSession, permission

from .getlocal import getconfig
from .getlocal import config_ad

from .codegen import gen
from .encrypt import strenc
from .decrypt import strdec

import time
import json


# nonebot plugin info
__plugin_name__ = 'encrypt'
__plugin_usage__ = r"""Encrypt <v1>
-
指令            encrypt
别名            enc
参数
[stuff]         - 对 [stuff] 进行加密
-
指令            decrypt
别名            dec
参数
[stuff]         - 对 [stuff] 进行解密
-
指令            revoke
参数
<空>            - 重置密码，重新生成（该操作同时会使之前生成的所有密码失效）
"""


@on_command('encrypt', aliases=('enc'), only_to_me=False)
async def encrypt(session: CommandSession):
    config = await getconfig(session)
    if time.time() - config['last_updated'] > 60*60*6:  # 六小时换一次
        await revoke(session, '啊 到时间了 在这之前咱先调下密码')
        config = await getconfig(session)

    if len(session.current_arg_text.strip()) > 100:
        await session.finish('太长啦……')
    session.state['raw'] = session.current_arg_text.strip()
    raw = session.get('raw', prompt='你倒是告诉咱要加密什么嘛 不说咱也不知道呀（')

    await session.send(await strenc(raw, session))


@on_command('decrypt', aliases=('dec'), only_to_me=False)
async def decrypt(session: CommandSession):
    session.state['en'] = session.current_arg_text.strip()
    en = session.get('en', prompt='你倒是告诉咱要解密什么嘛 不说咱也不知道呀（')

    try:
        org = await strdec(en, session)
    except:
        await session.finish('解不出啊……要不就是你在瞎搞 要不就是密码过期了')
    await session.send('解密完了（如果有乱码啥的 大概是密码过期了）\n' + org)


@on_command('revoke', only_to_me=False, permission=permission.SUPERUSER)
async def revoke_trigger(session: CommandSession):
    await revoke(session)


async def revoke(session, hint='又到换的时间了吗？好——'):
    await session.send(hint)
    config = await getconfig(session)
    config['code'] = await gen(config['code'])
    config['last_updated'] = time.time()
    with open(config_ad, 'w') as f:
        json.dump(config, f, sort_keys=True, indent=4)
