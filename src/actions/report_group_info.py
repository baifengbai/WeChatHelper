#
# Written By:   Weiping Liu
# Created:      Jun 28, 2021
#
import datetime, time
from helper.my_logging import *
from update_history import History
from settings.settings import Settings
from helper.utils import Utils
from actions.helper import Action_Helper

logger = getMyLogger(__name__)

class Action_ReportGroupInfo:
    def report_group_info(win, settings):
        logger.info('action: "report group info"')
        groups = settings['groups']
        for group in groups:
            logger.info('group: %s', group)
            group_info = Action_Helper.get_group_info(win, group)
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
            Action_ReportGroupInfo.report_info(win, settings['report_to'], group_info)

            if os.path.exists(filename) and 'date' in history:
                ds = history['date'].replace(' ', '_').replace(':', '')
                oldfile = settings['history_dir']+'h_'+group+'_'+ds+'.json'
                os.rename(filename, oldfile)

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
        Action_Helper.send_text(win, name, info)
