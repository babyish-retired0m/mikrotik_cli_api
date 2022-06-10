/ip firewall {
	address-list remove [find list="block"];
	address-list add list=block address="0.ciscosb.pool.ntp.org" comment="def2conf: ntp";
	address-list add list=block address="1.ciscosb.pool.ntp.org" comment="def2conf: ntp";
	address-list add list=block address="2.ciscosb.pool.ntp.org" comment="def2conf: ntp";
	address-list add list=block address="3.ciscosb.pool.ntp.org" comment="def2conf: ntp";
	address-list add list=block address="devicehelper.cisco.com" comment="def2conf: ntp";
	address-list add list=block address="time-pnp.cisco.com" comment="def2conf: ntp";
	address-list add list=block address="pnpserver.la.net.ua" comment="def2conf: ntp";
	filter remove [find comment~"defconf"];
	filter remove [find comment~"def2conf"];
	filter add chain=input action=drop in-interface-list=WAN protocol=tcp port=21,22,23,8291,8728,8729 comment="def2conf: traffic";
	filter add chain=input action=drop in-interface-list=WAN protocol=tcp port=80 comment="def2conf: traffic" disabled=yes;
	filter add chain=input action=drop in-interface-list=WAN protocol=tcp port=443 comment="def2conf: traffic" disabled=yes;
	filter add chain=input action=drop dst-address-list=block comment="def2conf: traffic";
	filter add chain=forward action=drop dst-address-list=block comment="def2conf: traffic";
	filter add chain=forward action=drop protocol=tcp src-address=192.168.88.0/24 dst-address=0.0.0.0/0 dst-port=80 comment="def2conf: traffic";
	filter add chain=input action=accept connection-state=established,related,untracked comment="defconf: accept established,related,untracked";
	filter add chain=input action=drop connection-state=invalid comment="defconf: drop invalid";
	filter add chain=input action=accept protocol=icmp comment="defconf: accept ICMP" disabled=yes;
	filter add chain=input action=accept dst-address=127.0.0.1 comment="defconf: accept to local loopback (for CAPsMAN)" disabled=yes;
	filter add chain=input action=drop in-interface-list=!LAN comment="defconf: drop all not coming from LAN";
	filter add chain=forward action=accept ipsec-policy=in,ipsec comment="defconf: accept in ipsec policy";
	filter add chain=forward action=accept ipsec-policy=out,ipsec comment="defconf: accept out ipsec policy";
	filter add chain=forward action=fasttrack-connection connection-state=established,related comment="defconf: fasttrack";
	filter add chain=forward action=accept connection-state=established,related,untracked comment="defconf: accept established,related, untracked";
	filter add chain=forward action=drop connection-state=invalid comment="defconf: drop invalid";
	filter add chain=forward action=drop connection-state=new connection-nat-state=!dstnat in-interface-list=WAN comment="defconf: drop all from WAN not DSTNATed";
}
/ip dns static {
	add address=193.106.144.6 name=0.ciscosb.pool.ntp.org comment="def2conf: ntp";
	add address=194.54.80.29 name=1.ciscosb.pool.ntp.org comment="def2conf: ntp";
	add address=79.142.192.4 name=2.ciscosb.pool.ntp.org comment="def2conf: ntp";
	add address=194.54.80.29 name=3.ciscosb.pool.ntp.org comment="def2conf: ntp";
	add address=52.205.197.159 name=devicehelper.cisco.com comment="def2conf: ntp";
	add address=34.202.215.187 name=time-pnp.cisco.com comment="def2conf: ntp";
}
/ipv6 firewall {
	address-list add list=bad_ipv6 address=::/128 comment="defconf: unspecified address";
	address-list add list=bad_ipv6 address=::1 comment="defconf: lo";
	address-list add list=bad_ipv6 address=fec0::/10 comment="defconf: site-local";
	address-list add list=bad_ipv6 address=::ffff:0:0/96 comment="defconf: ipv4-mapped";
	address-list add list=bad_ipv6 address=::/96 comment="defconf: ipv4 compat";
	address-list add list=bad_ipv6 address=100::/64 comment="defconf: discard only ";
	address-list add list=bad_ipv6 address=2001:db8::/32 comment="defconf: documentation";
	address-list add list=bad_ipv6 address=2001:10::/28 comment="defconf: ORCHID";
	address-list add list=bad_ipv6 address=3ffe::/16 comment="defconf: 6bone";
	filter remove [find comment~"defconf"];
	filter add chain=input action=drop comment="defconf: invalid";
	filter add chain=forward action=drop comment="defconf: drop packet";
	filter add chain=forward action=drop src-address-list=bad_ipv6 comment="defconf: drop packets with bad src ipv6";
	filter add chain=forward action=drop dst-address-list=bad_ipv6 comment="defconf: drop packets with bad dst ipv6";
}
:log info "script_ip_firewall_filter_rev_1.0 finished";
:beep;