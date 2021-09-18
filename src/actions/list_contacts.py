#
# Written By:   Weiping Liu
# Created:      Jun 28, 2021
#
import datetime, time
from helper.my_logging import *
from helper.utils import Utils
from settings.settings import Settings
from ui.contacts import UI_Contacts
from ui.manage_contacts import UI_ManageContacts
from ui.comm import UI_Comm
from ui.user import UI_User
from member_info import Members

logger = getMyLogger(__name__)

class Action_ListContacts:
    def list_contacts(win, settings):
        logger.info('action: "list_contacts"')

        UI_Contacts.click_contacts_button(win)
        contacts = UI_Contacts.get_contacts(win)
        # contacts = [{'WeChatID':'AngieChea001'}]
        pwin = UI_ManageContacts.open_manage_contacts(win)
        if pwin == None:
            return

        for c in contacts:
            tag = UI_ManageContacts.get_tag(pwin, c)
            c['tag']= tag

        friends = UI_ManageContacts.close_manage_contacts(pwin)

        if 'update_member' in settings and settings['update_member'] == True:
            user_info = UI_User.get_user_info(win)
            member_data = Members(user_info, "contacts.json")
            for m in contacts:
                member_data.update_member(m)

        filename = settings['report_dir'] + 'contacts.json'
        Utils.to_json_file(contacts, filename)

        logger.info('number of member contacts: %d', len(member_data.data))
        logger.info('number of contacts: %d', len(contacts))
