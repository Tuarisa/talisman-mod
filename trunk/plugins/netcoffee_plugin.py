#===istalismanplugin===
# -*- coding: utf-8 -*-

# Endless / talisman rev 84+
# version 0.03b by Tuarisa
# Freeware


def handler_netcoffee(groupchat, nick, aff, jid):
		tjid = get_true_jid(groupchat+'/'+nick)
		res=unicode(GROUPCHATS[groupchat][nick]['jid'])
		if res.count('QIP	'):
			order_visitor(groupchat, nick)
		res=res.split('/')[1]
#		msg(groupchat, res)
		if res.count('HotCoffee'):
			order_kickv(groupchat, nick)
				

def order_banv(groupchat, nick):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	ban=query.addChild('item', {'nick':nick, 'affiliation':'outcast'})
	ban.setTagData('reason', get_bot_nick(groupchat)+u': '+u' Неудачный выбор клиента.')
	iq.addChild(node=query)
	JCON.send(iq)
	
def order_kickv(groupchat, nick):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	kick=query.addChild('item', {'nick':nick, 'role':'none'})
	kick.setTagData('reason', get_bot_nick(groupchat)+': '+u' Неуданый выбор клиента. ')
	iq.addChild(node=query)
	JCON.send(iq)
	
def order_visitor(groupchat, nick):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	kick=query.addChild('item', {'nick':nick, 'role':'visitor'})
	kick.setTagData('reason', get_bot_nick(groupchat)+': ')
	iq.addChild(node=query)
	JCON.send(iq)


                    
		
register_join_handler(handler_netcoffee)