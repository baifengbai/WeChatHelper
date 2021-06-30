#
# Written By:   Weiping Liu
# Created:      Jun 22, 2021
#
import sys, os
from helper.my_logging import *
from ui.comm import UI_Comm
from settings.settings import Settings
from actions.actions import Actions
import pywinauto


def main(setting_file):
    logger.info('Using pywinauto version: %s', pywinauto.__version__)
    logger.info('settings from: %s', setting_file)
    settings = Settings.get_settings(setting_file)
    if settings == None:
        logger.error('error in setting file %s', setting_file)
        return

    win = UI_Comm.connect_wechat()
    if win == None:
        return

    # before doing any action, make sure there is no sub-windows in open,
    # and any special input method not active (cause input problem)

    actions = settings['actions']
    if 'report_group_info' in actions:
        Actions.report_group_info(win, actions['report_group_info'])
    elif 'welcome_new_member' in actions:
        Actions.welcome_new_member(win, actions['welcome_new_member'])
    logger.info('no more actions')
    # update_history()
    # accept_new_friends(win)

if __name__ == '__main__':
    if sys.argv[1] == None:
        logger.warning('need setting file')
    else:
        setting_file = os.path.abspath(sys.argv[1])
        logger = getMyLogger(__name__, setting_file)
        if os.path.exists(setting_file):
            main(setting_file)
