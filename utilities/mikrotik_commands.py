#!/usr/bin/env python3
"""
Copyright 2022. All rights reserved.
"""
__version__ = "1.0"

import json
import sys
import time
#import os
import utilities.password as password
import utilities.openssl as openssl
import utilities.file as file

class mikrotik_get_commands():
	def __init__(self, object):
		self.mikrotik = object
		self.mikrotik_connect_configuration = self.mikrotik.connect_configuration
		#self.Get_system_clock_set_time()
	def __Mikrotik_Connect_Configuration_Load__(self, path):
		return json.load(open(path))
	def __Mikrotik_Connect_Configuration_Dump__(self, mikrotik_connect_configuration):
		json.dump(mikrotik_connect_configuration, fp=open(self.mikrotik.connect_configuration_path,'w'),indent=4);
		print("Mikrotik Connect Configuration Dumped")
	def Get_Backup(self):
		mikrotik_backup_name=time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
		mikrotik_backup_password, mikrotik_backup_password_length, mikrotik_backup_password_time_to_generate = password.create(1)
		mikrotik_backup_password=mikrotik_backup_password[:21]
		self.mikrotik.send_commands([f"system backup save encryption=aes-sha256 name={mikrotik_backup_name} password=\"{mikrotik_backup_password}\"",f":log info \"mikrotik backup jobs done, name={mikrotik_backup_name}\""])
		self.mikrotik.get_sftp_client(f"/{mikrotik_backup_name}.backup",f"{self.mikrotik.mikrotik_parent_dir}{mikrotik_backup_name}.backup",get=True)
	def __Get_Certificate_Create_mikrotik_ssh_get_config__(self):
		mikrotik_certificate = openssl.Create_Certificate(domain=self.mikrotik.connect_configuration["configuration"]["host"], bit=self.mikrotik.connect_configuration["configuration"]["bit"], days=self.mikrotik.connect_configuration["configuration"]["days"], algorithm=self.mikrotik.connect_configuration["configuration"]["algorithm"], parent_dir=self.mikrotik.connect_configuration["configuration"]["mikrotik_parent_dir_openssl"])
		mikrotik_certificate_config_path = mikrotik_certificate.All()
		return self.__Mikrotik_Connect_Configuration_Load__(mikrotik_certificate_config_path)
	def Get_Certificate_Create_mikrotik_ssh(self):
		mikrotik_certificate_config = self.__Get_Certificate_Create_mikrotik_ssh_get_config__()
		mikrotik_username_private_key = self.mikrotik.connect_configuration["connect_private_key"]["username"]
		passphrase = password.create(1); mikrotik_password = passphrase[0][14:]
		mikrotik_username_new = time.strftime("%Y-%m-%d_%H-%M", time.localtime())+"_"+passphrase[0][:14]
		if self.mikrotik.get_sftp_client("/"+mikrotik_certificate_config["key"]["pub"]["name"],mikrotik_certificate_config["key"]["pub"]["path"],get=False):
			if self.mikrotik.send_commands("/system script add name=user_add source=\":execute {/user add address=192.168.88.0/24 group=full name=\\\""+mikrotik_username_new+"\\\" password=\\\""+mikrotik_password+"\\\";:log info \\\"user "+mikrotik_username_new[:16]+"... added\\\";:beep;/user/ssh-keys/import public-key-file="+mikrotik_certificate_config['key']['pub']['name']+"  user="+mikrotik_username_new+";:log info \\\"public-key-file imported user "+mikrotik_username_new+"\\\";:beep;}\""):
				print("user/ssh-key public-key-file imported")
				if self.mikrotik.send_commands("/system/script run user_add;:beep"):
					self.mikrotik.send_commands(":log info \"script run user_add\";:beep"); print("user "+mikrotik_username_new[:16]+"... added")
					if self.mikrotik.send_commands("/system/script remove user_add;:beep"):
						self.mikrotik.send_commands(":log info \"script user_add removed\";:beep"); print("script user_add removed")
						if self.mikrotik.send_commands("/user remove \""+mikrotik_username_private_key+"\";:beep"):
							print("user "+mikrotik_username_private_key[:16]+" removed")
							self.mikrotik.connect_configuration["configuration"]["connect_private_key"] = True
							self.mikrotik.connect_configuration["connect_private_key"]["username"] = mikrotik_username_new
							self.mikrotik.connect_configuration["connect_private_key"]["password"] = mikrotik_password
							self.mikrotik.connect_configuration["connect_private_key"]["pkey_path"] = mikrotik_certificate_config["key"]["private_key"]["path"]
							self.mikrotik.connect_configuration["connect_private_key"]["pkey_password"] = mikrotik_certificate_config["key"]["private_key"]["password"]
							self.mikrotik.connect_configuration["connect_private_key"]["pkey_length"] = len(self.mikrotik.connect_configuration["connect_private_key"]["pkey_password"])
							self.__Mikrotik_Connect_Configuration_Dump__(self.mikrotik.connect_configuration)
							self.mikrotik.send_commands(":log info \"user "+mikrotik_username_private_key[:16]+" removed\";:beep")
							self.__Get_Create_mikrotik_ssh_zsh__()
						else: sys.exit(1)
					else: sys.exit(1)
				else: sys.exit(1)
			else: sys.exit(1)
		else: sys.exit(1)
		
	def __Get_Create_mikrotik_ssh_zsh__(self):
		file.write_text(self.mikrotik.connect_configuration["configuration"]["mikrotik_parent_dir"]+"zsh.txt","ssh -i "+self.mikrotik.connect_configuration["connect_private_key"]["pkey_path"]+" "+self.mikrotik.connect_configuration["connect_private_key"]["username"]+"@"+self.mikrotik.connect_configuration["connect_private_key"]["host"]+"\n"+self.mikrotik.connect_configuration["connect_private_key"]["pkey_password"])
		
	def Get_Reset_Configuration(self):
		import sys
		self.mikrotik.send_commands(":beep;/system script add name=system_reset_configuration source=\":execute {:beep;/system/reset-configuration;:delay 1;:put y;}\"")
		if self.mikrotik.send_commands(":beep;/system script run system_reset_configuration"):
			self.mikrotik.connect_configuration["configuration"]["connect_default_1"] = False
			self.mikrotik.connect_configuration["configuration"]["connect_default_2"] = False
			self.mikrotik.connect_configuration["configuration"]["commands_default"] = False
			self.mikrotik.connect_configuration["configuration"]["connect_private_key"] = False
			self.mikrotik.connect_configuration["connect_private_key"]["username"] = self.mikrotik.connect_configuration["connect_default_2"]["username"]
			self.mikrotik.connect_configuration["connect_private_key"]["password"] = self.mikrotik.connect_configuration["connect_default_2"]["password"]
			self.mikrotik.connect_configuration["connect_private_key"]["pkey_path"] = None
			self.mikrotik.connect_configuration["connect_private_key"]["pkey_password"] = None
			self.__Mikrotik_Connect_Configuration_Dump__(self.mikrotik.connect_configuration)
		else: sys.exit(1)
	def Get_system_clock_set_time(self):
		import time
		mikrotik_system_time=time.strftime("%H:%M:%S", time.localtime())
		mikrotik_system_date=time.strftime("%b/%d/%Y", time.localtime())
		self.mikrotik.send_commands(f"/system clock set date={mikrotik_system_date.lower()} time={mikrotik_system_time};:beep")
	def Get_certificate_nordvpn(self):
		self.mikrotik.send_commands("/certificate/remove LocalCA;:beep")
		self.mikrotik.send_commands("/certificate/add name=LocalCA common-name=LocalCA key-usage=key-cert-sign,crl-sign key-size=4096 days-valid=256 digest-algorithm=sha512 trusted=yes country=PA state=PA organization=NordVPN locality=PA unit=PA;:beep")
		self.mikrotik.send_commands("/certificate/sign LocalCA;:beep")
		self.mikrotik.send_commands("/certificate/remove GeneratedNordVPN;:beep")
		self.mikrotik.send_commands("/certificate/add name=GeneratedNordVPN common-name=\"NordVPN CA\" key-usage=key-cert-sign,crl-sign key-size=4096 days-valid=256 digest-algorithm=sha512 trusted=yes country=PA state=PA organization=NordVPN locality=PA unit=PA;:beep")
		self.mikrotik.send_commands("/certificate sign GeneratedNordVPN ca=LocalCA;:beep")
		self.mikrotik.get_sftp_client("/" + "nordvpn_root.der", self.mikrotik.mikrotik_parent_dir + "nordvpn.com/" + "nordvpn_root.der",get=False)
		self.mikrotik.send_commands("/certificate import file-name=nordvpn_root.der name=nordvpn_root passphrase=\"\";:beep")
		self.mikrotik.send_commands("/ip/ipsec/identity/set 0 certificate=nordvpn_root;:beep")
		#self.mikrotik.send_commands("/certificate add common-name=\"NordVPN CA\" country=PA days-valid=256 digest-algorithm=sha512 key-size=4096 key-usage=ipsec-end-system,ipsec-tunnel,ipsec-user name=GeneratedNordVPN organization=NordVPN trusted=yes")
		#self.mikrotik.send_commands("/certificate sign GeneratedNordVPN")
	def Get_ip_ipsec_nordvpn(self,username="NordVPNuserCREDENTIALS",password="NordVPNuserCREDENTIALS"):
		self.Get_certificate_nordvpn()
		self.mikrotik.send_commands("/ip ipsec profile add name=NordVPN;:beep")
		self.mikrotik.send_commands("/ip ipsec proposal add name=NordVPN pfs-group=none;:beep")
		self.mikrotik.send_commands("/ip ipsec policy group add name=NordVPN;:beep")
		self.mikrotik.send_commands("/ip ipsec policy add dst-address=0.0.0.0/0 group=NordVPN proposal=NordVPN src-address=0.0.0.0/0 template=yes;:beep")
		self.mikrotik.send_commands("/ip ipsec mode-config add name=NordVPN responder=no;:beep")
		self.mikrotik.send_commands("/ip ipsec peer add address=pl210.nordvpn.com exchange-mode=ike2 name=NordVPN profile=NordVPN;:beep")
		self.mikrotik.send_commands("/ip ipsec identity add auth-method=eap certificate=\"GeneratedNordVPN\" eap-methods=eap-mschapv2 generate-policy=port-strict mode-config=NordVPN peer=NordVPN policy-template-group=NordVPN username=\""+username+"\" password=\""+password+"\";:beep")
		self.mikrotik.send_commands("/ip firewall address-list add address=192.168.88.0/24 list=local;:beep")
		self.mikrotik.send_commands("/ip ipsec mode-config set [find name=NordVPN] src-address-list=local;:beep")
		self.__Get_import_nordvpn_servers__()
		self.__Get_system_script_nordvpn_run__()
		self.__Get_system_scheduler_nordvpn__()
	def __Get_import_nordvpn_servers__(self):
		self.mikrotik.get_sftp_client("/" + "nordvpn.com_Standard_VPN_servers_dns_static.rsc", self.mikrotik.mikrotik_parent_dir + "nordvpn.com/" + "nordvpn.com_Standard_VPN_servers_dns_static.rsc",get=False)
		self.mikrotik.send_commands(":beep;import nordvpn.com_Standard_VPN_servers_dns_static.rsc;:beep")
		self.mikrotik.get_sftp_client("/" + "nordvpn.com_Standard_VPN_servers_firewall_address_list.rsc", self.mikrotik.mikrotik_parent_dir + "nordvpn.com/" + "nordvpn.com_Standard_VPN_servers_firewall_address_list.rsc",get=False)
		self.mikrotik.send_commands(":beep;import nordvpn.com_Standard_VPN_servers_firewall_address_list.rsc;:beep")
		self.mikrotik.get_sftp_client("/" + "nordvpn.com_Standard_VPN_servers_ipsec_peer.rsc", self.mikrotik.mikrotik_parent_dir + "nordvpn.com/" + "nordvpn.com_Standard_VPN_servers_ipsec_peer.rsc",get=False)
		self.mikrotik.send_commands(":beep;import nordvpn.com_Standard_VPN_servers_ipsec_peer.rsc;:beep")
		#Ukraine:local myrnd [:rndnum from=3512 to=3521];
		self.mikrotik.send_commands("/system/script add	name=\"nordvpn\" source=\":execute {:local myrnd [:rndnum from=0 to=4873];\\n/ip ipsec peer set [find disabled=no] disabled=yes;\\n/ip ipsec peer set [find name=\$myrnd] disabled=no;\\n/ip ipsec identity set 0 peer=\$myrnd;\\n:log info \\\"ip_ipsec_nordvpn peer \$myrnd\\\";\\n:beep;}\";:beep")
	def __Get_system_script_nordvpn_run__(self):
		self.mikrotik.send_commands("/system/script run nordvpn;:beep")
	def __Get_system_scheduler_nordvpn__(self):
		self.mikrotik.send_commands("/system/scheduler add name=NordVPN_Day interval=30m start-time=05:30:00 on-event=nordvpn;:beep")
		self.mikrotik.send_commands("/system/scheduler add name=NordVPN_Night interval=60m start-time=21:30:00 on-event=nordvpn;:beep")
		self.mikrotik.send_commands("/system/script/add name=nordvpnday2 source=\":execute {/system/scheduler set NordVPN_Night disabled=yes;}\";:beep")
		self.mikrotik.send_commands("/system/script/add name=nordvpnnight2 source=\":execute {/system/scheduler set NordVPN_Day disabled=yes;}\";:beep")
		self.mikrotik.send_commands("/system/scheduler add name=NordVPN_Day2 interval=1d start-time=05:30:00 on-event=nordvpnday2;:beep")
		self.mikrotik.send_commands("/system/scheduler add name=NordVPN_Night2 interval=1d start-time=21:30:00 on-event=nordvpnnight2;:beep")
	def Get_ip_firewall_filter(self):
		self.mikrotik.send_commands("/ip firewall filter add chain=forward action=accept protocol=tcp src-address=192.168.88.0/24 dst-address=0.0.0.0/0 dst-port=53 comment=\"traffic\";:beep")
		self.mikrotik.send_commands("/ip firewall filter add chain=forward action=accept protocol=udp src-address=192.168.88.0/24 dst-address=0.0.0.0/0 dst-port=53 comment=\"traffic\";:beep")
		self.mikrotik.send_commands("/ip firewall filter add chain=forward action=drop protocol=tcp src-address=192.168.88.0/24 dst-address=0.0.0.0/0 dst-port=80 comment=\"traffic\";:beep")
		self.mikrotik.send_commands("/ip firewall filter add chain=forward action=accept protocol=tcp src-address=192.168.88.0/24 dst-address=0.0.0.0/0 dst-port=443 comment=\"traffic\";:beep")
	def Get_ip_dns_over_https(self):
		self.mikrotik.send_commands("/ip/dns static add address=104.16.248.249 name=cloudflare-dns.com type=A comment=cloudflare;:beep")
		self.mikrotik.send_commands("/ip/dns static add address=104.16.249.249 name=cloudflare-dns.com type=A comment=cloudflare;:beep")
		self.mikrotik.send_commands("/ip/dns static add address=2606:4700::6810:f9f9 name=cloudflare-dns.com type=AAAA comment=cloudflare;:beep")
		self.mikrotik.send_commands("/ip/dns static add address=2606:4700::6810:f8f9 name=cloudflare-dns.com type=AAAA comment=cloudflare;:beep")
		self.mikrotik.get_sftp_client("cacert.pem", self.mikrotik.mikrotik_parent_dir + "configuration/cacert.pem",get=False)
		self.mikrotik.send_commands(":beep;/certificate import file-name=\"cacert.pem\" passphrase=\"\";:beep")
		self.mikrotik.send_commands("/ip/dns set servers=104.16.248.249,104.16.249.249 use-doh-server=\"https://cloudflare-dns.com/dns-query\" verify-doh-cert=yes;:beep")
	def Get_ip_firewall_address_list_CountryIPBlocks(self):
		self.mikrotik.get_sftp_client("/" + "CountryIPBlocks_IP-Firewall-Address-List.rsc", self.mikrotik.mikrotik_parent_dir + "firewall/" + "CountryIPBlocks_IP-Firewall-Address-List.rsc",get=False)
		self.mikrotik.get_sftp_client("/" + "CountryIPBlocks_PubFirewall.rsc", self.mikrotik.mikrotik_parent_dir + "firewall/" + "CountryIPBlocks_PubFirewall.rsc",get=False)
		self.mikrotik.send_commands(":beep;/import file-name=CountryIPBlocks_IP-Firewall-Address-List.rsc;:beep")
		self.mikrotik.send_commands(":beep;/import file-name=CountryIPBlocks_PubFirewall.rsc;:beep")
	def Get_ip_firewall_address_list_amazon(self):
		self.mikrotik.get_sftp_client("/" + "amazon.rsc", self.mikrotik.mikrotik_parent_dir + "firewall/" + "amazon.rsc",get=False)
		self.mikrotik.send_commands(":beep;/import file-name=amazon.rsc;:beep")
		self.mikrotik.send_commands("/ip/firewall/filter add chain=forward action=drop src-address-list=amazon comment=\"address-list\";:beep")
		self.mikrotik.send_commands("/ip/firewall/filter add chain=input action=drop src-address-list=amazon comment=\"address-list\";:beep")
	def Get_system_reboot(self):
		if self.mikrotik.send_commands(":beep;/system/script run system_reboot"):
			print("system rebooted")
	def Get_system_shutdown(self):
		if self.mikrotik.send_commands(":beep;/system/script run system_shutdown"):
			print("system shutdowned")
	def Get_system_sup_output(self):
		name="supout_"+time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())+".rif"
		self.mikrotik.send_commands(":beep;system/sup-output name=\""+name+"\";:beep")
		self.mikrotik.get_sftp_client("/"+name,self.mikrotik.mikrotik_parent_dir + "backup/" + name,get=True)
		print("system sup-output:",self.mikrotik.mikrotik_parent_dir + "backup/" + name)
		self.mikrotik.send_commands("/file/remove "+name+";:log \"change time\";:beep;")
if __name__ == '__main__':
	import json
	import sys
	import os
	import mikrotik_connect_ssh
	import mikrotik_commands
	connect_configuration_path = os.path.expanduser('~')+"/mikrotik/connect_configuration.txt"

	try:
		if os.path.isfile(connect_configuration_path):
			connect_configuration = json.load(open(connect_configuration_path))
			Get_mikrotik = mikrotik_connect_ssh.get_mikrotik_connect_ssh(mikrotik_parent_dir = connect_configuration["configuration"]["mikrotik_parent_dir"])
		else:
			Get_mikrotik = mikrotik_connect_ssh.get_mikrotik_connect_ssh()
		#Get_mikrotik.send_commands(":beep frequency=5000 length=100ms")
		mikrotik = mikrotik_commands.mikrotik_get_commands(Get_mikrotik)
		#mikrotik.Get_Certificate_Create_mikrotik_ssh()
		#mikrotik.Get_Backup()
	except KeyboardInterrupt:
		print('{}Canceling script...{}\n'.format('\033[33m', '\033[39m'))
		sys.exit(1)