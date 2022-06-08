/system script add name=certificate_LocalCA source={
	
	/certificate/add name=LocalCA common-name=LocalCA key-usage=key-cert-sign,crl-sign key-size=4096 days-valid=256 digest-algorithm=sha512 trusted=yes country=PA state=PA organization=NordVPN locality=PA unit=PA;
	:beep;
	/certificate/sign LocalCA;
	:beep;
}