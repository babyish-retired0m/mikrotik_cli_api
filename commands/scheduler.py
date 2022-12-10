#!/usr/bin/env python3
"""
Copyright 2022. All rights reserved.
"""
__version__ = "1.0"
import traceback
import sys

import commands.basecommand

class Scheduler(commands.basecommand):
	"""docstring for Scheduler"""
	def __init__(self):
		super(Scheduler, self).__init__()
		self.__name__ = 'Scheduler'

	def run_ssh(self, sshc):
		return {'raw_data': self._ssh_data_with_header(sshc, '/system scheduler print detail')}
		