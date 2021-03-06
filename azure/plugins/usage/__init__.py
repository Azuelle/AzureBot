import nonebot
from nonebot import on_command, CommandSession

# nonebot plugin info
__plugin_name__ = 'usage'
__plugin_usage__ = r"""Usage <v1>
-
指令            usage
别名            help
参数
<空>            - 发送功能列表
[command]       - 发送对应指令的帮助
"""


@on_command('usage', aliases=['help'], only_to_me=None)
async def _(session: CommandSession):
    # 获取设置了名称的插件列表
    plugins = list(filter(lambda p: p.name, nonebot.get_loaded_plugins()))

    arg = session.current_arg_text.strip()
    if not arg:
        # 如果用户没有发送参数，则发送功能列表
        await session.send(
            '我现在能干啥：\n' + '\n'.join(p.name for p in plugins))
        return

    # 如果发了参数则发送相应命令的使用帮助
    for p in plugins:
        if p.name.lower() == arg:
            await session.send(p.usage)
