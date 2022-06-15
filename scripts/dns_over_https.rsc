:beep;
/certificate import file-name="cacert.pem" passphrase="";
:beep;
/ip/dns static add address="104.16.248.249" name="cloudflare-dns.com" type=A comment="cloudflare";
/ip/dns static add address="104.16.249.249" name="cloudflare-dns.com" type=A comment="cloudflare";
/ip/dns static add address="2606:4700::6810:f9f9" name="cloudflare-dns.com" type=AAAA comment="cloudflare";
/ip/dns static add address="2606:4700::6810:f8f9" name="cloudflare-dns.com" type=AAAA comment="cloudflare";
/ip/dns set servers="104.16.248.249,104.16.249.249" use-doh-server="https://cloudflare-dns.com/dns-query" verify-doh-cert=yes allow-remote-requests=yes;
/ip firewall address-list {
add address=104.16.248.249 comment=\"def2conf: Cloudflare\" list=\"DNS_Servers\";
add address=104.16.249.249 comment=\"def2conf: Cloudflare\" list=\"DNS_Servers\";}
:beep;