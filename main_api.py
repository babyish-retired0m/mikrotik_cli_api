#!/usr/bin/env python3
__version__ = "1.0"
import argparse
import utilities.mikrotik_connect_ssh as mikrotik_connect_ssh
import utilities.mikrotik_commands as mikrotik_commands
	
class Checker:
	"""
	usage:
	a brief description of how the mikrotik api should be invoked on the command line.
	"""
	def __init__(self):
		Get_mikrotik = mikrotik_connect_ssh.get_mikrotik_connect_ssh()
		mikrotik = mikrotik_commands.mikrotik_get_commands(Get_mikrotik)
	def get_result(self, user_args):
		Get_mikrotik = mikrotik_connect_ssh.get_mikrotik_connect_ssh()
		mikrotik = mikrotik_commands.mikrotik_get_commands(Get_mikrotik)
		"""Get the context."""
		if user_args.beep:
			print(":beep frequency=5000 length=100ms")
			Get_mikrotik.send_commands(":beep frequency=5000 length=100ms")
		if user_args.system_backup:
			print("Get_Backup")
			mikrotik.Get_Backup()
		if user_args.certificate:
			print("Get_Certificate_Create_mikrotik_ssh")
			mikrotik.Get_Certificate_Create_mikrotik_ssh()
		if user_args.system_reset:
			print("Get_Reset_Configuration")
			mikrotik.Get_Reset_Configuration()
		if user_args.system_time:
			print("Get_system_time")
			mikrotik.Get_system_clock_set_time()
		if user_args.nordvpn:
			print("ip ipsec nordvpn")
			print("nordvpn_CREDENTIALS","username="+user_args.nordvpn[0],"password="+user_args.nordvpn[1])
			#mikrotik.Get_ip_ipsec_nordvpn(username=user_args.nordvpn[0],password=user_args.nordvpn[1])
		if user_args.certificate_nordvpn:
			print("Get_certificate_nordvpn")
			mikrotik.Get_certificate_nordvpn()
		if user_args.firewall:
			print("Get_ip_firewall_filter")
			mikrotik.Get_ip_firewall_filter()
		if user_args.doh:
			print("Get_ip_dns_over_https")
			mikrotik.Get_ip_dns_over_https()
		if user_args.firewall_country:
			print("Get_ip_firewall_address_list_CountryIPBlocks")
			mikrotik.Get_ip_firewall_address_list_CountryIPBlocks()
		if user_args.firewall_amazon:
			print("Get_ip_firewall_address_list_amazon")
			mikrotik.Get_ip_firewall_address_list_amazon()
			#username="NordVPNuserCREDENTIALS",password="NordVPNuserCREDENTIALS"
		if user_args.beep==False and user_args.system_backup==False and user_args.certificate==False and user_args.system_reset==False and user_args.system_time==False and user_args.nordvpn==None and user_args.certificate_nordvpn==False and user_args.firewall==False and user_args.doh==False and user_args.firewall_country==False and user_args.firewall_amazon==False and user_args.system_reboot==False and user_args.system_shutdown==False and user_args.system_sup_output==False and user_args.send_command==None:
			self.parser.print_help()
		if user_args.system_reboot:
			print("Get system reboot")
			mikrotik.Get_system_reboot()
		if user_args.system_shutdown:
			print("Get system shutdown")
			mikrotik.Get_system_shutdown()
		if user_args.system_sup_output:
			print("Get system sup_output")
			mikrotik.Get_system_sup_output()
		if user_args.send_command:
			Get_mikrotik.send_commands(user_args.send_command[0])
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
		group.add_argument('-SC', '--send', dest='send_command', nargs=1, type=str, help="send command as input separated by space.")
		
		args = self.parser.parse_args();
		return args

if __name__ == '__main__':
	import sys
	import main_api
	try:
		CheckerObject = Checker();
		CheckerObject.get_result(CheckerObject.get_args(json_args={}))
	except KeyboardInterrupt:
		print('{}Canceling script...{}\n'.format('\033[33m', '\033[39m'))
		sys.exit(1)