global config

config = {
	
	# details required to login to twitch IRC server
	'server': 'irc.twitch.tv',
	'port': 6667,
	'username': 'yourbotname',
	'oauth_password': 'oauth:abcdefghijklmnopqrstuvwxyz', # get this from http://twitchapps.com/tmi/
	
	# channel to join
	'channels': ['#twitch'],
	'channelid': {'#twitch': 12826 #you can use the getID.sh to get it
				},

	# the ignore users
	'ignore': ['yourbotname', 'nightbot', 'mikuia', 'moobot', 'vivbot', 'streamelements'],

	# announce each N level (0 for dont announce)
	'announce': 1,

	# just record ranking, no response, default is True

    'quiet': { '#twitch': False }, #Fasle means sending announce to chat 

	'clientID': 'abcdefghijklmnopqrstuvwxz', #this is yourbot's client id

	'cron': {
	},

	# if set to true will display any data received
	'debug': False,

	# if set to true will log all messages from all channels
	# todo
	'log_messages': True,

	# maximum amount of bytes to receive from socket - 1024-4096 recommended
	'socket_buffer_size': 2048,

	# duration of ranking check time
	'duration': 60
}

