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
    广播发送所有人
'''
class Action_ForwardMsg:
    def forward_msg(win, settings):
        logger.info('action: "forward_msg"')

        user_info = UI_User.get_user_info(win)
        if user_info == None:
            return

        if 'to' in settings:
            contacts = settings['to']
        else:
            contacts = Members(user_info, 'contacts.json').data

        if 'from' in settings:
            group = settings['from']
        else:
            group = None

        UI_Chats.click_chats_button(win)

        index = 0
        while index < len(contacts):
            index1 = UI_Chats.forward_msgs(win, group, contacts, index)
            if index1 == index:
                logger.warning('stop forwarding')
                break
            index = index1
