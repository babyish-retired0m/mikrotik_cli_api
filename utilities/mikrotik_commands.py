#!/usr/bin/env python3
"""
Copyright 2022. All rights reserved.
"""
__version__ = "1.3"

import json
import sys
import time
#import os
import utilities.password as password
import utilities.openssl as openssl
import utilities.file as file
File = file.Main(print_result=False)

import pathlib



class mikrotik_get_commands():
	def __init__(self, object):
		self.mikrotik = object
		self.mikrotik_connect_configuration = self.mikrotik.connect_configuration
		#self.Get_system_clock_set_time()
	def __Mikrotik_Connect_Configuration_Load__(self, path):
		return json.load(open(path))
	def __Mikrotik_Connect_Configuration_Dump__(self, mikrotik_connect_configuration):
		json.dump(mikrotik_connect_configuration, fp = open(self.mikrotik.connect_configuration_path, 'w'),indent = 4);
		print("Mikrotik Connect Configuration Dumped")
	def Get_Backup(self):
		mikrotik_backup_name = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
		mikrotik_backup_password, mikrotik_backup_password_length, mikrotik_backup_password_time_to_generate = password.create(1)
		mikrotik_backup_password = mikrotik_backup_password[:21]
		if self.mikrotik.send_commands([f"system backup save encryption=aes-sha256 name={mikrotik_backup_name} password=\"{mikrotik_backup_password}\"",f":log info \"mikrotik backup jobs done, name={mikrotik_backup_name}\""]):
			if self.mikrotik.get_sftp_client(f"/{mikrotik_backup_name}.backup", f"{self.mikrotik.mikrotik_parent_dir}{mikrotik_backup_name}.backup",get=True):
				if File.write_text(self.mikrotik.mikrotik_parent_dir + mikrotik_backup_name + "_password.txt", mikrotik_backup_password):
					print("Backup path:",self.mikrotik.mikrotik_parent_dir + mikrotik_backup_name)
					print("Backup password path:",self.mikrotik.mikrotik_parent_dir + mikrotik_backup_name + "_password.txt")
					print("Backup password:", mikrotik_backup_password)
	
	def Get_Certificate_Create_mikrotik_ssh(self):
		def __get_create_certificate_ssh_get_config__():
			mikrotik_certificate = openssl.Create_Certificate(domain = self.mikrotik.connect_configuration["configuration"]["host"], bit = self.mikrotik.connect_configuration["configuration"]["bit"], days = self.mikrotik.connect_configuration["configuration"]["days"], algorithm = self.mikrotik.connect_configuration["configuration"]["algorithm"], parent_dir = self.mikrotik.connect_configuration["configuration"]["mikrotik_parent_dir_openssl"])
			mikrotik_certificate_config_path = mikrotik_certificate.All()
			return self.__Mikrotik_Connect_Configuration_Load__(mikrotik_certificate_config_path)
		mikrotik_certificate_config = __get_create_certificate_ssh_get_config__()
		mikrotik_username_private_key = self.mikrotik.connect_configuration["connect_private_key"]["username"]
		passphrase = password.create(1); mikrotik_password = passphrase[0][14:]
		mikrotik_username_new = time.strftime("%Y-%m-%d_%H-%M", time.localtime()) + "_"+ mikrotik_password
		if self.mikrotik.get_sftp_client("/"+mikrotik_certificate_config["key"]["pub"]["name"],mikrotik_certificate_config["key"]["pub"]["path"],get=False):
			if self.mikrotik.send_commands(":local o [/system/script find name=user_add];:if ([:len $o] != 0) do={/system/script remove user_add;:log info \"script user_add removed\";:beep;};/system script add name=user_add source=\":execute {/user add address=192.168.88.0/24 group=full name=\\\""+mikrotik_username_new+"\\\" password=\\\""+mikrotik_password+"\\\";:log info \\\"user "+mikrotik_username_new[:16]+"... added\\\";:beep;/user/ssh-keys/import public-key-file="+mikrotik_certificate_config['key']['pub']['name']+" user="+mikrotik_username_new+";:log info \\\"public-key-file imported user "+mikrotik_username_new+"\\\";:beep;}\""):
				print("user/ssh-key public-key-file imported")
				if self.mikrotik.send_commands("/system/script run user_add;:log info \"script run user_add\";:beep"):
					print("user "+mikrotik_username_new[:16]+"... added")
					if self.mikrotik.send_commands("/system/script remove user_add;:log info \"script user_add removed\";:beep"):
						print("script user_add removed")
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
		File.write_text(self.mikrotik.connect_configuration["configuration"]["mikrotik_parent_dir"]+"zsh.txt","ssh -i "+self.mikrotik.connect_configuration["connect_private_key"]["pkey_path"]+" "+self.mikrotik.connect_configuration["connect_private_key"]["username"]+"@"+self.mikrotik.connect_configuration["connect_private_key"]["host"]+"\n"+self.mikrotik.connect_configuration["connect_private_key"]["pkey_password"])
		
	def Get_Reset_Configuration(self):
		#self.mikrotik.send_commands(":beep;/system script add name=system_reset_configuration source=\":execute {:beep;/system/reset-configuration;:delay 1;:put y;}\"")
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
		mikrotik_system_time = time.strftime("%H:%M:%S", time.localtime())
		mikrotik_system_date = time.strftime("%b/%d/%Y", time.localtime())
		self.mikrotik.send_commands(f"/system clock set date={mikrotik_system_date.lower()} time={mikrotik_system_time};:beep")
	
	def Get_ip_ipsec_nordvpn(self, username = "NordVPNuserCREDENTIALS", password = "NordVPNuserCREDENTIALS"):	
		__generate_certificate_nordvpn__()
		__import_nordvpn_servers__()
		__script_nordvpn_run__()
		self.mikrotik.send_commands("/ip ipsec identity add auth-method=eap certificate=\"GeneratedNordVPN\" eap-methods=eap-mschapv2 generate-policy=port-strict mode-config=NordVPN peer=Canada_36 policy-template-group=NordVPN username=\"" + username + "\" password=\"" + password + "\";:beep")
		__scheduler_nordvpn__()
		def __generate_certificate_nordvpn__():
			self.script_utility("script_certificate_LocalCA.rsc")
			self.script_utility("script_certificate_GeneratedNordVPN.rsc")
			if self.mikrotik.get_sftp_client("/" + "nordvpn_root.der", self.mikrotik.mikrotik_parent_dir + "nordvpn.com/" + "nordvpn_root.der", get=False):
				self.mikrotik.send_commands("/certificate import file-name=nordvpn_root.der name=nordvpn_root passphrase=\"\";:beep")
				#self.mikrotik.send_commands("/ip/ipsec/identity/set 0 certificate=nordvpn_root;:beep")
			else: sys.exit(1)
		def __import_nordvpn_servers__():
			script_files = ["nordvpn.com_Standard_VPN_servers_ipsec_peer_country.rsc", "nordvpn.com_Standard_VPN_servers_dns_static_country.rsc", "nordvpn.com_Standard_VPN_servers_firewall_address_list_country.rsc"]
			for script in script_files: self.script_utility(script)
		def __script_nordvpn_run__():
			self.script_utility("script_NordVPN.rsc")
		def __scheduler_nordvpn__():
			self.script_utility("scheduler_NordVPN.rsc")
			self.script_utility("script_NordVPNNight.rsc")
			self.script_utility("script_NordVPNDay.rsc")
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
		self.mikrotik.get_sftp_client("cacert.pem", self.mikrotik.mikrotik_parent_dir + "configuration/cacert.pem", get=False)
		self.mikrotik.send_commands(":beep;/certificate import file-name=\"cacert.pem\" passphrase=\"\";:beep")
		self.mikrotik.send_commands("/ip/dns set servers=104.16.248.249,104.16.249.249 use-doh-server=\"https://cloudflare-dns.com/dns-query\" verify-doh-cert=yes allow-remote-requests=yes;:beep")
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
		if self.mikrotik.send_commands(":beep;/system/script run system_reboot"): print("system rebooted")
	def Get_system_shutdown(self):
		if self.mikrotik.send_commands(":beep;/system/script run system_shutdown"): print("system shutdowned")
	def Get_system_sup_output(self):
		name="supout_"+time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())+".rif"
		self.mikrotik.send_commands(":beep;system/sup-output name=\""+name+"\";:beep")
		self.mikrotik.get_sftp_client("/"+name,self.mikrotik.mikrotik_parent_dir + "backup/" + name,get=True)
		print("system sup-output:",self.mikrotik.mikrotik_parent_dir + "backup/" + name)
		self.mikrotik.send_commands("/file/remove "+name+";:log \"change time\";:beep;")
	def Get_default_configuration(self):
		"""listing_files = File.dir_listing_files_in_this_directory_tree(path = self.mikrotik.mikrotik_parent_dir + "scripts/default_configuration", file_extension = "rsc")
		#listing_files = ["script_ip_firewall_filter_rev_1.0.rsc"]
		#listing_files.extend(path)
		for path in listing_files: 
			#print(path)
			print(path.name); 
			#if path.name != "script_system_reboot.rsc" and path.name != "script_system_reset_configuration.rsc" and path.name != "script_system_shutdown.rsc": self.Get_script(path.name)"""
		script_files = ["script_default_configuration_2.rsc",
								"script_ip_firewall_filter_rev_1.0.rsc",
								"script_dns_attack_prevention_rev_4.0.rsc",
								"script_ssh_regenerate_host_key.rsc",
								"script_system_reboot.rsc",
								"script_system_reset_configuration.rsc",
								"script_system_shutdown.rsc",
								"script_certificate_LocalCA.rsc",
								"script_certificate_GeneratedNordVPN.rsc"
								]
		for script in script_files:
			get_script_utility = self.script_utility(script)
	
	def script_utility(self, script, run = True):
		self.script = script
		self.script_run = run
		self.script_system_list = ["script_system_reboot.rsc", "script_system_reset_configuration.rsc", "script_system_shutdown.rsc"]
		def __script_remove__():
			return True if self.mikrotik.send_commands("/system/script remove \"" + self.script_name + "\"") else False
		def __script_import__():
			return True if self.mikrotik.send_commands("import " + self.script) else False
		def __script_check__():
			return True if self.script.startswith("script_") else False
		def __script_replace__():
			return self.script.replace("script_", "").replace(".rsc", "")
		def __script_run__():
			if __script_import__():
				print("file :", self.script, "imported")
				if __script_check__():
					if self.script in self.script_system_list: return True
					elif self.script_run:
						if self.mikrotik.send_commands("/system script run " + self.script_name):
							print("script :", self.script_name, "ran")
							return True
						else:
							print("script :", self.script_name, "False ran") 
							return False
					else:
						print("script : run = False")
						return True
				else: print("script : starts withs \"script_\" False"); return False
			else: print("file", self.script, "False imported");sys.exit(1)
		def __script_find__():
			path = pathlib.Path(self.mikrotik.mikrotik_parent_dir)
			if path.joinpath("scripts").exists():
				path = sorted(path.rglob(self.script))
				if len(path) > 0: return path[0]
				else: print("False existing file:", path); sys.exit(1)
			else: print("False existing path:", path); sys.exit(1)
		def __send_script__():
			localpath = pathlib.Path(__script_find__())
			remotepath = "/" + localpath.name;
			return True if self.mikrotik.get_sftp_client(remotepath = remotepath, localpath = localpath, get = False) else False
		def script_system():
			print("script :" + self.script_name + " removed") if __script_remove__() else print("therefore no existing \"" + self.script_name + "\" script")
			if __send_script__():
				if __script_run__():
					return True
				else:
					return False
			else:
				print("False sending script:", self.script) 
				sys.exit(1)
		self.script_name = __script_replace__()
		return True if script_system() else False
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