import os, sys
import time
import re
import json
from datetime import datetime

from slackclient import SlackClient

# is x teaching
isPersonTeaching = "is\s+(?P<name>.+)\s+teaching"
compiledIPT = re.compile(isPersonTeaching)

#does x teach today
doesPersonTeachToday = "does\s+(?P<name>.+)\s+teach today"
compiledDPTT = re.compile(doesPersonTeachToday)

# when is x teaching
whenIsPersonTeaching = "when\s+is\s+(?P<name>.+)\s+teaching"
compiledWIPT = re.compile(whenIsPersonTeaching)

# when does x teach
whenDoesPersonTeach = "when\s+does\s+(?P<name>.+)\s+teach"
compiledWDPT = re.compile(whenDoesPersonTeach)
whatDoesPersonTeach = "what\s+does\s+(?P<name>.+)\s+teach"
compiledWhatDPT = re.compile(whatDoesPersonTeach)

# who is teaching xxxx, who is teaching comp xxxx
whoIsTeachingCourse = "who\s+is\s+teaching\s+(?:comp)?\s*(?P<course>\d\d\d\d)"
compiledWITC = re.compile(whoIsTeachingCourse)
whosTeachingCourse = "who's\s+teaching\s+(?:comp)?\s*(?P<course>\d\d\d\d)"
compiledWTC = re.compile(whosTeachingCourse)
whoTeachesCourse = "who\s+teaches\s+(?:comp)?\s*(?P<course>\d\d\d\d)"
compiledWTC2 = re.compile(whoTeachesCourse)

datemap = [
           'M',
           'T',
           'W',
           'R',
           'F']



def nameMatch(name, database):
    """
    Passes back a list of matched users
    none if no matches
    """
    firstNameMatches = []
    lastNameMatches = []
    fullNameMatches = []
    for u in database:
        # using in, so things like tremblay will match
        # tremblay-savard
        count = 0
        for n in name.split():
            if n.lower() in u['lastname'].lower():
                lastNameMatches.append(u)
                count += 1
            if n.lower() in u['firstname'].lower():
                firstNameMatches.append(u)
                count += 1
            if count >= 2:
                # matched one, just matched another
                # will be a bug if we start adding middle names...
                fullNameMatches.append(u)
    if len(fullNameMatches) > 0:
        return fullNameMatches
    if len(lastNameMatches) > 0:
        return lastNameMatches
    if len(firstNameMatches) > 0:
        return firstNameMatches
    return None

def findUsers(name, database):
    """
    Find a user based on a name.
    The name can be a first name, last name, both.
    Fuzzy match, score the names to the users. Return best matches.
    returns a list
    """
    # check perfect firstname/lastname matches
    # check perfect lastname matches
    # check perfect firstname matches
    matches = nameMatch(name, database)
    if matches is not None:
        return matches
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

def checkWhenDoesPersonTeach(msg):
    matches = compiledWDPT.search(msg.lower())
    if matches:
        name = matches.group('name')
        return name
    matches = compiledWhatDPT.search(msg.lower())
    if matches:
        name = matches.group('name')
        return name


def checkWhoIsTeachingCourse(msg):
    matches = compiledWITC.search(msg.lower())
    if matches:
        name = matches.group('course')
        return name
    matches = compiledWTC.search(msg.lower())
    if matches:
        name = matches.group('course')
        return name
    matches = compiledWTC2.search(msg.lower())
    if matches:
        name = matches.group('course')
        return name

def getWhenIsPersonTeaching(name,database):
    users = findUsers(name, database)
    if users is None:
        return []

    statuses = []
    currtime = datetime.now()
    milTime = currtime.hour * 100 + currtime.minute

    weekday = currtime.weekday()  # 0-6...
    for u in users:
        doneTeaching = True
        classToday = False
        courses = []
        for c in u['courses']:
            if datemap[weekday] in c['days']:
                classToday = True
                if milTime <= c['to'] :
                    doneTeaching = False
                    courses.append({'key':c['to'],
                        'text': "{} at {}:{:02d}".format(c['course'],
                                c['from']//100, c['from']%100)})
        # sort the array by time
        courses = sorted(courses, key = lambda course: course['key'])
        coursesStr = [c['text'] for c in courses]
        if not classToday:
            statuses.append("{} {} does not have class today.".format(
                u['firstname'], u['lastname']))
        elif doneTeaching:
            statuses.append("{} {} is done teaching for the day.".format(
                u['firstname'], u['lastname']))
        else:
            statuses.append("{} {} is teaching {}.".format(
                u['firstname'], u['lastname'], 'and '.join(coursesStr)))

    return statuses

def getIsPersonTeaching(name, database):
    """
    Check if a user is teaching. Return strings about users that matched
    the name filter.
    returns an array of strings.
    """
    # find user in file
    users = findUsers(name, database)
    if users is None:
        return []

    statuses = []
    currtime = datetime.now()
    milTime = currtime.hour * 100 + currtime.minute
    for u in users:
        isTeaching = False
        for c in u['courses']:
            if c['from'] <= milTime and milTime <= c['to']:
                isTeaching = True
        if isTeaching:
            statuses.append("Yes, {} {} is currently teaching.".format(
                u['firstname'], u['lastname']))
        else:
            statuses.append("No, {} {} is not currently teaching.".format(
                u['firstname'], u['lastname']))

    return statuses

def checkDoesPersonTeachToday(msg):
    matches = compiledDPTT.search(msg.lower())
    if matches:
        name = matches.group("name")
        return name

def getDoesPersonTeachToday(name, database):
    users = findUsers(name,database)
    if users is None:
        return []

    currtime = datetime.now()
    milTime = currtime.hour * 100 + currtime.minute

    weekday = currtime.weekday()  # 0-6...

    statuses = []
    for u in users:
        classToday = False
        courses = []
        for c in u['courses']:
            if datemap[weekday] in c['days']:
                classToday = True
                doneTeaching = False
                courses.append({'key': c['to'],
                    'text': "{} from {}:{:02d} to {}:{:02d}".format(c['course'],
                        c['from']//100, c['from']%100,
                        c['to']//100, c['to']%100) })
        # sort the array by time
        courses = sorted(courses, key = lambda c: c['key'])
        coursesStr = [c['text'] for c in courses]
        if not classToday:
            statuses.append("{} {} does not have class today.".format(
                u['firstname'], u['lastname']))
        else:
            statuses.append("{} {} teaches {} today.".format(
                u['firstname'], u['lastname'], ', and '.join(coursesStr)))

    return statuses

def getWhenDoesPersonTeach(name, database):
    """
    Print when someone teaches
    Bug? If the user doesn't exist, it returns nothing. So, a prof
    that has no courses this term will not have a response.
    We'd need to maintain a list of all profs to remedy this
    """
    users = findUsers(name,database)
    if users is None:
        return []

    currtime = datetime.now()
    milTime = currtime.hour * 100 + currtime.minute

    weekday = currtime.weekday()  # 0-6...

    statuses = []
    for u in users:
        courses = []
        for c in u['courses']:
            courses.append({'key': c['to'],
                'text': "{} from {}:{:02d} to {}:{:02d} {}".format(c['course'],
                    c['from']//100, c['from']%100,
                    c['to']//100, c['to']%100, c['days']) })
        # sort the array by time
        courses = sorted(courses, key = lambda c: c['key'])
        coursesStr = [c['text'] for c in courses]
        statuses.append("{} {} teaches {}.".format(
            u['firstname'], u['lastname'], ', and '.join(coursesStr)))

    return statuses

def getWhoIsTeachingCourse(name, database):
    """
    Find all the people teaching a course. Return a list of names
    """
    profs = []

    for u in database:
        for c in u['courses']:
            if c['course'] == "COMP {}".format(name):
                profs.append("{} {}".format(u['firstname'], u['lastname']))
    return profs



def reply(slack_client, channel, message):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=message
    )


def parse_bot_commands(slack_client, slack_events, config, database):
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            message = event["text"]

            # note: order here is important, 
            # is person teaching must run before when is person teaching
            # TODO - this needs to be refactored in the worst way
            name = checkWhenIsPersonTeaching(message)
            statuses = None
            if name is not None:
                statuses = getWhenIsPersonTeaching(name, database)
            else:
                name = checkIsPersonTeaching(message)
                if name is not None:
                    statuses = getIsPersonTeaching(name, database)
            name = checkDoesPersonTeachToday(message)
            if name is not None:
                statuses = getDoesPersonTeachToday(name, database)
            name = checkWhenDoesPersonTeach(message)
            if name is not None:
                statuses = getWhenDoesPersonTeach(name, database)
            if statuses is not None:
                for s in statuses:
                    reply(slack_client, event['channel'], s)

            # phase 2, who is teaching a course
            courseName = checkWhoIsTeachingCourse(message)
            profs = []
            if courseName is not None:
                profs = getWhoIsTeachingCourse(courseName, database)
                if len(profs) > 0:
                    if len(profs) > 1:
                        profs[-1] = " and {}".format(profs[-1])
                        profList = ', '.join(profs)
                        profStr = "{} are teaching COMP {}.".format(profList,
                            courseName)
                    else:
                        profStr = "{} is teaching COMP {}.".format(profs[0],
                            courseName)
                    reply(slack_client, event['channel'], profStr)
                else:
                    noProf=("There is no one teaching COMP {} " +
                           "currently.").format(courseName)
                    reply(slack_client, event['channel'], noProf)



if __name__ == "__main__":
    # read config file
    f = open("teaching_status_config.json")
    config = json.load(f)
    f = open("database.json")
    database = json.load(f)

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
            try:
                message = slack_client.rtm_read()
            except:
                try:
                    print "Error: lost connection, trying to re-establish"
                    slack_client.rtm_connect(with_team_state=False)
                    userStatusbot_id = slack_client.api_call("auth.test")["user_id"]
                except:
                    message = ""
                    e = sys.exc_info()[0]
                    print "Error: " + str(e)

            parse_bot_commands(slack_client, message, config, database)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
