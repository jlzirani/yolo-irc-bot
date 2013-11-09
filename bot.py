from ircbot.masterBot import MasterBot, botTypeList, HelloBot
from ircbot.rssBot import RssBot

if __name__ == '__main__':
	global botTypeList
	botTypeList['hello'] = HelloBot 
	botTypeList['rss'] = RssBot

	MasterBot([("127.0.0.1", 6667)], "botTest", ["#test"]).start() 

