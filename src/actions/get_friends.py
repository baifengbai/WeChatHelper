#
# Written By:   Weiping Liu
# Created:      Jun 28, 2021
#
import datetime, time
from helper.my_logging import *
from settings.settings import Settings
from ui.chats import UI_Chats
from ui.chat_info import UI_ChatInfo
from ui.comm import UI_Comm
from ui.manage_contacts import UI_ManageContacts

logger = getMyLogger(__name__)

class Action_GetFriends:
    def get_friends(win, settings):
        logger.info('action: "get_friends"')
        tags = settings['tags']
        pwin = UI_ManageContacts.open_manage_contacts(win)
        if pwin == None:
            return
        # pwin.print_control_identifiers(filename='cc.txt')
        n = UI_ManageContacts.select_tag(pwin, tags[0])
        if n > 0:
            list = UI_ManageContacts.get_friends(pwin)
            print(list)
            print(len(list))
        UI_ManageContacts.close_manage_contacts(pwin)
