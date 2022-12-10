1#!/usr/bin/env python3
"""
Copyright 2022. All rights reserved.
"""
__version__ = "1.0"
import traceback
import sys


class BaseCommand(object):
	"""docstring for BseCommand"""
	# def _ssh_data(self, sshc, command):
	# 	result = ''
	# 	try:
	# 		stdin, stdout, stderr = sshc.exec_command(command)
	# 		result = str(stdout.read())
	# 	except Exception as e:
	# 		print(traceback.format_exc(), file = sys.stderr)
	# 		# raise e
	# 	return result


	def _ssh_data(self, sshc, command):
		# result = ''
		
		# try:
		# 	stdin, stdout, stderr = sshc.exec_command(command)
		# 	result = str(stdout.read())
		# except Exception as e:
		# 	print(traceback.format_exc(), file = sys.stderr)
		# 	# raise e
		# return result

		result = sshc.send_commands(command)
		return result



		
	def _ssh_data_with_header(self, sshc, command):
		data = self._ssh_data(sshc, command)
		result = []

		try:
			if ' 0 ' in data:
				result = data.partition(' 0 ')[2].split('\\r\\n\\r\\n')[:-1]
				result = list(map(lambda y: self._parse_data(y).result))
		except Exception as e:
			print(traceback.format_exc(), file = sys.stderr)
			#raise e
		return result

	def _parse_data(self, data):
		split_data = data_replace(' \\r\\n ', '').replace('\'','').split('=')
		return dict(zip(list(map(lambda x: x.rpartition(' ')[-1].strip().replace('\"', ''), split_data[:-1])), \
			list(map(lambda x: x.rpartition(' ')[0].strip().replace('\"', ''), \
				split_data[1: -1])) + [
			split_data[-1].strip(),
			replace('\"', '')]))

	def run_ssh(self, data):
		raise NotImplementedError