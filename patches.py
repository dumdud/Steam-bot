from time import sleep
from steam.enums import EChatEntryType
from steam.enums.emsg import EMsg
from steam.client.user import SteamUser, MsgProto
from steam.client import SteamClient

from schedule import CancelJob, Scheduler
from log import LOG

# "extends" SteamUser.send_message method with bbcode support and logging


def send_message_bbcode(self, message, cancel=False):
    try:
        LOG.info("-" * 60)
        LOG.info(f'Answer sent to {self.name}: "{message}"')

        if self._steam.chat_mode == 2:
            self._steam.send_um("FriendMessages.SendMessage#1", {
                'steamid': self.steam_id,
                'message': message,
                'chat_entry_type': EChatEntryType.ChatMsg,
                "contains_bbcode": True,
            })
        else:
            self._steam.send(MsgProto(EMsg.ClientFriendMsg), {
                'steamid': self.steam_id,
                'chat_entry_type': EChatEntryType.ChatMsg,
                'message': message.encode('utf8'),
            })
        if cancel:
            return CancelJob

    except Exception as e:
        LOG.info(e)


def get_user_and_send_message(self, steamid, message, cancel=False):

    user = self.get_user(steamid)
    user.send_message(message, cancel)

def run_pending(self):
    runnable_jobs = (job for job in self.jobs if job.should_run)
    for job in sorted(runnable_jobs):
        self._run_job(job)

Scheduler.run_pending = run_pending
SteamUser.send_message = send_message_bbcode

SteamClient.get_user_and_send_message = get_user_and_send_message
