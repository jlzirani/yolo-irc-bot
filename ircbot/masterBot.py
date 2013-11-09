from defaultBot import defaultBot
from threading import Thread

import re

class HelloBot(defaultBot):
	def __init__(self, servers, name, chans, args):
		self.init(servers, name, chans)
		self.pubMsg["hello"] = self.hello
		self.privMsg["hello"] = self.hello

	def hello(self, ev, cmd):
		if len(cmd) == 1:
			self.sendMsg(ev.target, ev.source.nick+": hello")

botTypeList = {}

class MasterBot(defaultBot):
	def __init__(self, servers, name, chans):
		self.bots = []
		self.servers = servers
		self.init(servers,name,chans)
		self.dirMsg["quit"] = self.killMinion
		self.dirMsg["bot-list"] = self.botList
		self.dirMsg["add-bot"] = self.addBot

	def spawnBot(self, ev, args):
		if not args["type"] in botTypeList:
			self.sendMsg(ev.target, ev.source.nick + ": bot type not recognized !")
		else:
			chans = re.findall(r'#[a-zA-Z0-9_]{2,9}', args["chans"]) 
			if len(chans) == 0:
				chans = [ ev.target ]
			bot = botTypeList[args["type"]](self.servers, args["name"], chans, args["args"])
			self.bots.append(bot)
			Thread(target=bot.start).start()

	def addBot(self, ev, cmd):
		if len(cmd) > 1:
			match = re.search(r'^(?P<type>[a-zA-Z0-9_]*)\s*(?P<name>[a-zA-Z0-9_]{3,9})(?P<chans>(?:\#[a-zA-Z0-9_]{2,9}|\s)*)(?P<args>.*)$', cmd[1])
			if match is not None :
				self.spawnBot( ev, match.groupdict() )
			else:
				self.sendMsg(ev.target, ev.source.nick + ": syntax not recognized !")

	def killMinion(self, ev, msg):
		for bot in self.bots:
			self.sendMsg(bot.connection.get_nickname(), "quit I'm killed by "+self.get_nickname()+" !")	
		self.disconnect(ev, msg)

	def botList(self, ev, cmd):
		if len(self.bots) == 0:
			self.sendMsg(ev.target, ev.source.nick+": I'm alone")
		else:
			self.sendMsg(ev.target, ev.source.nick+": " + ', '.join([bot.connection.get_nickname() for bot in self.bots]))


