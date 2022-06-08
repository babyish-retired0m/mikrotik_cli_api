/system scheduler add name="NordVPNDay2" interval=30m start-time=05:30:00 on-event=NordVPN;
/system scheduler add name="NordVPNNight2" interval=60m start-time=21:30:00 on-event=NordVPN;
/system scheduler add name="NordVPNDay" interval=1d start-time=05:30:00 on-event=NordVPNDay;
/system scheduler add name="NordVPNNight" interval=1d start-time=21:30:00 on-event=NordVPNNight;