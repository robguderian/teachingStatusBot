import os
import time
import re
import json
from datetime import datetime

from slackclient import SlackClient

isPersonTeaching = "is\s+(?P<name>.+)\s+teaching"
compiledIPT = re.compile(isPersonTeaching)

whenIsPersonTeaching = "when\s+is\s+(?P<name>.+)\s+teaching"
compiledWIPT = re.compile(whenIsPersonTeaching)

def findUser(name, config):
    """
    Find a user based on a name.
    The name can be a first name, last name, both.
    Fuzzy match, score the names to the users. Return best matches.
    """
    # check perfect firstname/lastname matches
    # check perfect lastname matches
    # check perfect firstname matches
    # use hamming distance to fuzzy match.
    pass

def checkIsPersonTeaching(msg):
    matches = compiledIPT.search(msg.lower())
    if matches:
        name = matches.group('name')
        return name

def checkWhenIsPersonTeaching(msg):
    matches = compiledWIPT.search(msg.lower())
    if matches:
        name = matches.group('name')
        return name

def getWhenIsPersonTeaching(name, config):
    pass

def getIsPersonTeaching(name, config):
    """
    Check if a user is teaching. Return strings about users that matched
    the name filter.
    returns an array of strings.
    """
    # find user in file
    users = findUsers(name, config)
    currtime = datetime.now()
    milTime = currtime.hour * 100 + currtime.minute

def parse_bot_commands(slack_events, config):
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            message = event["text"]

            # note: order here is important
            name = checkWhenIsPersonTeaching(message)
            if name is not None:
                getWhenIsPersonTeaching(name, config)
            else:
                name = checkIsPersonTeaching(message)
                if name is not None:
                    getIsPersonTeaching(name, config)

if __name__ == "__main__":
    # read config file
    f = open("teaching_status_config.json")
    config = json.load(f)

    # instantiate Slack client
    slack_client = SlackClient(config['SLACK_BOT_TOKEN'])
    # wotdbot's user ID in Slack: value is assigned after the bot starts up
    userStatusbot_id = None

    # constants
    RTM_READ_DELAY = 1 # 1 second delay between reading from RTM

    if slack_client.rtm_connect(with_team_state=False):
        print("Status Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        userStatusbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            parse_bot_commands(slack_client.rtm_read(), config)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
