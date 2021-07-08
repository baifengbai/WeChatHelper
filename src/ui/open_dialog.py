#
# Written By:   Weiping Liu
# Created:      Jul 7, 2021
#
from ui.comm import UI_Comm
from helper.my_logging import *

logger = getMyLogger(__name__)

class UI_OpenDialog:
    def open_file(win, filename=None):
        dlg = win.child_window(title='Open', control_type='Window')
        if not dlg.exists():
            logger.error('did not find "Open" dialog')
            return False
        edit = dlg.child_window(title='File name:', control_type='Edit')
        if not edit.exists():
            logger.error('did not find "File name:" edit')
            return False
        UI_Comm.click_control(edit)
        UI_Comm.send_text(edit, filename)
        return True
