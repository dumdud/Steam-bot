import re

import alarms
import utils
import wiki
from log import LOG

class Commands:
    def __init__(self, user, text, client):

        self.user = user
        self.client = client

        # Parses the chat message into 2 parts. The command to be run and the argument sent to that command
        split_text = re.split(r"(^!?\w*) .*?", text, re.DOTALL)
        self.args = [item for item in split_text if item != ""]
        self.command = self.args.pop(0)

        LOG.info(f"Command:{self.command}")
        LOG.info(f"Args: {self.args}")
        LOG.info(f"{self.user.name}, Steam_id: {self.user.steam_id}")

        self.intro = f"""
        commands:
        !alarm [message] [time] - I will send you a reminder every day with message at the specified time. Time format in 
        !timer [message] [time] - A reminder will be sent after the given time
        !list - List all your alarms and timers
        !wiki [article], (game) - Search the wiki of the game you're currently playing. You can specify an article and optionally a game to search for.    
        """

        self.run()

    def run(self):

        self.command = self.command.lower()
        if self.command.startswith("!"):
            LOG.info(self.command)

            return getattr(
                self,
                "command_" + self.command[1:],
                lambda: self.user.send_message("Command does not exist"),
            )()

        # send intro
        if not self.command.startswith("!"):
            return self.user.send_message(self.get_intro())

    def get_intro(self):
        return self.intro

    def command_alarm(self):
        alarms.create_alarm(self)

    def command_timer(self):
        alarms.timer(self)

    def command_list(self):
        alarms.list_alarms(self)

    def command_wiki(self):
        playing = utils.get_game_name(self.client, self.user)
        args = []

        if self.args:
            args = [arg.strip(" ") for arg in self.args[0].split(",")]

        if playing and len(args) == 1:
            response = wiki.search_fanwiki(playing, args[0])

        if playing and len(args) > 1:
            response = wiki.search_fanwiki(args[1], args[0])

        if playing and not args:
            response = wiki.search_fanwiki(playing)

        if not playing and len(args) == 1:
            response = wiki.search_fanwiki(args[0])

        if not playing and len(args) > 1:
            response = wiki.search_fanwiki(args[1], args[0])

        if not playing and not args:
            response = "No game specified"

        self.user.send_message(response)

    def command_delete(self):
        alarms.delete(self)


class Admin(Commands):
    """
    Special commands for users in the admins file
    """

    def __init__(self, user, text, client):
        super().__init__(user, text, client)

        self.intro = f"""{self.intro}\n
            ***Admin Commands***
         !name [new name]- Change the bot's name
         !disconnect - turn off the bot
        """

    def command_name(self):
        self.client.change_status(player_name=self.args)
        self.user.send_message(f"Name changed to {self.args}")

    def command_disconnect(self):
        self.client.logout()
        raise SystemExit
