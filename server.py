#!/usr/bin/env python

import watcher
from src.bot import *
from src.config.config import *

if __name__ == '__main__':
	w = watcher.Watcher()
	bot = Roboraj(config).run()
