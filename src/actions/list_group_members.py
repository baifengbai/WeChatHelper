#
# Written By:   Weiping Liu
# Created:      Jul 15, 2021
#
import pywinauto
import datetime, time
from helper.my_logging import *
from helper.utils import Utils
from settings.settings import Settings
from ui.chats import UI_Chats
from ui.chat_info import UI_ChatInfo
from ui.comm import UI_Comm

logger = getMyLogger(__name__)

class Action_ListGroupMembers:
    def list_group_members(win, settings):
        logger.info('action: "list_group_members"')
        groups = settings['groups']
        for group in groups:
            Action_ListGroupMembers.list_members(win, group, settings['report_dir'])

    def list_members(win, group, report_dir):
        if UI_Chats.chat_to(win, group) != True:
            return
        pwin = UI_ChatInfo.open_chat_info(win)
        if pwin == None:
            return
        UI_ChatInfo.view_more(pwin)

        list = pwin.window(title='Members', control_type='List')
        rect = list.parent().rectangle()
        pos = (rect.top + rect.bottom) / 2
        members = list.children(control_type='ListItem')
        member_info = []
        for member in members:
            name = member.window_text()
            if name == 'Add' or name == 'Delete':
                continue

            # scroll into view
            top = member.rectangle().top
            while top > pos:
                UI_Comm.mouse_scroll(pwin, -1)     # scroll content up
                if member.rectangle().top == top:
                    break
                top = member.rectangle().top
            # delay short time for new window open
            info = Action_ListGroupMembers.get_member_info(win, member)

            if info != None:
                member_info.append(info)
                logger.info('%s', str(info))
                # if len(member_info) > 3:
                #     break
        UI_ChatInfo.close_chat_info(win)

        filename = report_dir + group + '.json'
        Utils.to_json_file(member_info, filename)

    def get_member_info(win, member):
        # open member card
        UI_Comm.click_control(member)

        pane = win.child_window(title='WeChat', control_type='Pane')
        if not pane.exists():
            logger.warning('did not find member card pane')
            return None
        # pane.print_control_identifiers(filename='id.tex')

        # get number of TEXT controls
        n = 1
        try:
            fields = pane.child_window(control_type='Text')
            fields.exists()
        except pywinauto.findwindows.ElementAmbiguousError as e:
            n = int(str(e).split()[2])         # There are N elements

        name = pane.child_window(control_type='Edit', found_index=0)
        info = {'name': name.window_text()}

        for index in range(n):
            field = pane.child_window(control_type='Text', found_index=index)
            if not field.exists():
                break
            name = field.window_text()
            if name != '':
                value = field.parent().children()[1].window_text()
                info[name.replace(' ', '').replace(':', '')] = value

        pane.type_keys('{ESC}')     # close popup card
        return info
