# -*- coding: utf-8 -*-
import json, time, threading, requests
from ranks import *
from src.lib.functions_general import *

h = {'Accept': 'application/vnd.twitchtv.v5+json',
	'Client-ID': self.config.get('clientID', None)}

class Rank(threading.Thread):

	def __init__(self, config, irc, channel, cid, quiet=True):
		threading.Thread.__init__(self)
		self.config = config
		self.irc = irc
		self.channel = channel
		self.cid = cid #channel id
		self.quiet = quiet
		self.fname = 'rkfiles/' + self.channel[1:] + '.rk'
		self.data = self.parse()
		self.lock = threading.Lock()
		self.active = dict()
		self.live = False

	def run(self):
		self.timer()

	def parse(self):
		try:
			with open(self.fname, 'r') as inp:
				i = inp.read()
		except:
			print 'Open rank file of channel ' + self.channel + ' failed.'
			return []

		try:
			d = json.loads(i)
		except:
			print 'Rank file of channel ' + self.channel + ' is broken.'
			return []

		return d.get('data', [])

	def tofile(self):
		# Though open file everytime is inefficient
		try:
			with open(self.fname, 'w') as outp:
				outp.write(json.dumps( {'data': self.data} ))
		except:
			print 'Write to rank file of channel ' + self.channel + ' failed.'

	def update(self):
		def comp(u1, u2):
			if u1[3] > u2[3]: return 1
			elif u1[3] == u2[3]: return u1[2] - u2[2]
			else: return -1

		self.data[:] = sorted(self.data, reverse=True, cmp=comp)

		i = 1
		for d in self.data:
			d[0] = i #no
			if d[2] >= threshold[d[3]]: #reached new level!
				d[2] -= threshold[d[3]]
				d[3] += 1
				# some announce
				pbot('[%s] %s reached level %s, now no.%s!' % (self.channel, d[1], str(d[3]), str(d[0])) )
				ann = self.config.get('announce', 0)
				if ann > 0 and d[3] % ann == 0 and not self.quiet: #need announce
					if d[1].lower() == d[4].lower():
						resp = u' %s 升到%s級！目前第%s名。' % (d[4], str(d[3]), str(d[0]))
					else:
						resp = u' %s (%s) 升到%s級！目前第%s名。' % (d[4], d[1], str(d[3]), str(d[0]))
					self.irc.send_message(self.channel, resp)
			i += 1

	def getname(self, user): #get the nickname
		r = requests.get('https://api.twitch.tv/kraken/users?api_version=5&login=' + user, headers=h)

		return r.json()['users'][0].get('display_name', user) #no fool detection

	def find(self, user, add=False):
		for u in self.data:
			if u[1] == user:
				return u

		#if not found, new viewer!
		if add :
			u = [0, user, 0, 0, self.getname(user)]
			self.data.append(u)
			return u
		else: #only for search
			return None

	def top(self):
		if len(self.data) == 0:
			return None
		return self.data[0]

	def check(self): #check whether the channel is streaming
		r = requests.get('https://api.twitch.tv/kraken/streams/' + str(self.cid), headers=h)

		if r.json().get('stream', None) is None: return False
		else: return True

	def timer(self):
		duration = self.config.get('duration', 60)
		while True:
			time.sleep(duration)
			l = self.check()
			if not self.live and l:
				if not self.quiet:
					resp = u'開台了！開始記錄！'
					self.irc.send_message(self.channel, resp)
				pbot('[%s] has started streaming.' % self.channel)
			elif self.live and not l:
				if not self.quiet:
					resp = u'關台了'
					self.irc.send_message(self.channel, resp)
				pbot('[%s] stopped streaming.' % self.channel)
			self.live = l

			if len(self.active) == 0: continue

			with self.lock: #don't let others use
				nonactive = []
				for k in self.active:
					user = self.find(k, add=True)
					user[2] += self.active[k] #get XP
					self.active[k] -= 1 #cool down
					if self.active[k] == 0: #not active anymore
						nonactive.append(k)

				for gone in nonactive: #we can't touch the dict while iter
					del self.active[gone]

			self.update()
			self.tofile()

	def newchat(self, user):
		if user == self.channel[1:]:
			return #broadcaster not count
		with self.lock: #don't let others use
			self.active[user] = 10

