# -*- coding: utf-8 -*-   
from slackclient import SlackClient

sc = SlackClient("xoxp-9909592998-92068524464-297094416515-fbef9d82cbe201a3cf978ea64fd78118")
msg = "今天都打卡了"

def slack_send(msg):  
	print 'send slack start...'
	response = sc.api_call(
	  "chat.postMessage",
	  channel="#sz-check-in",
	  text=msg
	)
	if response["error"] != "":
		print('send slack error:' + response["error"])
	else:
		print 'send slack finished...'  

#response = sc.api_call("chat.postMessage", channel="#rc_monitor", text="<@jacky_liao>, <@miragelu>, <@candu>, <@mervynlin>")
