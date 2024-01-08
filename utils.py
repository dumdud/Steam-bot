from json import dump, loads
from json.decoder import JSONDecodeError
import time
import threading

from schedule import run_pending

from log import LOG


def create_json(filename):
    try:
        with open(f"{filename}.json", "x") as file:
            dump(dict(), file, indent=True)

        LOG.info(f"File {filename}.json created")

        return True

    except FileExistsError:
        return False


def read_json(filename):
    try:
        with open(f"{filename}.json", "r") as f:
            json_dict = loads(f.read())
            f.close()
        return json_dict

    except JSONDecodeError:
        return dict() #return empty dictionary


def is_json_empty(filename):
    return True if read_json(filename) == dict() else False


def write_json(key, value, filename):
    """
    Gets the content of json file, updates the values and rewrites them to the file

    :param key:
    :param value:
    """

    content = read_json(filename)
    try:
        content[str(key)].append(value)
    except KeyError:
        content.update({key: value})

    dump(content, open(f"{filename}.json", "w"), indent=True)


def get_game_name(client, user) -> str:
    """
    Gets the current game being played by the user

    :param client: SteamClient
    :param user: SteamUser
    :return: string
    """

    appid = user.get_ps("gameid", True)
    if not appid:
        return ""

    try:
        return client.get_product_info([appid])["apps"][appid]["common"]["name"]
    except KeyError:
        return ""


def run_continuously(interval=1):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):

            while not cease_continuous_run.is_set():
                run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()

    continuous_thread.start()
    return cease_continuous_run
