
import os
import json
from pathlib import Path

# get the absolute directory of todo file
cwd = os.path.dirname(__file__)

list_rd = 'azure_todo.json'                 # list relative directory
list_ad = os.path.join(cwd, list_rd)        # list absolute directory

config_rd = 'config.json'                   # config relative directory
config_ad = os.path.join(cwd, config_rd)    # config absolute directory

statnow_rd = 'statnow.txt'                   # statnow relative directory
statnow_ad = os.path.join(cwd, statnow_rd)    # statnow absolute directory


async def getconfig(session) -> dict:
    # check if config exists and open it
    if not Path(config_ad).is_file():
        # config doesn't exist, create one
        await session.send('你config咋不见了 咱又帮你重新整了一个 下次别瞎搞了行不')
        f = open(config_ad, 'w')
        f.write(
            '{"arg_aliases": {"add": ["add"], "del": ["del"], "list": ["list"],"clear": ["clear"]}}')
        f.close()
    # decode
    try:
        with open(config_ad, 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        # decoding went wrong
        await session.send('？怪事 你config炸了 赶紧去看看')
        print(e)
        return
    return config


async def getlist(session) -> list:
    # check if a list exists and open it
    if not Path(list_ad).is_file():
        # list doesn't exist, create one
        await session.send('唔……好像并没有找到 list 的样子 所以咱帮你整了个新的')
        with open(list_ad, 'w') as f:
            json.dump(['Add more stuff here!'], f, sort_keys=True, indent=4)
    # decode
    try:
        with open(list_ad, 'r') as f:
            entries = json.load(f)
    except json.JSONDecodeError as e:
        # decoding went wrong
        await session.send('？怪事 你list炸了 赶紧去看看')
        print(e)
        return
    return entries


async def getstatnow(session) -> str:
    try:
        with open(statnow_ad, 'r') as f:
            stat = f.read()
    except FileNotFoundError as e:
        stat = 'Doing nothing...'
    return stat
