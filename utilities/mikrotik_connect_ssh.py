#!/usr/bin/env python3
"""
Copyright 2022. All rights reserved.
"""
__version__ = "1.2"
import os
import json
import time
import utilities.paramiko_ssh as paramiko_ssh
import utilities.openssl as openssl
import utilities.password as password


class Clr:
    """Text colors."""
    RST = '\033[39m'; BLACK = '\033[30m'; RED = '\033[31m'
    GREEN = '\033[32m'; YELLOW = '\033[33m'; VIOLET = '\033[34m'
    PINK = '\033[35m'; BLUE = '\033[36m'; GREY = '\033[37m'
    BLACK2 = '\033[40m'; RST2 = '\033[49m'; RED2 = '\033[41m'
    GREEN2 = '\033[42m'; YELLOW2 = '\033[43m'; VIOLET2 = '\033[44m'
    PINK2 = '\033[45m'; BLUE2 = '\033[46m'; GREY2 = '\033[47m'

class get_mikrotik_connect_ssh():
	"""
	mikrotik = get_mikrotik_connect_ssh(mikrotik_parent_dir = os.path.expanduser('~')+"/mikrotik/")
	mikrotik.get_sftp_client() - get_sftp_client(remotepath, localpath, get=False). get=False - get sftp, get=True - put sftp.
	mikrotik.send_commands() - send_commands(":beep frequency=5000 length=100ms"). command(s) dict, list, str.
	"""
	def __init__(self, mikrotik_parent_dir = os.path.expanduser('~')+"/mikrotik/"):
		_connect_configuration = "configuration/connect_configuration.txt"
		_commands_default_path = "configuration/commands_default.txt"
		_dir_openssl = "openssl"
		self.mikrotik_parent_dir = mikrotik_parent_dir
		self.mikrotik_parent_dir_openssl = self.mikrotik_parent_dir + _dir_openssl + "/"
		self.connect_configuration_path = self.mikrotik_parent_dir + _connect_configuration
		if os.path.isfile(self.connect_configuration_path): 
			self.connect_configuration = json.load(open(self.connect_configuration_path))
		else:
			self.connect_configuration = self.__create_connect_configuration_dict__()
		self.commands_default_path = self.mikrotik_parent_dir + _commands_default_path
		self.command_beep = ":beep frequency=5000 length=10ms"
		self.command_beep_100 = ":beep frequency=5000 length=100ms"
	def __create_connect_configuration_dict__(self):
		self.mikrotik_default_username = "admin"
		self.mikrotik_default_password = password.create(1)
		self.host = "192.168.88.1"
		self.port = "22"
		self.bit = 4096
		self.days = 256
		self.algorithm = "sha256"
		_connect_default_1, _connect_default_2 = False, False
		_connect_private_key, _commands_default = False, False
		self.connect_configuration_dict = {"configuration": {"host": self.host, "bit": self.bit,
		"days": self.days, "algorithm": self.algorithm, "mikrotik_parent_dir": self.mikrotik_parent_dir, 
		"mikrotik_parent_dir_openssl": self.mikrotik_parent_dir_openssl,
		"connect_default_1": _connect_default_1, "connect_default_2": _connect_default_2,
		"connect_private_key": _connect_private_key, "commands_default": _commands_default},
		"connect_default_1": {"host": self.host, "port": self.port, "username": self.mikrotik_default_username, "password": None,
		"pkey_path": None, "pkey_password": None, "pkey_length": None},
		"connect_default_2" : {"host": self.host, "port": self.port, "username": self.mikrotik_default_username, "password": self.mikrotik_default_password[0],
		"pkey_path": None, "pkey_password": None, "pkey_length": None},
		"connect_private_key" : {"host": self.host, "port": self.port, "username": self.mikrotik_default_username, "password": self.mikrotik_default_password[0],
		"pkey_path": None, "pkey_password": None, "pkey_length": None}}
		json.dump(self.connect_configuration_dict, fp = open(self.connect_configuration_path, 'w'), indent = 4)
		return self.connect_configuration_dict
	def __get_commands__(self, commands):
		try:
			if isinstance(commands, dict):
				for (enum,command) in enumerate(commands):
					print(Clr.YELLOW+"command #"+str(enum)+":",Clr.RST+Clr.BLUE+commands[command]+Clr.RST)
					self.__get_command__(commands[command])
			elif isinstance(commands, list):
				for (enum,command) in enumerate(commands):
					print(Clr.YELLOW+"command #"+str(enum)+":",Clr.BLUE+command+Clr.RST)
					self.__get_command__(command)
			elif isinstance(commands, str):
				print(Clr.YELLOW+"command #0:",Clr.BLUE+commands+Clr.RST)
				get_Client_command = self.__get_command__(commands)
				if get_Client_command: return True;
				else: return False
			else: print("Are instance dict, list, str?")
			return True
		except Exception as error:
			print("Commands failed"); print(error); return False
	def __get_command__(self, command):
		Client = self.__get_connect_configuration__()
		try:
			get_response = Client.get_ssh_client(command)
			#Client.get_ssh_client(self.command_beep)
			#return True if get_Client_command else return False
			if get_response is True: 
				#print(Client.recv_status)
				#print("True");
				return True;
			else:
				#print(Client.recv_status)
				#print("False");
				return False
		except Exception as error:
			print("Command failed"); print(error); return False#break
	def get_sftp_client(self, remotepath, localpath, get = False):
		Client = self.__get_connect_configuration__()
		try:
			
			if get: 
				Client.get_sftp_client_get(remotepath, localpath)
				print(Clr.GREEN+"Successful sftp! Get:",Clr.RST+remotepath)
			else:
				Client.get_sftp_client_put(localpath, remotepath)
				print(Clr.GREEN+"Successful sftp! Put:",Clr.RST+remotepath)
			Client.get_ssh_client(self.command_beep);
			return True
		except Exception as error:
			print("Command sftp failed"); print(error); return False#break
	def __get_connect_configuration__(self):
		connect_conf=self.__get_configuration__()
		host, port = connect_conf["host"], connect_conf["port"]
		username, password = connect_conf["username"], connect_conf["password"]
		pkey_path = connect_conf["pkey_path"]
		pkey_password = connect_conf["pkey_password"]
		Client=paramiko_ssh.Connect(host, port, username, password, pkey_path, pkey_password, log = False)
		return Client
	def __get_configuration__(self):
		if self.connect_configuration["configuration"]["connect_default_1"] is False: configuration = self.connect_configuration["connect_default_1"]
		elif self.connect_configuration["configuration"]["connect_default_2"] is False: configuration = self.connect_configuration["connect_default_2"]
		elif self.connect_configuration["configuration"]["connect_private_key"] is False: configuration = self.connect_configuration["connect_default_2"]
		else: configuration = self.connect_configuration["connect_private_key"]
		return configuration
	def send_commands(self, commands):
		commands_default = json.load(open(self.commands_default_path))
		#connect_configuration = json.load(open(self.connect_configuration_path))
		import os
		if os.path.isfile(self.connect_configuration_path): self.connect_configuration=json.load(open(self.connect_configuration_path))
		else:
			self.connect_configuration = self.__create_connect_configuration_dict__()
		if self.connect_configuration["configuration"]["commands_default"] is False:
			print(Clr.RED2+"Default commands are False"+Clr.RST2)
			if self.connect_configuration["configuration"]["connect_default_1"] is False:
				commands_default["commands_default_1"]["user_password_access"] = "/user set 0 password=\""+self.connect_configuration["connect_default_2"]["password"]+"\""
				if self.__get_commands__(commands_default["commands_default_1"]) is True:
					self.connect_configuration["configuration"]["connect_default_1"] = True
					#connect_configuration["connect_default_2"]["password"] = commands_default
					json.dump(self.connect_configuration, fp = open(self.connect_configuration_path, 'w'), indent = 4)
			if self.connect_configuration["configuration"]["connect_default_2"] is False:
				commands_default["commands_default_2"]["system_clock"] = "/system clock set date="+time.strftime("%b/%d/%Y", time.localtime()).lower()+" time="+time.strftime("%H:%M:%S", time.localtime())
				if self.__get_commands__(commands_default["commands_default_2"]) is True:
					self.connect_configuration["configuration"]["connect_default_2"] = True
					self.connect_configuration["configuration"]["commands_default"] = True
					#connect_configuration["configuration"]["connect_private_key"] = True
					json.dump(self.connect_configuration, fp = open(self.connect_configuration_path, 'w'), indent = 4)
			if commands: self.__get_commands__(commands)
			else: print("Are list of command(s) dict, list, str?");
		else:
			get_response = self.__connect_default__(commands)
			if get_response: 
				#print("True"); 
				return True
			else: 
				#print("False");
				return False
			
	def __connect_default__(self, commands):
		connect_configuration = json.load(open(self.connect_configuration_path))
		if connect_configuration["configuration"]["connect_private_key"] is True:
			if commands:
				get_commands = self.__get_commands__(commands); 
				return True
			else: 
				print("Are list of command(s) dict, list, str?"); 
				return False
		else:
			print(Clr.RED2+"Connect private key is False"+Clr.RST2)
			if commands: get_commands = self.__get_commands__(commands); return True
			else: print("Are list of command(s) dict, list, str?"); return False

if __name__ == '__main__':
	import json
	import os
	import mikrotik_connect_ssh
	
	if os.path.isfile(os.path.expanduser('~')+"/mikrotik/connect_configuration.txt"):
		connect_configuration = json.load(open(connect_configuration_path))
		Get_mikrotik = mikrotik_connect_ssh.get_mikrotik_connect_ssh(mikrotik_parent_dir = connect_configuration["configuration"]["mikrotik_parent_dir"])
	else: Get_mikrotik = mikrotik_connect_ssh.get_mikrotik_connect_ssh()
	
	Get_mikrotik.send_commands(":beep frequency=5000 length=100ms")