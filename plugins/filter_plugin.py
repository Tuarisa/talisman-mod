#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  filter_plugin.py
#  exclusively for jabber.ru ;)
#  REQUIRES order_plugin.py

#  Initial Copyright © 2010 ъыь <Als@admin.ru.net>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

filter_temp_config=[]

def filter_check_order():
	try:
		if handler_order_message:				
			register_filterNS_handler()
			register_message_handler(filter_check_filtered_gch)
			register_stage2_init(filter_config_check_config)
	except:
		print '====================================================\nfilter_plugin.py plugin REQUIRES order_plugin.py for work.\nIt cannot be loaded alone.\n====================================================\n'
	

def register_filterNS_handler():
	JCON.RegisterHandler('iq', handler_filter_check, 'set', 'http://jabber.ru/muc-filter') 

def handler_filter_check(con, iq):	
	msg=xmpp.Message(node=iq.getQueryChildren()[0])
	body = msg.getBody()
	if body:	body=body.strip()
	if not body:	return
	gch=unicode(msg.getTo()).split('/')[0]
	for nick in GROUPCHATS[gch].keys():
		if GROUPCHATS[gch][nick]['jid'] == msg.getFrom():
			mfrom=unicode(gch)+u'/'+nick
			fbody=handler_order_message(1, msg.getType(), [mfrom, unicode(gch), nick], body)
			if not fbody is True: handler_send_filtered(msg.setBody(fbody.strip()),iq)

def handler_send_filtered(fbody, iq):
	result=iq.buildReply('result')
	query = result.getTag('query')
	query.addChild(node=iq.getQueryChildren()[0])
	JCON.send(result)
	raise xmpp.NodeProcessed

def filter_config_check_config():
	time.sleep(10)
	MESSAGE_HANDLERS.remove(filter_check_filtered_gch)
	gchs=GROUPCHATS.keys()
	for gch in filter_temp_config:
		GCHCFGS[gch]['filt']['fltmode']=1
		gchs.remove(gch)
	for gch in gchs:
		GCHCFGS[gch]['filt']['fltmode']=0
	
def filter_check_filtered_gch(raw, type, source, body):
	if source[0]==source[1]:
		x=raw.getChildren()[1]
		if x.getNamespace()=='http://jabber.org/protocol/muc#user':
			if x.getChildren()[0].getAttr('code')=='100':
				filter_temp_config.append(source[1])
		

register_stage0_init(filter_check_order)