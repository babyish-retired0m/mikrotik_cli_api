ip firewall address-list
remove [find list=block]
add address=devicehelper.cisco.com list=block comment="def2conf: ntp"
add address=0.ciscosb.pool.ntp.org list=block comment="def2conf: ntp"
add address=1.ciscosb.pool.ntp.org list=block comment="def2conf: ntp"
add address=2.ciscosb.pool.ntp.org list=block comment="def2conf: ntp"
add address=3.ciscosb.pool.ntp.org list=block comment="def2conf: ntp"
add address=time-pnp.cisco.com list=block comment="def2conf: ntp"
add address=pnpserver.la.net.ua list=block comment="def2conf: ntp"
add address=router0BE0B1.la.net.ua list=block comment="def2conf: ntp"
add address=lencr.org list=block comment="def2conf: malicious, malware, virus, hijacking"
add address=i.lencr.org list=block comment="def2conf: malicious, malware, virus, hijacking"
add address=x1.i.lencr.org list=block comment="def2conf: malicious, malware, virus, hijacking"
add address=r3.i.lencr.org list=block comment="def2conf: malicious, malware, virus, hijacking"