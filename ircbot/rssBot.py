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
		self.rss = [ (link, feedGenerator(Config(url=link, format=u'{title} - {link}', key='title', number=1, reverse=True, ignore_key_error=True))) for link in re.findall(r'(https?://\S+)', rsslink)]
		self.connection.execute_delayed(1,self.getrss, [])
		self.dirMsg["rss-list"] = self.rssList
		self.dirMsg["rss-remove"] = self.rssRemove
		self.dirMsg["rss-add"] = self.rssAdd

	def rssList(self, ev, cmd):
		if len(cmd) == 1:
			self.sendMsg(ev.target, ev.source.nick+": " + ', '.join([link[0]+"["+str(index)+"]" for (index, link) in enumerate(self.rss)]))

	def rssRemove(self, ev, cmd):
		if len(cmd) > 1 :
			obj = re.search(r'(?P<number>^[0-9]*$)|(?P<link>^https?://\S+$)', cmd[1])
			if obj is not None and obj.group('number') is not None:
				self.sendMsg(ev.target, "Removing: " + self.rss[int(obj.group('number'))][0])
				self.rss.pop(int(obj.group('number')))
			elif obj is not None and obj.group('link') is not None:
				self.sendMsg(ev.target, "Removing: " + obj.group('link'))
				self.rss = filter( lambda elem: not elem[0] == obj.group('link'), self.rss)

	def rssAdd(self, ev, cmd):
		if len(cmd) > 1:
			newFeed = [ (link, feedGenerator(Config(url=link, format=u'{title} - {link}', key='title', number=1, reverse=True, ignore_key_error=True))) for link in re.findall(r'(https?://\S+)', cmd[1])] 
			map(self.showRss, newFeed)
			self.rss += newFeed

	def showRss(self, gen):
		for entry in gen[1].next():
			entry = unicode(entry, "utf-8")
			for chan in self.chans:
				self.sendMsg(chan, entry)

	def getrss(self):
		map(self.showRss, self.rss)
		self.connection.execute_delayed(60*5,self.getrss, [])
