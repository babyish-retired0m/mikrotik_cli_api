#!/usr/bin/env python3
"""
length servers 5445
length Standard VPN servers 5031
length Dedicated IP 158
length Obfuscated Servers 110
length P2P 120
length Double VPN 94
length Onion Over VPN 3
length servers 5396
"""
__version__ = "1.0"
import json
import sys
sys.path.append("/Users/jozbox/python/functions/")
import file
File = file.Main()
path_json = "/Users/jozbox/python/hostname_advanced_testing/results/results_2022-05-27_07-12-00_hosts_nordvpn.json"
results=json.load(open(path_json))
#print(results["servers_standard"]["parameters"])
results_test = results["servers_standard"]["advanced_test"]
#results_test = results["servers_p2p"]["advanced_test"]
#results_test = results["servers_obfuscated"]["advanced_test"]
servers_standard = []
count=0
for (enum, host) in enumerate(results_test):
	#print(host)
	#print("#"+str(enum),host)
	#print(results_test[host]["verbose_ping"]["statistics"]["packet_loss"])
	#if results_test[host]["verbose_ping"]["statistics"]["packet_loss"] == 0: print("#"+str(enum),host); count+=1;
	#if not None in results_test[host]["verbose_traceroute"]["traceroute"]: print("#"+str(count),host); count+=1;
	if (results_test[host]["verbose_ping"]["statistics"]["packet_loss"] == 0) and (not None in results_test[host]["verbose_traceroute"]["traceroute"]): 
		#print("#"+str(count),host);
		#servers_standard[count] = host;
		count+=1;
		servers_standard.append(host)
		
#File.
servers_json = json.load(open("/Users/jozbox/python/hostname_advanced_testing/hosts/nordvpn/nordvpn.com_servers.json"))
servers_country = {}
servers_country_myarr = {}
count=0
for server in servers_json:
	if not server["country"] in servers_country: 
		servers_country[server["country"]]={}
		servers_country_myarr[count]=server["country"]
		count+=1;

#print("length servers_country",len(servers_country))
#print(servers_country)

for server in servers_json:
	if server["domain"] in servers_standard:
		servers_country[server["country"]][server["domain"]] = {"id":server["id"],
														"ip_address":server["ip_address"],
														"name":server["name"],
														"flag":server["flag"]
														}
#print(servers_country)	
print("length servers_country",len(servers_country))
"""for country in servers_country:
	if len(servers_country[country]) == 0:
		servers_country.pop(country)
print(servers_country)	
print("length servers_country",len(servers_country))"""
count_country=0
dns_str="/ip dns static\n"
peer_str="/ip ipsec peer\n"
address_list_str="/ip firewall address-list\n"
for country in servers_country:
	if len(servers_country[country]) != 0:
		#print(servers_country[country])
		count_server=0
		#if len(servers_country[country]) != 0:
		for server in servers_country[country]:
			#print(server)
			#print(servers_country[country][server])
			dns_str+="add address=\""+servers_country[country][server]['ip_address']+"\" comment=\"NordVPN\" name=\""+server+"\"\n"
			peer_str+="add name=\""+country+"_"+str(count_server)+"\" address=\""+server+"\" profile=NordVPN exchange-mode=ike2 send-initial-contact=yes disabled=yes\n"
			address_list_str+="add address=\""+server+"\" comment=\""+country+"\" list=\"NordVPN\"\n"
			count_server+=1;
	count_country+=1

#print(servers_country_myarr)

mystr=""
for server in servers_country_myarr:
	mystr+=str(server)+"="+"\""+servers_country_myarr[server]+"\";"
print(mystr)

#print(dns_str)
#print(peer_str)
#print(address_list_str)

#File.write_text("/Users/jozbox/python/mikrotik_cli_api/nordvpn.com/nordvpn.com_Standard_VPN_servers_dns_static_country.rsc",dns_str)
#File.write_text("/Users/jozbox/python/mikrotik_cli_api/nordvpn.com/nordvpn.com_Standard_VPN_servers_ipsec_peer_country.rsc",peer_str)
#File.write_text("/Users/jozbox/python/mikrotik_cli_api/nordvpn.com/nordvpn.com_Standard_VPN_servers_firewall_address_list_country.rsc",address_list_str)