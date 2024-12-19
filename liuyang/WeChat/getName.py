import itchat
import time

# 登录微信
itchat.auto_login(hotReload=True)

# 获取群聊列表
chatrooms = itchat.get_chatrooms(update=True)

# 选择特定的群聊
target_group_name = 'My family'
target_chatroom = None
for room in chatrooms:
    if room['NickName'] == target_group_name:
        target_chatroom = room
        break

if not target_chatroom:
    print(f"未找到群聊 {target_group_name}")
    exit()

# 获取群聊成员
members = itchat.update_chatroom(target_chatroom['UserName'], detailedMember=True)['MemberList']

# 导出成员名单
with open('members.txt', 'w', encoding='utf-8') as f:
    for member in members:
        f.write(member['NickName'] + '\n')

print("成员名单已导出至 members.txt")