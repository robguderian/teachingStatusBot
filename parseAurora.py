import re
import json

from bs4 import BeautifulSoup, UnicodeDammit


def toMilTime(hour, minute, ampm):
    startTime = int(hour)
    if startTime < 12 and ampm == 'pm':
        startTime += 12
    startTime = startTime * 100 + int(minute)
    return startTime

def convertTimes(strTime):
    # gets 11:30 am - 12:45 pm
    print strTime
    matches = timesRE.match( strTime)
    startTime = toMilTime(matches.group(1), matches.group(2),
                          matches.group(3))
    endTime = toMilTime(matches.group(4), matches.group(5),
                          matches.group(6))
    return (startTime, endTime)

def addCourse(data, email, coursename, days, fromTime, toTime):
    # check the array for this name
    if email is not None and email.a is not None:
        print email.a['href']
        matches = re.match("mailto:(\w+)\.(.+)@\w+", email.a['href'])
        firstname = matches.group(1)
        lastname = matches.group(2)

        addedToUser = False
        newCourse =  { 'from':fromTime,
                       'to':toTime,
                       'days':days,
                       'course':coursename}
        for u in data:
            if u['firstname'] == firstname and u['lastname'] == lastname:
                u['courses'].append( newCourse )
                addedToUser = True
        if not addedToUser:
            newuser = {'firstname': firstname,
                       'lastname': lastname,
                       'courses': []}
            newuser['courses'].append(newCourse)
            data.append(newuser)


database = []

html_doc = open('courses.html')
soup = BeautifulSoup(html_doc, 'html5lib')

# load up the table that has all the courses
# find finds the first datadisplaytable
course_table = soup.find("table", class_="datadisplaytable")

# ok. This format is hot garbage. So....
# keep state. Search through <tr>s evens are headers, odds are bodies.
isHeader = True

courseName = re.compile(".+ - \d+ - (\w\w\w\w \d\d\d\d) - (\w)\d\d")
timesRE= re.compile("(\d+):(\d+) (\w+) - (\d+):(\d+) (\w+)")
currCourse = ""
isCourse = False

# the dict to hold the prof name, and course data
for tr in soup.find_all('tr', recursive=True):
    #import pdb; pdb.set_trace()
    match = courseName.search(tr.get_text())
    if match is not None:
        print "Found course: " + tr.get_text()
        currCourse = match.group(1)
        isCourse = match.group(2) == "A"

    else:
        # only slurp in data if this is a course, not a lab
        # not all courses have a lecture slot table? Great.
        #import pdb; pdb.set_trace()
        lectureslot = tr.find("table", class_="datadisplaytable",
                recursive=True)
        if isCourse and lectureslot is not None:
            data = lectureslot.find_all('td')
            # Double check that this is, indeed, a lecture
            if data is not None and data[0].get_text() == "Lecture":
                print "Adding lecture: " + data[0].get_text()
                times = convertTimes(data[1].get_text())
                addCourse(database,
                          data[6],
                          currCourse,
                          data[2].get_text(),
                          times[0],
                          times[1])


writeFile = open('database.json', 'w')
j = json.dumps(database)
writeFile.write(j)
writeFile.close()
