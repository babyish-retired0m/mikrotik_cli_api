/ip {
service disable ftp,telnet,www,www-ssl,api,winbox,api-ssl;
firewall service-port set disabled=yes numbers=0,1,2,3,4,5;
service set ssh address=192.168.88.0/24;
ssh set strong-crypto=yes host-key-size=4096;
proxy set enabled=no;
socks set enabled=no;
upnp set enabled=no;
cloud set ddns-enabled=no update-time=no;
dns set cache-size=4096;
dns set allow-remote-requests=yes;
neighbor discovery-settings set discover-interface-list=none lldp-med-net-policy-vlan=disabled;
}
/tool mac-server set allowed-interface-list=none;
/tool mac-server mac-winbox set allowed-interface-list=none;
/caps-man {
manager set enabled=no;
manager interface remove [find comment="defconf"];
manager interface set [find default=yes] forbid=yes;
provisioning remove [find comment="defconf"];
configuration remove [find comment="defconf"];
}
/system logging {
add action=memory topics=dns disabled=yes;
add action=echo topics=dns disabled=yes;
add action=echo topics=ipsec disabled=yes;
add action=echo topics=error disabled=yes;
enable numbers=0;
}
/tool bandwidth-server set enabled=no max-sessions=1 authenticate=no
:log info "script_default_configuration_2 finished";
:beep;
