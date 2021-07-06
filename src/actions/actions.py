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

logger = getMyLogger(__name__)

class Actions:
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
            removed = Actions.remove_from_group(win, group, members)
            if len(removed) == 0:
                continue
            text = ''
            for m in removed:
                if text != '':
                    text += ', '
                text += '"'+m['name']+'"'
            text += ' 被移出群聊'
            Actions.send_text(win, settings['report_to'], text)

    def remove_from_group(win, group_name, members):
        removed = []
        pywinauto.timings.Timings.window_find_timeout = 0.2
        group_info = Actions.get_group_info(win, group_name)
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

            dlg = Actions.open_delete_member_dialog(pwin)
            if dlg == None:
                continue
            if Dlg_DeleteMember.delete_member(dlg, member) == True:
                removed.append(member)
            Actions.close_delete_member_dialog(pwin)
        return removed

    def open_delete_member_dialog(pwin):
        delete = Actions.find_delete_member_button(pwin)
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
                if dlg.window_text() == title:
                    return dlg
            except pywinauto.findwindows.ElementNotFoundError:
                UI_Comm.click_control(delete)
        logger.warning('could not open "delete member dialog"')
        return None

    def close_delete_member_dialog(pwin):
        title = 'DeleteMemberWnd'
        # make sure close 'delete member' dialog
        retry = 3
        while retry > 0:
            retry -= 1
            time.sleep(0.2)
            try:
                dlg = pwin.window(title=title, control_type='Window')
                if dlg.window_text() == title:
                    Dlg_DeleteMember.close_dialog(dlg)
            except pywinauto.findwindows.ElementNotFoundError:
                break

    def find_delete_member_button(pwin):
        # find 'Delete member' button
        list = pwin.window(title='Members', control_type='List')
        items = list.children(control_type='ListItem')
        for item in items:
            if item.window_text() == 'Delete':
                return item
        return None

    def welcome_new_member(win, settings):
        logger.info('action: "welcome new member"')
        groups = settings['groups']
        for group in groups:
            logger.info('group: %s', group)
            group_info = Actions.get_group_info(win, group)
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
                Actions.send_text(win, settings['report_to'], settings['perform']['send_text'])

    def report_group_info(win, settings):
        logger.info('action: "report group info"')
        groups = settings['groups']
        for group in groups:
            logger.info('group: %s', group)
            group_info = Actions.get_group_info(win, group)
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
            if 'blacklist' in settings['threshold']:
                condition |= len(black_members) + len(moveout_members) >= settings['blacklist']
            if condition == False:
                logger.info('threshold condition does not meet')
                continue

            group_info['new_members'] = new_members
            group_info['blacklist'] = black_members
            group_info['moveout'] = moveout_members
            Actions.report_info(win, settings['report_to'], group_info)

            logger.info(u'updating group info: %s', group)
            history['members'] = group_info['members']
            history['name'] = group
            history['date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            History.write_history(history, filename)

    def report_info(win, name, group_info):
        new_members = group_info['new_members']
        blacklist = group_info['blacklist']
        moveout = group_info['moveout']
        info = '"'+group_info['name']+'" 群信息更新:\n'
        info += '人数：'+str(len(group_info['members']))+'\n'
        info += '新加入：'+str(len(new_members))+'\n'
        for s in new_members:
            info += '  "' + s + '"\n'
        info += '黑名单：'+str(len(blacklist))+'\n'
        for s in blacklist:
            info += '  "'+s['name']+'"\n'
        info += '黑名单：'+str(len(moveout))+'\n'
        for s in moveout:
            info += '  "'+s['name']+'"\n'
        Actions.send_text(win, name, info)

    def send_text(win, name, text):
        if name != '':
            UI_Chats.chat_to(win, name)
        edit = UI_Chats.click_edit(win)
        UI_Comm.send_text(edit, text)

    def get_group_info(win, group_name):
        UI_Chats.click_chats_button(win)
        UI_Chats.chat_to(win, group_name)

        group_info = UI_ChatInfo.get_chat_info(win)
        if group_info['name'] != group_name:
            logger.error(u'wrong group "%s"', group_info['name'])
            return None
        return group_info
