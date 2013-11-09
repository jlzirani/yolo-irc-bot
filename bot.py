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
 
 Copyright 2013 Jean-Luc Z.
"""

from ircbot.masterBot import MasterBot, botTypeList, HelloBot
from ircbot.rssBot import RssBot

if __name__ == '__main__':
	global botTypeList
	botTypeList['hello'] = HelloBot 
	botTypeList['rss'] = RssBot

	MasterBot([("127.0.0.1", 6667)], "botTest", ["#test"]).start() 

