:do {
/system/script add name="NordVPN" source=":do {\
/ip ipsec peer set [find disabled=no] disabled=yes;
#length servers countries 60
:local countryArray {0=\"Poland\";1=\"Denmark\";2=\"Belgium\";3=\"Hungary\";4=\"United States\";5=\"Austria\";6=\"Switzerland\";7=\"Czech Republic\";8=\"Norway\";9=\"United Kingdom\";10=\"France\";\
11=\"Netherlands\";12=\"Germany\";13=\"Israel\";14=\"Bosnia and Herzegovina\";15=\"Croatia\";16=\"Taiwan\";17=\"Slovakia\";18=\"Spain\";19=\"Italy\";\
20=\"Canada\";21=\"Romania\";22=\"Japan\";23=\"Vietnam\";24=\"South Africa\";25=\"Greece\";26=\"Portugal\";27=\"Singapore\";28=\"Sweden\";29=\"Slovenia\";\
30=\"Ireland\";31=\"Argentina\";32=\"Serbia\";33=\"Australia\";34=\"Albania\";35=\"New Zealand\";36=\"Latvia\";37=\"Hong Kong\";38=\"Chile\";39=\"Georgia\";\
40=\"Iceland\";41=\"Cyprus\";42=\"South Korea\";43=\"Luxembourg\";44=\"North Macedonia\";45=\"Mexico\";46=\"Thailand\";47=\"United Arab Emirates\";48=\"Finland\";49=\"Brazil\";\
50=\"Malaysia\";51=\"Indonesia\";52=\"Turkey\";53=\"Ukraine\";54=\"Lithuania\";55=\"India\";56=\"Costa Rica\";57=\"Estonia\";58=\"Bulgaria\";59=\"Moldova\";}
:local myrnd [:rndnum from=0 to=59];
:local countryNum (\$countryArray->[:tostr \$myrnd]);
:local country [:tostr \$countryNum];
:local peerNum [:len [/ip ipsec peer find name~\"\$country\"]];
:local myrnd [:rndnum from=0 to=\$peerNum];
:local peer [(\$country . \"_\" . \$myrnd)]
/ip ipsec peer enable [find name=\$peer];
/ip ipsec identity set 0 peer=\$peer disabled=no;
:log info \"ip_ipsec_nordvpn peer \$peer\";
:beep;}"
}