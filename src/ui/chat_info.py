#
# Written By:   Weiping Liu
# Created:      Jun 22, 2021
#
import time
from helper.my_logging import *
from ui.comm import UI_Comm
from ui.chats import UI_Chats
import pywinauto

logger = getMyLogger(__name__)

class UI_ChatInfo:
    def get_chat_info(win):
        UI_ChatInfo.open_chat_info(win)
        pwin = win.window(title='Chat Info', control_type='Window')

        # need to scroll into view
        UI_Comm.mouse_scroll(pwin, -30)
        group_name = UI_ChatInfo.get_group_name(pwin)
        announce = UI_ChatInfo.get_announcement(pwin)
        UI_Comm.mouse_scroll(pwin, 30)

        # view more suppose to list ALL members
        UI_ChatInfo.view_more(pwin)

        members = []
        list = win.window(title='Members', control_type='List')
        items = list.children(control_type='ListItem')
        for m in items:
            name = m.window_text()
            # logger.info('ListItem.window_text: "%s"', name)
            # don't count on 'Add/Delete' buttons
            if name != 'Add' and name != 'Delete':
                members.append(name)

        UI_ChatInfo.close_chat_info(win)

        logger.info('found members: %d', len(members))
        return {'name':group_name, 'announce':announce, 'members':members}

    def open_chat_info(win):
        button = win.window(title='Chat Info', control_type='Button')
        UI_Comm.click_control(button)

    def close_chat_info(win):
        UI_Chats.click_edit(win)

    def view_more(pwin):
        # in case of less member, there is no 'View More Members'
        try:
            button = pwin.window(title='View More Members', control_type='Button')
            UI_Comm.click_control(button, True, False)
        except pywinauto.findwindows.ElementNotFoundError:
            pass

    def get_announcement(pwin):
        p = pwin.window(title='Group Notice', control_type='Text').parent()
        pane = p.children(control_type='Pane')[0]
        text = pane.children(control_type='Text')[0].window_text()
        return text

    def get_group_name(pwin):
        # print(pwin.print_control_identifiers())
        # child_window(title="Group Name", control_type="Text")
        p = pwin.child_window(title='Group Name', control_type='Text').parent()
        pane = p.children(control_type='Pane')[0]
        text = pane.children(control_type='Text')[0].window_text()
        return text
