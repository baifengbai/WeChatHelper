#
# Written By:   Weiping Liu
# Created:      Jun 22, 2021
#
import time
import pywinauto
from ui.comm import UI_Comm
from ui.contacts import UI_Contacts
from helper.utils import Utils
from helper.my_logging import *

logger = getMyLogger(__name__)

class UI_ManageContacts:
    def open_manage_contacts(win):
        # click "Contacts Button"
        if UI_Contacts.click_contacts_button(win) == None:
            return None
        list = UI_Contacts.get_contacts_list(win)
        if list == None:
            return None
        UI_Comm.click_control(list)
        list.type_keys('^{HOME}')

        retry = 10
        while retry > 0:
            retry -= 1
            UI_Comm.mouse_scroll(list, 1)     # scroll content down
            button = win.child_window(title='Manage Contacts', control_type='Button')
            if button.exists() and button.rectangle().top > list.rectangle().top:
                break
        if button.exists() == False:
            logger.warning('did not find "Manage Contacts"')
            return None
        UI_Comm.click_control(button)

        pwin = pywinauto.Desktop(backend='uia')['Manage Contacts']
        if pwin.exists():
            return pwin
        # manage = win.parent().children(title='Manage Contacts', control_type='Window')
        # if len(manage) > 0:
        #     return manage[0]
        logger.warning('failed to open "Manage Contacts"')
        return None

    def select_tag(pwin, tag):
        tags_pane = pwin.child_window(title='Tags', control_type='Pane')
        # use 'No tag' to check if it is in open
        no_tag = pwin.child_window(title='No tag', control_type='Pane')
        if not no_tag.exists():
            UI_Comm.click_control(tags_pane)

        tag_pane = pwin.child_window(title=tag, control_type='Pane')
        if tag_pane.exists():
            UI_Comm.click_control(tag_pane)
            p = tag_pane.child_window(control_type='Text', found_index=1)
            n = p.window_text()
            return int(n.strip('()'))

        return 0

    def search_text(pwin, text):
        edit = pwin.child_window(title='Search', control_type='Edit')
        if not edit.exists():
            logger.warning('did not find edit field')
            return None
        # put focus on edit, clear willl show up
        UI_Comm.click_control(edit)
        clear = pwin.child_window(title='Clear', control_type='Button')
        UI_Comm.click_control(clear)
        # after clear the edit, need to set focus again
        UI_Comm.click_control(edit)
        edit.draw_outline()
        edit.type_keys(Utils.parse_keys(text))
        edit.type_keys('{ENTER}')
        return edit

    def find_item(pwin, key):
        UI_ManageContacts.search_text(pwin, key)
        list = pwin.child_window(title='', control_type='List')
        if not list.exists():
            return None
        items = list.children(control_type='ListItem')
        if len(items) == 1:     # unique item in list
            return items[0]
        return None

    # search for wechat_id, return tag setting
    def get_tag(pwin, contact):
        tag = None
        item = UI_ManageContacts.find_item(pwin, contact['WeChatID'])
        if item == None:
            item = UI_ManageContacts.find_item(pwin, contact['name'])
        if item == None:
            logger.warning('did not find "%s":"%s"', contact['name'], contact['WeChatID'])
            return None

        tag = item.children()[0].children()[0].children()[3]
        tag = tag.children()[0].children()[0].window_text()
        return tag

    def close_manage_contacts(pwin):
        button = pwin.child_window(title='Close', control_type='Button')
        if button.exists():
            UI_Comm.click_control(button)
        return
