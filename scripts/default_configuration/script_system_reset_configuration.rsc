/system script add comment=def2conf name=\
    system_reset_configuration source=\
    ":execute {/system/reset-configuration;:delay 1;:put y;}"
