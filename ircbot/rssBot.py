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
