/system script add comment=def2conf name=system_shutdown source=":\
    execute {:log info \"system shutdown\";:beep;/system/shutdown;:delay 1;:pu\
    t y;}"