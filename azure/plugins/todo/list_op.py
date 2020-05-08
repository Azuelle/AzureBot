
import os
import json
from pathlib import Path

from .getlocal import list_ad
from .getlocal import config_ad


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
    await session.send('加完了√')
    await full_list(entries, session)


async def clear_entry(session):
    with open(list_ad, 'w') as f:
        json.dump([], f, sort_keys=True, indent=4)
    await session.send('清完了√')


async def del_entry(entries: list, session):
    target = session.get('del_target')
    if target > len(entries) or target <= 0:
        await session.send('在？你在删空气？')
        return
    del entries[target-1]
    with open(list_ad, 'w') as f:
        json.dump(entries, f, sort_keys=True, indent=4)
    await session.send('删完了√')
    await full_list(entries, session)
