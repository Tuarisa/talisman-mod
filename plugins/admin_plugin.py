#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  admin_plugin.py

#  Initial Copyright © 2002-2005 Mike Mintz <mikemintz@gmail.com>
#  Modifications Copyright © 2007 Als <Als@exploit.in>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

def popups_check(gch):
	DBPATH='dynamic/'+gch+'/config.cfg'
	if GCHCFGS[gch].has_key('popups'):
		if GCHCFGS[gch]['popups'] == 1:
			return 1
		else:
			return 0
	else:
		GCHCFGS[gch]['popups']=1
		write_file(DBPATH,str(GCHCFGS[gch]))
		return 1
				
def handler_admin_join(type, source, parameters):
	if not source[1] in GROUPCHATS:
		source[2]=source[1].split('@')[0]
	if parameters:
		passw=''
		args = parameters.split()
		if not args[0].count('@') or not args[0].count('.')>=1:
			reply(type, source, u'ошибочный запрос. прочитай помощь по использованию команды')
			return
		if len(args)>1:
			groupchat = args[0]
			passw = string.split(args[1], 'pass=', 1)
			if not passw[0]:
				reason = ' '.join(args[2:])
			else:
				reason = ' '.join(args[1:])
		else:
			groupchat = parameters
			reason = ''
		get_gch_cfg(groupchat)
		for process in STAGE1_INIT:
			with smph:
				INFO['thr'] += 1
				threading.Thread(None,process,'atjoin_init'+str(INFO['thr']),(groupchat,)).start()
		DBPATH='dynamic/'+groupchat+'/config.cfg'
		write_file(DBPATH, str(GCHCFGS[groupchat]))
		if passw:
			join_groupchat(groupchat, DEFAULT_NICK)
		else:
			join_groupchat(groupchat, DEFAULT_NICK, passw)
		MACROS.load(groupchat)
		reply(type, source, u'я зашёл в ' + groupchat)
		if popups_check(groupchat):
			if reason:
				msg(groupchat, u'меня привёл '+source[2]+u' по причине:\n'+reason)
			else:
				msg(groupchat, u'меня привёл '+source[2])
	else:
		reply(type, source, u'ошибочный запрос. прочитай помощь по использованию команды')

def handler_admin_leave(type, source, parameters):
	if not source[1] in GROUPCHATS:
		source[2]=source[1].split('@')[0]
	args = parameters.split()
	if len(args)>1:
		level=int(user_level(source[1]+'/'+source[2], source[1]))
		if level<40 and args[0]!=source[1]:
			reply(type, source, u'недостаточно прав')
			return
		reason = ' '.join(args[1:]).strip()
		if not GROUPCHATS.has_key(args[0]):
			reply(type, source, u'меня там нет')
			return
		groupchat = args[0]
	elif len(args)==1:
		level=int(user_level(source[1]+'/'+source[2], source[1]))
		if level<40 and args[0]!=source[1]:
			reply(type, source, u'недостаточно прав')
			return
		if not GROUPCHATS.has_key(args[0]):
			reply(type, source, u'меня там нет')
			return
		reason = ''
		groupchat = args[0]
	else:
		if not source[1] in GROUPCHATS:
			reply(type, source, u'это возможно только в конференции')
			return
		groupchat = source[1]
		reason = ''
	if popups_check(groupchat):
		if reason:
			msg(groupchat, u'меня уводит '+source[2]+u' по причине:\n'+reason)
		else:
			msg(groupchat, u'меня уводит '+source[2])
	if reason:
		leave_groupchat(groupchat, u'меня уводит '+source[2]+u' по причине:\n'+reason)
	else:
		leave_groupchat(groupchat,u'меня уводит '+source[2])
	reply(type, source, u'я ушёл из ' + groupchat)


def handler_admin_msg(type, source, parameters):
	if not parameters:
		reply(type, source, u'ошибочный запрос. прочитай помощь по использованию команды')
		return
	msg(string.split(parameters)[0], string.join(string.split(parameters)[1:]))
	reply(type, source, u'сообщение ушло')
	
def handler_glob_msg_help(type, source, parameters):
	total = '0'
	totalblock='0'
	if GROUPCHATS:
		gch=GROUPCHATS.keys()
		for x in gch:
			if popups_check(x):
				msg(x, u'Новости от '+source[2]+u':\n'+parameters+u'\nНапоминаю, что как всегда все помощь можно получить написав "помощь".\nО всех глюках, ошибках, ляпях, а также предложения и конструктивную критику прошу направлять мне таким образом: пишем "передать botadmin и тут ваше сообщение", естественно без кавычек.\nСПАСИБО ЗА ВНИМАНИЕ!')
				totalblock = int(totalblock) + 1
			total = int(total) + 1
		reply(type, source, 'сообщение ушло в '+str(totalblock)+' конференций (из '+str(total)+')')
	else:
		reply(type, source, u'ошибочный запрос. прочитай помощь по использованию команды')
		
def handler_glob_msg(type, source, parameters):
	total = '0'
	totalblock='0'
	if parameters:
		if GROUPCHATS:
			gch=GROUPCHATS.keys()
			for x in gch:
				if popups_check(x):
					msg(x, u'Новости от '+source[2]+':\n'+parameters)
					totalblock = int(totalblock) + 1
				total = int(total) + 1
			reply(type, source, 'сообщение ушло в '+str(totalblock)+' конференций (из '+str(total)+')')
	else:
		reply(type, source, u'ошибочный запрос. прочитай помощь по использованию команды')
	

def handler_admin_say(type, source, parameters):
	if parameters:
		args=parameters.split()[0]
		msg(source[1], parameters)
	else:
		reply(type, source, u'ошибочный запрос. прочитай помощь по использованию команды')

def handler_admin_restart(type, source, parameters):
	if not source[1] in GROUPCHATS:
		source[2]=source[1].split('@')[0]
	if parameters:
		reason = parameters
	else:
		reason = ''
	gch=[]
	if GROUPCHATS:
		gch=GROUPCHATS.keys()
	if reason:
		for x in gch:
			if popups_check(x):
				msg(x, u'меня перезагружает '+source[2]+u' по причине:\n'+reason)
	else:
		for x in gch:
			if popups_check(x):
				msg(x, u'меня перезагружает '+source[2])
	prs=xmpp.Presence(typ='unavailable')
	if reason:
		prs.setStatus(source[2]+u': рестарт -> '+reason)
	else:
		prs.setStatus(source[2]+u': рестарт')
	JCON.send(prs)
	time.sleep(1)
	JCON.disconnect()

def handler_admin_exit(type, source, parameters):
	if not source[1] in GROUPCHATS:
		source[2]=source[1].split('@')[0]
	if parameters:
		reason = parameters
	else:
		reason = ''
	gch=[]
	if GROUPCHATS:
		gch=GROUPCHATS.keys()
	if reason:
		for x in gch:
			if popups_check(x):
				msg(x, u'меня выключает '+source[2]+u' по причине:\n'+reason)
	else:
		for x in gch:
			if popups_check(x):
				msg(x, u'меня выключает '+source[2])
	prs=xmpp.Presence(typ='unavailable')
	if reason:
		prs.setStatus(source[2]+u': выключаюсь -> '+reason)
	else:
		prs.setStatus(source[2]+u': выключаюсь')
	JCON.send(prs)
	time.sleep(2)
	os.abort()
	
def handler_popups_onoff(type, source, parameters):
	if not source[1] in GROUPCHATS:
		reply(type, source, u'это возможно только в конференции')
		return
	if parameters:
		try:
			parameters=int(parameters.strip())
		except:
			reply(type,source,u'ошибочный запрос. прочитай помощь по использованию команды')
			return		
		DBPATH='dynamic/'+source[1]+'/config.cfg'
		if parameters==1:
			GCHCFGS[source[1]]['popups']=1
			reply(type,source,u'глобальные оповещения включены')
		else:
			GCHCFGS[source[1]]['popups']=0
			reply(type,source,u'глобальные оповещения выключены')
		write_file(DBPATH,str(GCHCFGS[source[1]]))
	else:
		ison=GCHCFGS[source[1]]['popups']
		if ison==1:
			reply(type,source,u'здесь глобальные оповещения включены')
		else:
			reply(type,source,u'здесь глобальные оповещения выключены')
			
def handler_botautoaway_onoff(type, source, parameters):
	if not source[1] in GROUPCHATS:
		reply(type, source, u'это возможно только в конференции')
		return
	if parameters:
		try:
			parameters=int(parameters.strip())
		except:
			reply(type,source,u'ошибочный запрос. прочитай помощь по использованию команды')
			return		
		DBPATH='dynamic/'+source[1]+'/config.cfg'
		if parameters==1:
			GCHCFGS[source[1]]['autoaway']=1
			reply(type,source,u'автоотсутствие включено')
		else:
			GCHCFGS[source[1]]['autoaway']=0
			reply(type,source,u'автоотсутствие отключено')
		get_autoaway_state(source[1])
		write_file(DBPATH,str(GCHCFGS[source[1]]))
	else:
		ison=GCHCFGS[source[1]]['autoaway']
		if ison==1:
			reply(type,source,u'здесь автоотсутствие включено')
		else:
			reply(type,source,u'здесь автоотсутствие отключено')	
	
def handler_changebotstatus(type, source, parameters):
	if parameters:
		args,show,status=parameters.split(' ',1),'',''
		if args[0] in ['away','xa','dnd','chat']:
			show=args[0]
		else:
			show=None
			status=parameters
		if not status:
			try:
				status=args[1]
			except:
				status=None
		change_bot_status(source[1],status,show,0)
		GCHCFGS[gch]['status']={'status': status, 'show': show}
	else:
		stmsg=GROUPCHATS[source[1]][get_bot_nick(source[1])]['stmsg']
		status=GROUPCHATS[source[1]][get_bot_nick(source[1])]['status']
		if stmsg:
			reply(type,source, u'я сейчас '+status+u' ('+stmsg+u')')
		else:
			reply(type,source, u'я сейчас '+status)
			
def get_autoaway_state(gch):
	if not 'autoaway' in GCHCFGS[gch]:
		GCHCFGS[gch]['autoaway']=1
	if GCHCFGS[gch]['autoaway']:
		LAST['gch'][gch]['autoaway']=0
		LAST['gch'][gch]['thr']=None
		
def set_default_gch_status(gch):
	if isinstance(GCHCFGS[gch].get('status'), str): #temp workaround
		GCHCFGS[gch]['status']={'status': u'напишите "помощь" и следуйте указаниям, чтобы понять как со мной работать', 'show': u''}
	elif not isinstance(GCHCFGS[gch].get('status'), dict):
		GCHCFGS[gch]['status']={'status': u'напишите "помощь" и следуйте указаниям, чтобы понять как со мной работать', 'show': u''}


register_command_handler(handler_admin_join, 'зайти', ['суперадмин','мук','все'], 40, 'Зайти в определённую конференцию. Если она запаролена то пишите пароль сразу после её названия.', 'зайти <конференция> [pass=пароль] [причина]', ['зайти z@conference.jabber.aq', 'зайти z@conference.jabber.aq test', 'зайти z@conference.jabber.aq pass=1234 test'])
register_command_handler(handler_admin_leave, 'свал', ['админ','мук','все'], 20, 'Заставляет выйти из текущей или определённой конференции.', 'свал <конференция> [причина]', ['свал z@conference.jabber.aq спать', 'свал спать','свал'])
register_command_handler(handler_admin_msg, 'мессага', ['админ','мук','все'], 40, 'Отправляет сообщение от имени бота на определённый JID.', 'мессага <jid> <сообщение>', ['мессага guy@jabber.aq здорово чувак!'])
register_command_handler(handler_admin_say, 'сказать', ['админ','мук','все'], 20, 'Говорить через бота в конференции.', 'сказать <сообщение>', ['сказать салют пиплы'])
register_command_handler(handler_admin_restart, 'рестарт', ['суперадмин','все'], 100, 'Перезапускает бота.', 'рестарт [причина]', ['рестарт','рестарт ы!'])
register_command_handler(handler_admin_exit, 'пшёл', ['суперадмин','все'], 100, 'Остановка и полный выход бота.', 'пшёл [причина]', ['пшёл','пшёл глюки'])
register_command_handler(handler_glob_msg, 'globmsg', ['суперадмин','мук','все'], 100, 'Разослать сообщение (новостное) по всем конференциям, в которых сидит бот.', 'globmsg [сообщение]', ['globmsg всем привет!'])
register_command_handler(handler_glob_msg_help, 'hglobmsg', ['суперадмин','мук','все'], 100, 'Разослать сообщение (новостное) по всем конфам, в которых сидит бот. Сообщение будет содержать в себе предустановленный заголовок с короткой справкой об испольовании бота.', 'hglobmsg [сообщение]', ['hglobmsg всем привет!'])
register_command_handler(handler_popups_onoff, 'popups', ['админ','мук','все'], 30, 'Отключает (0) или включает (1) сообщения о входах/выходах, рестартах/выключениях, а также глобальные новости. Без параметра покажет текущее состояние.', 'popups [1|0]', ['popups 1','popups'])
register_command_handler(handler_botautoaway_onoff, 'autoaway', ['админ','мук','все'], 30, 'Отключает (0) или включает (1) автосмену статуса бота на away при отсутствии команд в течении 10 минут. Без параметра покажет текущее состояние.', 'autoaway [1|0]', ['autoaway 1','autoaway'])
register_command_handler(handler_changebotstatus, 'stch', ['админ','мук','все'], 20, 'Меняет статус бота на указанный из списка:\naway - отсутствую,\nxa - давно отсутствую,\ndnd - не беспокоить,\nchat - хочу чатиться,\nа также статусное сообщение (если оно даётся).', 'stch [статус] [сообщение]', ['stch away','stch away я сдох'])

register_stage1_init(get_autoaway_state)
register_stage1_init(set_default_gch_status)
