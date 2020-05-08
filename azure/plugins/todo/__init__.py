
from nonebot import on_command, CommandSession

from .list_op import full_list
from .list_op import add_entry
from .list_op import del_entry
from .list_op import clear_entry

from .checkperm import check_modify_perm
from .checkperm import check_view_perm

from .getlocal import getconfig
from .getlocal import getlist
from .getlocal import getstatnow
from .getlocal import statnow_ad

# nonebot plugin info
__plugin_name__ = 'Todo / 待办'
__plugin_usage__ = r"""Todo <v1>
-
指令            todo
别名            todolist / read
参数
<空>            - 默认为 list
                  详见对应参数 
add [stuff]     - 添加项目
                - 别名
                    a
del [index]     - 删除编号为 [index] 的项目
                - 别名
                    remove / delete / d / r
list [index]    - 列出所有项目
                - 别名
                    show / l
clear [index]   - 清除所有项目
                - 别名
                    removeall / deleteall / delall / c
-
指令            statnow
别名            now / doing
参数
<空>            - 显示当前状态
[stuff]         - 设置当前状态为 [stuff]
"""

# main command
@on_command('todo', aliases=('todolist', 'read'), only_to_me=False)
async def todo(session: CommandSession):
    entries = await getlist(session)

    # handling command
    op = session.get('op')

    if op == 'list':
        if not await check_view_perm(session):
            await session.finish('爬，不准你看[CQ:face,id=9]')
        await full_list(entries, session)

    if op == 'add':
        if not await check_modify_perm(session):
            await session.finish('不准你改[CQ:face,id=111]')
        await add_entry(entries, session)

    if op == 'del':
        if not await check_modify_perm(session):
            await session.finish('不准你改[CQ:face,id=111]')
        await del_entry(entries, session)

    if op == 'clear':
        if not await check_modify_perm(session):
            await session.finish('不准你改[CQ:face,id=111]')
        await clear_entry(session)


@todo.args_parser
async def _(session: CommandSession):
    config = await getconfig(session)

    stripped_arg = session.current_arg_text.strip()
    if not stripped_arg:
        # no argument, defaults to list
        session.state['op'] = 'list'
        return

    op = stripped_arg.split()[0]
    stuff = stripped_arg[len(op)+1:]

    if op in config['arg_aliases']['add']:
        session.state['op'] = 'add'
        session.state['entry'] = stuff

    if op in config['arg_aliases']['del']:
        session.state['op'] = 'del'
        mul = 1
        if stuff[0] == '-':
            mul = -1
            stuff = stuff[1:]
        if not stuff.isnumeric():
            session.finish('你想删的是"{}"……所以你到底要删哪一条（思考'.format(stuff))
        session.state['del_target'] = int(stuff)*mul

    if op in config['arg_aliases']['list']:
        session.state['op'] = 'list'

    if op in config['arg_aliases']['clear']:
        session.state['op'] = 'clear'

# statnow command
@on_command('statnow', aliases=('now', 'doing'), only_to_me=False)
async def statnow(session: CommandSession):
    arg = session.current_arg_text.strip()
    if not arg:
        await session.finish('现在在干啥：\n'+await getstatnow(session))

    if not await check_modify_perm(session):
        await session.finish('不准你改[CQ:face,id=111]')

    await session.send('懂啦 你在'+arg)
    with open(statnow_ad, 'w') as f:
        f.write(arg)
