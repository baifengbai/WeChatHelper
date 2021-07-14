#
# Written By:   Weiping Liu
# Created:      Jul 6, 2021
#
import time, os
from helper.my_logging import *
from ui.chats import UI_Chats
from settings.settings import Settings
from helper.utils import Utils

logger = getMyLogger(__name__)

class Action_SendFile:
    def send_file(win, settings):
        logger.info('action: "send file"')
        sent = 0
        groups = settings['groups']
        if 'folder' not in settings:
            logger.warning('need to have "folder" in settings')
            return sent
        # verify the folder exists
        folder = settings['folder']
        if not os.path.exists(folder):
            logger.warning('folder does not exists "%s"', folder)
            return sent

        files = []
        for f in os.listdir(folder):
            files.append(folder+'\\'+f)

        logger.info('number of files: %d', len(files))
        if len(files) == 0:
            return sent

        for group in groups:
            UI_Chats.click_chats_button(win)
            UI_Chats.chat_to(win, group)
            Action_SendFile.upload_files(win, files)

    def upload_files(win, files):
        for f in files:
            fullpath = os.path.abspath(f)
            if UI_Chats.upload_file(win, fullpath) == True:
                # move to sent folder
                pass

        return len(files)
