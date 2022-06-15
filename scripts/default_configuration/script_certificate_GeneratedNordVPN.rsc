/system script add name=certificate_GeneratedNordVPN comment="def2conf" source={
:local name "GeneratedNordVPN";
:local nameTEMP ($name . "TEMP");
:local o [/certificate find name=$name];
/certificate/add name=$nameTEMP common-name=LocalCA key-usage=key-cert-sign,crl-sign key-size=4096 \
days-valid=256 digest-algorithm=sha512 trusted=yes country=PA state=PA organization=NordVPN locality=PA unit=PA;
:beep;
/certificate/sign $nameTEMP;
:beep;
:if ([:len $o] != 0) do={/certificate/remove $name;};
/certificate set $nameTEMP name=$name;
:beep;
}