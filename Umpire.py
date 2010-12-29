#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import time
import ConfigParser
import PongBot

class Umpire():

    def __init__(self, configfile):
        self._configfile = configfile
        config = ConfigParser.ConfigParser()
        config.read(configfile)

        self._lastgame = config.getint('Umpire', 'lastgame')

        self._xmpp = PongBot.PongBot(configfile)

    def start(self):
        self._resetGame()  #Will increment last game
        self._xmpp.start()
        self._xmpp.resetGame( self._generateScore() )
        
    def leftButton(self):
        self._pointLeft = self._pointLeft + 1
        self._move = self._move + 1
        self._xmpp.pointLeft( self._generateScore() )

    def rightButton(self):
        self._pointRight = self._pointRight + 1
        self._move = self._move + 1
        self._xmpp.pointRight(self._generateScore() )

    def longPressLeft(self):
        self._resetGame()
        self._xmpp.resetGame( self._generateScore() )

    def longPressRight(self):
        self.longPressLeft()

    def stop(self):
        self._xmpp.disconnect()

    def _generateScore(self):
        config = ConfigParser.ConfigParser()
        config.read(self._configfile)
        config.set('Umpire', 'lastgame', self._lastgame)
        with open(self._configfile, 'wb') as configfile:
            config.write(configfile)
        return {'left': self._pointLeft, 'right': self._pointRight, 'game': self._lastgame, 'move': self._move}
                
    def _resetGame(self):
        self._lastgame = self._lastgame + 1
        self._move = 0
        self._pointLeft = 0
        self._pointRight = 0
    
if __name__ == '__main__':

    logging.basicConfig(level=5, format='%(levelname)-8s %(message)s')

    ump = Umpire('pingpong.ini')
    ump.start()
    ump.leftButton()
    ump.rightButton()
    ump.rightButton()
    ump.stop()

