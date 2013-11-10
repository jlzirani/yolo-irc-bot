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

from threading import Thread
from module import botMod
from bot import ircBot

import re

botTypeList = {}

class MasterMod(botMod):
	def __init__(self, bot):
		super(MasterMod, self).__init__(bot)
		self.bots = []
		self.dirMsg= { "quit": self.killMinion, "bot-list": self.botList, "add-bot": self.addBot}
		self.installModule()


	def spawnBot(self, ev, args):
		if not args["type"] in botTypeList:
			self.bot.sendMsg(ev.target, ev.source.nick + ": bot type not recognized !")
		else:
			chans = re.findall(r'#[a-zA-Z0-9_]{2,9}', args["chans"]) 
			if len(chans) == 0:
				chans = [ ev.target ]
			bot = ircBot( self.bot.servers, args["name"], chans)
			bot.addModule(botTypeList[args["type"]], [args["args"]])
			self.bots.append(bot)
			Thread(target=bot.start).start()

	def addBot(self, ev, cmd):
		if len(cmd) > 1:
			match = re.search(r'^(?P<type>[a-zA-Z0-9_]*)\s*(?P<name>[a-zA-Z0-9_]{3,9})(?P<chans>(?:\#[a-zA-Z0-9_]{2,9}|\s)*)(?P<args>.*)$', cmd[1])
			if match is not None :
				self.spawnBot( ev, match.groupdict() )
			else:
				self.bot.sendMsg(ev.target, ev.source.nick + ": syntax not recognized !")

	def killMinion(self, ev, msg):
		for bot in self.bots:
			self.bot.sendMsg(bot.connection.get_nickname(), "quit I'm killed by "+self.bot.get_nickname()+" !")	
		self.bot.die()

	def botList(self, ev, cmd):
		if len(self.bots) == 0:
			self.bot.sendMsg(ev.target, ev.source.nick+": I'm alone")
		else:
			self.bot.sendMsg(ev.target, ev.source.nick+": " + ', '.join([bot.connection.get_nickname() for bot in self.bots]))


