from defaultBot import defaultBot
from threading import Thread

from feedstail import feedGenerator
from feedstail.config import Config


class rssBot(defaultBot):
	def __init__(self, servers, name, chans, rsslink):
		self.chans = chans
		self.init(servers, name, chans)
		self.addWatcher(rsslink)
			
	def addWatcher(self, rsslink):
		gen = feedGenerator(Config(url=rsslink, format=u'{title} - {link}', key='title', number=1, reverse=True, ignore_key_error=True))
		self.connection.execute_delayed(1,self.getrss, [gen])

	def getrss(self, gen):
		for i in gen.next():
			for chan in self.chans:
				self.connection.privmsg(chan, unicode( i, "utf-8"))

		self.connection.execute_delayed(60*5,self.getrss, [gen])


class MasterBot(defaultBot):
	def __init__(self, servers, name, chans):
		self.bots = []
		self.servers = servers
		self.init(servers,name,chans)
		self.pubMsg["add"] = self.addMinion
		self.privMsg["quit"] = self.privKillAll
		self.pubMsg["quit"] = self.pubKillAll
		self.pubMsg["help"] = self.helpMsg
		self.pubMsg["botlist"] = self.botlist

	def addMinion(self, serv, ev):
		result = ev.arguments[0].split(' ')
		bot = rssBot(self.servers, result[1], ["#rss"], result[2])
		self.bots.append(bot)
		Thread(target = bot.start).start()

	def helpMsg(self, serv, ev):
		serv.privmsg(ev.target, ev.source.nick + ": Hello Hacker! You are talking to "+self.connection.get_nickname()+" and you have requested this help text. Have a nice chat and get the bot with you!")

	def pubKillAll(self, c, ev):
		self.privKillAll(ev)

	def privKillAll(self, ev):
		for bot in self.bots:
			self.connection.privmsg(bot.connection.get_nickname(), "quit I'm killed by "+self.connection.get_nickname()+" !")	
		self.disconnect( ev )


	def botlist(self, c, ev):
		c.privmsg(ev.target, "bot list : " + ','.join([bot.connection.get_nickname() for bot in self.bots]))


if __name__ == '__main__':
	MasterBot([("127.0.0.1", 6667)], "masterBot", ["#rss"]).start() 

