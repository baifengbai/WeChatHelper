#
# Written By:   Weiping Liu
# Created:      Jun 22, 2021
#
from ui.comm import UI_Comm
from helper.my_logging import *

logger = getMyLogger(__name__)

class Dlg_AddMember:
    # returns number of selected
    def add_member(dlg, name, id=None):
        # dlg.set_focus()

        r = Dlg_AddMember.search_unique(dlg, name)
        if r == False:
            r = Dlg_AddMember.search_unique(dlg, id)

        if r == True:
            logger.info('selected "%s"', name)

        return r

    def search_unique(dlg, text):
        # put name in 'Search Edit' field
        edit = dlg.window(title='Search', control_type='Edit')

        edit.draw_outline()
        edit.set_focus()
        edit.type_keys('^A{BACKSPACE}')
        UI_Comm.send_text(edit, text)

        # if the name exists, it must have only 1 candidate and 1 selected
        n1 = Dlg_AddMember.number_candidate(dlg)
        if n1 != 1:
            edit.type_keys('{ENTER}')   # de-select
        return n1 == 1

    def click_ok(dlg):
        button = dlg.window(title='OK', control_type='Button')
        UI_Comm.click_control(button)

    def click_cancel(dlg):
        button = dlg.window(title='Cancel', control_type='Button')
        UI_Comm.click_control(button)

    def number_candidate(dlg):
        list = dlg.window(control_type='List', found_index=0)
        items = list.children(control_type='ListItem')
        return len(items)

    def number_selected(dlg):
        list = dlg.window(control_type='List', found_index=1)
        items = list.children(control_type='ListItem')
        return len(items)
