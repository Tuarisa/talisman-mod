#===istalismanplugin===
# -*- coding: utf-8 -*-

version_pendingg=[]

def handler_banos(groupchat, nick, aff, role):
        if check_file(groupchat,'banver.txt'):
                jid=groupchat+'/'+nick
                iq = xmpp.Iq('get')
                id='vers'+str(random.randrange(1000, 9999))
                globals()['version_pendingg'].append(id)
                iq.setID(id)
                iq.addChild('query', {}, [], 'jabber:iq:version');
                jid=groupchat+'/'+nick
                iq.setTo(jid)
                JCON.SendAndCallForResponse(iq, handler_version4_answ, {'groupchat': groupchat, 'nick': nick})
                return

def handler_version4_answ(coze, res, groupchat, nick):
	id=res.getID()
	if id in globals()['version_pendingg']:
		globals()['version_pendingg'].remove(id)
	else:
		print 'someone is doing wrong...'
		return
	rep =''
	if res:
		if res.getType() == 'result':
			name = '[no name]'
			version = '[no ver]'
			os = '[no os]'
			props = res.getQueryChildren()
			for p in props:
				if p.getName() == 'name':
					name = p.getData()
				elif p.getName() == 'version':
					version = p.getData()
				elif p.getName() == 'os':
					os = p.getData()
			#if name:
				#rep = name
			if version:
                                if os:
                                        gfr = version+' '+os
                                        BANVER = 'dynamic/'+groupchat+'/banver.txt'
                                        fp = open(BANVER, 'r')
                                        banver = eval(fp.read())
                                        tojid = groupchat+'/'+nick
                                        if gfr in banver:
                                                govn=get_true_jid(groupchat+'/'+nick)
                                                node='<item affiliation="outcast" jid="'+govn+u'"><reason>Ваша ось занесена в бан-лист бота.</reason></item>'
                                                node=xmpp.simplexml.XML2Node(unicode('<iq from="'+JID+'/'+RESOURCE+'" id="ban1" to="'+groupchat+'" type="set"><query xmlns="http://jabber.org/protocol/muc#admin">'+node+'</query></iq>').encode('utf8'))
                                                JCON.send(node)
                                                return

def banver_subscribe(type, source, parameters):
        #parameters = reewf
        BANVER = 'dynamic/'+source[1]+'/banver.txt'
        fp = open(BANVER, u'r')
        juk = eval(read_file(BANVER))
        if parameters:
                if parameters in juk:
                        reply(type, source, u'такая версия в бан-листе уже есть')
                        return
                #if parameters in NOBANN5:
                        #reply(type, source, u'низзя')
                        #return
                else:
                        juk[parameters] = {}
                        write_file(BANVER,str(juk))
                        fp.close()
                        reply(type, source, u'версия '+parameters+u' добавлена в банлист')

def banver_show(type, source, parameters):
    BANVER = 'dynamic/'+source[1]+'/banver.txt'
    fp = open(BANVER, 'r')
    juk = eval(read_file(BANVER))
    fp.close()
    if len(juk) == 0:
      reply(type, source, u'Список пуст!')
      return
    p =1
    spisok = ''
    for usr in juk:
          spisok += str(p)+'. '+usr+'\n'
          p +=1
    reply(type, source, u'(всего '+str(len(juk))+u'):\n'+spisok)

def banver_unsubscribe(type, source, parameters):
      BANVER = 'dynamic/'+source[1]+'/banver.txt'
      if parameters:
            fp = open(BANVER, 'r')
            juk = eval(read_file(BANVER))
            fp.close()
            if parameters in juk:
                    del juk[parameters]
            else:
                  reply(type, source, u'не найдено!')
                  return
            write_file(BANVER,str(juk))

            reply(type, source, u'версия '+parameters+u' удалена')
	
register_join_handler(handler_banos)
register_command_handler(banver_subscribe, 'banver+', ['все'], 20, 'добавить версию и ось в банлист', 'banver+ <version><os>', ['banver+ 9032 Windows XP'])
register_command_handler(banver_show, 'banver_show', ['все'], 20, 'просмотр списка банлиста по версии клиента', 'banver_show', ['banver_show'])
register_command_handler(banver_unsubscribe, 'banver-', ['все'], 20, 'удалить версию из банлиста', 'banver- <version>', ['banver- 9032 Windows XP'])

