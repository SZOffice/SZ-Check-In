# -*- coding: utf-8 -*-   
from slackclient import SlackClient

#XXXXX get from https://api.slack.com/custom-integrations/legacy-tokens
sc = SlackClient("XXXXX")
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
