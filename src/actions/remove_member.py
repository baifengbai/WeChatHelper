#
# Written By:   Weiping Liu
# Created:      Jun 28, 2021
#
import time
import pywinauto
from helper.my_logging import *
from ui.comm import UI_Comm
from ui.chat_info import UI_ChatInfo
from ui.delete_member import Dlg_DeleteMember
from update_history import History
from settings.settings import Settings
from helper.utils import Utils
from actions.helper import Action_Helper

logger = getMyLogger(__name__)

class Action_RemoveMember:
    def remove_member(win, settings):
        logger.info('action: "remove member"')
        groups = settings['groups']
        if 'members' in settings:
            members = settings['members']
        else:
            logger.info('remove members in [settings]')
            members = Settings.get_moveout()

        for group in groups:
            logger.info('group: %s', group)
            removed = Action_RemoveMember.remove_from_group(win, group, members)
            if len(removed) == 0:
                continue
            text = ''
            for m in removed:
                if text != '':
                    text += ', '
                text += '"'+m['name']+'"'
            text += ' 被移出群聊'
            Action_Helper.send_text(win, settings['report_to'], text)

    def remove_from_group(win, group_name, members):
        removed = []

        group_info = Action_Helper.get_group_info(win, group_name)
        if group_info == None:
            return removed

        remove = []
        for m in members:
            if m['name'] in group_info['members']:
                remove.append(m)

        for member in remove:
            pwin = UI_ChatInfo.open_chat_info(win)
            if pwin == None:
                break

            dlg = Action_RemoveMember.open_delete_member_dialog(pwin)
            if dlg == None:
                continue
            if Dlg_DeleteMember.delete_member(dlg, member) == True:
                removed.append(member)
            Action_RemoveMember.close_delete_member_dialog(pwin)
        return removed

    def open_delete_member_dialog(pwin):
        delete = Action_RemoveMember.find_delete_member_button(pwin)
        if delete == None:
            logger.warning('you don\'t have right to remove member')
            return None

        # open 'delete member' dialog
        title = 'DeleteMemberWnd'
        retry = 3
        while retry > 0:
            retry -= 1
            time.sleep(0.2)
            try:
                dlg = pwin.window(title=title, control_type='Window')
                if dlg.exists():
                    return dlg
            except pywinauto.findwindows.ElementNotFoundError:
                UI_Comm.click_control(delete)
        logger.warning('could not open "delete member dialog"')
        return None

    def close_delete_member_dialog(pwin):
        title = 'DeleteMemberWnd'
        r = False
        # make sure close 'delete member' dialog
        retry = 3
        while retry > 0:
            retry -= 1
            time.sleep(0.2)
            try:
                dlg = pwin.window(title=title, control_type='Window')
                if not dlg.exists():
                    r = True
                    break
                Dlg_DeleteMember.close_dialog(dlg)
            except pywinauto.findwindows.ElementNotFoundError:
                r = True
                break
        if r == False:
            logger.warning('failed to close "%s" dialog', title)
        return r

    def find_delete_member_button(pwin):
        # find 'Delete member' button
        list = pwin.window(title='Members', control_type='List')
        items = list.children(control_type='ListItem')
        for item in items:
            if item.window_text() == 'Delete':
                return item
        return None
