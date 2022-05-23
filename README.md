# mikrotik cli api
Collect of useful commands for mikrotik's should be invoked on the command line.
# usage

Reset mikrotik system configuration to defaults.


python3 main_api.py --help

usage: main_api.py [-B] [-b] [-c] [-R] [-t] [-n username password] [-cn] [-f] [-d] [-fc] [-fa] [-h] [-v] [-r] [-S] [-s]
                   [-SC SEND_COMMAND]

Collect of useful commands for mikrotik's:

  -B, --beep            send command :beep
  
  -b, --backup          mikrotik get backup
  
  -c, --certificate     mikrotik get certificate create ssh
  
  -R, --reset           mikrotik get reset configuration
  
  -t, --time            mikrotik change system time
  
  -n username password, --nordvpn username password
                        CREDENTIALS as input separated by space: username password.
                        
  -cn, --certificate_nordvpn
                        mikrotik get certificate nordvpn
                        
  -f, --firewall        mikrotik get ip firewall filter
  
  -d, --doh             mikrotik get ip dns over https
  
  -fc, --firewall_country
                        mikrotik get ip firewall address list countryIPBlocks
                        
  -fa, --firewall_amazon
                        mikrotik get ip firewall address list amazon
                        
  -h, --help            Show this help message and exit
  
  -v, --version         show program's version number and exit
  
  -r, --reboot          mikrotik get system reboot
  
  -S, --shutdown        mikrotik get system shutdown
  
  -s, --sup_output      mikrotik get system sup_output
  
  -SC SEND_COMMAND, --send SEND_COMMAND
                        send command as input.
