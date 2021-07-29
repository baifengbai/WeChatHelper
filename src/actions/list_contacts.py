#
# Written By:   Weiping Liu
# Created:      Jun 28, 2021
#
import datetime, time
from helper.my_logging import *
from settings.settings import Settings
from ui.contacts import UI_Contacts
from ui.comm import UI_Comm
from ui.user import UI_User
from member_info import Members

logger = getMyLogger(__name__)

class Action_ListContacts:
    def list_contacts(win, settings):
        logger.info('action: "list_contacts"')

        user_info = UI_User.get_user_info(win)
        if user_info == None:
            return
        if UI_Contacts.click_contacts_button(win) == None:
            return

        contacts = UI_Contacts.get_contacts(win)
        # print('contacts:', len(contacts))

        member_data = Members(user_info)
        for m in contacts:
            member_data.update_member(m)
