#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  netcoffe-plugin.py	

#  Initial Copyright © 2010 Tuarisa <Tuarisa@gmail.com>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

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