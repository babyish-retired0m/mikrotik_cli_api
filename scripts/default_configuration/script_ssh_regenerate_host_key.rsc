:execute {
	/system script add comment="def2conf" name=ssh_regenerate_host_key source=":execute {/ip ssh regenerate-host-key;:log info \"mikrotik ip ssh regenerate-host-key, host-key-size=4096 jobs done\";:log info \"SSH host key regenerated!\"}";
}