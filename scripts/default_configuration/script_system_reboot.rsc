/system script add comment=def2conf name=system_reboot source=":\
    execute {:log info \"system reboot\";:beep;/system/reboot;:delay 1;:put y;\
    }"