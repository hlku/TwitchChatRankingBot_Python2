# -*- coding: utf-8 -*-
"""
Simple IRC Bot for Twitch.tv

Developed by Aidan Thomson <aidraj0@gmail.com>
"""

import lib.irc as irc_
from lib.functions_general import *
import lib.functions_commands as commands
import rank.rank as rk
from rank.ranks import *

class Roboraj:

	def __init__(self, config):
		self.config = config
		self.irc = irc_.irc(config)
		self.socket = self.irc.get_irc_socket_object()

		self.ranks = dict()
		for channel in self.config.get('channels', []):
			cid = self.config['channelid'].get(channel)
			quiet = self.config['quiet'].get(channel, True)
			self.ranks[channel] = rk.Rank(self.config, self.irc, channel, cid, quiet)

	def run(self):
		irc = self.irc
		sock = self.socket
		config = self.config
		for rank in self.ranks:
			self.ranks[rank].start()
			resp = u'! 98bot進入聊天室，計算聊天等級開始。'
			irc.send_message(rank, resp)

		while True:
			data = sock.recv(config['socket_buffer_size']).rstrip()

			if len(data) == 0:
				pp('Connection was lost, reconnecting.')
				sock = self.irc.get_irc_socket_object()

			if config['debug']:
				print data

			# check for ping, reply with pong
			irc.check_for_ping(data)

			if irc.check_for_message(data):
				message_dict = irc.get_message(data)

				channel = message_dict['channel']
				message = message_dict['message']
				username = message_dict['username']

				if username.lower() in self.config['ignore']: continue

				# give XP to this user
				rks = self.ranks.get(channel, None)
				if rks is not None and rks.live == True: rks.newchat(username)
				if rks.quiet: continue

				#I'm lazy to write a module
				msg = message.strip().split(' ')
				target = username
				if len(msg) > 1: target = msg[1].lower()
				if msg[0].lower() == '!rank':
					if username == channel[1:] and len(msg) == 1: #broadcaster don't have level
						u = rks.top()
						if u is not None:
							if u[4].lower() == u[1].lower(): 
								resp = u'! 報告台主，目前講話最多的是 %s，%s級，經驗值%s/%s。' % (u[4], str(u[3]), str(u[2]), str(threshold[u[3]]))
							else: 
								resp = u'! 報告台主，目前講話最多的是%s (%s)，%s級，經驗值%s/%s。' % (u[4], u[1], str(u[3]), str(u[2]), str(threshold[u[3]]))
						else:
							resp = u'! 報告台主，你到現在都沒有半個觀眾講過話，幫QQ'
					else:
						u = rks.find(target)
						if u is not None:
							if u[4].lower() == u[1].lower(): 
								resp = u'! %s 目前%s級，排第%s名，經驗值%s/%s。' % (u[4], str(u[3]), str(u[0]), str(u[2]), str(threshold[u[3]]))
							else:
								resp = u'! %s (%s) 目前%s級，排第%s名，經驗值%s/%s。' % (u[4], u[1], str(u[3]), str(u[0]), str(u[2]), str(threshold[u[3]]))
						else:
							resp = u'! 找不到 %s 的等級，大概還沒講過話吧。' % target
					irc.send_message(channel, resp)
					continue

				# for checking the bot is online
				if message.strip().lower() == '!98bot' or message.strip().split(' ')[0].lower() == '!98bot':
					if rks.live:
						resp = u'! 正在努力記錄大家的經驗值。'
					else:
						resp = u'! 目前沒開台沒經驗值，但我不會阻止你講話～'
					irc.send_message(channel, resp)
					continue


				# check if message is a command with no arguments
				if commands.is_valid_command(message) or commands.is_valid_command(message.split(' ')[0]):
					command = message

					if commands.check_returns_function(command.split(' ')[0]):
						if commands.check_has_correct_args(command, command.split(' ')[0]):
							args = command.split(' ')
							del args[0]

							command = command.split(' ')[0]

							if commands.is_on_cooldown(command, channel):
								pbot('Command is on cooldown. (%s) (%s) (%ss remaining)' % (
									command, username, commands.get_cooldown_remaining(command, channel)), 
									channel
								)
							else:
								pbot('Command is valid an not on cooldown. (%s) (%s)' % (
									command, username), 
									channel
								)
								
								result = commands.pass_to_function(command, args)
								commands.update_last_used(command, channel)

								if result:
									resp = '%s' % result
									pbot(resp, channel)
									irc.send_message(channel, resp)

					else:
						if commands.is_on_cooldown(command, channel):
							pbot('Command is on cooldown. (%s) (%s) (%ss remaining)' % (
									command, username, commands.get_cooldown_remaining(command, channel)), 
									channel
							)
						elif commands.check_has_return(command):
							pbot('Command is valid and not on cooldown. (%s) (%s)' % (
								command, username), 
								channel
							)
							commands.update_last_used(command, channel)

							resp = '%s' % commands.get_return(command)
							commands.update_last_used(command, channel)

							pbot(resp, channel)
							irc.send_message(channel, resp)

