
class botMod(object):
	def __init__(self, bot):
		self.dirMsg = {}
		self.pubMsg = {}
		self.privMsg = {}
		self.bot = bot

	def sendMsg(self, chan, msg):
		self.bot.connection.privmsg(chan, msg)

	def get_nickname(self):
		return self.bot.get_nickname()

	def installModule(self):
		self.bot.dirMsg.update( self.dirMsg )
		self.bot.pubMsg.update( self.pubMsg )
		self.bot.privMsg.update( self.privMsg )

