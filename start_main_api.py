#!/usr/bin/env python3
__version__ = "2.0"
import argparse
import utilities.mikrotik_connect_ssh as mikrotik_connect_ssh
import utilities.mikrotik_commands as mikrotik_commands
import os
import sys
import pathlib

import commands.clock as Clock
import commands.dns as DNS
import commands.scheduler as Scheduler


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
		elif user_args.default_configuration:
			self.mikrotik.Get_default_configuration()
		elif user_args.system_backup:
			#print("Get_Backup")
			self.mikrotik.Get_Backup()
		elif user_args.certificate:
			#print("Get_Certificate_Create_mikrotik_ssh")
			print("{}Warning: Certificate_Create_mikrotik_ssh is enabled. It takes more time...{}\n".format('\033[33m', '\033[39m'))
			self.mikrotik.Get_Certificate_Create_mikrotik_ssh()
		elif user_args.system_reset:
			#print("Get_Reset_Configuration")
			self.mikrotik.Get_Reset_Configuration()
		elif user_args.system_time:
			print("Get_system_time")
			self.mikrotik.Get_system_clock_set_time()
		elif user_args.nordvpn:
			#print("ip ipsec nordvpn")
			print("nordvpn_CREDENTIALS","username="+user_args.nordvpn[0],"password="+user_args.nordvpn[1])
			self.mikrotik.Get_ip_ipsec_nordvpn(username=user_args.nordvpn[0],password=user_args.nordvpn[1])
		elif user_args.certificate_nordvpn:
			#print("Get_certificate_nordvpn")
			print("{}Warning: nordvpn certificate Create mikrotik is enabled. It takes more time...{}\n".format('\033[33m', '\033[39m'))
			self.mikrotik.Get_certificate_nordvpn()
		#elif user_args.firewall:
			#print("Get_ip_firewall_filter")
			#self.mikrotik.Get_ip_firewall_filter()
		elif user_args.doh:
			#print("Get_ip_dns_over_https")
			self.mikrotik.Get_ip_dns_over_https()
		elif user_args.firewall_country:
			#print("Get_ip_firewall_address_list_CountryIPBlocks")
			print("{}Warning: firewall address list CountryIPBlocks Create mikrotik is enabled. It takes more time...{}\n".format('\033[33m', '\033[39m'))
			self.mikrotik.Get_ip_firewall_address_list_CountryIPBlocks()
		elif user_args.firewall_amazon:
			print("{}Warning: firewall address list Amazon Create mikrotik is enabled. It takes more time...{}\n".format('\033[33m', '\033[39m'))
			self.mikrotik.script_utility("firewall_address_list_amazon.rsc")
		elif user_args.system_reboot:
			#print("Get system reboot")
			self.mikrotik.Get_system_reboot()
		elif user_args.system_shutdown:
			#print("Get system shutdown")
			self.mikrotik.Get_system_shutdown()
		elif user_args.system_sup_output:
			#print("Get system sup_output")
			print("{}Warning: system sup_output Create mikrotik is enabled. It takes more time...{}\n".format('\033[33m', '\033[39m'))
			self.mikrotik.Get_system_sup_output()
		elif user_args.send_command:
			#print(user_args)
			command=""
			for i in user_args.send_command:
				command+=i+" "
			self.Get_mikrotik.send_commands(command)
		elif user_args.sftp_get:
			path = pathlib.Path(user_args.sftp_get)
			remotepath = "/" + path.name
			localpath = os.path.dirname(__file__) + "/" + path.name
			self.Get_mikrotik.get_sftp_client(remotepath, localpath, get = True)
			print("path:",localpath)
		elif user_args.sftp_put:
			path = pathlib.Path(user_args.sftp_put)
			if path.exists():
				localpath = path
				remotepath = "/" + path.name
			else: ("False existing file:",path)
			self.Get_mikrotik.get_sftp_client(remotepath, localpath, get = False)
		elif user_args.dns:
			self.mikrotik.Get_dns_attack_prevention()
		elif user_args.dns_static_hosts:
			print("{}Warning: mikrotik dns static address list Create is enabled. It takes more time...{}\n".format('\033[33m', '\033[39m'))
			#self.mikrotik.script_utility(script = "dns_static_hosts.rsc")
			self.mikrotik.script_utility(script = "dns_static_hosts_ip6.rsc")
		elif user_args.main:
			self.mikrotik.main()


	def get_args(self, json_args={}):
		"""Set argparse options."""
		self.parser=argparse.ArgumentParser(add_help=False,description="Collect of useful commands for mikrotik's:")	
		#group = self.parser.add_argument_group('group1', 'group1 description')
		group = self.parser.add_mutually_exclusive_group(required = True)
		group.add_argument('-B', '--beep', dest='beep', action='store_true', default=False, help="send command :beep")
		group.add_argument('-D', '--default', dest='default_configuration', action='store_true', default=False, help="default_configuration")
		group.add_argument('-b', '--backup', dest='system_backup', action='store_true', default=False, help="mikrotik get backup")
		group.add_argument('-c', '--certificate', dest='certificate', action='store_true', default=False, help="mikrotik get certificate create ssh")
		group.add_argument('-R', '--reset', dest='system_reset', action='store_true', default=False, help="mikrotik get reset configuration")
		group.add_argument('-t', '--time', dest='system_time', action='store_true', default=False, help="mikrotik change system time")
		group.add_argument('-n', '--nordvpn', dest='nordvpn', nargs=2, type=str, help="CREDENTIALS as input separated by space: username password.")
		group.add_argument('-cn', '--certificate_nordvpn', dest='certificate_nordvpn', action='store_true', default=False, help="mikrotik get certificate nordvpn")
		#group.add_argument('-f', '--firewall', dest='firewall', action='store_true', default=False, help="mikrotik get ip firewall filter")
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
		group.add_argument('-dA', '--dns', dest='dns', action='store_true', default=False, help="mikrotik get ip dns attack prevention")
		group.add_argument('-dH', '--dns_hosts', dest='dns_static_hosts', action='store_true', default=False, help="mikrotik add addresses ip dns static hosts")
		group.add_argument('-m', '--main', dest='main', action='store_true', default=False, help='Send main commands result')
		
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
