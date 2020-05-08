
# perms
modify_perm = {1651031685, 2379246182}
ban_view_perm = {3100820745}


async def check_modify_perm(session):
    user_id = session.event['user_id']
    return user_id in modify_perm


async def check_view_perm(session):
    user_id = session.event['user_id']
    return not user_id in ban_view_perm
