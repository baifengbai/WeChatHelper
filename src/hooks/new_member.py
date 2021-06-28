#
# Written By:   Weiping Liu
# Created:      Jun 22, 2021
#
from helper.my_logging import *
from helper.utils import Utils
from ui.comm import UI_Comm
from ui.chats import UI_Chats
from settings.settings import Settings
import pywinauto

logger = getMyLogger(__name__)

class NewMember:
    def send_announce(win, group_info, name=None):
        if name != None:
            UI_Chats.chat_to(win, name)
        NewMember.send_text(win, group_info['announce'])

    def send_text(win, text):
        edit = UI_Chats.click_edit(win)
        parsed = Utils.parse_keys(text)
        edit.type_keys(parsed, pause=0)

        # ENTER to send
        win.type_keys('{ENTER}')
