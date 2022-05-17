#!/usr/bin/env python3
"""
Copyright 2022. All rights reserved.
"""
__version__ = "1.2"
#Creating CA Certificates
import os
import utilities.file as file
import time
import utilities.password as password

class Create_Certificate:
	def __init__(self, domain, bit=4096, days=256, algorithm="sha256", parent_dir=os.path.expanduser('~')+"/openssl/results/"):
		"""
		Print all the usefull info about Certificate.
		"""
		self.domain=domain
		self.passphrase_ca, length, time_to_generate = password.create(1)
		self.passphrase_key, length, time_to_generate = password.create(1)
		passphrase_key_crt, length, time_to_generate = password.create(1)
		self.passphrase_key_crt=passphrase_key_crt[:6]
		#private key
		self.key_ca=domain+"_CA.key"
		#root certificate
		self.key_ca_certificate=domain+"_CA.pem"
		self.certificate_ca_signed=domain+"_CA.crt"
		#private key
		self.key=domain+".key"
		self.key_p12=domain+".p12"
		#create a CSR
		self.key_csr=domain+".csr"
		#certificate
		#certificate_signed
		self.key_crt=domain+".crt"
		self.key_pub=domain+".pub"
		#bit long modulus 2048 /* 4096, 8196,16392,32784,65568*/
		self.bit=str(bit)
		#bit="8196" #Signed by not Verified
		#bit="32784"
		self.algorithm=algorithm
		self.days=str(days)
		self.config="config"
		if file.check_dir(parent_dir) is False:
			file.dirs_make(parent_dir)
		else: file.dirs_make(path)
		path=parent_dir+self.domain+"/"
		dir = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())+"_bit_"+self.bit+"_days_"+self.days
		self.path=path+dir+"/"
		self.dirs_make(self.path)
		self.parameters={"ca":{
				"private_key":{"password":self.passphrase_ca,"path":self.path+self.key_ca,"bit":self.bit,"name":self.key_ca},
				"certificate":{"algorithm":self.algorithm,"days":self.days,"path":self.path+self.key_ca_certificate,"name":self.key_ca_certificate},
				"configuration":{
						"CN":self.domain,"subjectAltName":"DNS.1="+self.domain,"authorityKeyIdentifier":"keyid,issuer","basicConstraints":"CA:FALSE","keyUsage":"digitalSignature,nonRepudiation,keyEncipherment,dataEncipherment","C":"US","ST":"VA","L":"Truro","O":"Delicious_Brains_Inc","OU":"Mergebot","emailAddress":"noreply@mergebot.com"
									}
				},
			"key":{
				"private_key":{"password":self.passphrase_key,"path":self.path+self.key,"bit":self.bit,"name":self.key},
				"certificate":{"algorithm":self.algorithm,"days":self.days,"path":self.path+self.key_crt,"pass":self.passphrase_key_crt,"name":self.key_crt},
				"configuration":{
						"CN":self.domain,"subjectAltName":self.domain,"authorityKeyIdentifier":"keyid,issuer","basicConstraints":"CA:FALSE","keyUsage":"digitalSignature,nonRepudiation,keyEncipherment,dataEncipherment","C":"US","ST":"VA","L":"Truro","O":"Delicious_Brains_Inc","OU":"Mergebot","emailAddress":"noreply@mergebot.com"
								},
				"request":{"path":self.path+self.key_csr,"name":self.key_csr},
				"p12":{"pass":self.passphrase_key_crt,"name":self.passphrase_key_crt},
				"pub":{"path":self.path+self.key_pub,"outform":"PEM","name":self.key_pub}
				},
			"configuration":{
					"directory_parent":parent_dir,
					"directory":dir,
					"path":self.path,
					"domain":domain,
					"bit":bit,
					"days":days,
					"algorithm":algorithm,
					"Unix_Epoch_Time":time.time(),
					"date":time.strftime("%Y-%m-%d", time.gmtime()),
					"time":time.strftime("%H:%M:%S", time.gmtime())
								}
			}
		self.write_text_as_json(self.path+self.config,self.parameters)
		print("Directory parent:",parent_dir)
	def All(self):
		self.Key_CA()
		self.Key_Private()
		self.Key_p12()
		self.Key_pub()
		return self.path+self.config+".json"
		
	def write_text_json(self, path, text):
		import json
		json.dump(text, fp=open(path+".json",'w'),indent=4)
	def Key_CA(self):
		#Creating CA Certificates
		os.system(f'openssl genrsa -des3 -passout pass:"{self.passphrase_ca}" -out {self.path+self.key_ca} {self.bit}')
		#Creating CA root certificate self.parameters["ca"]["configuration"]["CN"]
		os.system(f"openssl req -x509 -new -nodes -key {self.path+self.key_ca} -passin pass:'{self.passphrase_ca}' -{self.algorithm} -days {self.days} -out {self.path+self.key_ca_certificate} -subj '/CN={self.parameters['ca']['configuration']['CN']}/subjectAltName={self.parameters['ca']['configuration']['subjectAltName']}/authorityKeyIdentifier={self.parameters['ca']['configuration']['authorityKeyIdentifier']}/basicConstraints={self.parameters['ca']['configuration']['basicConstraints']}/keyUsage={self.parameters['ca']['configuration']['keyUsage']}/'")
	def Key_Private(self):
		#private key the private key
		os.system(f"openssl genrsa -des3 -passout pass:'{self.passphrase_key}' -out '{self.path+self.key}' {self.bit}")
		os.system(f"chmod 400 {self.path+self.key}")
		#create a CSR the certificate signing request
		os.system(f"openssl req -new -key {self.path+self.key} -passin pass:{self.passphrase_key} -out {self.path+self.key_csr} -subj '/CN={self.parameters['key']['configuration']['CN']}/subjectAltName={self.parameters['key']['configuration']['subjectAltName']}/authorityKeyIdentifier={self.parameters['key']['configuration']['authorityKeyIdentifier']}]/basicConstraints={self.parameters['key']['configuration']['basicConstraints']}/keyUsage={self.parameters['key']['configuration']['keyUsage']}/'")
		#Create Certificate the signed certificate
		os.system(f"openssl x509 -req -passin pass:'{self.passphrase_ca}' -CA {self.path+self.key_ca_certificate} -CAkey {self.path+self.key_ca} -CAcreateserial -in {self.path+self.key_csr} -out {self.path+self.key_crt} -days {self.days} -{self.algorithm}")
	def Key_p12(self):
		#Creating p12
		os.system(f"openssl pkcs12 -export -out {self.path+self.key_p12} -passout pass:'{self.passphrase_key_crt}' -in {self.path+self.key_crt} -inkey {self.path+self.key} -passin pass:{self.passphrase_key}")
	def Key_pub(self):
		#Creating pub
		os.system(f"openssl rsa -in {self.path+self.key} -passin pass:{self.passphrase_key} -pubout -out {self.path+self.key_pub}")# -outform PEM

if __name__ == '__main__':
	mikrotik=Create_Certificate("192.168.88.1")
	mikrotik.All()
	"""mikrotik.Key_CA()
	mikrotik.Key_Private()
	mikrotik.Key_p12()
	mikrotik.Key_pub()"""