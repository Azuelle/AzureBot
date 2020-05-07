
# magical 8ball

# inspired by discord bot Tatsu

from nonebot import on_command, CommandSession
import random

result = ['大概',
          '那肯定',
          '不知道',
          '或许',
          '我觉得不太对',
          '我觉得确实']

# main command
@on_command('8ball', aliases=('answer', 'ans', 'getans', 'getanswer', 'magic8ball'), only_to_me=False)
async def get_result(session: CommandSession):
    await session.send(result[random.randint(0, len(result)-1)])
