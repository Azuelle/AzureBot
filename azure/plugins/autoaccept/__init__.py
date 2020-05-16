from nonebot import on_request, RequestSession

__plugin_name__ = 'AutoAccept / 自动接受'
__plugin_usage__ = r"""AutoAccept <v1>
-
自动接受好友请求 / 群聊邀请
"""


@on_request('friend')
async def handle_request(session: RequestSession):
    await session.approve()
    await session.send('（探头）')


@on_request('group.invite')
async def handle_request(session: RequestSession):
    await session.approve()
    await session.send('是jk的bot哦（瞄')
