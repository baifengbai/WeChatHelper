#
# Written By:   Weiping Liu
# Created:      Jun 22, 2021
#
import time
import pywinauto
from ui.comm import UI_Comm
from ui.add_member import Dlg_AddMember
from ui.open_dialog import UI_OpenDialog
from helper.utils import Utils
from helper.my_logging import *

logger = getMyLogger(__name__)

class UI_Chats:
    def click_chats_button(win):
        # click "Chats Button"
        button = win.child_window(title=u'Chats', control_type='Button')
        if button.exists():
            UI_Comm.click_control(button)
            return button
        return None

    def chat_to(win, name):
        # search from chat name list
        if UI_Chats.search_name(win, name) == True:
            return True

        # if we cannot find the name from search, try to search from
        # contacts list
        # click '+' ("Start Group Chat Button") to open the dialog
        logger.info('did not get %s from chat search, try contacts', name)
        button = win.child_window(title='Start Group Chat', control_type='Button')
        UI_Comm.click_control(button)

        if Dlg_AddMember.add_member(win, name) == False:
            logger.warning('not in contacts: %s', name)
            return False
        return True

    # history = {
    #   members:['name1', ...],
    #   msgs:[{tag:time, msg:[text1, text2, ...]}]
    # }
    def get_chat_msgs(win):
        msgs = []
        list = win.child_window(title=u'消息', control_type='List')
        items = list.children(control_type='ListItem')
        tag = None
        msg = []
        for item in items:
            # print(item.window_text())
            pane = item.children(control_type='Pane')
            # date-time mark line
            if pane[0].window_text() != '':
                item_time = pane[0].window_text()
                dt = utils.format_time_tag(item_time)
                # got time tag
                if tag != None:
                    msgs.append({'tag':tag, 'msg':msg})
                tag = dt
                msg = []
            # informational item
            edit = pane[0].children(control_type='Edit')
            if len(edit) > 0 and tag != None:
                msg.append(edit[0].window_text())
        if tag != None:
            msgs.append({'tag':tag, 'msg':msg})
        return msgs

    def check_chat_name(win, name):
        title = win.child_window(title=name, control_type='Button', found_index=0)
        return title.exists()
        # except pywinauto.findwindows.ElementAmbiguousError as e:
        #     n = int(str(e).split()[2])  # "There are 2 elements ...
        #     for x in range(n):
        #         print(n, 'buttons')
        # return True # title.exists()

    # click the edit box
    def click_edit(win):
        UI_Chats.click_chats_button(win)
        edit = win.child_window(title='Enter', control_type='Edit')
        if not edit.exists():
            return None
        retry = 3
        while retry > 0:
            UI_Comm.click_control(edit)
            if edit.has_keyboard_focus():
                break
            time.sleep(0.2)
            retry -= 1

        if retry == 0 and not edit.has_keyboard_focus():
            logger.warning('failed set focus on "edit"')
            raise Error
        return edit

    def set_focus_search(win):
        UI_Chats.click_chats_button(win)
        # put focus in 'Search Edit' field
        search = win.window(title=u'Search', control_type='Edit')
        retry = 3
        while retry > 0:
            if search.has_keyboard_focus():
                break
            UI_Comm.click_control(search)   # get focus
            time.sleep(0.2)
            retry -= 1
        if retry == 0 and not search.has_keyboard_focus():
            logger.warning('failed set focus on "search"')
            raise Error
        return search

    # in chats window, using 'search' to find name
    def search_name(win, name):
        search = UI_Chats.set_focus_search(win)
        # entering [name] in edit box, then 'Enter'
        UI_Comm.send_text(search, name)

        # check if we see chat 'title' turn to the name
        found = False
        # wait short time
        wt = 5
        while wt > 0:
            if UI_Chats.check_chat_name(win, name) == True:
                found = True
                logger.info('chat to "%s"', name)
                break
            wt -= 1
            time.sleep(0.2)
            search.type_keys('{ENTER}')
        return found

    def open_chat_info_window(win):
        button = win.window(title='Chat Info', control_type='Button')
        UI_Comm.click_control(button)

    def click_send_file(win):
        button = win.child_window(title='Send File', control_type='Button')
        if not button.exists():
            logger.warning('did not find "Send File" button')
            return None
        UI_Comm.click_control(button)
        return button

    def upload_file(win, filename):
        logger.info('uploading "%s"', filename)
        if UI_Chats.click_send_file(win) == None:
            return False
        if UI_OpenDialog.open_file(win, filename) == False:
            return False
        edit = UI_Chats.click_edit(win)
        edit.type_keys('{ENTER}')
        return True
