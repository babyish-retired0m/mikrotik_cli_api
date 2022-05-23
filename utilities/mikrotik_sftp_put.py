#!/usr/bin/env python3
__version__ = "1.0"
import json
import sys
import os

import utilities.mikrotik_connect_ssh as mikrotik_connect_ssh

class Clr:
    """Text colors."""
    RST = '\033[39m'; BLACK = '\033[30m'; RED = '\033[31m'
    GREEN = '\033[32m'; YELLOW = '\033[33m'; VIOLET = '\033[34m'
    PINK = '\033[35m'; BLUE = '\033[36m'; GREY = '\033[37m'
    BLACK2 = '\033[40m'; RST2 = '\033[49m'; RED2 = '\033[41m'
    GREEN2 = '\033[42m'; YELLOW2 = '\033[43m'; VIOLET2 = '\033[44m'
    PINK2 = '\033[45m'; BLUE2 = '\033[46m'; GREY2 = '\033[47m'
	

try:
	connect_configuration_path = os.path.expanduser('~')+"/mikrotik/connect_configuration.txt"
	commands_default_path = os.path.expanduser('~')+"/mikrotik/commands_default.txt"
	

	
	if os.path.isfile(connect_configuration_path):
		connect_configuration = json.load(open(connect_configuration_path))
		Get_mikrotik = mikrotik_connect_ssh.get_mikrotik_connect_ssh(mikrotik_parent_dir = connect_configuration["configuration"]["mikrotik_parent_dir"])
	else:
		Get_mikrotik = mikrotik_connect_ssh.get_mikrotik_connect_ssh()
	
	
	
	if len(sys.argv) != 2:
		print(f'{Clr.YELLOW2}usage:{Clr.RST2} {Clr.YELLOW}{sys.argv[0]} {Clr.BLUE}192.168.88.1.pub{Clr.RST}')
		sys.exit(1)
	else:
		localpath=str(sys.argv[1])
		print(sys.argv[1])
		directory = localpath.split('/')
		directory.reverse()
		remotepath = directory[0]
		Get_mikrotik.get_sftp_client("/"+remotepath,localpath,get=False)

except Exception as error:
		print("Authentication failed")
		print(error)