"""
 This file is part of yolo-irc-bot.
 
 Yolo-irc-bot is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 Yolo-irc-bot is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
 
 Copyright 2013 Jean-Luc Z.
"""

import irc.bot
from defaultMod import defaultMod

class ircBot(irc.bot.SingleServerIRCBot):

	def init(self, servers, name, chans):
                self.name = name
		self.servers = servers
                self.chans = chans
                self.privMsg = {}
		self.pubMsg = {}
		self.dirMsg = {}
		self.modules = []
                irc.bot.SingleServerIRCBot.__init__(self, servers, name, "Je suis un bot!")
		self.addModule(defaultMod)

	def __init__(self, servers, name, chans):
		self.init(servers, name, chans)

	def addModule(self, module, args = []):
		self.modules.append(module(self, *args))

	def get_nickname(self):
		return self.connection.get_nickname()

	def on_welcome(self, serv, ev):
		for i in self.chans:
			serv.join(i)

	def on_pubmsg(self, serv, ev):
		msg = ev.arguments[0]
		cmd = msg.split(' ', 1)
		
		if cmd[0] == self.get_nickname()+":" and len(cmd) > 1:
			cmd = cmd[1].split(' ',1)
			if cmd[0] in self.dirMsg:
				self.dirMsg[cmd[0]]( ev, cmd)
			else:
				self.sendMsg(ev.target, ev.source.nick+": I didn't recognized the command: " + cmd[0])

		elif cmd[0] in self.pubMsg:
			self.pubMsg[cmd[0]]( ev, cmd)


	def on_privmsg(self, serv, ev):
		cmd = ev.arguments[0].split(' ', 1)	
		if cmd[0] in self.privMsg:
			self.privMsg[cmd[0]]( ev , cmd )

	def sendMsg(self, target, message):
		self.connection.privmsg(target, message)


