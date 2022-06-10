# Generate by ISP Supplies | LearnMikroTik.com's Firewall tool
# Available at http://mikrotikconfig.com
#
#
#/ip firewall address-list
#add address=0.0.0.0/22 comment="Country" list=CountryIPBlocks
#/ip firewall filter add chain=input action=drop dst-address-list=CountryIPBlocks comment="def2conf: traffic" place-before=6;
#/ip firewall filter add chain=forward action=drop dst-address-list=CountryIPBlocks comment="def2conf: traffic" place-before=6;