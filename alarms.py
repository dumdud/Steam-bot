import datetime
import re
from json import dump

import schedule

import utils
from log import LOG


def schedule_test(client, id_list):

    current = datetime.datetime.now() + datetime.timedelta(seconds=6)

    sched_time = f"{current.hour}:{current.minute}:{current.second}"

    LOG.info(sched_time)

    for id in id_list:

        schedule.every().day.at(sched_time).do(
            client.get_user_and_send_message, id, "test"
        )
    


def load_alarms(client):

    data = utils.read_json("alarms")
    if not data:

        LOG.info("No alarms to load")
        return

    try:
        for steam_id in data:
            for DICT in data[steam_id]:
                message, time, cancel, enabled = DICT.values()

                if enabled:
                    LOG.info(f"Loading alarm for {steam_id} at {time}")

                    schedule.every().day.at(time).do(
                        client.get_user_and_send_message, steam_id, message, cancel
                    ).tag(steam_id)
        LOG.info("Alarms loaded")

    except ValueError as e:

        LOG.info(e)


def list_alarms(Command):
    data = utils.read_json("alarms.json")
    alarm_list = "You have the following alarms:\n"

    try:
        for d in data[str(Command.user.steam_id)]:
            message, msg_time, _, enabled = d.values()
            if enabled:
                alarm_list = alarm_list + \
                    f'Alarm:"{message}" at "{msg_time}"\n'

    except KeyError:
        alarm_list = "You have no alarms\n"

    Command.user.send_message(alarm_list)


def create_alarm(bot):
    try:
        message, msg_time, once = re.search(
            r"(?<=!alarm) (.*) ([0-1]?[0-9]:[0-5][0-9]|[2][0-3]:[0-5][0-9])(\s?once)?",
            bot.text,
        ).groups()

        if once is True:
            once = True
            alarm_dict = {
                "message": message,
                "time": msg_time,
                "once": True,
                "enabled": True,
            }

        else:
            once = False
            alarm_dict = {
                "message": message,
                "time": msg_time,
                "once": False,
                "enabled": True,
            }

        utils.write_json(int(bot.user.steam_id), alarm_dict, "alarms")

        LOG.info("-" * 60)

        LOG.info(
            f'\nmessage: {alarm_dict["message"]}\nscheduled time: {alarm_dict["time"]}'
        )

        bot.user.send_message(f'scheduled a reminder for {alarm_dict["time"]}')

        schedule.every().day.at(msg_time).do(
            bot.user.send_message, message, once=once
        ).tag(f"{bot.user.steam_id}")

    except AttributeError:

        utils.send_message(bot.user, "Parameters Missing or Invalid")


def timer(bot):

    try:

        # message, formated_time = re.search(

        #     r"\s?(.*?)\s?([0-9]?[0-9]:[0-5][0-9]|\d{1,3})",

        #     str(bot.args),

        # ).groups()

        message, num1, num2, num3 = re.search(
            # Groups an optional string at the start followed by up to 3 groups of with 1-3 digits each separated by a ":" character.
            r"(.*?)\s?(?:(\d{1,3})(?:\:(\d{1,3}))?(?:\:(\d{1,3}))?)",
            str(bot.args[0]),
        ).groups()

        if not message:
            message = "done"

        if not num2:
            total_minutes = int(num1)
        else:
            total_minutes = int(num2) + (int(num1) * 60)

        LOG.info(total_minutes)

        # if ":" in formated_time:

        #     hours, minutes = [int(time) for time in formated_time.split(":")]

        #     total_minutes = minutes

        #     for _ in range(hours):

        #         total_minutes += 60

        # else:

        #     total_minutes = int(formated_time)

        #     formated_time = (

        #         f"{prefix_zero((total_minutes / 60))}:{prefix_zero((total_minutes % 60))}"

        #     )

        LOG.info("-" * 60)

        LOG.info(f'Message: "{message}" scheduled in: {total_minutes} minutes')

        bot.user.send_message(
            f"scheduled a reminder in {total_minutes} minutes")

        schedule.every(total_minutes).minutes.do(
            bot.user.send_message, message, once=True
        )

    except AttributeError as e:

        LOG.info(e)

        bot.user.send_message("Parameters Missing or Invalid")


def delete(bot):
    utils.send_message(
        bot.user,
        "This will delete all of your alarms and reminders. Type !confirm to accept.",
    )

    resp = bot.client.wait_event("chat_message", timeout=5)

    if resp is None:

        utils.send_message(bot.user, "Request timed out.")

    elif resp[1] == "!confirm":

        schedule.clear(f"{bot.user.steam_id}")

        alarms = utils.read_json("alarms")

        alarms.pop(str(bot.user.steam_id))

        with open("alarms.json", "w") as file:

            dump(alarms, file)

        utils.send_message(bot.user, "Schedule cleared.")
