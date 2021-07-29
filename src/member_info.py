#
# Written By:   Weiping Liu
# Created:      Jun 22, 2021
#
import time
import imagehash
import copy
from helper.utils import Utils
from settings.settings import Settings
from helper.my_logging import *

logger = getMyLogger(__name__)

# data = [
#   {
#       WeChatID:'xxx',
#       img:'filename',     # no folder name
#       ...
#   },
#   ...
#   ]
class Members:
    def __init__(self, user):
        if not 'WeChatID' in user:
            logger.error('need "WeChatID"')
        self.folder = '.\\data\\'+user['WeChatID'] + '\\'
        self.img_folder = self.folder + 'img\\'
        self.filename = self.folder + 'members.json'
        self.data = self.read()

        if os.path.exists(self.img_folder) == False:
            os.makedirs(self.img_folder)

    def read(self):
        data = Utils.from_json_file(self.filename)
        if data == None:
            return []
        return data

    def write(self):
        Utils.to_json_file(self.data, self.filename)

    def update_member(self, info):
        logger.info('update member: "%s"', info['name'])
        info['update'] = Utils.get_time_now()
        if 'img' in info:
            img = info['img']
            key = Utils.get_img_key(img)
            if key != None:
                img_file = key + '.png'
                img.save(self.img_folder+img_file, 'png')
                info['imgfile'] = img_file
            del info['img']

        is_new = True
        for i in range(len(self.data)):
            if self.is_same_member(self.data[i], info) == 'y':
                self.data[i] = self.merge_info(self.data[i], info)
                is_new = False
                break
        if is_new:
            logger.info("new member %s", info['name'])
            self.data.append(info)
        # write file
        self.write()

    def merge_info(self, info0, info):
        merged = copy.deepcopy(info0)
        for x in info:
            if not x in merged:
                merged[x] = info[x]
                continue
            if x in ['name', 'WeChatID', 'From', 'Region', 'Alias', 'Group Alias', 'Tag']:
                merged[x] = info[x]
                continue
            if x in ['update', 'imgfile']:
                continue
            if x in ['groups']:
                merged = self.merge_array(merged, info, x)
                continue
            logger.warning('not merged item: "%s"', x)
        return merged

    def merge_array(self, merged, info, key):
        for v in info[key]:
            if not v in merged[key]:
                merged[key].append(v)
        return merged

    def find_info(self, info):
        merged = None
        for i in range(len(self.data)):
            if self.data[i] == None:
                logger.error('data error')
            if info == None:
                logger.error('info error')
            if self.is_same_member(self.data[i], info) == 'y':
                merged = self.merge_info(self.data[i], info)
                return merged
        return info

    def is_same_member(self, m1, m2):
        key = 'WeChatID'
        r = self.check_key(key, m1, m2)
        if r != None:
            return r

        key = 'PicKey'
        r = self.check_key(key, m1, m2)
        if r != None:
            return r

        key = 'name'
        r = self.check_key(key, m1, m2)
        if r != None:
            return r

        logger.warning('no result for the same member')
        return False

    def check_key(self, key, m1, m2):
        if key in m1 and key in m2:
            if m1[key] == m2[key]:
                return 'y'
            else:
                return 'n'
        return None
