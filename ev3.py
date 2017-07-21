#!/usr/bin/env python3
# encoding: utf-8

"""Main controller class for interfacing with the ev3dev API."""

# Copyright (c) 2017 Snips
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import time, random
import ev3dev.ev3 as ev3
from threading import Timer

random.seed( time.time() )

THINKING_PHRASES = [
    "That is a very good question! Let me think about it",
    "I am hearing you. Oh! Look at my left hand!",
    "Is that a trick question? Well, I'll try my best nevertheless",
    "Ouch! That's a tough one! Requires intense ventilation!",
    "Never been asked this before. Let me see what I can do",
    "Nice one! You almost got me there. Thinking",
    "Thinking so hard. I am the best thinker. I do the best thinking",
    "Hold tight, doing computery things. Beep beep beep",
]

ERROR_MESSAGES = [
    "I'm afraid I don't know how to answer this",
    "Really sorry, I don't think I can handle this request",
    "Hey! That's not what I was programmed to do!",
    "I'm sorry but I don't understand this",
    "Let me come back to you on that one",
    "Hahaha, you got me there. Can't answer that",
    "Segfault! Segfault! Segfault!",
    "I burnt my CPU trying to answer that question",
    "Uh ooooh, uh oooh. I... I... I... don't know what to say",
    "Can't handle this. I, I, I just can't handle this.",
]

def check(condition, message):
    if not condition:
        print(message)
        raise Exception(message)

class ev3rstorm:

    def __init__(self):
        self.lm = ev3.LargeMotor('outB')
        self.rm = ev3.LargeMotor('outC')
        self.mm = ev3.MediumMotor()
        self.ts = ev3.TouchSensor()

        check(self.lm.connected, 'Left leg not connected')
        check(self.rm.connected, 'Right leg not connected')
        check(self.mm.connected, 'Left arm not connected')
        check(self.ts.connected, 'Right arm not connected')

        self.on_touch = None

        for m in (self.lm, self.rm, self.mm):
            m.reset()
            m.position = 0
            m.stop_action = 'brake'

    def start(self):
        self.log("Starting")
        self.set_state("idle")
        
        current_press_state = False
        
        while True:
            if self.ts.is_pressed and current_press_state == False:
                current_press_state = True
                if self.on_touch != None:
                    self.on_touch()
            current_press_state = self.ts.is_pressed
            time.sleep(0.1)

    def log(self, msg):
        print("[EV3] " + msg)

    def speak(self, msg):
        time.sleep(1)
        return ev3.Sound.speak(msg)

    def speak_error(self):
        self.speak(ERROR_MESSAGES[random.randint(0, len(ERROR_MESSAGES)-1)])

    def move(self, direction="left", distance="10", unit="centimeter"):

        if direction == "left":
            self.rm.run_timed(time_sp=1000, speed_sp=500)
        elif direction == "right":
            self.lm.run_timed(time_sp=1000, speed_sp=500)
        elif direction == "forward":
            self.rm.run_timed(time_sp=100*int(distance), speed_sp=500)
            self.lm.run_timed(time_sp=100*int(distance), speed_sp=500)
        elif direction == "back":
            self.rm.run_timed(time_sp=100*int(distance), speed_sp=-500)
            self.lm.run_timed(time_sp=100*int(distance), speed_sp=-500)

    def shoot(self, direction='up'):
        self.mm.run_to_rel_pos(speed_sp=900, position_sp=(-1080 if direction == 'up' else 1080))

    def set_state(self, state="idle"):
        self.log("STATE: " + str(state))
        self.led(state)
        self.beep(state)
        if state == "thinking":
            self.speak(THINKING_PHRASES[random.randint(0, len(THINKING_PHRASES)-1)])
            t = Timer(6.0, self.start_arm_motor)
            t.start()
        else:
            self.arm_motor(False)

    def start_arm_motor(self):
        self.arm_motor(True)

    def arm_motor(self, on=False):
        if on:
            self.mm.run_forever(speed_sp=700)
        else:
            self.mm.stop()