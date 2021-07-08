#
# Written By:   Weiping Liu
# Created:      Jun 22, 2021
#
import time
import pywinauto
from helper.utils import Utils
from helper.my_logging import *

logger = getMyLogger(__name__)

class UI_Comm:
    def connect_wechat(class_name='WeChatMainWndForPC'):
        logger.info('connecting to "WeChat"')
        try:
            app = pywinauto.application.Application(backend='uia').connect(class_name=class_name)
        except:
            logger.error('connecting to WeChat failed')
            return None
        return app['WeChat']

    # optionally highlight the window rect
    def click_control(control, center=True, highlight=True):
        coords = control.rectangle()
        if center == True:
            x = int((coords.right - coords.left) / 2)
            y = int((coords.bottom - coords.top) / 2)
        else:
            x = 5
            y = 5
        pywinauto.mouse.click(button='left', coords=(coords.left+x, coords.top+y))
        if highlight is True:
            control.draw_outline()

    def send_text(control, text):
        # parse text
        control.type_keys(Utils.parse_keys(text), pause=0)
        time.sleep(1)   # have to delay short time, or 'Enter' does not work!
        control.type_keys('{ENTER}')
        # in case of input method, first Enter used as confirm input
        # in case of open dialog, Enter cause window closed
        # control.type_keys('{ENTER}')

    def mouse_scroll(control, dist):
        coords = control.rectangle()
        x = int((coords.right - coords.left) / 2)
        y = int((coords.bottom - coords.top) / 2)
        pywinauto.mouse.scroll(coords=(coords.left+x, coords.top+y), wheel_dist=dist)
