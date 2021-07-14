#
# Written By:   Weiping Liu
# Created:      Jun 28, 2021
#
import datetime, time
from helper.my_logging import *
from settings.settings import Settings
from ui.chats import UI_Chats
from ui.chat_info import UI_ChatInfo
from ui.comm import UI_Comm

logger = getMyLogger(__name__)

class Action_InviteFriends:
    def invite_friends(win, settings):
        logger.info('action: "invite_friends"')
        group = settings['from_group']
        if UI_Chats.chat_to(win, group) != True:
            return

        # default, not dry run
        dryrun = False
        if 'dryrun' in settings:
            dryrun = settings['dryrun']

        text = settings['invite_text']

        for name in settings['friends']:
            Action_InviteFriends.invite(win, name, text, dryrun)
            # WeChat does not allow a lot operation in short time
            # delay enough time
            time.sleep(10)

    def slow_down_click(control, center=True, outline=True):
        time.sleep(5)
        UI_Comm.click_control(control, center, outline)

    def invite(win, name, text, dryrun):
        logger.info('invite "%s"', name)
        pwin = UI_ChatInfo.open_chat_info(win)
        if pwin == None:
            return
        UI_ChatInfo.view_more(pwin)

        rect = pwin.rectangle()
        list = pwin.window(title='Members', control_type='List')
        members = list.children(control_type='ListItem')
        for index in range(len(members)):
            # find the name
            if members[index].window_text() != name:
                continue

            # scroll into view
            while members[index].rectangle().bottom > rect.bottom:
                UI_Comm.mouse_scroll(pwin, -1)     # scroll content up
                # time.sleep(0.1)

            Action_InviteFriends.invite_member(win, members[index], text, dryrun)
            break
        UI_ChatInfo.close_chat_info(win)

    # return None for failed invite or
    # msg text for invited
    def invite_member(win, member, text, dryrun):
        name = member.window_text()
        member.draw_outline()
        # click the member icon to open
        Action_InviteFriends.slow_down_click(member)
        pane = win.child_window(title='WeChat', control_type='Pane')
        if not pane.exists():
            logger.warning('could not open friend "%s"', name)
            pane.type_keys('{ESC}')
            return

        # if member is already a friend, WeChat ID will be shown
        # otherwise, 'Add as friend' button should be there.
        add = pane.child_window(title='Add as friend', control_type='Button')
        if not add.exists():
            if pane.child_window(title="WeChat ID: ", control_type="Text").exists():
                logger.info('"%s" is already friend', name)
            else:
                logger.warning('could not add friend "%s"', name)
            pane.type_keys('{ESC}')
            return

        Action_InviteFriends.slow_down_click(add, True, False)
        Action_InviteFriends.add_friend(win, text, dryrun)

    def add_friend(win, text, dryrun):
        retry = 3
        while retry > 0:
            request = win.child_window(title='WeChat', control_type='Window')
            if request.exists():
                break
            retry -= 1
            time.sleep(1)   # wait popup show up

        if not request.exists():
            logger.info('did not see request dialog')
            return

        if not request.child_window(title='Add Friends', control_type='Text').exists():
            if request.child_window(title='Tip', control_type='Text').exists():
                Action_InviteFriends.confirm_sent(win)
                return

        edit = request.child_window(control_type='Edit', found_index=0)
        Action_InviteFriends.slow_down_click(edit)
        edit.type_keys('^a{BACKSPACE}')
        UI_Comm.send_text(edit, text, False)
        msg = edit.get_value()
        # close
        if dryrun:
            title = 'Cancel'
        else:
            title = 'OK'
        button = request.child_window(title=title, control_type='Button')
        button.draw_outline()
        Action_InviteFriends.slow_down_click(button, True, False)
        Action_InviteFriends.confirm_sent(win)
        return

    def confirm_sent(win):
        retry = 3
        while retry > 0:
            retry -= 1
            tip = win.child_window(title='WeChat', control_type='Window')
            if not tip.exists():
                continue
            if not tip.child_window(title="Tip", control_type="Text").exists():
                continue
            button = tip.child_window(title='OK', control_type='Button')
            if not button.exists():
                continue
            button.draw_outline()
            Action_InviteFriends.slow_down_click(button, True, False)
            logger.info('confirmed sent')
            return
        logger.warning('no confirm sent')
        return

'''
-- already friend
child_window(title="WeChat", control_type="Pane")
   |    |    |    |    |    | child_window(title="刘维平", control_type="Edit")
   |    |    |    |    |    | child_window(title="WeChat ID: ", control_type="Text")
   |    |    |    |    |    | child_window(title="ayixiangke", control_type="Edit")
   |    |    |    | child_window(title="刘维平", control_type="Button")
   |    |    |    |    | child_window(title="Region", control_type="Text")
   |    |    |    |    | child_window(title="Linfen Shanxi ", control_type="Edit")
   |    |    |    | child_window(title="Share Contact Card", control_type="Button")
   |    |    |    | child_window(title="Messages", control_type="Button")

-- add friend
child_window(title="WeChat", control_type="Pane")
   |    |    |    |    |    | child_window(title="briadmin", control_type="Edit")
   |    |    |    | child_window(title="briadmin", control_type="Button")
   |    |    |    | child_window(title="Add as friend", control_type="Button")

-- request window
child_window(title="WeChat", control_type="Window")
   |    |    | child_window(title="Add Friends", control_type="Text")
   |    |    | child_window(title="Close", control_type="Button")
   |    |    | child_window(title="I'm 刘维平", control_type="Edit")
   |    | child_window(title="Must send a friend request and wait until it's accepted.", control_type="Edit")
   |    |    | child_window(title="OK", control_type="Button")
   |    |    | child_window(title="Cancel", control_type="Button")

-- tip Pane
child_window(title="WeChat", control_type="Window")
   |    |    |    | child_window(title="Tip", control_type="Text")
   |    |    |    | child_window(title="Close", control_type="Button")
   |    |    |    | child_window(title="Sent", control_type="Edit")
   |    |    |    | child_window(title="OK", control_type="Button")

'''
