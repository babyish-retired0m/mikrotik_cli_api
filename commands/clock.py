#!/usr/bin/env python3
"""
Copyright 2022. All rights reserved.
"""
__version__ = "1.0"
import traceback
import sys

from commands.basecommand import BaseCommand


class Clock(BaseCommand):
	"""docstring for Clock"""
	def __init__(self):
		super(Clock, self).__init__()
		self.__name__ = 'Clock'

	def run_ssh(self, sshc):
		#data = self._ssh_data(sshc, command)

		result = self._ssh_data_with_header(sshc, '/system clock print')
		
		return {'raw_data': result}