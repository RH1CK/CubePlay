# -*- coding: utf-8 -*-
import urllib, urlparse, sys, xbmcplugin ,xbmcgui, xbmcaddon, xbmc, os, json, hashlib, re, urllib2, htmlentitydefs
from metahandler import metahandlers

AddonID = 'plugin.video.CubePlayMeta'
Addon = xbmcaddon.Addon(AddonID)
AddonName = Addon.getAddonInfo("name")
icon = Addon.getAddonInfo('icon')

addonDir = Addon.getAddonInfo('path').decode("utf-8")
iconsDir = os.path.join(addonDir, "resources", "images")

libDir = os.path.join(addonDir, 'resources', 'lib')
sys.path.insert(0, libDir)
import common

addon_data_dir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
cacheDir = os.path.join(addon_data_dir, "cache")
if not os.path.exists(cacheDir):
	os.makedirs(cacheDir)

cFonte1 = Addon.getSetting("cFonte1")
cFonte2 = Addon.getSetting("cFonte2")
cFonte3 = Addon.getSetting("cFonte3")

cTxt1 = Addon.getSetting("cTxt1")
cTxt2 = Addon.getSetting("cTxt2")
cTxt3 = Addon.getSetting("cTxt3")

def setViewS():
	xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
def setViewS2():
	xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')	
	xbmc.executebuiltin("Container.SetViewMode(\"55\")")
def setViewM():
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	
def getLocaleString(id):
	return Addon.getLocalizedString(id).encode('utf-8')

def Categories(): #70
	try:
		info2=""
		link = common.OpenURL("http://netcine.us/tvshows/page/1/").replace('\n','').replace('\r','')
		l2 = re.compile("box_movies(.+)").findall(link)
		lista = re.compile("img src\=\"[^\"]+.+?alt\=\"([^\"]+)").findall(l2[0])
		for x in lista:
			info2+=x.replace("&#8211;","-").replace("&#038;","&").replace("&#8217;","\'")+"\n"
	except:
		info2=""
	if cTxt1 and cFonte1:
		AddDir("[COLOR white][B]["+cTxt1+"][/B][/COLOR]" , "", 51, "", "https://ckneiferinstructional.files.wordpress.com/2010/12/tv-shows-completed1.jpg", info=info2)
	if cTxt2 and cFonte2:
		AddDir("[COLOR white][B]["+cTxt2+"][/B][/COLOR]" , "", 52, "", "https://ckneiferinstructional.files.wordpress.com/2010/12/tv-shows-completed1.jpg", info=info2)
	if cTxt3 and cFonte3:
		AddDir("[COLOR white][B]["+cTxt3+"][/B][/COLOR]" , "", 53, "", "https://ckneiferinstructional.files.wordpress.com/2010/12/tv-shows-completed1.jpg", info=info2)
	AddDir("[COLOR orange][B][Atualiza][/B][/COLOR]" , "", 200, "", "https://ckneiferinstructional.files.wordpress.com/2010/12/tv-shows-completed1.jpg", isFolder=False)
# --------------  Fim menu
def Series(x): #60
	if "http" in x:
		try:
			link = common.OpenURL(x)
			link = re.sub('(http.+)\s(http.+)\s(http.+)', r"\1;\2;\3", link )
			link = re.sub('(http.+)\s(http.+)', r"\1;\2", link )
			lista = re.compile("(.+);(.*)\s(.+)").findall(link)
			lista = sorted(lista, key=lambda lista: lista[0])
			#ST(link)
			for name2,id2,url2 in lista:
				mg = metahandlers.MetaData()
				mmm = mg.get_meta('tvshow', name2, imdb_id=id2)
				url3 = url2.split(";")
				serv = ""
				for x in url3:
					if "netcine" in x:
						serv+=" [COLOR yellow][NC][/COLOR]"
					elif "redecanais" in x:
						serv+=" [COLOR blue][RC][/COLOR]"
					elif "mmfilmes" in x:
						serv+=" [COLOR purple][MM][/COLOR]"
				if not "asdadsffdsfd" in url2:
					AddDir(name2 + serv, url2, 69, "", "", isFolder=True, metah=mmm)
		except urllib2.URLError, e:
			AddDir("Não foi possível carregar as séries" , "", 0, isFolder=False)
	else:
		AddDir("Nenhuma fonte" , "", 0, isFolder=False)
def Series2(): #69
	url3 = url.split(";")
	name2=[]
	for x in url3:
		if "netcine" in x:
			name2.append("[COLOR yellow][NC][/COLOR]")
		elif "redecanais" in x:
			name2.append("[COLOR blue][RC][/COLOR]")
		elif "mmfilmes" in x:
			name2.append("[COLOR purple][MM][/COLOR]")
	if len(url3) > 1:
		d = xbmcgui.Dialog().select("Escolha o servidor:", name2)
	else:
		d=0
	global url
	url = url3[d]
	if "NC" in name2[d]:
		ListSNC(background)
	elif "RC" in name2[d]:
		TemporadasRC(index)
	elif "MM" in name2[d]:
		ListSMM(background)
		setViewS()
# --------------  NETCINE
def ListSNC(x): #61
	#AddDir("Reload" , "", 40, isFolder=False)
	try:
		link = common.OpenURL(url).replace('\n','').replace('\r','').replace('<div class="soci">',"class='has-sub'").replace('\t',"")
		m = re.compile(".emporada (\d+)(.+?class\=\'has-sub\')").findall(link)
		i=1
		if "None" in background: #season
			for season2,epis in m:
				AddDir("Temporada "+season2+"" ,url, 61, iconimage, iconimage, isFolder=True, background=i, metah=eval(metah))
				i+=1
			setViewS()
		else:
			m2 = re.compile("href\=\"([^\"]+).+?(\d+) - (\d+)").findall( m[int(x)-1][1] )
			m3 = re.compile("icon-chevron-right\W+\w\W+([^\<]+)").findall( m[int(x)-1][1] )
			for url2,S,E in m2:
				AddDir("",url2, 62, iconimage, iconimage, isFolder=False, IsPlayable=True, background=background, metah=eval(metah), episode=E)
				i+=1
			setViewS2()
	except urllib2.URLError, e:
		AddDir("Server NETCINE offline, tente novamente em alguns minutos" , "", 0, isFolder=False)
def PlayS(): #62
	try:
		link = common.OpenURL(url).replace('\n','').replace('\r','')
		m = re.compile("\"play-.\".+?src=\"([^\"]+)").findall(link)
		listan = re.compile("\#play-...(\w*)").findall(link)
		i=0
		listaf=[]
		listal=[]
		for url2 in m:
			link3 = common.OpenURL(url2)
			m3 = re.compile("http[^\"]+").findall(link3)
			for url3 in m3:
				link4 = common.OpenURL(m3[0])
				m4=re.compile("http.+netcine[^\"]+").findall(link4) 
				link5 = common.OpenURL(m4[0])
				link5 = re.sub('window.location.+', '', link5)
				m5= re.compile("http.+?mp4[^\"]+").findall(link5)
				m5 = list(reversed(m5))
				for url4 in m5:
					listal.append(url4)
					dubleg="[COLOR green]HD[/COLOR][/B]" if "ALTO" in url4 else "[COLOR red]SD[/COLOR][/B]"
					listaf.append("[B][COLOR blue]"+listan[i] +"[/COLOR] "+dubleg)
					if "ALTO" in url4:
						d=url4
			i+=1
		if d and len(listaf) == 2:
			PlayUrl(name, d, iconimage, info)
		else:
			d = xbmcgui.Dialog().select("Escolha a resolução:", listaf)
			if d!= -1:
				PlayUrl(name, listal[d], iconimage, info)
	except urllib2.URLError, e:
		xbmcgui.Dialog().ok('Cube Play', 'Erro, tente novamente em alguns minutos')
# --------------  FIM NETCINE
# --------------  REDECANAIS SERIES,ANIMES,DESENHOS
def PlaySRC(): #133 Play series
	try:
		url2 = re.sub('redecanais\.[^\/]+', "redecanais.cz", url.replace("https","http") )
		link = common.OpenURL(url2)
		desc = re.compile('<p itemprop=\"description\"><p>(.+)<\/p><\/p>').findall(link)
		if desc:
			desc = re.sub('&([^;]+);', lambda m: unichr(htmlentitydefs.name2codepoint[m.group(1)]), desc[0]).encode('utf-8')
		player = re.compile('<iframe name=\"Player\".+src=\"([^\"]+)\"').findall(link)
		if player:
			mp4 = common.OpenURL(player[0])
			mmp4 = re.compile('http.{5,95}mp4').findall(mp4)
			PlayUrl(name, mmp4[0] + "?play|Referer="+player[0], iconimage, name)
		else:
			xbmcgui.Dialog().ok('Cube Play', 'Erro, tente novamente em alguns minutos')
	except urllib2.URLError, e:
		xbmcgui.Dialog().ok('Cube Play', 'Erro, tente novamente em alguns minutos')
def TemporadasRC(x): #135 Episodios
	#AddDir("Reload" , "", 40, isFolder=False)
	url2 = re.sub('redecanais\.[^\/]+', "redecanais.cz", url.replace("https","http") )
	link = common.OpenURL(url2).replace('\n','').replace('\r','').replace('</html>','<span style="font').replace("https","http")
	temps = re.compile('(<span style="font-size: x-large;">(.+?)<\/span>)').findall(link)
	i= 0
	if x==None:
		for b,tempname in temps:
			tempname = re.compile('\d+').findall(tempname)
			if tempname:
				#if tempname[0]!="0":
				AddDir("Temporada " + tempname[0] , url, 135, iconimage, iconimage, info="", isFolder=True, index=i, background=tempname[0], metah=eval(metah))
				i+=1
		AddDir("Todos Episódios" ,url, 139, iconimage, iconimage, metah=eval(metah))
		setViewS()
	else:
		temps2 = re.compile('size: x-large;\">.+?<span style\=\"font').findall(link)
		#x=int(x)-1
		epi = re.compile('<strong>(E.+?)<\/strong>(.+?)(<br|<\/p)').findall(temps2[int(x)])
		for name2,url2,brp in epi:
			E = re.compile('\d+').findall(name2)
			if E:
				E=E[0]
			else:
				E="1"
			urlm = re.compile('href\=\"(.+?)\"').findall(url2)
			url2 = re.sub('(\w)-(\w)', r'\1 \2', url2)
			if urlm:
				urlm[0] = "http://www.redecanais.cz/" + urlm[0] if "http" not in urlm[0] else urlm[0]
			if len(urlm) > 1:
				urlm[1] = "http://www.redecanais.cz/" + urlm[1] if "http" not in urlm[1] else urlm[1]
				AddDir("" ,urlm[0], 133, "", "",  isFolder=False, IsPlayable=True, background=background, metah=eval(metah), episode=E, DL="[COLOR yellow](D)[/COLOR] ")
				AddDir("" ,urlm[1], 133, "", "",  isFolder=False, IsPlayable=True, background=background, metah=eval(metah), episode=E, DL="[COLOR blue](L)[/COLOR] ")
			elif urlm:
				AddDir("" ,urlm[0], 133, "", "",  isFolder=False, IsPlayable=True, background=background, metah=eval(metah), episode=E, DL="")
		setViewS2()
def AllEpisodiosRC(): #139 Mostrar todos Epi
	url2 = re.sub('redecanais\.[^\/]+', "redecanais.cz", url.replace("https","http") )
	link = common.OpenURL(url)
	match = re.compile('<strong>(E.+?)<\/strong>(.+?)(<br|<\/p)').findall(link)
	S= 0
	if match:
		for name2,url2,brp in match:
			E = re.compile('\d+').findall(name2)
			if E:
				E=E[0]
				if int(E) == 1:
					S = S + 1
			else:
				E="1"
			urlm = re.compile('href\=\"(.+?)\"').findall(url2)
			if urlm:
				if "http" not in urlm[0]:
					urlm[0] = "http://www.redecanais.cc/" + urlm[0]
			if len(urlm) > 1:
				if "http" not in urlm[1]:
					urlm[1] = "http://www.redecanais.cc/" + urlm[1]
				AddDir("" ,urlm[0], 133, "", "",  isFolder=False, IsPlayable=True, background=str(S), metah=eval(metah), episode=E, DL="[COLOR yellow](D)[/COLOR] ")
				AddDir("" ,urlm[1], 133, "", "",  isFolder=False, IsPlayable=True, background=str(S), metah=eval(metah), episode=E, DL="[COLOR blue](L)[/COLOR] ")
			elif urlm:
				AddDir("" ,urlm[0], 133, "", "",  isFolder=False, IsPlayable=True, background=str(S), metah=eval(metah), episode=E, DL="")
# ----------------- FIM REDECANAIS SERIES,ANIMES,DESENHOS
# ----------------- Inicio MM filmes Series
def ListSMM(x): #191
	link = common.OpenURL(url)
	m = re.compile('boxp\(.([^\']+)').findall(link)
	i=1
	if m:
		if x=="None":
			link2 = common.OpenURL(m[0],headers={'referer': "http://www.mmfilmes.tv/"})
			m2 = re.compile('opb\(.([^\']+).+?.{3}.+?[^\\>]+.([^\<]+)').findall(link2)
			listar=[]
			listal=[]
			for link,res in m2:
				listal.append(link)
				listar.append(res)
			if len(listar)==1:
				d=0
			else:
				d = xbmcgui.Dialog().select("Selecione o server:", listar)
			if d== -1:
				d= 0
			if m2:
				link3 = common.OpenURL(m2[0][0],headers={'referer': "http://www.mmfilmes.tv/"}).replace("\n","").replace("\r","").replace('".Svplayer"',"<end>").replace('\t'," ")
				link3 = re.sub('(\(s \=\= \d+\))', r'<end>\1', link3 )
				m3 = re.compile('s \=\= (\d+)(.+?\<end\>)').findall(link3)
				for temp in m3:
					AddDir("Temporada "+ temp[0] ,listal[d], 192, iconimage, iconimage, isFolder=True, background=i, metah=eval(metah))
					i+=1
def ListEpiMM(x): #192
	link3 = common.OpenURL(url,headers={'referer': "http://www.mmfilmes.tv/"}).replace("\n","").replace("\r","").replace('".Svplayer"',"<end>").replace('\t'," ")
	link3 = re.sub('(\(s \=\= \d+\))', r'<end>\1', link3 )
	m3 = re.compile('s \=\= (\d+)(.+?\<end\>)').findall(link3)
	r=-1
	p=1
	dubleg = re.compile("t \=\= \'([^\']+)(.+?\})").findall( m3[int(x) -1][1] )
	epi = re.compile("e \=\= (\d+).+?addiframe\(\'([^\']+)").findall( m3[int(x) -1][1] )
	for E,url2 in epi:
		url2 = "http://player.mmfilmes.tv" + url2 if not "http" in url2 else url2
		if p == int(E) :
			r+=1
		if len(dubleg[r][1]) < 30:
			r+=1
		dl = "[COLOR yellow](D)[/COLOR] " if "dub" in dubleg[r][0] else "[COLOR blue](L)[/COLOR] "
		AddDir("",url2, 194, iconimage, iconimage, isFolder=False, IsPlayable=True, background=background, metah=eval(metah), episode=E, DL=dl)
def PlaySMM(): #194
	if "drive.google" in url:
		xbmcgui.Dialog().ok('Cube Play', 'Erro, video não encontrado')
		sys.exit()
	link2 = common.OpenURL(url,headers={'referer': "http://player.mmfilmes.tv"}).replace('"',"'")
	m2 = re.compile('(h[^\']+).+?label...(\w+)').findall(link2)
	legenda = re.compile('([^\']+\.(vtt|srt|sub|ssa|txt|ass))').findall(link2)
	listar=[]
	listal=[]
	for link,res in m2:
		listal.append(link)
		listar.append(res)
	if len(listal) < 1:
		xbmcgui.Dialog().ok('Cube Play', 'Erro, video não encontrado')
		sys.exit(int(sys.argv[1]))
	if "720" in listar[0]:
		d = 0
	else:
		d = xbmcgui.Dialog().select("Selecione a resolução", listar)
	if d!= -1:
		url2 = re.sub(' ', '%20', listal[d] )
		if legenda:
			legenda = re.sub(' ', '%20', legenda[0][0] )
			if not "http" in legenda:
				legenda = "http://player.mmfilmes.tv/" + legenda
			PlayUrl(name, url2, iconimage, info, sub=legenda)
		else:
			PlayUrl(name, url2, iconimage, info)
# --------------  FIM MMfilmes
def PlayUrl(name, url, iconimage=None, info='', sub=''):
	url = re.sub('\.mp4$', '.mp4?play', url)
	url = common.getFinalUrl(url)
	xbmc.log('--- Playing "{0}". {1}'.format(name, url), 2)
	listitem = xbmcgui.ListItem(path=url)
	if metah:
		metah2 = eval(metah)
		mg = metahandlers.MetaData()
		eInfo = mg.get_episode_meta(metah2['TVShowTitle'], metah2['imdb_id'], background, episode)
		S=str(eInfo['season'])
		E=str(eInfo['episode'])
		tvshowt=metah2['TVShowTitle']
		#listitem=xbmcgui.ListItem(background+"."+episode+" "+eInfo['title'], iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
		listitem.setArt({"poster": eInfo['cover_url'], "banner": eInfo['cover_url'], "fanart": eInfo['backdrop_url'] })
		listitem.setInfo( type="Video", infoLabels= metah2 )
		listitem.setInfo( type="Video", infoLabels= eInfo )
		listitem.setInfo( type="Video", infoLabels= {'genre': '[COLOR blue]S'+str(eInfo['season'])+'E'+str(eInfo['episode'])+'[/COLOR]: '+metah2['TVShowTitle']} )
	else:
		listitem.setInfo(type="Video", infoLabels={"mediatype": "video", "Title": name, "Plot": info })
		if iconimage is not None:
			try:
				listitem.setArt({'thumb' : iconimage})
			except:
				listitem.setThumbnailImage(iconimage)
	if sub!='':
		listitem.setSubtitles(['special://temp/example.srt', sub ])

	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
def Data(x):
	x = eInfo = re.sub('\d\d(\d+)\-(\d+)\-(\d+)', r'\3/\2/\1', x )
	return "[COLOR yellow]("+x+")[/COLOR]"
def EPI(x):
	x = re.sub('[0]+(\d+)', r'\1', x )
	return x
def AddDir(name, url, mode, iconimage='', logos='', index="", move=0, isFolder=True, IsPlayable=False, background=None, cacheMin='0', info='', DL='', year='', metah={}, episode=''):
	urlParams = {'name': name, 'url': url, 'mode': mode, 'iconimage': iconimage, 'logos': logos, 'cache': cacheMin, 'index': index, 'info': info, 'background': background, 'DL': DL, 'year': year, 'metah': metah, 'episode': episode}
	if metah:
		if background and episode:
			mg = metahandlers.MetaData()
			#sInfo = mg.get_seasons(metah['TVShowTitle'], metah['imdb_id'], [1])
			eInfo = mg.get_episode_meta(metah['TVShowTitle'], metah['imdb_id'], background, EPI(episode))
			liz=xbmcgui.ListItem(DL+background+"."+EPI(episode)+" "+eInfo['title'] +" "+Data(eInfo['premiered'])+ " [COLOR blue]["+str(eInfo['rating'])+"][/COLOR]", iconImage=metah['cover_url'], thumbnailImage=metah['cover_url'])
			liz.setArt({"thumb": eInfo['cover_url'], "poster": eInfo['cover_url'], "banner": eInfo['cover_url'], "fanart": eInfo['backdrop_url'] })
			infoLabels = {}
			infoLabels['Premiered'] = "2018-01-01"
			liz.setInfo( type="Video", infoLabels= eInfo )
			#ST(eInfo)
			#liz.setInfo( type='Video', {'premiered': '2018-01-01'} )
			#liz.setInfo('video', { 'Premiered': '01-01-2018' })
			#ST(eInfo)
			#eInfo = re.sub('\'duration\'\:[^,]+,', '', str(eInfo) )
			#eInfo = eval(eInfo)
			#liz.setRating("imdb", 4.6, 8940, False)
		else:
			liz=xbmcgui.ListItem(name, iconImage=metah['cover_url'], thumbnailImage=metah['cover_url'])
			liz.setArt({"poster": metah['cover_url'], "banner": metah['cover_url'], "fanart": metah['backdrop_url'] })
			liz.setInfo( type="Video", infoLabels= metah )
	else:
		liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage )
		liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": info })
		liz.setArt({"poster": iconimage, "banner": logos, "fanart": logos })
		#listMode = 21 # Lists
	if IsPlayable:
		liz.setProperty('IsPlayable', 'true')
	items = []
	if mode == 1 or mode == 2:
		items = []
	if mode == 10:
		urlParams['index'] = index
	u = '{0}?{1}'.format(sys.argv[0], urllib.urlencode(urlParams))
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)

def Refresh():
	xbmc.executebuiltin("XBMC.Container.Refresh()")

def Update():
	Path = xbmc.translatePath( xbmcaddon.Addon().getAddonInfo('path') ).decode("utf-8")
	try:
		fonte = urllib2.urlopen( "https://pastebin.com/raw/6aHzYAFW" ).read().replace('\n','')
		prog = re.compile('#checkintegrity25852').findall(fonte)
		if prog:
			py = os.path.join( Path, "default.py")
			file = open(py, "w")
			file.write(fonte)
			file.close()
	except:
		pass
	xbmc.sleep(2000)
	
def ST(x):
	x = str(x)
	Path = xbmc.translatePath( xbmcaddon.Addon().getAddonInfo('path') ).decode("utf-8")
	py = os.path.join( Path, "study.txt")
	#file = open(py, "a+")
	file = open(py, "w")
	file.write(x)
	file.close()

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))
url = params.get('url')
logos = params.get('logos', '')
name = params.get('name')
iconimage = params.get('iconimage')
cache = int(params.get('cache', '0'))
index = params.get('index')
move = int(params.get('move', '0'))
mode = int(params.get('mode', '0'))
info = params.get('info')
background = params.get('background')
DL = params.get('DL')
year = params.get('year')
metah = params.get('metah')
episode = params.get('episode')

if mode == 0:
	Categories()
	setViewM()
elif mode == 40:
	Refresh()
elif mode == 51:
	Series(cFonte1)
	setViewS()
elif mode == 52:
	Series(cFonte2)
	setViewS()
elif mode == 53:
	Series(cFonte3)
	setViewS()
elif mode == 61:
	ListSNC(background)
elif mode == 62:
	PlayS()
	setViewS()
elif mode == 69:
	Series2()
elif mode == 71:
	MoviesNC()
	setViewM()
elif mode == 78:
	ListMoviesNC()
	setViewS()
elif mode == 79:
	PlayMNC()
	setViewS()
elif mode == 81:
	CategoryOrdem2(url)
#------------
elif mode == 135:
	TemporadasRC(index)
elif mode == 133:
	PlaySRC()
elif mode == 139:
	AllEpisodiosRC()
	setViewS2()
#-------------
elif mode == 191:
	ListSMM(background)
	setViewS()
elif mode == 192:
	ListEpiMM(background)
	setViewS2()
elif mode == 194:
	PlaySMM()
elif mode == 200:
	Update()
	xbmc.executebuiltin("XBMC.Container.Refresh()")
xbmcplugin.endOfDirectory(int(sys.argv[1]))
#checkintegrity25852