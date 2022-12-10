#!/usr/bin/env python3
"""
Copyright 2022. All rights reserved.
"""
__version__ = "1.0"
import traceback
import sys
import re

from commands.basecommand import BaseCommand


class DNS(BaseCommand):
	"""docstring for DNS"""
	def __init__(self):
		super(DNS, self).__init__()
		self.__name__ = 'DNS Cache'

	def run_ssh(self, sshc):
		data = self._ssh_data(sshc, '/ip dns print detail')
		enabled = 'allow-remote-requests: yes' in data.lower()

		result = self._ssh_data_with_header(sshc, '/ip dns cache print detail')
		#sus_dns

		return {'raw_data': result}
