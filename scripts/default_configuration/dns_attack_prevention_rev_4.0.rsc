/ip firewall address-list {
address-list remove [find list="LAN_Addresses"]
address-list remove [find list="DNS_Servers"]
add address=10.0.0.0/8 comment="def2conf: dns_attack" list="LAN_Addresses";
add address=172.16.0.0/12 comment="def2conf: dns_attack" list="LAN_Addresses";
add address=192.168.0.0/16 comment="def2conf: dns_attack" list="LAN_Addresses";
add address=1.0.0.1 comment="def2conf: Cloudflare" list="DNS_Servers";
add address=1.1.1.1 comment="def2conf: Cloudflare" list="DNS_Servers";
add address=8.8.4.4 comment="def2conf: Google" list="DNS_Servers";
add address=8.8.8.8 comment="def2conf: Google" list="DNS_Servers";
};
/ip firewall filter {
remove [find comment~"def2conf: dns_attack"];
add action=jump chain=input comment="def2conf: dns_attack Jump to DNS_INPUT Chain" dst-port=53 jump-target=DNS_INPUT log=yes protocol=udp;
add action=accept chain=DNS_INPUT comment="def2conf: dns_attack Make exceptions for LAN DNS (RFC1918) inquiries" port=53 protocol=udp src-address-list="LAN_Addresses";
add action=add-src-to-address-list address-list=DNS_DDoS address-list-timeout=none-dynamic chain=DNS_INPUT comment="def2conf: dns_attack Add other DNS inquiries to DNS_DDoS Offenders List" port=53 protocol=udp src-address-list="!LAN_Addresses"
add action=drop chain=DNS_INPUT comment="def2conf: dns_attack Drop Traffic Sourced from DNS_DDoS Offenders" src-address-list=DNS_DDoS;
add action=return chain=DNS_INPUT comment="def2conf: dns_attack Return from DNS_INPUT Chain";
add action=jump chain=output comment="def2conf: dns_attack Jump to DNS_OUTPUT Chain" dst-port=53 jump-target=DNS_OUTPUT protocol=udp;
add action=accept chain=DNS_OUTPUT comment="def2conf: dns_attack Make Exceptions for Traffic to the DNS_Servers" dst-address-list="DNS_Servers" dst-port=53 protocol=udp;
add action=drop chain=DNS_OUTPUT comment="def2conf: dns_attack Drop All Other Out Bound DNS Traffic" dst-port=53 protocol=udp;
add action=return chain=DNS_OUTPUT comment="def2conf: dns_attack Return from DNS_OUTPUT Chain";
add action=jump chain=forward comment="def2conf: dns_attack Jump to DNS_FORWARD Chain" jump-target=DNS_FORWARD;
add action=accept chain=DNS_FORWARD comment="def2conf: dns_attack Make Exceptions for Trafffic from the DNS_Servers going to the LAN Addresses (RFC1918)" dst-address-list="LAN_Addresses" port=53 protocol=udp src-address-list="DNS_Servers";
add action=accept chain=DNS_FORWARD comment="def2conf: dns_attack Make Exceptions for Traffic from the LAN Addresses (RFC1918) going to the DNS_Servers" dst-address-list="DNS_Servers" port=53 protocol=udp src-address-list="LAN_Addresses";
add action=drop chain=DNS_FORWARD comment="def2conf: dns_attack Drop All Others DNS Traffic" port=53 protocol=udp;
add action=drop chain=forward comment="def2conf: dns_attack Drop Traffic to DNS DNS_DDoS Offenders" dst-address-list=DNS_DDoS;
};
:log info "Def2conf_script_dns_attack_prevention_rev_4_0_finished";
:beep;