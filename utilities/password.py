#!/usr/bin/env python3
"""
Copyright 2022. All rights reserved.
"""
__version__ = "1.0"
import bcrypt
import time
import random
def ran():
	return random.randint(4,14)
def create(modulus=14):
	start=time.time()
	passwd=bcrypt.gensalt(rounds=ran())#rounds < 4 or rounds > 31
	hashed_passwd=''
	for i in list(range(modulus)):
		salt=bcrypt.gensalt(rounds=ran())
		hashed=bcrypt.hashpw(passwd, salt)
		hashed_passwd+=hashed.decode()
	#print('length:',len(hashed_passwd))
	hashed=hashed_passwd.replace('$',str(ran())).replace('/',str(ran()))
	end=time.time()
	time_to_generate = end-start
	#print("It took more than {0:.2f} seconds to generate the hash value with the specified cost factor.".format(time_to_generate))
	#print(hashed)
	return str(hashed), len(hashed_passwd), time_to_generate
if __name__ == '__main__':
	create()