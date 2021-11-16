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

        data = {
            'group_name': 'Contacts',
            'time': Utils.get_time_now(),
            'size': len(contacts),
            'members': contacts
        }
        filename = settings['save_to'] + 'contacts.json'
        Utils.to_json_file(data, filename)

        logger.info('number of contacts: %d', len(contacts))
