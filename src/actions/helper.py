#
# Written By:   Weiping Liu
# Created:      Jun 28, 2021
#
import datetime, time
import pywinauto
from helper.my_logging import *
from ui.comm import UI_Comm
from ui.chats import UI_Chats
from ui.chat_info import UI_ChatInfo
from ui.delete_member import Dlg_DeleteMember
from update_history import History
from settings.settings import Settings
from helper.utils import Utils

logger = getMyLogger(__name__)

class Action_Helper:
    def send_text(win, name, text):
        if name != '':
            UI_Chats.chat_to(win, name)
        edit = UI_Chats.click_edit(win)
        UI_Comm.send_text(edit, text)

    def get_group_info(win, group_name):
        UI_Chats.click_chats_button(win)
        UI_Chats.chat_to(win, group_name)

        group_info = UI_ChatInfo.get_chat_info(win)
        if group_info['name'] != group_name:
            logger.error(u'wrong group "%s"', group_info['name'])
            return None
        return group_info
