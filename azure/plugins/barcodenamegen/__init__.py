import nonebot
from nonebot import on_command, CommandSession

import random

# nonebot plugin info
__plugin_name__ = 'barcodenamegen'
__plugin_usage__ = r"""Barcode Name Generator <v1>
-
指令            barcodenamegen
别名            bcngen, barcode, bcgen
参数
<空>            - 生成
-vb / -|        - 生成（不含 |)
"""


@on_command('barcodenamegen', aliases=['bcngen', 'barcode', 'bcgen'], only_to_me=None)
async def _(session: CommandSession):
    sym = ['i', 'l', 'I', '|']
    arg = session.current_arg_text.strip()
    if(arg == '-vb' or arg == '-|'):
        sym.remove('|')
    siz = len(sym)
    gen = ''
    for i in range(0, random.randint(10, 18)):
        gen += sym[random.randint(0, siz-1)]
    await session.send(gen)
