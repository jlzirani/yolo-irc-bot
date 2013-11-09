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

from defaultBot import defaultBot
from feedstail import feedGenerator
from feedstail.config import Config
import re

class RssBot(defaultBot):
	def __init__(self, servers, name, chans, rsslink):
		self.init(servers, name, chans)
		self.addWatcher(re.findall(r'(https?://\S+)', rsslink))

	def addWatcher(self, rsslink):
		for link in rsslink:
			gen = feedGenerator(Config(url=link, format=u'{title} - {link}', key='title', number=1, reverse=True, ignore_key_error=True))
			self.connection.execute_delayed(1,self.getrss, [gen])

	def getrss(self, gen):
		for i in gen.next():
			for chan in self.chans:
				self.connection.privmsg(chan, unicode( i, "utf-8"))

		self.connection.execute_delayed(60*5,self.getrss, [gen])
