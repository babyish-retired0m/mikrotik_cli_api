/system script add comment=def2conf name="dns_attack_prevention_rev_4.0" source=":execute {
	/ip firewall address-list {
		add address=10.0.0.0/8 comment=\"def2conf\" list=\"LAN Addresses (RFC1918)\";
		add address=172.16.0.0/12 comment=\"def2conf\" list=\"LAN Addresses (RFC1918)\";
		add address=192.168.0.0/16 comment=\"def2conf\" list=\"LAN Addresses (RFC1918)\";
		add address=1.1.1.1 comment=\"def2conf: Cloudflare\" list=\"DNS Servers\";
		add address=1.0.0.1 comment=\"def2conf: Cloudflare\" list=\"DNS Servers\";
		add address=8.8.8.8 comment=\"def2conf: Google\" list=\"DNS Servers\";
		add address=8.8.8.8 comment=\"def2conf: Google\" list=\"DNS Servers\";
		add address=104.16.248.249 comment=\"def2conf: Cloudflare\" list=\"DNS Servers\";
		add address=104.16.249.249 comment=\"def2conf: Cloudflare\" list=\"DNS Servers\";
				}
	/ip firewall filter {
		add action=jump chain=input comment=\"def2conf: Jump to DNS_INPUT Chain\" dst-port=53 jump-target=DNS_INPUT log=yes protocol=udp;
		add action=accept chain=DNS_INPUT comment=\"def2conf: Make exceptions for LAN DNS inquiries\" port=53 protocol=udp src-address-list=\"LAN Addresses (RFC1918)\";
		add action=add-src-to-address-list address-list=DNS_DDoS address-list-timeout=none-dynamic chain=DNS_INPUT comment=\"def2conf: Add other DNS inquiries to DNS_DDoS Offenders List\" port=53 protocol=udp src-address-list=\"!LAN Addresses (RFC1918)\"
		add action=drop chain=DNS_INPUT comment=\"def2conf: Drop Traffic Sourced from DNS_DDoS Offenders\" src-address-list=DNS_DDoS;
		add action=return chain=DNS_INPUT comment=\"def2conf: Return from DNS_INPUT Chain\";
		add action=jump chain=output comment=\"def2conf: Jump to DNS_OUTPUT Chain\" dst-port=53 jump-target=DNS_OUTPUT protocol=udp;
		add action=accept chain=DNS_OUTPUT comment=\"def2conf: Make Exceptions for Traffic to the DNS Servers\" dst-address-list=\"DNS Servers\" dst-port=53 protocol=udp;
		add action=drop chain=DNS_OUTPUT comment=\"def2conf: Drop All Other Out Bound DNS Traffic\" dst-port=53 protocol=udp;
		add action=return chain=DNS_OUTPUT comment=\"def2conf: Return from DNS_OUTPUT Chain\";
		add action=jump chain=forward comment=\"def2conf: Jump to DNS_FORWARD Chain\" jump-target=DNS_FORWARD;
		add action=accept chain=DNS_FORWARD comment=\"def2conf: Make Exceptions for Trafffic from the DNS Servers going to the LAN\" dst-address-list=\"LAN Addresses (RFC1918)\" port=53 protocol=udp src-address-list=\"DNS Servers\";
		add action=accept chain=DNS_FORWARD comment=\"def2conf: Make Exceptions for Traffic from the LAN going to the DNS Servers\" dst-address-list=\"DNS Servers\" port=53 protocol=udp src-address-list=\"LAN Addresses (RFC1918)\";
		add action=drop chain=DNS_FORWARD comment=\"def2conf: Drop All Others DNS Traffic\" port=53 protocol=udp;
		add action=drop chain=forward comment=\"def2conf: Drop Traffic to DNS DNS_DDoS Offenders\" dst-address-list=DNS_DDoS;
			}
	:log info \"Def2conf_script_dns_attack_prevention_rev_4_0_finished\";
	:beep;
}"