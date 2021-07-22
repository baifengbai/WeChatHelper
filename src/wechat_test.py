#
# Written By:   Weiping Liu
# Created:      Jun 22, 2021
#
import sys, os, time
from helper.my_logging import *
from ui.comm import UI_Comm
from ui.chats import UI_Chats
from ui.chat_info import UI_ChatInfo
from ui.user import UI_User
from settings.settings import Settings
import pywinauto

logger = getMyLogger(__name__, __file__)
print(__name__)

def main():
    logger.info('Using pywinauto version: %s', pywinauto.__version__)
    win = UI_Comm.connect_wechat()
    if win == None:
        return

    print(UI_User.get_user_info(win))
    input('wait')
    # print('argv:', sys.argv)
    # Settings.get_settings(os.path.abspath(sys.argv[1]))
    # logger.info('testing ... %s', 'zhongwen中文')

    # UI_Comm.send_text(search, 'A刘维平A')
    edit = UI_Chats.click_edit(win)
    search = UI_Chats.set_focus_search(win)
    print(search.has_keyboard_focus())
    print(edit.has_keyboard_focus())


    # chat_info = UI_ChatInfo.get_chat_info(win)
    # print(chat_info)
    # return

    # UI_Chats.click_edit(win)
    # win.type_keys('@')
    # w = win.window(control_type='List', found_index=0)
    # # print(w.print_control_identifiers())
    # bt = w.children(control_type='ListItem')
    # for b in bt:
    #     if b.children()[0].children()[0].window_text() == '老程':
    #         UI_Comm.click_control(b, True, False)



if __name__ == '__main__':
    main()
