/system script add comment=def2conf name=system_shutdown source=":do {:log info \"system shutdown\";:beep;/system/shutdown;:delay 1;:put y;}"