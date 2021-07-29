#
# Written By:   Weiping Liu
# Created:      Jun 28, 2021
#
import datetime, time, random
from helper.my_logging import *
from helper.utils import Utils
from settings.settings import Settings
from ui.chats import UI_Chats
from ui.chat_info import UI_ChatInfo
from ui.comm import UI_Comm
from ui.user import UI_User
from ui.wechat_pane import UI_WeChatPane
from member_info import Members

logger = getMyLogger(__name__)

'''
    从指定的群组邀请朋友
        随机抽取群里的朋友，邀请限定数量：limit", Default=10
        邀请发出后会在data/USER/members.json作标记 invited:datetime
'''
class Action_InviteFriends:
    def invite_friends(win, settings):
        logger.info('action: "invite_friends"')

        user_info = UI_User.get_user_info(win)
        if user_info == None:
            return
        member_data = Members(user_info)

        group = settings['from_group']
        if UI_Chats.chat_to(win, group) != True:
            return

        text = settings['invite_text']

        limit = 10  # default
        if 'limit' in settings:
            limit = int(settings['limit'])

        for i in range(linit):
            Action_InviteFriends.invite(win, member_data, text)

    def invite(win, member_data, text):
        pwin = UI_ChatInfo.open_chat_info(win)
        if pwin == None:
            return None
        UI_ChatInfo.view_more(pwin)

        list = pwin.window(title='Members', control_type='List')
        rect = list.parent().rectangle()
        members = list.children(control_type='ListItem')

        # pick a member to be invited
        #   1. is not a friend
        #   2. was not invited
        info = None
        for member in members:
            if member.window_text() == 'Add':
                continue
            if member.window_text() == 'Delete':
                continue

            UI_ChatInfo.scroll_in_view(list, member)

            info = UI_WeChatPane.get_member_info(win, member)
            if info == None:
                continue
            info = member_data.find_info(info)
            if info == None:
                continue
            if 'WeChatID' in info or 'invited' in info:
                continue

            msg = Action_InviteFriends.invite_member(win, member, text)
            if msg != False:
                info['invited'] = Utils.get_time_now() + ' ' + msg
                member_data.update_member(info)
        UI_ChatInfo.close_chat_info(win)

    # return None for failed invite or
    # msg text for invited
    def invite_member(win, member, text):
        name = member.window_text()
        member.draw_outline()
        # click the member icon to open
        UI_Comm.click_control(member)
        pane = win.child_window(title='WeChat', control_type='Pane')
        if not pane.exists():
            logger.warning('could not open friend "%s"', name)
            pane.type_keys('{ESC}')
            return False

        # if member is already a friend, WeChat ID will be shown
        # otherwise, 'Add as friend' button should be there.
        add = pane.child_window(title='Add as friend', control_type='Button')
        if not add.exists():
            if pane.child_window(title="WeChat ID: ", control_type="Text").exists():
                logger.info('"%s" is already friend', name)
            else:
                logger.warning('could not add friend "%s"', name)
            pane.type_keys('{ESC}')
            return False

        UI_Comm.click_control(add)
        return Action_InviteFriends.add_friend(win, text)

    def add_friend(win, text):
        retry = 3
        while retry > 0:
            request = win.child_window(title='WeChat', control_type='Window')
            if request.exists():
                break
            retry -= 1
            time.sleep(1)   # wait popup show up

        if not request.exists():
            logger.info('did not see request dialog')
            return False

        if not request.child_window(title='Add Friends', control_type='Text').exists():
            if request.child_window(title='Tip', control_type='Text').exists():
                return Action_InviteFriends.confirm_sent(win)

        edit = request.child_window(control_type='Edit', found_index=0)
        UI_Comm.click_control(edit)
        edit.type_keys('^a{BACKSPACE}')
        UI_Comm.send_text(edit, text, False)
        button = request.child_window(title='OK', control_type='Button')
        button.draw_outline()
        UI_Comm.click_control(button, True, False)
        return Action_InviteFriends.confirm_sent(win)

    def confirm_sent(win):
        retry = 3
        while retry > 0:
            retry -= 1
            tip = win.child_window(title='WeChat', control_type='Window')
            if not tip.exists():
                continue
            if not tip.child_window(title="Tip", control_type="Text").exists():
                continue
            button = tip.child_window(title='OK', control_type='Button')
            if not button.exists():
                continue
            msg = tip.child_window(control_type='Edit', found_index=0).window_text()
            logger.info('"%s"', msg)
            button.draw_outline()
            UI_Comm.click_control(button, True, False)
            logger.info('confirmed sent')
            return msg
        logger.warning('no confirm sent')
        return False

'''
-- already friend
child_window(title="WeChat", control_type="Pane")
   |    |    |    |    |    | child_window(title="刘维平", control_type="Edit")
   |    |    |    |    |    | child_window(title="WeChat ID: ", control_type="Text")
   |    |    |    |    |    | child_window(title="ayixiangke", control_type="Edit")
   |    |    |    | child_window(title="刘维平", control_type="Button")
   |    |    |    |    | child_window(title="Region", control_type="Text")
   |    |    |    |    | child_window(title="Linfen Shanxi ", control_type="Edit")
   |    |    |    | child_window(title="Share Contact Card", control_type="Button")
   |    |    |    | child_window(title="Messages", control_type="Button")

-- add friend
child_window(title="WeChat", control_type="Pane")
   |    |    |    |    |    | child_window(title="briadmin", control_type="Edit")
   |    |    |    | child_window(title="briadmin", control_type="Button")
   |    |    |    | child_window(title="Add as friend", control_type="Button")

-- request window
child_window(title="WeChat", control_type="Window")
   |    |    | child_window(title="Add Friends", control_type="Text")
   |    |    | child_window(title="Close", control_type="Button")
   |    |    | child_window(title="I'm 刘维平", control_type="Edit")
   |    | child_window(title="Must send a friend request and wait until it's accepted.", control_type="Edit")
   |    |    | child_window(title="OK", control_type="Button")
   |    |    | child_window(title="Cancel", control_type="Button")

-- tip Pane
child_window(title="WeChat", control_type="Window")
   |    |    |    | child_window(title="Tip", control_type="Text")
   |    |    |    | child_window(title="Close", control_type="Button")
   |    |    |    | child_window(title="Sent", control_type="Edit")
   |    |    |    | child_window(title="OK", control_type="Button")

'''
