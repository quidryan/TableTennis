#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ubw
import logging
import time
import Detector
import ConfigParser
import pprint

class Poller():

    def __init__(self, configfile):
        config = ConfigParser.ConfigParser()
        config.read(configfile)

        self.port = config.get('Poller', 'port')

        self.u = ubw.Ubw(self.port)

        self.detector = Detector.Detector(configfile)

    def start(self):
        self.u.Reset()
        self.detector.start()
        # Add additional handler
        self.u.responses.append((ubw.INPUT_STATE, self.HandleInputState))

        self.u.Configure(255,255,255,0)

        #Should for input thread to identify INPUT_STATE and call our handler
        self.u.Timer(50,0)
        #for i in range(10*1):
        #    self.u.InputState()
        #    time.sleep(1)

    def stop(self):
        self.u.Timer(0,0)
        self.u.Stop()
        self.detector.stop()

    def HandleInputState(self,input_state):
        """Handle the current pin input state response from the UBW.
        Print out our own response
        Args:
            input_state: dictionary of response values
        """

        portc = int(input_state['portc'])

        #pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(input_state)
        open = ubw.ValueToMap(portc)[2]
	buttonpressed = not open
        self.detector.poll(buttonpressed, False)


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')

    ump = Poller('pingpong.ini')
    ump.start()
    try:
        #Timer is running, just bide our time
        while True:
            time.sleep(2)
    finally:
        ump.stop()

