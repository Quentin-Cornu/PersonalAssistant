#!/usr/bin/env python3
# encoding: utf-8

import argparse
import json
import os
import time
import threading
import paho.mqtt.client as mqtt
import weather 
import quickstart as calendar
import maps
import hello

if str(os.environ['USER']) == 'robot':
    import ev3
else:
    import ev3_dummy as ev3

class ThreadHandler:

   def __init__(self):
        self.thread_pool = []
        self.run_events = []

   def run(self, target, args=()):
        run_event = threading.Event()
        run_event.set()
        t = threading.Thread(target=target, args=args + (run_event, ))
        self.thread_pool.append(t)
        self.run_events.append(run_event)
        t.start()

   def start_run_loop(self):
        try:
            while 1:
                time.sleep(.1)
        except KeyboardInterrupt:
            self.stop()

   def stop(self):
        for run_event in self.run_events:
            run_event.clear()

        for t in self.thread_pool:
            t.join()

class Server:

    def __init__(self, mqtt_hostname, mqtt_port, mqtt_topic):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.mqtt_hostname = mqtt_hostname
        self.mqtt_port = mqtt_port
        self.mqtt_topic = mqtt_topic

        self.threading = ThreadHandler()
    
    def log(self, msg):  
        print("[SERVER] " + msg)
    
    def log_mqtt(self, msg): 
        print("[MQTT] " + msg)

    def start(self):
        self.threading.run(target=self.start_blocking)
        self.threading.start_run_loop()
    
    def start_blocking(self, run_event):
        self.log_mqtt("Connecting to " + self.mqtt_hostname + " on port " + str(self.mqtt_port))
        while True and run_event.is_set():
            self.log_mqtt("Trying to connect to " + str(self.mqtt_hostname))
            self.client.connect(self.mqtt_hostname, self.mqtt_port, 60)
            break
        self.client.subscribe(self.mqtt_topic, 0)
        self.log_mqtt("Subscribed to topic " + self.mqtt_topic)
        while run_event.is_set():
            self.client.loop()
 
    def on_connect(self, client, userdata, flags, rc):
        self.log_mqtt("Connected with result code " + str(rc))
        
    def on_disconnect(self, client, userdata, rc):
        self.log_mqtt("Disconnected with result code " + str(rc))

    def on_message(self, client, userdata, msg): 
        if (msg.topic == "hermes/nlu/intentParsed") and msg.payload: 
            self.log_mqtt("New itent: " + str(msg.payload))

            data = json.loads(str(msg.payload.decode('ascii')))
            intent = data['intent']['intentName']
            
            slots = dict()
            for i in range(len(data["slots"])):
                slots[ data['slots'][i]['slotName'] ] = data['slots'][i]['value']['value']
            
            robot = ev3.ev3rstorm()

            # --------------------------------------------------------------------------------------
            #                                WHAT CAN MINDSTORM DO 
            # --------------------------------------------------------------------------------------
            if (intent == "user_Hk9PxP07b__Calendar"): 
                robot.speak(calendar.set_talk(slots))

            elif (intent == "user_Hk9PxP07b__DistanceIntent"): 
                robot.speak(maps.set_talk(slots))

            elif (intent == "user_Hk9PxP07b__HelloIntent"): 
                robot.speak(hello.set_talk())

def main():
    server = Server('raspberrypi.local', 9898, '#') 
    server.start()

if __name__ == '__main__':
    main()
