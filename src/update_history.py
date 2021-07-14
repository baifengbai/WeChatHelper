#
# Written By:   Weiping Liu
# Created:      Jun 22, 2021
#
import time
from helper.utils import Utils
from settings.settings import Settings
from helper.my_logging import *

logger = getMyLogger(__name__)

# history = {
#   msgs:[taag:time, info:[text1, text2, ...]}]
#   }
class History:
    def read_history(filename):
        history = Utils.from_json_file(filename)
        if history == None:
            return {'name':'', 'date':'', 'members':[], 'msgs':[]}
        return history

    def write_history(history, filename):
        Utils.to_json_file(history, filename)

    def check_new_members(history, members):
        new_members = []
        for m in members:
            if m not in history['members']:
                new_members.append(m)
        return new_members

    def check_blacklist(history, blacklist):
        members = []
        for m in blacklist:
            if m['name'] in history['members']:
                # i = history['members'].index(m['name'])
                # print('black:', history['members'][i])
                members.append(m)
        return members
