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
import datetime
import re
from module import botMod

class defaultMod(botMod):
	def __init__(self, bot):
		super(defaultMod, self).__init__(bot)
		self.dirMsg = { "quit": self.disconnect, "help": self.helpMsg}
		self.installModule()

	def disconnect(self, ev, cmd):
		if len(cmd) > 1:
			second = 0
			delayedDie = re.search(r'^([0-5]?[0-9]h)?([0-5]?[0-9]m)?([0-5]?[0-9]s)?\s*(.*)', cmd[1]).groups()

			if delayedDie[0] is not None:
				second = re.findall(r'[0-9]+', delayedDie[0])[0] * 3600
			if delayedDie[1] is not None:
				second = re.findall(r'[0-9]+', delayedDie[1])[0] * 60
			if delayedDie[2] is not None:
				second = re.findall(r'[0-9]+', delayedDie[2])[0] 
			param = [] 
			if not delayedDie[3] == '':
				param.append(delayedDie[3])

			self.bot.connection.execute_delayed(second,self.bot.die,param)
		else:
			self.bot.die()

	def helpMsg(self, ev, cmd):
		self.bot.sendMsg(ev.target, ev.source.nick + ": Hello Hacker! You are talking to "+self.bot.get_nickname()+" and you have requested this help text.")
		self.bot.sendMsg(ev.target, "I have the following commands: "+ ', '.join(set(self.bot.dirMsg.keys()+ self.bot.pubMsg.keys() + self.bot.privMsg.keys())))
		self.bot.sendMsg(ev.target, "Have a nice chat and get the bot with you !")

