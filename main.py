import steam.monkey
steam.monkey.patch_minimal()

import getpass

from steam.client import SteamClient
from steam.enums import EResult

import patches
import commands
from alarms import load_alarms, schedule_test
from log import LOG
from utils import create_json, is_json_empty, read_json, run_continuously, write_json

create_json("alarms")
create_json("credentials")

if is_json_empty("credentials"):
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    CREDS = {"username": username, "password": password}

    for key, value in CREDS.items():
        write_json(key, value, "credentials")

else:

    CREDS = read_json("credentials")

ADMINS = [int(admin) for admin in open("admins.txt")]
continuous_run = run_continuously(2)
client = SteamClient()
client.set_credential_location("./")


@client.friends.on("friend_invite")
def handle_friend_request(user):
    client.friends.add(user.steam_id)
    LOG.info(f"Steam friend added: {user.name}.")

@client.on("chat_message")
def handle_message(user, text):
    if user.steam_id in ADMINS:
        commands.Admin(user, text, client)
        return
    commands.Commands(user, text, client)

@client.on("connected")
def handle_connected():
    LOG.info("Connected to %s", client.current_server_addr)

@client.on("reconnect")
def handle_reconnect(delay):
    LOG.info("Reconnect in %ds...", delay)

@client.on("disconnected")
def handle_disconnect():
    LOG.info("Disconnected.")
    login()
    # if client.relogin_available:
    #     LOG.info("Reconnecting...")
    #     client.reconnect(maxdelay=30)

def login():
    if not client.get_sentry(CREDS["username"]):
            result = client.cli_login(**CREDS)
            client.store_sentry(CREDS["username"])
    else:
        result = client.login(**CREDS)            

    while result == EResult.TryAnotherCM:
        result = client.login(**CREDS)

    return result

def main():
    try:
        result = login()

        if result != EResult.OK:
            LOG.error(repr(result))
            continuous_run.set()
            raise SystemExit

        load_alarms(client)
        client.run_forever()

    except Exception as e:
        continuous_run.set()
        print(e)

    except KeyboardInterrupt:
        continuous_run.set()

        if client.connected:
            client.logout()
            raise SystemExit


if __name__ == "__main__":
    main()
