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

    def get_item_info(item):
        view = item.children()[0].children()[0].children()
        # UI_Comm.click_control(view[0])    # checkbox
        img = view[1].children()[0].capture_as_image()
        img_key = Utils.get_img_key(img)
        name = view[1].children()[1].window_text()
        info = {'name':name, 'img_key':img_key}
        return info

    def is_same_info(info1, info2):
        if info1['name'] != info2['name']:
            return False
        if info1['img_key'] != info2['img_key']:
            return False
        return True

    def get_friends(pwin):
        list = pwin.child_window(control_type='List', found_index=1)
        list.draw_outline()

        friends = []
        finish = False
        while finish == False:
            if len(friends) == 0:
                items = list.children(control_type='ListItem')
                for item in items:
                    info = UI_ManageContacts.get_item_info(item)
                    friends.append(info)
                    logger.info('%s', info)
            else:
                finish = True
                for i in range(8):
                    # get last item
                    items = list.children(control_type='ListItem')
                    index = len(items)-1
                    tmp = []
                    info = UI_ManageContacts.get_item_info(items[index])
                    logger.info('+%s', info)
                    if not UI_ManageContacts.is_same_info(info, friends[len(friends)-1]):
                        finish = False
                        friends.append(info)
                        break
                    UI_Comm.mouse_scroll(list, -1)
        return friends

    def close_manage_contacts(pwin):
        button = pwin.child_window(title='Close', control_type='Button')
        if button.exists():
            UI_Comm.click_control(button)
        return
