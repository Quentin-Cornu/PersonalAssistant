from __future__ import print_function
import httplib2
import os

import googlemaps
import requests
import json
import quickstart

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

API_KEY = '<Your Google API key>'
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = '<Your Calendar name>'
CALENDAR_ID = '<Your Calendar ID>'


def geolocate():
	url = "https://www.googleapis.com/geolocation/v1/geolocate"
	querystring = {"key":"<Your Google API key>"}

	payload = "{\n  \"macAddress\": \"<your MAC address>\"\n}"
	headers = {
	    'content-type': "application/json",
	    'cache-control': "no-cache"
	    }

	response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
	return(response.text)

def create_http(origins, destinations, mode=""):
	string = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
	string += 'origins=' + origins + '&'
	string += 'destinations=' + destinations + '&'
	if mode != "" :
		string += 'mode=' + mode + '&'
	string += 'key=' + API_KEY
	return string

def get_distance(origin, destination, mode=""):
	url = create_http(origin, destination, mode)
	# print(url)
	r = requests.get(url).json()
	try:
		if (r['status'] == 'OK'):
			distance = r['rows'][0]['elements'][0]['duration']['text']
		else:
			distance = "-1"
		return distance
	except:
		return "-1"

def distance_to_tab(distance): 
	if distance == "-1" :
		return {'hours': -1, 'mins': -1}
	else:
		if distance.find("hours")==-1 :
			distance = distance.replace('mins', '')
			mins = int(distance)
			return {'hours': 0, 'mins': mins}
		
		elif distance.find("days")!=-1 :
			return {'hours': -1, 'mins': -1}

		else :
			distance = distance.replace('hours ', '')
			distance = distance.replace('mins', '')
			esp = ' '
			if distance[0]!='0':
				hours = int(distance[:distance.find(esp)]) 
				mins = int(distance[distance.find(esp):]) 
			else:
				hours = 0
				mins = int(distance) 
			return {'hours': hours, 'mins': mins}

def set_talk(slots):

	try:
		origin = slots['CityOrigin']
	except:
		location = json.loads(geolocate())
		lat = location['location']['lat']
		lng = location['location']['lng']
		origin = str(lat) + ',' + str(lng)

	try:
		destination = slots['CityDestination']
	except:
		try:
			credentials = quickstart.get_credentials()
			http = credentials.authorize(httplib2.Http())
			service = discovery.build('calendar', 'v3', http=http)
			try:
				beg = str_To_Date(slots['date']['value']['value']['from'])
				end = str_To_Date(slots['date']['value']['value']['to'])
			except:
				try:
					beg = quickstart.str_To_Date(slots['dateEvent']['value'])
					end = quickstart.end_Of_Day(beg)
				except:
					beg = datetime.datetime.utcnow()
					end = quickstart.end_Of_Day(beg)
					
			eventsResult = service.events().list(
				calendarId=CALENDAR_ID, timeMin=beg.isoformat()+'Z', timeMax=end.isoformat()+'Z', singleEvents=True, # 'Z' indicates UTC time
	        	orderBy='startTime').execute()
			events = eventsResult.get('items', [])
			try:
				order = slots['order'].lower()
			except:
				order = 'initial'
			if (order == "initial" or order == "next"):
				index = 0
			else:
				index = len(events)-1
			if (len(events)==0) :
				destination = ""
			else:
				destination = events[index]['location']
		except:
			destination = ""

	try:
		mode = slots['TravelMode']
		distance = get_distance(origin, destination, mode)
	except:
		distance = get_distance(origin, destination)

	if distance_to_tab(distance)['hours']==-1 or distance_to_tab(distance)['mins']==-1 :
		talk = "Sorry, I can't find any way to go there."
	else :
		hours = distance_to_tab(distance)['hours']
		mins = distance_to_tab(distance)['mins']

		talk = "It will take you "
		if hours != 0 :
			talk += str(hours) + " hours and "
		talk += str(mins) + " minutes to go to " + destination

	return talk 