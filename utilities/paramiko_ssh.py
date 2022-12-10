#!/usr/bin/env python3
"""
Copyright 2022. All rights reserved.
"""
__version__ = "1.4"
#1.4 get_ssh_client_results()

try:
	import paramiko
except ImportError:
	raise SystemExit("Please install paramiko, pip3 install paramiko")
import logging
import os
import utilities.utility as utility
import utilities.file as file
File = file.Main(print_result=False)

#logger= paramiko.util.logging.getLogger()
#logger.setLevel(logging.WARNING)
class Connect():
	def __init__(self, host, port, username, password, pkey_path, pkey_password, log=True):
		self.host=host
		self.port=port
		self.username=username
		self.password=password
		self.pkey_path=pkey_path
		self.pkey_password=pkey_password
		self.recv_status = "False"#exec_command
		if log:
			logging.basicConfig()
			#self.logger=logging.getLogger('paramiko')
			#self.logger.setLevel(logging.INFO)
			
			#logging.getLogger("paramiko").setLevel(logging.WARNING)
			logging.getLogger("paramiko").setLevel(logging.DEBUG)
			#logging.getLogger("paramiko").setLevel(logging.ERROR)
			#logging.getLogger("paramiko").setLevel(logging.INFO)
			#logging.getLogger("paramiko").setLevel(logging.CRITICAL)
	

	def __get_paramiko_log_path(self):
		dir_logs = os.path.expanduser('~') + "/Library/Logs/"
		log_path = dir_logs + "Paramiko/"
		if File.check_dir(log_path) is False: File.dirs_make(log_path)
		if File.check_dir(log_path): paramiko.util.log_to_file(log_path + "paramiko.log")
	

	def __get_connect__(self):
		self.__get_paramiko_log_path()
		ssh_client = paramiko.SSHClient()
		# To avoid an "unknown hosts" error. Solve this differently if you must...
		ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		if self.pkey_path is not None:
			# This mechanism uses a private key.
			#print("This mechanism uses a private key.")
			"""print("hostname is:", self.host)
			print("Username is:", self.username)
			print("Path key is:", self.pkey_path)
			print("Password key is:", self.pkey_password)"""
			if self.pkey_password is not None:
				print("This mechanism uses a private key:", self.pkey_path, " private key password:",self.password[:15]+"..."," username:",self.username,end=" ")
				self.pkey = paramiko.RSAKey.from_private_key_file(self.pkey_path,self.pkey_password)
			else:
				self.pkey = paramiko.RSAKey.from_private_key_file(self.pkey_path)
			ssh_client.connect(hostname = self.host, username = self.username, pkey = self.pkey, disabled_algorithms = dict(pubkeys=["rsa-sha2-512", "rsa-sha2-256"]), timeout = 11)
		elif self.password is None:
			print("Password is None, username:",self.username[:15]+"...",end=" ")
			ssh_client.connect(hostname=self.host,username=self.username,password="")
		else:
			print("This mechanism uses a password:",self.password[:15]+"..."," username:",self.username+"...",end=" ")
			# This mechanism uses a password.
			# Get it from cli args or a file or hard code it, whatever works best for you
			#password = self.password
			ssh_client.connect(hostname=self.host,username=self.username,
		                       # Uncomment one of the following...
		                        password=self.password
		                       # pkey=pkey
		                       )
		#print(ssh_client)
		return ssh_client
	


	def get_BaseCommand(self, command):
		ssh_client = self.__get_connect__()
		
		result = None
		try:
			# 
			# stdin , stdout, stderr = ssh_client.exec_command(command)
			# result = str(stdout.read())
			# #
			chan = ssh_client.get_transport().open_session()
			chan.exec_command(command)

			if chan.recv_exit_status() != 0:
				print(traceback.format_exc(), file = chan.recv_stderr(5000))
			else:
				stdin = chan.recv_stdin()
				stdout = chan.recv_stdout()
				stderr = chan.recv_stderr()
				result = str(stdout.read())
				return result
		except Exception as e:
			#
			print(traceback.format_exc(), file = sys.stderr)
			# #
			# print(traceback.format_exc(), file = chan.recv_stderr())
			# raise e
		return result


	def get_ssh_client(self,command):
		#print("Command is:",command)
		ssh_client=self.__get_connect__()
		# do something restricted
		# If you don't need escalated permissions, omit everything before "mkdir"
		
		#command = "echo {} | sudo -S mkdir /var/log/test_dir 2>/dev/null".format(password)
		
		# In order to inspect the exit code
		# you need go under paramiko's hood a bit
		# rather than just using "ssh_client.exec_command()"
		chan = ssh_client.get_transport().open_session()
		chan.exec_command(command)
		
		exit_status = chan.recv_exit_status()
		
		if exit_status != 0:
			stderr = chan.recv_stderr(5000)
		
		# Note that sudo's "-S" flag will send the password prompt to stderr
		# so you will see that string here too, as well as the actual error.
		# It was because of this behavior that we needed access to the exit code
		# to assert success.
			print(f"{utility.Clr.RED}Uh oh{utility.Clr.RST}")
			#self.logger.error("Uh oh")
			#self.logger.error(stderr)
			self.recv_status = "recv_status False"
			#print("self.recv_status",self.recv_status)
			return False
		else:
			#self.logger.info("Successful!")
			#logger.info("Houston, we have a ", "interesting problem", exc_info=1)
			print(f"{utility.Clr.GREEN}Successful!{utility.Clr.RST}")
			self.recv_status = "recv_status True"
			#print("self.recv_status",self.recv_status)
			return True
	

	def get_sftp_client_get(self,remotepath, localpath):
		ssh_client=self.__get_connect__()
		sftp=ssh_client.open_sftp()
		sftp.get(remotepath, localpath)
		if sftp:
			sftp.close()
			return True
		if ssh_client: ssh_client.close()
	

	def get_sftp_client_put(self,localpath, remotepath):
		ssh_client=self.__get_connect__()
		sftp=ssh_client.open_sftp()
		sftp.put(localpath, remotepath)
		if sftp:
			sftp.close()
			return True
		if ssh_client: ssh_client.close()



if __name__ == '__main__':
	import json
	configuration=json.load(open("./configuration/connect_configuration.txt"))
	get_Connect=Connect(host=configuration["connect_private_key"]["host"],
						port=configuration["connect_private_key"]["port"],
						username=configuration["connect_private_key"]["username" ],
						password=configuration["connect_private_key"]["password"],
						pkey_path=configuration["connect_private_key"]["pkey_path"],
						pkey_password=configuration["connect_private_key"]["pkey_password"],
						log=False)
	get_Connect.get_ssh_client(":beep")