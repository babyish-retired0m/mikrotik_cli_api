#!/usr/bin/env python3
__version__ = "1.2"
def getpcname():
	from os import environ
	from platform import node
	from socket import gethostname
	n1 = node()
	n2 = gethostname()
	n3 = environ.get("COMPUTERNAME")
	if n1 == n2 == n3:
		pcname = n1
	elif n1 == n2:
		pcname = n1
	elif n1 == n3:
		pcname = n1
	elif n2 == n3:
		pcname = n2
	else:
		pcname = n1
		print("Computernames are not equal to each other")
		#raise Exception("Computernames are not equal to each other")
	if pcname.endswith('.local'): return pcname[:pcname.find('.local')]
	else: return pcname
def getusername():
	from os import getlogin
	from getpass import getuser
	n1=getlogin()
	n2=getuser()
	if n1 == n2: user = n1
	elif n2 == 'root': user = n1
	else: raise Exception("Username are not equal to each other")
	return user
def getcurrentdirectory():
	from os import getcwd,path
	n1=getcwd() 
	n2=path.expanduser('~')
	if n1 == n2: return '~'
	else: return n1
class Clr:
    """Text colors."""
    RST = '\033[39m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    VIOLET = '\033[34m'
    PINK = '\033[35m'
    BLUE = '\033[36m'
    GREY = '\033[37m'
    BLACK2 = '\033[40m'
    RST2 = '\033[49m'
    RED2 = '\033[41m'
    GREEN2 = '\033[42m'
    YELLOW2 = '\033[43m'
    VIOLET2 = '\033[44m'
    PINK2 = '\033[45m'
    BLUE2 = '\033[46m'
    GREY2 = '\033[47m'
def Percents(iter,L):
	k = iter * round(100/L,1)
	lo = list(range(0,100,1))
	if k in lo:
		print("{0}{2} percents{1}".format(Clr.RED2,Clr.RST2,lo[lo.index(k)]))
def get_unix_time(): 
	import time
	return time.time()
if __name__ == '__main__':
	import os
	print(getusername()+'@'+getpcname(),getcurrentdirectory(),'% ')
	#print(os.path.expanduser('~'))