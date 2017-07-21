from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
import math

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = '<Your Calendar Name'
CALENDAR_ID = '<Your Calendar ID>'

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def end_Of_Day(date):
    dateEnd = date + datetime.timedelta(days=1)
    dateEnd = datetime.datetime(dateEnd.year, dateEnd.month, dateEnd.day)
    return dateEnd

def date(slots):
    try:
        beg = str_To_Date(slots['date']['value']['value']['from'])
        end = str_To_Date(slots['date']['value']['value']['to'])
    except:
        try:
            beg = str_To_Date(slots['date']['value']['value']['value'])
            end = end_Of_Day(beg)
        except:
            beg = datetime.datetime.utcnow()
            end = end_Of_Day(beg)

    return {'beggin': beg, 'end': end}

def str_To_Date(strDate):
    return datetime.datetime(int(strDate[:4]), int(strDate[5:7]), int(strDate[8:10]), int(strDate[11:13]), int(strDate[14:16]), int(strDate[17:19]))

def duration(startDate, endDate):
    delay = endDate-startDate
    days = delay.days
    hours = math.floor(delay.seconds/(60*60))
    minutes = math.floor((delay.seconds-60*60*hours)/60)
    talk = ""
    if days != 0:
        talk += str(days)
        if days==1:
            talk += " day "
        else:
            talk += " days "
    if hours != 0:
        talk += str(hours)
        if hours==1:
            talk += " hour "
        else:
            talk += " hours "
    if minutes != 0:
        talk += str(minutes)
        if minutes==1:
            talk += " minute "
        else:
            talk += " minutes "
    return talk


def set_talk(slots):
    """Shows basic usage of the Google Calendar API.
    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    beg = date(slots)['beggin']
    end = date(slots)['end']

    eventsResult = service.events().list(
        calendarId=CALENDAR_ID, timeMin=beg.isoformat()+'Z', timeMax=end.isoformat()+'Z', singleEvents=True, # 'Z' indicates UTC time
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    try: 
        order = slots['order'].lower()
        try: 
            feature = slots['feature'].lower()
        except: 
            feature = 'none'
    except:
        order = 'none'

    if (order == "how many"):
        if len(events) :
            talk = "You have " + str(len(events)) + " events."
        else :
            talk = "There is no upcoming events, enjoy your day !"
    elif (order != 'none'):  
        if (order == "initial" or order == "next"):
            index = 0
        elif (order == "last"):
            index = len(events)-1

        talk = "Your " + order + " event "
        if(feature == 'start'):
            talk = talk + "starts at " + str(str_To_Date(events[index]['start']['dateTime']).hour) + ":" + str(str_To_Date(events[index]['start']['dateTime']).minute)
        elif(feature == 'end'):
            talk = talk + "ends at " + str(str_To_Date(events[index]['end']['dateTime']).hour) + ":" + str(str_To_Date(events[index]['end']['dateTime']).minute)
        elif(feature == 'where'):
            try:
                talk = talk + "is at " + events[index]['location']
            except:
                talk += "has no address."

        elif(feature == 'how long'):
            talk = talk + "lasts " + duration(str_To_Date(events[index]['start']['dateTime']),str_To_Date(events[index]['end']['dateTime']))
        else: 
            if len(events)==0 :
                talk = "There is no upcoming events, enjoy your day !"
            else:
                talk = talk + "is " + events[index]['summary'] + " at " + str(str_To_Date(events[index]['start']['dateTime']).hour) + ":" + str(str_To_Date(events[index]['start']['dateTime']).minute)

    else: 
        if len(events):
            talk = "You have " + str(len(events)) + " events that day : " 
            for event in events:
                talk = talk + event['summary'] + " at " + str(str_To_Date(event['start']['dateTime']).hour) + ":" + str(str_To_Date(event['start']['dateTime']).minute) + ", "
        else:
            talk = "There is no upcoming events, enjoy your day !"

    return talk