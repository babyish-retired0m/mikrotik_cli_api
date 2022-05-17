#!/usr/bin/env python3
"""
Copyright 2022. All rights reserved.
"""
__version__ = "1.0"
try:
	import paramiko
except ImportError:
	raise SystemExit("Please install paramiko, pip3 install paramiko")
import logging

class Clr:
    """Text colors."""
    RST = '\033[39m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    VIOLET = '\033[34m'
    PINK = '\033[35m'
    BLUE = '\033[36m'
    GREY = '\033[37m'
    BLACK2 = '\033[40m'
    RST2 = '\033[49m'
    RED2 = '\033[41m'
    GREEN2 = '\033[42m'
    YELLOW2 = '\033[43m'
    VIOLET2 = '\033[44m'
    PINK2 = '\033[45m'
    BLUE2 = '\033[46m'
    GREY2 = '\033[47m'

#logger= paramiko.util.logging.getLogger()
#logger.setLevel(logging.WARNING)
class Connect():
	def __init__(self, host,port,username,password,pkey_path,pkey_password,log=False):
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
	def __get_connect__(self):
		paramiko.util.log_to_file("paramiko.log")
		ssh_client = paramiko.SSHClient()
		# To avoid an "unknown hosts" error. Solve this differently if you must...
		ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		if self.pkey_path is not None:
			#print("This mechanism uses a private key.")
			# This mechanism uses a private key.
			self.pkey = paramiko.RSAKey.from_private_key_file(self.pkey_path,self.pkey_password)
			ssh_client.connect(hostname=self.host,username=self.username,pkey=self.pkey,disabled_algorithms=dict(pubkeys=["rsa-sha2-512", "rsa-sha2-256"]))
		elif self.password is None:
			print("Password is None, username:",self.username[:5]+"...",end=" ")
			ssh_client.connect(hostname=self.host,username=self.username,password="")
		else:
			print("This mechanism uses a password:",self.password[:5]+"..."," username:",self.username[:5]+"...",end=" ")
			# This mechanism uses a password.
			# Get it from cli args or a file or hard code it, whatever works best for you
			password = self.password
			ssh_client.connect(hostname=self.host,username=self.username,
		                       # Uncomment one of the following...
		                        password=self.password
		                       # pkey=pkey
		                       )
		return ssh_client
	def get_ssh_client(self,command):
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
			print(f"{Clr.RED}Uh oh{Clr.RST}")
			#self.logger.error("Uh oh")
			#self.logger.error(stderr)
			self.recv_status = "recv_status False"
			return False
		else:
			#self.logger.info("Successful!")
			#logger.info("Houston, we have a ", "interesting problem", exc_info=1)
			print(f"{Clr.GREEN}Successful!{Clr.RST}")
			self.recv_status = "recv_status True"
			return True
	def get_sftp_client_get(self,remotepath, localpath):
		ssh_client=self.__get_connect__()
		sftp=ssh_client.open_sftp()
		sftp.get(remotepath, localpath)
		if sftp: sftp.close()
		if ssh_client: ssh_client.close()
	def get_sftp_client_put(self,localpath, remotepath):
		ssh_client=self.__get_connect__()
		sftp=ssh_client.open_sftp()
		sftp.put(localpath, remotepath)
		if sftp: sftp.close()
		if ssh_client: ssh_client.close()