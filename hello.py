from __future__ import print_function
import httplib2
import os

import weather 
import quickstart as calendar
import maps
import json
from pyowm import OWM
import datetime

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import math

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = '<Your Calendar Name>'
CALENDAR_ID = '<Your Calendar ID>'

def set_talk():
	nom = "<Your name>"

	location = json.loads(maps.geolocate())
	lat = int(location['location']['lat'])
	lng = int(location['location']['lng'])

	API_key = '<Your API key>' # create an API key on https://openweathermap.org/api 
	owm = OWM(API_key)

	obs = owm.weather_at_coords(lat, lng)
	w = obs.get_weather()
	l = obs.get_location()

	talk = "Hello " + nom + ", the weather is currently " + w.get_detailed_status() + " and the temperature is " + str(int(round(w.get_temperature(unit='celsius')['temp']))) + " degrees. "

	slots = b'{"input":"what is my next meeting today","intent":{"intentName":"user_Hk9PxP07b__CalendarIntent","probability":0.34624666},"slots":[{"value":{"kind":"Custom","value":"first"},"rawValue":"next","range":{"start":11,"end":15},"entity":"order2","slotName":"PrecisionDate2"},{"value":{"kind":"Builtin","value":{"kind":"Time","value":{"kind":"InstantTime","value":{"value":"2017-07-10 00:00:00 +00:00","grain":"Day","precision":"Exact"}}}},"rawValue":"today","range":{"start":24,"end":29},"entity":"snips/datetime","slotName":"DateEvent"}]}'
	event_talk = calendar.set_talk(slots)
	talk = talk + event_talk

	credentials = calendar.get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('calendar', 'v3', http=http)

	beg = calendar.date(slots)['beggin']
	end = calendar.date(slots)['end']

	eventsResult = service.events().list(
        calendarId=CALENDAR_ID, timeMin=beg.isoformat()+'Z', timeMax=end.isoformat()+'Z', singleEvents=True, # 'Z' indicates UTC time
        orderBy='startTime').execute()
	events = eventsResult.get('items', [])

	try :
		address = events[0]['location']
		new_slot = '{"input":"","intent":{"intentName":"user_Hk9PxP07b__DistanceIntent","probability":0.8132438},"slots":[{"rawValue":' + str(address) + ',"value":{"kind":"Custom","value":"lille"},"range":{"start":21,"end":26},"entity":"snips/default--CityDestination","slotName":"CityDestination"}]}'
		talk = talk + maps.set_talk(slots)
	except:
		talk = talk 
	
	return talk 