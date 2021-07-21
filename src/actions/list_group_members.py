#
# Written By:   Weiping Liu
# Created:      Jul 15, 2021
#
import pywinauto
import datetime, time
from helper.my_logging import *
from helper.utils import Utils
from settings.settings import Settings
from ui.chats import UI_Chats
from ui.chat_info import UI_ChatInfo
from ui.comm import UI_Comm
from ui.wechat_pane import UI_WeChatPane
from ui.user import UI_User
from member_info import Members

logger = getMyLogger(__name__)

class Action_ListGroupMembers:
    def list_group_members(win, settings):
        logger.info('action: "list_group_members"')
        groups = settings['groups']
        for group in groups:
            members = Action_ListGroupMembers.list_members(win, group)
            if 'update_member' in settings and settings['update_member'] == True:
                user_info = UI_User.get_user_info(win)
                member_data = Members(user_info)
                for m in members:
                    m['groups'] = [group]
                    member_data.update_member(m)

            filename = settings['report_dir'] + group + '.json'
            Utils.to_json_file(members, filename)

    def list_members(win, group):
        if UI_Chats.chat_to(win, group) != True:
            return
        pwin = UI_ChatInfo.open_chat_info(win)
        if pwin == None:
            return
        UI_ChatInfo.view_more(pwin)

        list = pwin.window(title='Members', control_type='List')
        rect = list.parent().rectangle()
        pos = (rect.top + rect.bottom) / 2
        members = list.children(control_type='ListItem')
        member_info = []
        for member in members:
            name = member.window_text()
            if name == 'Add' or name == 'Delete':
                continue

            # scroll into view
            top = member.rectangle().top
            while top > pos:
                UI_Comm.mouse_scroll(pwin, -1)     # scroll content up
                if member.rectangle().top == top:
                    break
                top = member.rectangle().top
            # delay short time for new window open
            info = Action_ListGroupMembers.get_member_info(win, member)

            if info != None:
                member_info.append(info)
                logger.info('%s', str(info))
                # if len(member_info) > 3:
                #     break
        UI_ChatInfo.close_chat_info(win)
        return member_info

    def get_member_info(win, member):
        # open member card
        UI_Comm.click_control(member)
        return UI_WeChatPane.get_member_info(win)
