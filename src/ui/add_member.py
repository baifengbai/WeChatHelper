#
# Written By:   Weiping Liu
# Created:      Jun 22, 2021
#
from ui.comm import UI_Comm
from helper.my_logging import *

logger = getMyLogger(__name__)

class Dlg_AddMember:
    def add_member(win, name):
        # make sure the dialog was opened from the caller
        pwin = win.child_window(title='AddMemberWnd', control_type='Window')
        pwin.set_focus()

        # put name in 'Search Edit' field
        edit = pwin.window(title='Search', control_type='Edit')
        # UIApi.click_control(edit)
        edit.draw_outline()
        edit.set_focus()
        UI_Comm.send_text(edit, name)

        # if the name exists, it must have only 1 candidate and 1 selected
        n1 = Dlg_AddMember.number_candidate(pwin)
        n2 = Dlg_AddMember.number_selected(pwin)
        r = n1 == 1 and n2 == 1
        if r:
            Dlg_AddMember.click_ok(pwin)
        else:
            logger.error('candidate:selected "%d:%d"', n1, n2)
            Dlg_AddMember.click_cancel(pwin)
        return r

    def click_ok(dlg):
        button = dlg.window(title='OK', control_type='Button')
        UI_Comm.click_control(button, True, False)

    def click_cancel(dlg):
        button = dlg.window(title='Cancel', control_type='Button')
        UI_Comm.click_control(button, True, False)

    def number_candidate(dlg):
        list = dlg.window(control_type='List', found_index=0)
        items = list.children(control_type='ListItem')
        return len(items)

    def number_selected(dlg):
        list = dlg.window(control_type='List', found_index=1)
        items = list.children(control_type='ListItem')
        return len(items)
