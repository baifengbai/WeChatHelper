#
# Written By:   Weiping Liu
# Created:      Jun 22, 2021
#
from ui.comm import UI_Comm
from helper.my_logging import *

logger = getMyLogger(__name__)

# this window is open after clicked '-' button for deleting members
# name='DeleteMemberWnd'

class Dlg_DeleteMember:
    def delete_member(dlg, member):
        if dlg.window_text() != 'DeleteMemberWnd':
            logger.error('the dialog is not "DeleteMemberWnd"')
            return False

        # put name in 'Search Edit' field
        edit = dlg.window(title='Search', control_type='Edit')
        UI_Comm.click_control(edit)
        if not edit.has_keyboard_focus():
            logger.warning('failed to put focus on edit')
            return False

        # search with id, or name
        text = member['name']
        if 'id' in member:
            text = member['id']
        UI_Comm.send_text(edit, text)

        items = Dlg_DeleteMember.get_candidate_items(dlg)
        if len(items) == 0:
            logger.warning('the member does not exist "%s"', member['name'])
            Dlg_DeleteMember.close_dialog(dlg)
            return False
        elif len(items) > 1:
            logger.warning('the member id/name not unique')
            Dlg_DeleteMember.close_dialog(dlg)
            return False
        selected = Dlg_DeleteMember.get_selected_items(dlg)
        if len(selected) != 1:
            Dlg_DeleteMember.click_candidate(dlg, items[0])
        # double check
        selected = Dlg_DeleteMember.get_selected_items(dlg)
        if len(selected) != 1:
            logger.warning('something wrong')
            return False
        Dlg_DeleteMember.click_delete(dlg)

        confirm = dlg.window(title='WeChat', control_type='Window')
        if confirm.window_text() == 'WeChat':
            Dlg_DeleteMember.confirm_delete(confirm)
            return True
        return False

    def confirm_delete(confirm):
        delete = confirm.window(title='Delete', control_type='Button')
        UI_Comm.click_control(delete)

    def click_delete(dlg):
        delete = dlg.window(title='Delete', control_type='Button')
        # once 'delete' clicked, another confirm window with the
        # same name button show up, doo not highlight it
        UI_Comm.click_control(delete)

    def close_dialog(dlg):
        button = dlg.window(title='Close', control_type='Button')
        UI_Comm.click_control(button)

    def click_candidate(dlg, item):
        select = item.children()[0].children()[2]
        UI_Comm.click_control(select)

    def get_selected_items(dlg):
        pane = dlg.children(control_type='Pane')[1]
        pane = pane.children(control_type='Pane')[2]
        list = pane.children(control_type='List')[0]
        items = list.children(control_type='ListItem')
        return items

    # get candidate list
    def get_candidate_items(dlg):
        pane = dlg.children(control_type='Pane')[1]
        pane = pane.children(control_type='Pane')[0]
        list = pane.children(control_type='List')[0]
        items = list.children(control_type='ListItem')
        return items
