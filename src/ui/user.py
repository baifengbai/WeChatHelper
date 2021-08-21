#
# Written By:   Weiping Liu
# Created:      Jun 22, 2021
#
import time
import pywinauto
from ui.comm import UI_Comm
from ui.add_member import Dlg_AddMember
from ui.open_dialog import UI_OpenDialog
from ui.wechat_pane import UI_WeChatPane
from helper.utils import Utils
from helper.my_logging import *

logger = getMyLogger(__name__)

class UI_User:
    def click_user_button(win):
        # click "Chats Button"
        button = win.child_window(control_type='Button', found_index=0)
        if button.exists():
            UI_Comm.click_control(button)
            return button
        return None

    def get_user_info(win):
        if UI_User.click_user_button(win) == None:
            return None
        info = UI_WeChatPane.get_member_info(win)
        return info

    def chat_to(win):
        if UI_User.click_user_button(win) == None:
            return None
        UI_WeChatPane.chat_to(win)
