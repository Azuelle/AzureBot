
# tjk's cute(maybe?) bot

import nonebot
import config

from os import path

if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_builtin_plugins()
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'azure', 'plugins'),
        'azure.plugins'
    )
    nonebot.run()
