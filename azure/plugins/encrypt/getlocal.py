
import os
import json
from pathlib import Path

# get the absolute directory of todo file
cwd = os.path.dirname(__file__)

config_rd = 'config.json'                   # config relative directory
config_ad = os.path.join(cwd, config_rd)    # config absolute directory


async def getconfig(session) -> dict:
    # check if config exists and open it
    if not Path(config_ad).is_file():
        # config doesn't exist, create one
        await session.send('你config咋不见了 咱又帮你重新整了一个 下次别瞎搞了行不')
        f = open(config_ad, 'w')
        f.write(
            '{"last_updated": 0, "code": 233}')
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
