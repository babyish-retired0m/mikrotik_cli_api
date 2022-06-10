#!/usr/bin/env python3
__version__ = "1.0"
import sys
sys.path.append("/Users/jozbox/python/functions/")
import file
File = file.Main()
servers = File.open_as_list("/Users/jozbox/python/hostname_advanced_testing/hosts/hosts_amazon_3.txt")

dns_str="/ip dns static\n"
peer_str="/ip ipsec peer\n"
address_list_str="/ip firewall address-list\n"

for server in servers:
	#dns_str+="add address=\""+server+"\" comment=\"NordVPN\" name=\""+server+"\"\n"
	#peer_str+="add name=\""+country+"_"+str(count_server)+"\" address=\""+server+"\" profile=NordVPN exchange-mode=ike2 send-initial-contact=yes disabled=yes\n"
	address_list_str+="add address=\""+server+"\" list=\"amazon\"\n"
	#count_server+=1;

		
#File.write_text("/Users/jozbox/python/mikrotik_cli_api/scripts/firewall_address_list_amazon.rsc", address_list_str)