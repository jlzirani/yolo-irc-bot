import irc.bot

class defaultBot(irc.bot.SingleServerIRCBot):
	def init(self, servers, name, chans):
                self.name = name
                self.chans = chans
                self.privMsg = {"quit": self.disconnect, }
		self.pubMsg = {}
                irc.bot.SingleServerIRCBot.__init__(self, servers, name, "Je suis un bot!")


	def __init__(self, servers, name, chans):
		self.init(servers, name, chans)

	def on_welcome(self, serv, ev):
		for i in self.chans:
			serv.join(i)

	def on_pubmsg(self, serv, ev):
		dir(ev)
		cmd = ev.arguments[0].split(' ',1) [0]
		if cmd in self.pubMsg:
			self.pubMsg[cmd]( serv, ev)


	def on_privmsg(self, serv, ev):
		message = ev.arguments[0]
		cmd = message.split(' ',1)[0]
		if cmd in self.privMsg:
			self.privMsg[cmd]( ev )


	def disconnect(self, ev ):
		message = ev.arguments[0].split(' ',1)
		if len(message) > 1:
			self.die(message[1])
		else:
			self.die()

