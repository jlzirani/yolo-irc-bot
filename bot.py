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

from ircbot.masterMod import MasterMod, botTypeList
from ircbot.rssMod import RssMod
from ircbot.bot import ircBot
import ConfigParser

if __name__ == '__main__':
	global botTypeList
	botTypeList['rss'] = RssMod

	Config = ConfigParser.ConfigParser()
	Config.read("config.ini")

	server = (Config.get('general', 'server'), int(Config.get('general', 'port')))

	masterBot = ircBot([server], Config.get('general', 'masterBot'), Config.get('general', 'chan'))
	masterBot.addModule(MasterMod)

	masterBot.start()

