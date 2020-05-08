
from nonebot import on_command, CommandSession

import os
import json
from pathlib import Path

# nonebot plugin info
__plugin_name__ = 'Todo'
__plugin_usage__ = r"""Todo

懒得写帮助
"""


# perms
modify_perm = {1651031685, 2379246182}
ban_view_perm = {3100820745}

# get the absolute directory of todo file
cwd = os.path.dirname(__file__)

list_rd = 'azure_todo.json'                 # list relative directory
list_ad = os.path.join(cwd, list_rd)        # list absolute directory

config_rd = 'config.json'                   # config relative directory
config_ad = os.path.join(cwd, config_rd)    # config absolute directory

# main command
@on_command('todo', aliases=('todolist', 'Todo', 'read'), only_to_me=False)
async def handle_todo(session: CommandSession):
    # check if a list exists and open it
    if not Path(list_ad).is_file():
        # list doesn't exist, create one
        await session.send('唔……好像并没有找到表的样子 所以咱帮你整了个新的')
        with open(list_ad, 'w') as f:
            json.dump(['Add more stuff here!'], f, sort_keys=True, indent=4)
    # decode
    try:
        with open(list_ad, 'r') as f:
            entries = json.load(f)
    except json.JSONDecodeError as e:
        # decoding went wrong
        await session.send('？怪事 你 list 炸了 赶紧去看看')
        print(e)
        return

    # handling command
    op = session.get('op')

    if op == 'list':
        if not await check_view_perm(session):
            await session.finish('不准你看[CQ:face,id=9]')
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


@handle_todo.args_parser
async def _(session: CommandSession):
    # check if config exists and open it
    if not Path(config_ad).is_file():
        # config doesn't exist, create one
        await session.send('你 config 呢')
        f = open(config_ad, 'w')
        f.write(r"""{
    "arg_aliases": {
        "add": [
            "add",
            "a"
        ],
        "del": [
            "del",
            "remove",
            "delete",
            "d",
            "r"
        ],
        "list": [
            "list",
            "show",
            "l"
        ],
        "clear": [
            "clear",
            "removeall",
            "deleteall",
            "delall",
            "c"
        ]
    }
}""")
        f.close()
    # decode
    try:
        with open(config_ad, 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        # decoding went wrong
        await session.send('？怪事 你 config 炸了 赶紧去看看')
        print(e)
        return

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


async def full_list(entries: list, session):
    if not entries:
        await session.send('目前你 todo list 上啥都没有…')
        return

    tmp_index = 0
    fullstr = '现在你的 todo list 上还有这些玩意儿\n'
    for entry in entries:
        tmp_index = tmp_index+1
        fullstr = fullstr + '[{}] {}\n'.format(tmp_index, entry)
    await session.send(fullstr)


async def add_entry(entries: list, session):
    new_entry = session.get('entry')
    entries.append(new_entry)
    with open(list_ad, 'w') as f:
        json.dump(entries, f, sort_keys=True, indent=4)
    await session.send('好了帮你加完了')
    full_list(entries, session)


async def clear_entry(session):
    with open(list_ad, 'w') as f:
        json.dump([], f, sort_keys=True, indent=4)
    await session.send('咱清完了')


async def del_entry(entries: list, session):
    target = session.get('del_target')
    if target > len(entries) or target <= 0:
        await session.send('你在删空气？')
        return
    del entries[target-1]
    with open(list_ad, 'w') as f:
        json.dump(entries, f, sort_keys=True, indent=4)
    await session.send('删啦√')
    full_list(entries, session)


async def check_modify_perm(session):
    user_id = session.event['user_id']
    return user_id in modify_perm


async def check_view_perm(session):
    user_id = session.event['user_id']
    return not user_id in ban_view_perm
