#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
import ConfigParser
import Umpire
from collections import deque
import pprint

class Detector():

    """
    Hysterisis of button presses
    """
    def __init__(self, configfile):
        config = ConfigParser.ConfigParser()
        config.read(configfile)

        self.cleanthreshold = config.getint('Detector', 'shortpress')
        self.longpress = config.getint('Detector', 'longpress')
        self.dirtythreshold = config.getint('Detector', 'dirtythreshold')

        self.left = self._side_factory()
        self.right = self._side_factory()
        self.ump = Umpire.Umpire(configfile)

    def _side_factory(self):
        return {'clean': 0, 'dirty': 0, 'longpress': 0}

    def start(self):
        self.left = self._side_factory()
        self.right = self._side_factory()
        self.ump.start()

    def stop(self):
        self.ump.stop()

    def poll(self, leftbutton, rightbutton):
        self.left = self._history(leftbutton, self.left, True)
        if self.left['clean'] > 0 or self.left['dirty'] > 0 :
            logging.info("Left: %s" % self.left)
        else:
            logging.debug("Left: %s" % self.left)

        self.right= self._history(rightbutton, self.right, False)
        #logging.debug("Right: %s" % self.right)

    def _history(self, input, side, is_left):
        # Inspect queue, looking for transition events
        if input == True:
            side['clean'] += 1
        else:
            if side['clean'] > 0:
                # Only count dirty's if we've had a clean
                side['dirty'] += 1

        if side['clean'] >= self.cleanthreshold:
            # Possibilty for a button press
            if side['dirty'] >= self.dirtythreshold:
                # Button released
                if not side['longpress']:
                    logging.info("BUTTON PRESSED")
                    if is_left:
                        self.ump.leftButton()
                    else:
                        self.ump.rightButton()
                # If long press already detected, then we don't want what we've detected so far to count as a button press
                return self._side_factory()
            else:
                # Still holding button
                if side['clean'] > self.longpress and not side['longpress']:
                    # Qualifies as long press
                    logging.info("LONG PRESS")
                    if is_left:
                        self.ump.longPressLeft()
                    else:
                        self.ump.longPressRight()

                    # Prevent detecting this again
                    side['longpress'] = True
        return side

if __name__ == '__main__':

    logging.basicConfig(level=5, format='%(levelname)-8s %(message)s')

    detector = Detector('pingpong.ini')
    detector.start()
    detector.poll(True, False)
    detector.poll(True, False)
    detector.poll(False, False)
    detector.poll(True, False)
    detector.poll(True, False)
    detector.poll(True, False)
    detector.poll(True, False)
    detector.poll(True, False)
    detector.poll(True, False)
    detector.poll(True, False)
    detector.poll(True, False)
    detector.poll(True, False)
    detector.poll(True, False)
    detector.poll(True, False)
    detector.poll(True, False)
    detector.poll(False, False)
    detector.poll(False, False)
    detector.poll(False, False)
    detector.poll(False, False)
    detector.poll(False, False)
    detector.poll(False, False)
    detector.poll(False, False)
    detector.stop()

