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
from ui.add_member import Dlg_AddMember
from member_info import Members, Cache

logger = getMyLogger(__name__)

'''
    从通信录中邀请朋友加入群聊
'''
class Action_InviteJoinGroup:
    def invite_join_group(win, settings):
        logger.info('action: "invite_join_group"')

        user_info = UI_User.get_user_info(win)
        if user_info == None:
            return
        contacts = Members(user_info, 'contacts.json').data
        cache_data = Cache(user_info)

        group = settings['to_group']
        if UI_Chats.chat_to(win, group) != True:
            return

        tags = settings['tags']

        cache_item = 'invite_join_group.'+group
        index = cache_data.get(cache_item)
        if index == None:
            index = 0
        while index < len(contacts):
            index1 = Action_InviteJoinGroup.invite(win, contacts, tags, index)
            if index1 == index:
                logger.warning('cannot continue')
                break
            cache_data.set(cache_item, index)

    def invite(win, contacts, tags, index):
        r_index = index     # for return
        pwin = UI_ChatInfo.open_chat_info(win)
        if pwin == None:
            return False

        if UI_ChatInfo.click_add_member(pwin) == False:
            return False

        dlg = pwin.child_window(title='AddMemberWnd', control_type='Window')
        if dlg.exists() == False:
            logger.warning('did not see window: "AddMemberWnd"')
            return False

        limit = 1
        while r_index < len(contacts):
            contact = contacts[r_index]
            r_index += 1
            if contact['tag'] in tags:
                Dlg_AddMember.add_member(dlg, contact['name'], contact['WeChatID'])
            if Dlg_AddMember.number_selected(dlg) >= limit:
                break

        if Dlg_AddMember.number_selected(dlg) > 0:
            Dlg_AddMember.click_ok(dlg)
        else:
            Dlg_AddMember.click_cancel(dlg)
        # posible popup window
        if dlg.exists():
            popup = dlg.child_window(title='WeChat', control_type='Window')
            if popup.exists():
                msg = popup.child_window(control_type='Edit', found_index=0).window_text()
                logger.warning('msg: "%s"', msg)
                ok = popup.child_window(title='OK', control_type='Button')
                UI_Comm.click_control(ok)

                # "Unable to add member. Try again later."
                if msg.startswith('Unable to add member'):
                    r_index -= 1
                    # time.sleep(3)
                    Dlg_AddMember.click_cancel(dlg)

        UI_ChatInfo.close_chat_info(win)
        return r_index
