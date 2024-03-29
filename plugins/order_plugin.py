#===istalismanplugin===
# -*- coding: utf-8 -*-

#  Talisman plugin
#  order_plugin.py

#  Initial Copyright © 2007 Als <Als@exploit.in>
#  First Version and Idea © 2007 dimichxp <dimichxp@gmail.com>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

order_stats = {}
order_obscene_raw_words = [u'бляд', u' блят', u' бля ', u' блять ', u' плять ', u' хуй', u' ибал', u' ебал', u'нахуй', u' хуй', u' хуи', u'хуител', u' хуя', u'хуя', u' хую', u' хуе', u' ахуе', u' охуе', u'хуев', u' хер ', u' хер', u'хер', u' пох ', u' нах ', u'писд', u'пизд', u'рizd', u' пздц ', u' еб', u' ёб', u' епана ', u' епать ', u' ипать ', u' выепать ', u' ибаш', u' уеб', u'проеб', u'праеб', u'приеб', u'съеб', u'сьеб', u'взъеб', u'взьеб', u'въеб', u'вьеб', u'выебан', u'перееб', u'недоеб', u'долбоеб', u'долбаеб', u' ниибац', u' неебац', u' неебат', u' ниибат', u' пидар', u' рidаr', u' пидар', u' пидор', u'педор', u'пидор', u'пидарас', u'пидараз', u' педар', u'педри', u'пидри', u' заеп', u' заип', u' заеб', u'ебучий', u'ебучка ', u'епучий', u'епучка ', u' заиба', u'заебан', u'заебис', u' выеб', u'выебан', u' поеб', u' наеб', u' наеб', u'сьеб', u'взьеб', u'вьеб', u' гандон', u' гондон', u'пахуи', u'похуис', u' манда ', u'мандав', u' залупа', u' залупог']

global stop_spam_list
global stop_global_spam_list
check_file(file='spam.txt')
db=eval(read_file('dynamic/spam.txt'))
stop_global_spam_list = db.values()

order_obscene_words = []

for word in order_obscene_raw_words:
	order_obscene_words.append(re.compile(word, re.I+re.U))
	
def order_check_db(gch,jid,nick):
	if nick in GROUPCHATS[gch]:
		order_stats[gch][jid]={'kicks': 0, 'devoice': {'cnd': 0, 'time': 0}, 'msgbody': '', 'prstime': {'fly': 0, 'status': 0}, 'prs': {'fly': 0, 'status': 0}, 'msg': 0, 'msgtime': 0, 'flood': 0, 'smile': 0}
	check_file(gch, 'spam.txt')
	global stop_spam_list
	db=eval(read_file('dynamic/'+gch+'/spam.txt'))
	stop_spam_list = db.values()
	
	

def order_check_obscene_words(body, ff=0):
	body=u' '+body+u' '
	if ff:
		for x in order_obscene_words:
			body=re.sub(x, order_mask_badword, body)
		return body
	else:
		for x in order_obscene_raw_words:
			if body.count(x):
				return True
	return False
	
def order_mask_badword(mobj):
	bword,mword=mobj.group(0),u'%s'
	mask=list(string.punctuation)
	random.shuffle(mask)
	if bword.startswith(' '):
		mword=u' '+mword
	if bword.endswith(' '):
		mword=mword+u' '
	return mword % u''.join(mask[:len(bword.strip())])
	
##############################################################################

def order_check_time_flood(body, gch, jid, nick, ff=0):
	lastmsg=order_stats[gch][jid]['msgtime']
	if lastmsg and time.time()-lastmsg<=2.2:
		order_stats[gch][jid]['msg']+=1
		if order_stats[gch][jid]['msg']>3:
			order_stats[gch][jid]['devoice']['time']=time.time()
			order_stats[gch][jid]['devoice']['cnd']=1
			order_stats[gch][jid]['msg']=0
			order_kick(gch, nick, u'слишком быстрая отправка сообщений')
			return True
		if ff :	return ''
	if ff: return body
	return False

def order_check_len_flood(mlen, body, gch, jid, nick, ff=0):
	if len(body)>mlen:
		order_stats[gch][jid]['flood']+=1
		if order_stats[gch][jid]['flood']>3:
			order_stats[gch][jid]['devoice']['time']=time.time()
			order_stats[gch][jid]['devoice']['cnd']=1
			order_kick(gch, nick, u'флуд')
			return True
		if ff: return body[:mlen]+u' ...'
	if ff: return body
	return False

def order_check_obscene(body, gch, jid, nick, ff=0):
	body=order_check_obscene_words(body, ff)
	if body:
		if ff:
			return body
		order_stats[gch][jid]['devoice']['time']=time.time()
		order_stats[gch][jid]['devoice']['cnd']=1
		order_kick(gch, nick, u'нецензурно')
		return True
	if ff: return body
	return False

def order_check_caps(body, gch, jid, nick, ff=0):
	if len(body)>5:
		tbody,ccnt=body,0
		nicks = GROUPCHATS[gch].keys()
		for x in nicks:
			if tbody.count(x):
				tbody=tbody.replace(x,'')
		for x in [x for x in tbody.replace(' ', '')]:
			if x.isupper():
				ccnt+=1
			if ccnt>=len(tbody)/2 and ccnt>9:
				if ff: return tbody.lower()
				order_stats[gch][jid]['devoice']['time']=time.time()
				order_stats[gch][jid]['devoice']['cnd']=1
				order_kick(gch, nick, u'слишком много ЗАГЛАВНЫХ букв')
				return True
	if ff: return body
	return False

def order_check_like(body, gch, jid, nick, ff=0):
	lcnt=0
	lastmsg=order_stats[gch][jid]['msgtime']
	if lastmsg and order_stats[gch][jid]['msgbody']:
		if time.time()-lastmsg>60:
			order_stats[gch][jid]['msgbody']=body.split()
		else:
			for x in order_stats[gch][jid]['msgbody']:
				for y in body.split():
					if x==y:
						lcnt+=1
			if lcnt:
				lensrcmsgbody=len(body.split())
				lenoldmsgbody=len(order_stats[gch][jid]['msgbody'])
				avg=(lensrcmsgbody+lenoldmsgbody/2)/2
				if lcnt>=avg:
					order_stats[gch][jid]['msg']+=1
					if order_stats[gch][jid]['msg']>=2:
						order_stats[gch][jid]['devoice']['time']=time.time()
						order_stats[gch][jid]['devoice']['cnd']=1
						order_stats[gch][jid]['msg']=0
						order_kick(gch, nick, u'сообщения слишком похожи')
						return True
					if ff: body=''
			order_stats[gch][jid]['msgbody']=body.split()
	else:
		order_stats[gch][jid]['msgbody']=body.split()
	if ff:	return body
	return False
	
def order_check_newline(body, gch, jid, nick, ff=0):
	ncnt=body.count(u'\n')
	if ncnt>10 :
		if ff: return body.replace(u'\n', u'', ncnt-10)
		order_stats[gch][jid]['devoice']['time']=time.time()
		order_stats[gch][jid]['devoice']['cnd']=1
		order_kick(gch, nick, u'слишком много переносов строки')
		return True
	if ff: return body
	return False
	
def order_check_smile(body, gch, jid, nick, ff=0):
	resmile=re.compile(r"[0o>}\])]?[:;8%\+\^=][',]?-?(?:[\^_sdpco0#@*$|]|\)+|\(+)=?", re.I)
	smlcnt,tmpsml=len(re.findall(resmile, body)),0
	for word in body.split():
		if word.startswith('*') and word.endswith('*') and word[1:-1].isupper():	tmpsml+=1
	smlcnt+=tmpsml
	if smlcnt > 3:
		order_stats[gch][jid]['smile']+=1
		if order_stats[gch][jid]['smile']>=3:
			order_stats[gch][jid]['devoice']['time']=time.time()
			order_stats[gch][jid]['devoice']['cnd']=1
			order_kick(gch, nick, u'слишком много смайликов :)')
			return True
		if ff: return re.sub(resmile, u'', body, smlcnt-3)
	if ff: return body
	return False
	
def order_check_longword(body, gch, jid, nick, ff=0):
	for word in body.split():
		if len(word)>20 and not body.startswith(u'http:'):
			order_stats[gch][jid]['devoice']['time']=time.time()
			order_stats[gch][jid]['devoice']['cnd']=1
			order_kick(gch, nick, u'гиппопотомонстросескиппедалофаг')
			return True
	if ff: return body
	return False
	
def order_check_spam(body, gch, jid, nick, ff=0):
	for x in stop_spam_list:
		spam_re = re.compile(x, re.I)
		if spam_re.search(body):
			order_kick(gch, nick, u'Спамер несчастный!')
			return True
	for x in stop_global_spam_list:
		spam_re = re.compile(x, re.I)
		if spam_re.search(body):
			order_kick(gch, nick, u'Спамер несчастный!')
			return True	
	if ff: return body
	return False

####################################################################################################

def order_kick(groupchat, nick, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	kick=query.addChild('item', {'nick':nick, 'role':'none'})
	kick.setTagData('reason', get_bot_nick(groupchat)+': '+reason)
	iq.addChild(node=query)
	JCON.send(iq)

def order_visitor(groupchat, nick, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	visitor=query.addChild('item', {'nick':nick, 'role':'visitor'})
	visitor.setTagData('reason', get_bot_nick(groupchat)+u': '+reason)
	iq.addChild(node=query)
	JCON.send(iq)

def order_ban(groupchat, nick, reason):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	ban=query.addChild('item', {'nick':nick, 'affiliation':'outcast'})
	ban.setTagData('reason', get_bot_nick(groupchat)+u': '+reason)
	iq.addChild(node=query)
	JCON.send(iq)

def order_unban(groupchat, jid):
	iq = xmpp.Iq('set')
	iq.setTo(groupchat)
	iq.setID('kick'+str(random.randrange(1000, 9999)))
	query = xmpp.Node('query')
	query.setNamespace('http://jabber.org/protocol/muc#admin')
	query.addChild('item', {'jid':jid, 'affiliation':'none'})
	iq.addChild(node=query)
	JCON.send(iq)

def order_check_idle():
	for gch in GROUPCHATS.keys():
		if GCHCFGS[gch]['filt']['idle']['cond']==1:
			timee=GCHCFGS[gch]['filt']['idle']['time']
			now=time.time()
			for nick in GROUPCHATS[gch].keys():
				if GROUPCHATS[gch][nick]['ishere']==1:
					if user_level(gch+'/'+nick,gch)<11:
						idle=now-GROUPCHATS[gch][nick]['idle']
						if idle > timee:
							order_kick(gch, nick, u'молчание более '+timeElapsed(idle))
	threading.Timer(120,order_check_idle).start()

####################################################################################################

def handler_order_message(raw, type, source, body):
	nick=source[2]
	groupchat=source[1]
	if groupchat in GROUPCHATS.keys() and user_level(source,groupchat)<11:
		if get_bot_nick(groupchat)!=nick:
			jid=get_true_jid(groupchat+'/'+nick)
			filt=GCHCFGS[groupchat]['filt']
			if groupchat in order_stats and jid in order_stats[groupchat]:
				if raw == 1:
					if filt['time']==1:
						body=order_check_time_flood(body, groupchat, jid, nick, raw)
					if filt['len']==1:
						if body != True:
							body=order_check_len_flood(1500, body, groupchat, jid, nick, raw)
						else:
							return ''
					if filt['long']==1:
						if body != True:
							body=order_check_longword(body, groupchat, jid, nick, raw)
						else:
							return ''
					if filt['newline']==1:
						if body != True:
							body=order_check_newline(body, groupchat, jid, nick, raw)
						else:
							return ''
					if filt['spam']==1:
						if body != True:
							body=order_check_spam(body, groupchat, jid, nick, raw)
						else:
							return ''
					if filt['caps']==1:
						if body != True:
							body=order_check_caps(body, groupchat, jid, nick, raw)
						else:
							return ''
					if filt['like']==1:
						if body != True:
							body=order_check_like(body, groupchat, jid, nick, raw)
						else:
							return ''
					if filt['obscene']==1:
						if body != True:
							body=order_check_obscene(body, groupchat, jid, nick, raw)
						else:
							return ''
					if filt['smile']==1:
						if body != True:
							body=order_check_smile(body, groupchat, jid, nick, raw)
						else:
							return ''
					return body
				if not filt['fltmode']:
					if filt['long']==1:
						if order_check_longword(body, groupchat, jid, nick, raw):	return
					if filt['spam']==1:
						if order_check_spam(body, groupchat, jid, nick, raw):	return
					if filt['time']==1:
						if order_check_time_flood(body, groupchat, jid, nick):	return
					if filt['len']==1:
						if order_check_len_flood(1500, body, groupchat, jid, nick):	return
					if filt['obscene']==1:
						if order_check_obscene(body, groupchat, jid, nick):	return
					if filt['caps']==1:
						if order_check_caps(body, groupchat, jid, nick):	return
					if filt['like']==1:
						if order_check_like(body, groupchat, jid, nick):	return
					if filt['newline']==1:
						if order_check_newline(body, groupchat, jid, nick):	return
					if filt['smile']==1:
						if order_check_smile(body, groupchat, jid, nick):	return
					order_stats[groupchat][jid]['msgtime']=time.time()


def handler_order_join(groupchat, nick, aff, role):
	jid=get_true_jid(groupchat+'/'+nick)
	if nick in GROUPCHATS[groupchat] and user_level(groupchat+'/'+nick,groupchat)<11:
		now = time.time()
		if not groupchat in order_stats.keys():
			order_stats[groupchat] = {}
		order_check_db(groupchat,jid,nick)
		ostats=order_stats[groupchat][jid]
		if ostats['devoice']['cnd']==1:
			if now-ostats['devoice']['time']>300:
				ostats['devoice']['cnd']=0
			else:
				order_visitor(groupchat, nick, u'право голоса снято за предыдущие нарушения')

		if GCHCFGS[groupchat]['filt']['kicks']['cond']==1:
			kcnt=GCHCFGS[groupchat]['filt']['kicks']['cnt']
			if ostats['kicks']>kcnt:
				order_ban(groupchat, nick, u'слишком много киков')
				return

		if GCHCFGS[groupchat]['filt']['fly']['cond']==1:
			lastprs=ostats['prstime']['fly']
			ostats['prstime']['fly']=time.time()
			if now-lastprs<=70:
				ostats['prs']['fly']+=1
				if ostats['prs']['fly']>4:
					ostats['prs']['fly']=0
					fmode=GCHCFGS[groupchat]['filt']['fly']['mode']
					ftime=GCHCFGS[groupchat]['filt']['fly']['time']
					if fmode=='ban':
						order_ban(groupchat, nick, u'хватит летать')
						time.sleep(ftime)
						order_unban(groupchat, jid)
					else:
						order_kick(groupchat, nick, u'хватит летать')
						return
			else:
				ostats['prs']['fly']=0

		if GCHCFGS[groupchat]['filt']['obscene']==1:
			if order_check_obscene(nick, groupchat, jid, nick):	return

		if GCHCFGS[groupchat]['filt']['len']==1:
			if order_check_len_flood(20, nick, groupchat, jid, nick):	return

	elif groupchat in order_stats and jid in order_stats[groupchat]:
		del order_stats[groupchat][jid]
	else:
		pass

def handler_order_presence(prs):
	ptype = prs.getType()
	if ptype in ['unavailable','error']:
		return
	groupchat = prs.getFrom().getStripped()
	nick = prs.getFrom().getResource()
	stmsg = prs.getStatus()
	jid=get_true_jid(groupchat+'/'+nick)
	item=findPresenceItem(prs)

	if groupchat in order_stats and jid in order_stats[groupchat]:
		if item['affiliation'] in ['member','admin','owner']:
			del order_stats[groupchat][jid]
			return
	else:
		if item['affiliation']=='none':
			order_check_db(groupchat,jid,nick)

	if nick in GROUPCHATS[groupchat] and user_level(groupchat+'/'+nick,groupchat)<11:
		if groupchat in order_stats and jid in order_stats[groupchat]:
			ostats=order_stats[groupchat][jid]
			now = time.time()
			if now-GROUPCHATS[groupchat][nick]['joined']>1:
				if item['role']=='participant':
					ostats['devoice']['cnd']=0
				lastprs=ostats['prstime']['status']
				ostats['prstime']['status']=now

				if GCHCFGS[groupchat]['filt']['presence']==1:
					if now-lastprs>300:
						ostats['prs']['status']=0
					else:
						ostats['prs']['status']+=1
						if ostats['prs']['status']>5:
							ostats['prs']['status']=0
							order_kick(groupchat, nick, u'презенс-флуд')
							return

				if GCHCFGS[groupchat]['filt']['obscene']==1:
					if order_check_obscene(nick, groupchat, jid, nick):	return

				if GCHCFGS[groupchat]['filt']['prsstlen']==1 and stmsg:
					if order_check_len_flood(200, nick, groupchat, jid, nick):	return

def handler_order_leave(groupchat, nick, reason, code):
	jid=get_true_jid(groupchat+'/'+nick)
	if nick in GROUPCHATS[groupchat] and user_level(groupchat+'/'+nick,groupchat)<11:
		if groupchat in order_stats and jid in order_stats[groupchat]:
			if GCHCFGS[groupchat]['filt']['presence']==1:
				if reason=='Replaced by new connection':
					return
				if code:
					if code=='307': # kick
						order_stats[groupchat][jid]['kicks']+=1
						return
					elif code=='301': # ban
						del order_stats[groupchat][jid]
						return
					elif code=='407': # members-only
						return
			if GCHCFGS[groupchat]['filt']['fly']['cond']==1:
				now = time.time()
				lastprs=order_stats[groupchat][jid]['prstime']['fly']
				order_stats[groupchat][jid]['prstime']['fly']=time.time()
				if now-lastprs<=70:
					order_stats[groupchat][jid]['prs']['fly']+=1
				else:
					order_stats[groupchat][jid]['prs']['fly']=0

######################################################################################################################

def handler_order_filt(type, source, parameters):
	if parameters:
		parameters=parameters.split()
		if len(parameters)<2:
			reply(type,source,u'синтакс инвалид')
			return
		if GCHCFGS[source[1]].has_key('filt'):
			if parameters[0]=='time':
				if parameters[1]=='0':
					reply(type,source,u'временная фильтрация сообщений отключена')
					GCHCFGS[source[1]]['filt']['time']=0
				elif parameters[1]=='1':
					reply(type,source,u'временная фильтрация сообщений включена')
					GCHCFGS[source[1]]['filt']['time']=1
				else:
					reply(type,source,u'синтакс инвалид')
			elif parameters[0]=='presence':
				if parameters[1]=='0':
					reply(type,source,u'временная фильтрация презенсов отключена')
					GCHCFGS[source[1]]['filt']['presence']=0
				elif parameters[1]=='1':
					reply(type,source,u'временная фильтрация презенсов включена')
					GCHCFGS[source[1]]['filt']['presence']=1
				else:
					reply(type,source,u'синтакс инвалид')
			elif parameters[0]=='len':
				if parameters[1]=='0':
					reply(type,source,u'фильтрация длинных сообщений отключена')
					GCHCFGS[source[1]]['filt']['len']=0
				elif parameters[1]=='1':
					reply(type,source,u'фильтрация длинных сообщений включена')
					GCHCFGS[source[1]]['filt']['len']=1
				else:
					reply(type,source,u'синтакс инвалид')
			elif parameters[0]=='like':
				if parameters[1]=='0':
					reply(type,source,u'фильтрация подозрительно одинаковых сообщений отключена')
					GCHCFGS[source[1]]['filt']['like']=0
				elif parameters[1]=='1':
					reply(type,source,u'фильтрация подозрительно одинаковых сообщений включена')
					GCHCFGS[source[1]]['filt']['like']=1
				else:
					reply(type,source,u'синтакс инвалид')
			elif parameters[0]=='caps':
				if parameters[1]=='0':
					reply(type,source,u'фильтрация капса отключена')
					GCHCFGS[source[1]]['filt']['caps']=0
				elif parameters[1]=='1':
					reply(type,source,u'фильтрация капса включена')
					GCHCFGS[source[1]]['filt']['caps']=1
				else:
					reply(type,source,u'синтакс инвалид')
			elif parameters[0]=='spam':
				if parameters[1]=='0':
					reply(type,source,u'фильтрация спама отключена')
					GCHCFGS[source[1]]['filt']['spam']=0
				elif parameters[1]=='1':
					reply(type,source,u'фильтрация спама включена')
					GCHCFGS[source[1]]['filt']['spam']=1
				else:
					reply(type,source,u'синтакс инвалид')
			elif parameters[0]=='prsstlen':
				if parameters[1]=='0':
					reply(type,source,u'фильтрация длинных статусных сообщений отключена')
					GCHCFGS[source[1]]['filt']['prsstlen']=0
				elif parameters[1]=='1':
					reply(type,source,u'фильтрация длинных статусных сообщений включена')
					GCHCFGS[source[1]]['filt']['prsstlen']=1
				else:
					reply(type,source,u'синтакс инвалид')
			elif parameters[0]=='obscene':
				if parameters[1]=='0':
					reply(type,source,u'фильтрация мата отключена')
					GCHCFGS[source[1]]['filt']['obscene']=0
				elif parameters[1]=='1':
					reply(type,source,u'фильтрация мата включена')
					GCHCFGS[source[1]]['filt']['obscene']=1
				else:
					reply(type,source,u'синтакс инвалид')
			elif parameters[0]=='fly':
				if parameters[1]=='cnt':
					try:
						int(parameters[2])
					except:
						reply(type,source,u'синтакс инвалид')
					if int(parameters[2]) in xrange(0,121):
						reply(type,source,u'разморозка установлена на '+parameters[2]+u' секунд')
						GCHCFGS[source[1]]['filt']['fly']['time']=int(parameters[2])
					else:
						reply(type,source,u'не более двух минут (120 секунд)')
				elif parameters[1]=='mode':
					if parameters[2] in ['kick','ban']:
						if parameters[2] == 'ban':
							reply(type,source,u'за полёты будем банить')
							GCHCFGS[source[1]]['filt']['fly']['mode']='ban'
						else:
							reply(type,source,u'за полёты будем кикать')
							GCHCFGS[source[1]]['filt']['fly']['mode']='kick'
					else:
						reply(type,source,u'синтакс инвалид')
				elif parameters[1]=='0':
					reply(type,source,u'фильтр полётов отключен')
					GCHCFGS[source[1]]['filt']['fly']['cond']=0
				elif parameters[1]=='1':
					reply(type,source,u'фильтр полётов включен')
					GCHCFGS[source[1]]['filt']['fly']['cond']=1
				else:
					reply(type,source,u'синтакс инвалид')
			elif parameters[0]=='kicks':
				if parameters[1]=='cnt':
					try:
						int(parameters[2])
					except:
						reply(type,source,u'синтакс инвалид')
					if int(parameters[2]) in xrange(2,10):
						reply(type,source,u'автобан после '+parameters[2]+u' киков')
						GCHCFGS[source[1]]['filt']['kicks']['cnt']=int(parameters[2])
					else:
						reply(type,source,u'от 2 до 10 киков')
				elif parameters[1]=='0':
					reply(type,source,u'фильтр автобана после нескольких киков отключен')
					GCHCFGS[source[1]]['filt']['kicks']['cond']=0
				elif parameters[1]=='1':
					reply(type,source,u'фильтр автобана после нескольких киков включен')
					GCHCFGS[source[1]]['filt']['kicks']['cond']=1
				else:
					reply(type,source,u'синтакс инвалид')
			elif parameters[0]=='idle':
				if parameters[1]=='time':
					try:
						int(parameters[2])
					except:
						reply(type,source,u'синтакс инвалид')
					reply(type,source,u'кик за молчание после '+parameters[2]+u' секунд ('+timeElapsed(int(parameters[2]))+u')')
					GCHCFGS[source[1]]['filt']['idle']['time']=int(parameters[2])
				elif parameters[1]=='0':
					reply(type,source,u'фильтр кика за молчание отключен')
					GCHCFGS[source[1]]['filt']['idle']['cond']=0
				elif parameters[1]=='1':
					reply(type,source,u'фильтр кика за молчание включен')
					GCHCFGS[source[1]]['filt']['idle']['cond']=1
			elif parameters[0]=='newline':
				if parameters[1]=='0':
					reply(type,source,u'фильтрация множественных переносов строки отключена')
					GCHCFGS[source[1]]['filt']['newline']=0
				elif parameters[1]=='1':
					reply(type,source,u'фильтрация множественных переносов строки включена')
					GCHCFGS[source[1]]['filt']['newline']=1
				else:
					reply(type,source,u'синтакс инвалид')
			elif parameters[0]=='smile':
				if parameters[1]=='0':
					reply(type,source,u'фильтрация смайликов отключена')
					GCHCFGS[source[1]]['filt']['smile']=0
				elif parameters[1]=='1':
					reply(type,source,u'фильтрация смайликов включена')
					GCHCFGS[source[1]]['filt']['smile']=1
				else:
					reply(type,source,u'синтакс инвалид')
			elif parameters[0]=='long':
				if parameters[1]=='0':
					reply(type,source,u'фильтрация длинных слов отключена')
					GCHCFGS[source[1]]['filt']['long']=0
				elif parameters[1]=='1':
					reply(type,source,u'фильтрация длинных слов включена')
					GCHCFGS[source[1]]['filt']['long']=1
				else:
					reply(type,source,u'синтакс инвалид')
			else:
				reply(type,source,u'синтакс инвалид')
				return
			#save_gch_cfg(source[1])
		else:
			reply(type,source,u'случилось что-то странное, ткните админа бота')
	else:
		rep,foff,fon=u'',[],[]
		time=GCHCFGS[source[1]]['filt']['time']
		prs=GCHCFGS[source[1]]['filt']['presence']
		flen=GCHCFGS[source[1]]['filt']['len']
		like=GCHCFGS[source[1]]['filt']['like']
		caps=GCHCFGS[source[1]]['filt']['caps']
		prsstlen=GCHCFGS[source[1]]['filt']['prsstlen']
		obscene=GCHCFGS[source[1]]['filt']['obscene']
		fly=GCHCFGS[source[1]]['filt']['fly']['cond']
		flytime=str(GCHCFGS[source[1]]['filt']['fly']['time'])
		flymode=GCHCFGS[source[1]]['filt']['fly']['mode']
		kicks=GCHCFGS[source[1]]['filt']['kicks']['cond']
		kickscnt=str(GCHCFGS[source[1]]['filt']['kicks']['cnt'])
		idle=GCHCFGS[source[1]]['filt']['idle']['cond']
		idletime=GCHCFGS[source[1]]['filt']['idle']['time']
		newline=GCHCFGS[source[1]]['filt']['newline']
		smile=GCHCFGS[source[1]]['filt']['smile']
		longw=GCHCFGS[source[1]]['filt']['long']
		fltmode=GCHCFGS[source[1]]['filt']['fltmode']
		spam=GCHCFGS[source[1]]['filt']['spam']
		if time:
			fon.append(u'временная фильтрация сообщений')
		else:
			foff.append(u'временная фильтрация сообщений')
		if spam:
			fon.append(u'фильтрация по стоп-спам листу')
		else:
			foff.append(u'фильтрация по стоп-спам листу')
		if prs:
			fon.append(u'временная фильтрация презенсов')
		else:
			foff.append(u'временная фильтрация презенсов')
		if flen:
			fon.append(u'фильтрация длинных сообщений')
		else:
			foff.append(u'фильтрация длинных сообщений')
		if like:
			fon.append(u'фильтрация подозрительно одинаковых сообщений')
		else:
			foff.append(u'фильтрация подозрительно одинаковых сообщений')
		if caps:
			fon.append(u'фильтрация капса')
		else:
			foff.append(u'фильтрация капса')
		if prsstlen:
			fon.append(u'фильтрация длинных статусных сообщений')
		else:
			foff.append(u'фильтрация длинных статусных сообщений')
		if obscene:
			fon.append(u'фильтрация мата')
		else:
			foff.append(u'фильтрация мата')
		if fly:
			fon.append(u'фильтр полётов (режим '+flymode+u', таймер '+flytime+u' секунд)')
		else:
			foff.append(u'фильтр полётов')
		if kicks:
			fon.append(u'автобан после '+kickscnt+u' киков')
		else:
			foff.append(u'автобан после нескольких киков')
		if idle:
			fon.append(u'кик за молчание через '+str(idletime)+u' секунд ('+timeElapsed(idletime)+u')')
		else:
			foff.append(u'кик за молчание')
		if newline:
			fon.append(u'фильтрация множественных переносов строки')
		else:
			foff.append(u'фильтрация множественных переносов строки')
		if smile:
			fon.append(u'фильтрация смайлов')
		else:
			foff.append(u'фильтрация смайлов')
		if longw:
			fon.append(u'фильтрация длинных слов')
		else:
			foff.append(u'фильтрация длинных слов')
		if fltmode:
			fon.append(u'\nфильтрация через сервер конференций')
		else:
			foff.append(u'\nфильтрация через сервер конференций')
		fon=u', '.join(fon)
		foff=u', '.join(foff)
		if fon:
			rep+=u'ВКЛЮЧЕНЫ\n'+fon+u'\n\n'
		if foff:
			rep+=u'ВЫКЛЮЧЕНЫ\n'+foff
		reply(type,source,rep.strip())


def get_order_cfg(gch):
	if not 'filt' in GCHCFGS[gch]:
		GCHCFGS[gch]['filt']={}
	for x in ['time','presence','len','like','caps','prsstlen','obscene','kicks','fly','excess','idle','newline','fltmode','smile','long', 'spam']:
		if x == 'excess':
			if not x in GCHCFGS[gch]['filt']:
				GCHCFGS[gch]['filt'][x]={'cond':0, 'mode': 'kick'}
			continue
		if x == 'kicks':
			if not x in GCHCFGS[gch]['filt']:
				GCHCFGS[gch]['filt'][x]={'cond':1, 'cnt': 2}
			continue
		if x == 'fly':
			if not x in GCHCFGS[gch]['filt']:
				GCHCFGS[gch]['filt'][x]={'cond':1, 'mode': 'ban', 'time': 60}
			continue
		if x == 'idle':
			if not x in GCHCFGS[gch]['filt']:
				GCHCFGS[gch]['filt'][x]={'cond':0, 'time': 3600}
			continue
		if x == 'fltmode':
			if not x in GCHCFGS[gch]['filt']:
				GCHCFGS[gch]['filt'][x]=0
			continue
		if not x in GCHCFGS[gch]['filt']:
			GCHCFGS[gch]['filt'][x]=1

###############################################
def handler_spam_add(type, source, parameters):
	global stop_global_spam_list
	global stop_spam_list
	if not parameters:
		reply(type, source, u'ииии?')
	try:
		re.compile(parameters)
	except:
		reply(type, source, u'Фигня этот ваш регексп')
		return False
	for x in stop_spam_list:
		if parameters.count(x):
			reply(type, source, u'такое уже есть')
			return False
	for x in stop_global_spam_list:
		if parameters.count(x):
			reply(type, source, u'такое уже есть')
			return False	
	res=spam_add(source[1],parameters,'dynamic/'+source[1]+'/spam.txt')
	db=eval(read_file('dynamic/'+source[1]+'/spam.txt'))
	stop_spam_list = db.values()
	if res: reply(type, source, u'добавлено')	
	
def handler_spam_del(type, source, parameters):
	if not parameters:
		reply(type, source, u'ииии?')
	res=spam_del(source[1],parameters,'dynamic/'+source[1]+'/spam.txt')
	db=eval(read_file('dynamic/'+source[1]+'/spam.txt'))
	stop_spam_list = db.values()
	if res: reply(type, source, u'удалено')
		
def handler_spam_show(type, source, parameters):
	rep,res=u'',spam_show(source[1],DBPATH='dynamic/'+source[1]+'/spam.txt')
	if res:
		res=sorted(res.items(),lambda x,y: int(x[0]) - int(y[0]))
		for num,phrase in res:
			rep+=num+u') '+phrase+u'\n'
		reply(type,source,rep.strip())
	else:
		reply(type,source,u'нет стоп-спам фраз')

def spam_add(gch,phrase=None,DBPATH=None):
	if check_file(gch,'spam.txt'):
		spamdb = eval(read_file(DBPATH))
		for x in range(1, 201):
			if str(x) in spamdb.keys():
				continue
			else:
				spamdb[str(x)]=phrase
				write_file(DBPATH, str(spamdb))
				return True
		return False
	else:
		return None
		
def spam_del(gch,phrase=None,DBPATH=None):
	if check_file(gch,'spam.txt'):
		spamdb = eval(read_file(DBPATH))
		if phrase=='0':
			spamdb.clear()
			write_file(DBPATH, str(spamdb))
			return True
		else:
			try:
				del spamdb[phrase]
				write_file(DBPATH, str(spamdb))
				return True
			except:
				return False
	else:
		return None
		
def spam_show(gch,phrase=None,DBPATH=None):
	if check_file(gch,'spam.txt'):
		spamdb = eval(read_file(DBPATH))
		return spamdb
	else:
		return None
		
#############################################################

def handler_global_spam_add(type, source, parameters):
	global stop_global_spam_list
	if not parameters:
		reply(type, source, u'ииии?')
	try:
		re.compile(parameters)
	except:
		reply(type, source, u'Фигня этот ваш регексп')	
		return False
	for x in stop_global_spam_list:
		if parameters.count(x):
			reply(type, source, u'такое уже есть')
			return False
	res=spam_add(source[1],parameters,'dynamic/spam.txt')
	db=eval(read_file('dynamic/spam.txt'))
	stop_global_spam_list = db.values()
	if res: reply(type, source, u'добавлено')	
	
def handler_global_spam_del(type, source, parameters):
	global stop_global_spam_list
	if not parameters:
		reply(type, source, u'ииии?')
	res=spam_del(source[1],parameters,'dynamic/spam.txt')
	db=eval(read_file('dynamic/spam.txt'))
	stop_global_spam_list = db.values()
	if res: reply(type, source, u'удалено')
		
def handler_global_spam_show(type, source, parameters):
	rep,res=u'',spam_show(source[1],DBPATH='dynamic/spam.txt')
	if res:
		res=sorted(res.items(),lambda x,y: int(x[0]) - int(y[0]))
		for num,phrase in res:
			rep+=num+u') '+phrase+u'\n'
		reply(type,source,rep.strip())
	else:
		reply(type,source,u'нет стоп-спам фраз')

#############################################################

register_message_handler(handler_order_message)
register_join_handler(handler_order_join)
register_leave_handler(handler_order_leave)
register_presence_handler(handler_order_presence)
register_command_handler(handler_order_filt, 'filt', ['админ','мук','все'], 20, 'Включает или отключает определённые фильтры для конференции.\ntime - временной фильтр (не более одного сообщения в 2.2 секунды)\nlen - количественный фильтр (кол-во символов в сообщении не более 1500)\npresence - фильтр презенсов (не более 5 презенсов за 5 минут)\nlike - фильтр одинаковых сообщений (не более 2 одинаковых или очень похожих подряд)\ncaps - фильтр ЗАГЛАВНЫХ букв (не более 9 и не более чем половина сообщения)\nprsstlen - фильтр длинных статусных сообщений (не более 200 символов)\nobscene - фильтр матов\nfly - фильтр полётов (частых входов/выходов в конмату), имеет два режима ban и kick, таймер от 0 до 120 секунд\nkicks - автобан после N киков, параметр cnt - количество киков от 1 до 10\nidle - кик за молчание в общем чате после N секунд, параметр time - кол-во секунд для срабатывания\nlong - фильтрация длинных слов (более 20 букв)\nsmile - фильтр смайликов (не более 3 в сообщении)\nnl - фильтр множественных переносов строк в сообщении и презенсе (не более 10 переносов)', 'filt [фильтр] [режим] [состояние]', ['filt smile 1', 'filt len 0','filt fly mode ban'])
register_command_handler(handler_spam_add, 'spam+', ['админ','мук','все'], 15, 'Добавить фразу в чёрный спам-список. Можно добавлять не фразы, а регулярные выражения, если Вы не знаете, что это, лучше просто добавьте фразу. ', 'spam+ <фраза>', ['spam+ чики'])
register_command_handler(handler_spam_del, 'spam-', ['админ','мук','все'], 15, 'Удалить фразу из спам-списка', 'spam+ <номер фразы>', ['spam- 5'])
register_command_handler(handler_spam_show, 'spam*', ['админ','мук','все'], 15, 'Показать все фразы', 'spam*', ['spam*'])
register_command_handler(handler_global_spam_add, 'gspam+', ['админ','мук','все'], 40, 'Добавить фразу в чёрный спам-список. Можно добавлять не фразы, а регулярные выражения, если Вы не знаете, что это, лучше просто добавьте фразу. ', 'spam+ <фраза>', ['spam+ чики'])
register_command_handler(handler_global_spam_del, 'gspam-', ['админ','мук','все'], 40, 'Удалить фразу из спам-списка', 'spam+ <номер фразы>', ['spam- 5'])
register_command_handler(handler_global_spam_show, 'gspam*', ['админ','мук','все'], 30, 'Показать все фразы', 'spam*', ['spam*'])
register_stage1_init(get_order_cfg)
register_stage2_init(order_check_idle)
