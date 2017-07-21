# PersonalAssistant
Create a personal assistant using the **SNIPS SDK** and voice control.

## Setup the Snips Platform

You are about to create your first personal assistant that can give you the weather forecast, the time travel between two cities or even how long it is to go to your first meeting tomorrow by cycle.

First of all, you will have to setup the Snips Voice Platform (check the [documentation](https://github.com/snipsco/snips-platform-documentation/wiki)).

Once you set your Raspberry up, [dowload](https://external-gateway.snips.ai/v1/registry/assistants/proj_SyWDILWV-/download?apiToken=Syb5DgPRQZHkGqDgwAXZH1Q5PxvCmZByVcwlP0QW) the assistant.

Zip the assistant folder and copy it on your raspberry using scp : 
```
$ scp Downloads/assistant.zip pi@rasperrypi.local:
```
SSH into your raspberry and install the assistant with 
```
(pi) $ snips-install-assistant assistant.zip
```
You can run `snips` or `snips-watch` (Take a look at the [video tutorial](https://youtu.be/NYnYSgIeKso?t=3m37s) to know how to use **snips-watch**)

## Run the program on a Mindstorm or a terminal
The following program is made to be run either on a [LEGO Mindstorm](http://www.ev3dev.org) (answers will be spoken) or a Terminal (answers will be displayed). You can also use the text to send it in speaker (using a Text to Speech).

### server.py 
is the main program you run on your device. It will receive the messages published on MQTT topics and chose the corresponding action. 

### hello.py
will returns a sentence that can be displayed on the terminal or be talked by the mindstorm. hello.py returns a short summary of your day (weather or events for exemple).

You have to modify a few lines :
- Your name (to personalise a little bit your assistant) 
- Replace your calendar Name and ID
- Get your API key on the [OpenWeather website](https://openweathermap.org/api) and copy it in the API_key variable.

###### Type of sentences you can say :
> Good morning !

> Hello Mindstorm.

(of course these are just exemples, feel free to ask differently)

### maps.py
will return a sentence that can contain time travel, according to a starting point, an ending point, or a Google event that contains an address.

You have to modify a few lines :
- Replace your calendar Name and ID
- Get your API key on the [Google Maps API website](https://developers.google.com/maps/?hl=fr) and copy it in the API_key variable.
- Replace your MAC address in the querystring variable

###### Type of sentences you can say :
> How long is the travel from Chicago to New York ?

> How long is it to go to my initial appointment on Monday ?

> How long will it take to go from Paris to my last meeting on Friday by car ? 

### quickstart.py 
will return a sentence that contains informations about your events on a Google Calendar.

You have to modify a few lines :
- Replace your calendar Name and ID
- Get your API key on the [Google Maps API website](https://developers.google.com/maps/?hl=fr) and copy it in the API_key variable.

###### Type of sentences you can say :
> What is my initial event tomorrow ? 

> How long is my last meeting on Wednesday ?

> When does the last event on Friday ends ? 

### ev3 / ev3_dummy
contains the scripts that makes the robot (or the Terminal) interact with you. Here you will find how to display a sentence or start a motor.
