
# magical 8ball

# inspired by discord bot Tatsu

from nonebot import on_command, CommandSession
import random

# nonebot plugin info
__plugin_name__ = '8ball'
__plugin_usage__ = r"""8ball <v0>
-
指令            8ball
别名            answer / ans / getans / getanswer / magic8ball
参数
[statement]     - 你的问题（是/否）
"""

result = ['不可能',
          '不太可能',
          '也许',
          '很可能',
          '那肯定']

# main command
@on_command('8ball', aliases=('answer', 'ans', 'getans', 'getanswer', 'magic8ball'), only_to_me=False)
async def get_result(session: CommandSession):
    await session.send(result[random.randint(0, len(result)-1)])
