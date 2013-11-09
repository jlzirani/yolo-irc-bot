import irc.bot
import datetime
import re

class defaultBot(irc.bot.SingleServerIRCBot):
	def init(self, servers, name, chans):
                self.name = name
                self.chans = chans
                self.privMsg = {"quit": self.disconnect, }
		self.pubMsg = {}
		self.dirMsg = {"quit": self.disconnect, "help": self.helpMsg}
                irc.bot.SingleServerIRCBot.__init__(self, servers, name, "Je suis un bot!")

	def __init__(self, servers, name, chans):
		self.init(servers, name, chans)

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

		if cmd[0] in self.pubMsg:
			self.pubMsg[cmd[0]]( ev, cmd)


	def on_privmsg(self, serv, ev):
		cmd = ev.arguments[0].split(' ', 1)	
		if cmd[0] in self.privMsg:
			self.privMsg[cmd[0]]( ev , cmd )


	def helpMsg(self, ev, cmd):
		self.sendMsg(ev.target, ev.source.nick + ": Hello Hacker! You are talking to "+self.get_nickname()+" and you have requested this help text.")
		self.sendMsg(ev.target, "I have the following commands: "+ ', '.join(set(self.dirMsg.keys()+ self.pubMsg.keys() + self.privMsg.keys())))
		self.sendMsg(ev.target, "Have a nice chat and get the bot with you !")


	def disconnect(self, ev, cmd):
		if len(cmd) > 1:
			second = 0
			delayedDie = re.search(r'^([0-5]?[0-9]h)?([0-5]?[0-9]m)?([0-5]?[0-9]s)?\s*(.*)', cmd[1]).groups()

			if delayedDie[0] is not None:
				second = datetime.datetime.strptime(delayedDie[0],'%Hh').hour * 3600
			if delayedDie[1] is not None:
				second += datetime.datetime.strptime(delayedDie[1],'%Mm').minute*60
			if delayedDie[2] is not None:
				second += datetime.datetime.strptime(delayedDie[2],'%Ss').second

			param = [] 
			if not delayedDie[3] == '':
				param.append(delayedDie[3])

			self.connection.execute_delayed(second,self.die,param)
		else:
			self.die()

	def sendMsg(self, target, message):
		self.connection.privmsg(target, message)
