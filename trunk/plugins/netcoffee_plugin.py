#===istalismanplugin===
# -*- coding: utf-8 -*-

# Endless / talisman rev 84+
# version 0.01a by Tuarisa
#


def handler_netcoffee(groupchat, nick, aff, jid):
		#tjid = get_true_jid(groupchat+'/'+nick)
		resurs=''
		#msg(groupchat, u' просто тест')
		msg(groupchat, jid)
		#msg(groupchat, groupchat+'/'+nick)
		
		
		if tjid.count('/'):
			resurs=tjid.split('/')[1]
		if resurs =='hotcofee' :
				order_banv(groupchat, nick)
		

def order_banv(groupchat, nick):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	ban=query.addChild('item', {'nick':nick, 'affiliation':'outcast'})
	ban.setTagData('reason', get_bot_nick(groupchat)+u': '+u' Hotcoffee!')
	iq.addChild(node=query)
	JCON.send(iq)
		
register_join_handler(handler_netcoffee)