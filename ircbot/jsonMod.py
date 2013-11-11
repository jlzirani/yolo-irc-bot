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
 
 Copyright 2013 Jean-Luc Z
"""

from module import botMod
import re

class JsonMod(botMod):
	def __init__(self, bot, rsslink):
		super(JsonMod, self).__init__(bot)
		self.json = re.findall(r'(https?://\S+)', rsslink)
		self.dirMsg = {"json-list": self.jsonList, "json-remove":  self.jsonRemove, "json-add": self.jsonAdd}
		self.installModule()
	#	self.bot.connection.execute_delayed(1,self.getJson, [])

	def jsonList(self, ev, cmd):
		if len(cmd) == 1:
			self.bot.sendMsg(ev.target, ev.source.nick+": " + ', '.join([item[1]+"["+str(item[0])+"]" for item in  enumerate(self.json)]))

	def jsonRemove(self, ev, cmd):
		if len(cmd) > 1 :
			obj = re.search(r'(?P<number>^[0-9]*$)|(?P<link>^https?://\S+$)', cmd[1])
			if obj is not None and obj.group('number') is not None:
				self.bot.sendMsg(ev.target, "Removing: " + self.json[int(obj.group('number'))])
				self.json.pop(int(obj.group('number')))
			elif obj is not None and obj.group('link') is not None:
				self.bot.sendMsg(ev.target, "Removing: " + obj.group('link'))
				self.json = filter( lambda elem: not elem[0] == obj.group('link'), self.json)

	def jsonAdd(self, ev, cmd):
		if len(cmd) > 1:
			newFeed = re.findall(r'(https?://\S+)', cmd[1]) 
			self.rss += newFeed

	def getJson(self):
		pass
