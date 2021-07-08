#
# Written By:   Weiping Liu
# Created:      Jun 28, 2021
#
import datetime, time
import pywinauto
from helper.my_logging import *
from ui.comm import UI_Comm
from ui.chats import UI_Chats
from ui.chat_info import UI_ChatInfo
from ui.delete_member import Dlg_DeleteMember
from update_history import History
from settings.settings import Settings
from helper.utils import Utils
from actions.helper import Action_Helper

logger = getMyLogger(__name__)

class Action_WelcomeNewMember:
    def welcome_new_member(win, settings):
        logger.info('action: "welcome new member"')
        groups = settings['groups']
        for group in groups:
            logger.info('group: %s', group)
            group_info = Action_Helper.get_group_info(win, group)
            filename = settings['history_dir']+'h_'+group+'.json'
            history = History.read_history(filename)

            new_members = History.check_new_members(history, group_info['members'])
            logger.info('new members: %d', len(new_members))

            blacklist = Settings.get_blacklist()
            moveout = Settings.get_moveout()
            black_members = History.check_blacklist(group_info, blacklist)
            logger.info('blacklist members: %d', len(black_members))
            moveout_members = History.check_blacklist(group_info, moveout)
            logger.info('moveout members: %d', len(moveout_members))

            # trigger repoprt with theshold
            condition = False
            if 'new_member' in settings['threshold']:
                condition |= len(new_members) >= settings['threshold']['new_member']
            if condition == False:
                logger.info('threshold condition does not meet')
                continue

            logger.info(u'updating group info: %s', group)
            history['members'] = group_info['members']
            history['name'] = group
            history['date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            History.write_history(history, filename)

            if 'send_text' in settings['perform']:
                Action_Helper.send_text(win, settings['report_to'], settings['perform']['send_text'])
