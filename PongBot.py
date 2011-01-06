#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import time
import sleekxmpp
import ConfigParser
from threading import Event
import signal

class PongBot(sleekxmpp.ClientXMPP):

    #jid = 'winterhomework@halfempty.org'
    #password = 'jimmy007'
    #server = 'talk.google.com'
    #to='winterhomework@partychapp.appspotchat.com'
    #to='justin@halfempty.org'
    def __init__(self, configfile):
        config = ConfigParser.ConfigParser()
        config.read(configfile)

        self._jid=config.get('XMPP', 'jid')
        self._password=config.get('XMPP', 'password')
        self._server=config.get('XMPP', 'server')
        self._port=config.getint('XMPP', 'port')
        self._to=config.get('XMPP', 'to')
        self._useMUC=config.getboolean('XMPP', 'useMUC')

        logging.debug("JID is %s" % self._jid)
        logging.debug("Password is %s" % self._password)
        sleekxmpp.ClientXMPP.__init__(self, self._jid, self._password)

        self.add_event_handler("session_start", self._session_start)
        self.add_event_handler("message", self._handleIncoming) 
        self.add_event_handler("groupchat_message", self._handleIncomingGroupChatMessage) 
        self.add_event_handler("sent_presence", self._handlePresence) 
        self.registerPlugin('xep_0030') # Service Discovery
        self.registerPlugin('xep_0004') # Data Forms
        self.registerPlugin('xep_0045') # Group Chat
        self.registerPlugin('xep_0060') # PubSub
        self.registerPlugin('xep_0199') # XMPP Ping

    def start(self):
        """ 
        Caller to perform actual connection, blocks until presence is ready
        """
        self._evt = Event();
        if self.connect((self._server, self._port)):
            self.process(threaded=True)
            logging.info("Processing started")
            self._evt.wait()

        else:
            logging.error("Unable to connect")
            self._evt.set()

    def joinRoom(self):
        #initialize and handle Group Chat room 
        muc = self.plugin['xep_0045'] 
        logging.info( "trying to Join room" )
        room = self._to
        join = muc.joinMUC(room, self._jid) 
        print 'join: ', join, '\n' 
        #if join == 'True': 
        #    conf = muc.getRoomConfig('score') 
        #    print 'conf: ', join, '\n' 
        #    form = muc.getRoomForm('%s@%s' % ('score','muc')) 
        #    print 'form: ', form, '\n' 

    def _session_start(self, start):
        self.getRoster()
        logging.info("Sending Prescense")
        self.sendPresence()

    def _handlePresence(self, presence):
        logging.info("Receved presence")
        if self._useMUC:
            self.joinRoom()
        self._evt.set()

    def _handleIncoming(self, msg):
        logging.info("Message created %s" % msg)
        #msg.reply("Pong").send()

    def _handleIncomingGroupChatMessage(self, msg):
        logging.info("Group Message created %s" % msg)
        #msg.reply("Pong").send()

    def pointLeft(self, dict):
        self._post(dict, "Point Left")
        
    def pointRight(self, dict):
        self._post(dict, "Point Right")
        
    def resetGame(self, dict):
        self._post(dict, "Game Reset")

    def _post(self, dict, verb):
        """
        Dictionary to include: 
            left: Score for Left side of table
            right: Score for Right side of table
            game: Which Game is being played, unique identifier per-game
            move: Sequence of move made
        """
        logging.info("sending %s to %s" % (verb, self._to))
        if self._useMUC:
            mtype = 'groupchat'
        else:
            mtype = 'chat'
        self.sendMessage(self._to, "%s in %d[%d] %s vs %s" % (verb, dict['game'], dict['move'], dict['left'], dict['right']), mtype=mtype)
        
if __name__ == '__main__':

    logging.basicConfig(level=5, format='%(levelname)-8s %(message)s')

    def handler(signum, frame):
        print 'Here you go'

    signal.signal(signal.SIGINT, handler)

    xmpp = PongBot('pingpong.ini')
    xmpp.start()
    xmpp.resetGame({'left':0, 'right':0, 'game':1045, 'move':0})
    xmpp.pointLeft({'left':1, 'right':0, 'game':1045, 'move':1})
    xmpp.pointRight({'left':1, 'right':1, 'game':1045, 'move':2})
    xmpp.disconnect()
 
