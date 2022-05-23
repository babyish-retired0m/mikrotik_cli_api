#!/usr/bin/env python3
__version__ = "1.8"
import argparse
import utilities.mikrotik_connect_ssh as mikrotik_connect_ssh
import utilities.mikrotik_commands as mikrotik_commands
import os
import pathlib
class Cli_api:
	"""
	usage:
	a brief description of how the mikrotik api should be invoked on the command line.
	"""
	def __init__(self, mikrotik_parent_dir = os.path.dirname(__file__) + "/"):
		self.Get_mikrotik = mikrotik_connect_ssh.get_mikrotik_connect_ssh(mikrotik_parent_dir)
		self.mikrotik = mikrotik_commands.mikrotik_get_commands(self.Get_mikrotik)
	def get_result(self, user_args):
		"""Get the context."""
		if user_args.beep:
			#print(":beep frequency=5000 length=100ms")
			self.Get_mikrotik.send_commands(":beep frequency=5000 length=100ms")
		if user_args.system_backup:
			#print("Get_Backup")
			self.mikrotik.Get_Backup()
		if user_args.certificate:
			#print("Get_Certificate_Create_mikrotik_ssh")
			print("{}Warning: Certificate_Create_mikrotik_ssh is enabled. It takes more time...{}\n".format('\033[33m', '\033[39m'))
			self.mikrotik.Get_Certificate_Create_mikrotik_ssh()
		if user_args.system_reset:
			#print("Get_Reset_Configuration")
			self.mikrotik.Get_Reset_Configuration()
		if user_args.system_time:
			print("Get_system_time")
			self.mikrotik.Get_system_clock_set_time()
		if user_args.nordvpn:
			#print("ip ipsec nordvpn")
			print("nordvpn_CREDENTIALS","username="+user_args.nordvpn[0],"password="+user_args.nordvpn[1])
			print("{}Warning: nordvpn Create mikrotik is enabled. It takes more time...{}\n".format('\033[33m', '\033[39m'))
			self.mikrotik.Get_ip_ipsec_nordvpn(username=user_args.nordvpn[0],password=user_args.nordvpn[1])
		if user_args.certificate_nordvpn:
			#print("Get_certificate_nordvpn")
			print("{}Warning: nordvpn certificate Create mikrotik is enabled. It takes more time...{}\n".format('\033[33m', '\033[39m'))
			self.mikrotik.Get_certificate_nordvpn()
		if user_args.firewall:
			#print("Get_ip_firewall_filter")
			self.mikrotik.Get_ip_firewall_filter()
		if user_args.doh:
			#print("Get_ip_dns_over_https")
			self.mikrotik.Get_ip_dns_over_https()
		if user_args.firewall_country:
			#print("Get_ip_firewall_address_list_CountryIPBlocks")
			print("{}Warning: firewall address list CountryIPBlocks Create mikrotik is enabled. It takes more time...{}\n".format('\033[33m', '\033[39m'))
			self.mikrotik.Get_ip_firewall_address_list_CountryIPBlocks()
		if user_args.firewall_amazon:
			#print("Get_ip_firewall_address_list_amazon")
			print("{}Warning: firewall address list Amazon Create mikrotik is enabled. It takes more time...{}\n".format('\033[33m', '\033[39m'))
			self.mikrotik.Get_ip_firewall_address_list_amazon()
		if user_args.beep==False and user_args.system_backup==False and user_args.certificate==False and user_args.system_reset==False and user_args.system_time==False and user_args.nordvpn==None and user_args.certificate_nordvpn==False and user_args.firewall==False and user_args.doh==False and user_args.firewall_country==False and user_args.firewall_amazon==False and user_args.system_reboot==False and user_args.system_shutdown==False and user_args.system_sup_output==False and user_args.send_command==None and user_args.sftp_get==None and user_args.sftp_put==None:
			self.parser.print_help()
		if user_args.system_reboot:
			#print("Get system reboot")
			self.mikrotik.Get_system_reboot()
		if user_args.system_shutdown:
			#print("Get system shutdown")
			self.mikrotik.Get_system_shutdown()
		if user_args.system_sup_output:
			#print("Get system sup_output")
			print("{}Warning: system sup_output Create mikrotik is enabled. It takes more time...{}\n".format('\033[33m', '\033[39m'))
			self.mikrotik.Get_system_sup_output()
		if user_args.send_command:
			#print(user_args)
			command=""
			for i in user_args.send_command:
				command+=i+" "
			self.Get_mikrotik.send_commands(command)
		if user_args.sftp_get:
			path = pathlib.Path(user_args.sftp_get)
			remotepath = "/" + path.name
			localpath = os.path.dirname(__file__) + "/"
			self.Get_mikrotik.get_sftp_client(remotepath, localpath, get = True)
		if user_args.sftp_put:
			path = pathlib.Path(user_args.sftp_get)
			if path.exists():
				remotepath = path
				localpath = "/" + path.name
			else: ("False existing file:",p)
			self.Get_mikrotik.get_sftp_client(remotepath, localpath, get = False)
	def get_args(self, json_args={}):
		"""Set argparse options."""
		self.parser=argparse.ArgumentParser(add_help=False,description="Collect of useful commands for mikrotik's:")
		if len(json_args) > 0:
			args = self.parser.parse_args()
			setattr(args, 'beep', True)
			setattr(args, 'backup', False)
			return args		
		group = self.parser.add_argument_group('group1', 'group1 description')
		group.add_argument('-B', '--beep', dest='beep', action='store_true', default=False, help="send command :beep")
		group.add_argument('-b', '--backup', dest='system_backup', action='store_true', default=False, help="mikrotik get backup")
		group.add_argument('-c', '--certificate', dest='certificate', action='store_true', default=False, help="mikrotik get certificate create ssh")
		group.add_argument('-R', '--reset', dest='system_reset', action='store_true', default=False, help="mikrotik get reset configuration")
		group.add_argument('-t', '--time', dest='system_time', action='store_true', default=False, help="mikrotik change system time")
		group.add_argument('-n', '--nordvpn', dest='nordvpn', nargs=2, type=str, help="CREDENTIALS as input separated by space: username password.")
		group.add_argument('-cn', '--certificate_nordvpn', dest='certificate_nordvpn', action='store_true', default=False, help="mikrotik get certificate nordvpn")
		group.add_argument('-f', '--firewall', dest='firewall', action='store_true', default=False, help="mikrotik get ip firewall filter")
		group.add_argument('-d', '--doh', dest='doh', action='store_true', default=False, help="mikrotik get ip dns over https")
		group.add_argument('-fc', '--firewall_country', dest='firewall_country', action='store_true', default=False, help="mikrotik get ip firewall address list countryIPBlocks")
		group.add_argument('-fa', '--firewall_amazon', dest='firewall_amazon', action='store_true', default=False, help="mikrotik get ip firewall address list amazon")
		group.add_argument('-h', '--help', default=argparse.SUPPRESS,action='help',help="Show this help message and exit")
		group.add_argument('-v', '--version', action='version', version='%(prog)s '+ __version__)
		group.add_argument('-r', '--reboot', dest='system_reboot', action='store_true', default=False, help="mikrotik get system reboot")
		group.add_argument('-S', '--shutdown', dest='system_shutdown', action='store_true', default=False, help="mikrotik get system shutdown")
		group.add_argument('-s', '--sup_output', dest='system_sup_output', action='store_true', default=False, help="mikrotik get system sup_output")
		group.add_argument('-SC', '--send', dest='send_command', action='extend', nargs='+', type=str, help="send command as input, comment \" \\\"")
		group.add_argument('-g', '--get', dest='sftp_get', type=pathlib.Path, help="mikrotik sftp get, remote file name")
		group.add_argument('-p', '--put', dest='sftp_put', type=pathlib.Path, help="mikrotik sftp put, local file path")
		
		args = self.parser.parse_args();
		return args

if __name__ == '__main__':
	import start_main_api
	try:
		Mikrotik_cli_api = Cli_api(mikrotik_parent_dir = os.path.dirname(__file__) + "/");
		Mikrotik_cli_api.get_result(Mikrotik_cli_api.get_args(json_args={}))
	except KeyboardInterrupt:
		print('{}Canceling script...{}\n'.format('\033[33m', '\033[39m'))
		sys.exit(1)
