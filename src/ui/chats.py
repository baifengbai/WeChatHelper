#
# Written By:   Weiping Liu
# Created:      Jun 22, 2021
#
import time
import pywinauto
from ui.comm import UI_Comm
from ui.add_member import Dlg_AddMember
from helper.utils import Utils
from helper.my_logging import *

logger = getMyLogger(__name__)

class UI_Chats:
    def click_chats_button(win):
        # click "Chats Button"
        button = win.child_window(title=u'Chats', control_type='Button')
        UI_Comm.click_control(button)

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

    def send_text(win, text):
        # parse text
        parsed = Utils.parse_keys(text)
        win.type_keys(parsed)
        win.type_keys('{ENTER}')

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

    def get_chat_name(win):
        # find chat title and 'chat info' have the same parent
        share = win.window(title='Chat Info', control_type='Button').parent().parent()
        pane = share.children(control_type='Pane')[0]
        pane = pane.children(control_type='Pane')[0]
        pane = pane.children(control_type='Pane')[1]
        pane = pane.children(control_type='Pane')[0]
        ws = pane.children(control_type='Button')
        if len(ws) == 1:
            return ws[0].window_text()
        logger.warning('did not find "title" in chatting window')
        return None

    # click the edit box
    def click_edit(win):
        edit = win.window(title='Enter', control_type='Edit')
        UI_Comm.click_control(edit)
        return edit

    def send_text(win, text):
        win.type_keys(text)
        win.type_keys('{ENTER}')

    # in chats window, using 'search' to find name
    def search_name(win, name):
        # put focus in 'Search Edit' field
        search = win.window(title=u'Search', control_type='Edit')
        # here we have 2 clicks, in case the focus was not in the window
        # first click activate the window, second click put focus
        UI_Comm.click_control(search)   # get focus
        UI_Comm.click_control(search)   # get focus

        # entering [name] in edit box, then 'Enter'
        win.type_keys(name)
        time.sleep(1)   # delay for entered text to be accepted
        win.type_keys('{ENTER}')

        # check if we see chat 'title' turn to the name
        found = False
        try:
            title = win.window(title=name, control_type='Button', found_index=0)
            title.draw_outline()
            found = (title.window_text() == name)
        except pywinauto.findwindows.ElementNotFoundError:
            pass

        if found:
            logger.info('chat to "%s"', name)
        time.sleep(1)
        return found

    def open_chat_info_window(win):
        button = win.window(title='Chat Info', control_type='Button')
        UI_Comm.click_control(button)
