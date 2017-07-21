#!/usr/bin/env python3
# encoding: utf-8

"""Mock class for simulating ev3dev API calls, used when not running on the ev3."""

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
import os

random.seed( time.time() )

class ev3rstorm:

    def __init__(self):
        self.on_touch = None

    def start(self):
        self.log("Starting")
        self.set_state("idle")
        while True:
            input("Press Enter to continue...")
            self.on_touch()

    def log(self, msg):
        print("[EV3-DUMMY] " + msg)

    def rc_loop(self): 
        self.log("Remote Control loop")

    def say_hello(self):
        self.log("Hello")

    def speak(self, msg):
        self.log("[SPEAK] " + msg)

    def move(self, direction="left", distance="10", unit="centimeter"): # distance is here in centimeter per default
        if direction == "left":
            self.log("Turn left")
        elif direction == "right":
            self.log("Turn right")
        elif direction == "forward":
            self.log("Move forward for " + str(distance) + " centimeters")
        elif direction == "back":
            self.log("Move back for "  + str(distance) + " centimeters")

    def shoot(self, direction="forward"):
        self.log("Shoot")

    def set_state(self, state="idle"):
        s = "unknown"
        if state == "idle":
            s = "idle"
        elif state == "loading":
            s = "loading"
        elif state == "ready":
            s = "ready"
        elif state == "preparing":
            s = "preparing"
        elif state == "listening":
            s = "listening"
        elif state == "done_listening":
            s = "done_listening"
        elif state == "error":
            s = "error"
        elif state == "thinking":
            s = "thinking"
        self.log("State {}".format(s))