# -*- coding: utf-8 -*-
import urllib, urlparse, sys, xbmcplugin ,xbmcgui, xbmcaddon, xbmc, os, json, hashlib, re, urllib2, htmlentitydefs

AddonID = 'plugin.video.CubePlay'
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

cPage = Addon.getSetting("cPage")
Versao = "18.04.06"
Cat = Addon.getSetting("Cat")
Clista=[ "todos",                     "acao", "animacao", "aventura", "comedia", "drama", "fantasia", "ficcao-cientifica", "romance", "suspense", "terror"]
Clista2=["Sem filtro (Mostrar Todos)","Acao", "Animacao", "Aventura", "Comedia", "Drama", "Fantasia", "Ficcao-Cientifica", "Romance", "Suspense", "Terror"]

Path = xbmc.translatePath( xbmcaddon.Addon().getAddonInfo('path') ).decode("utf-8")

def setViewS():
	xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
def setViewM():
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	
playlistsFile = "http://localhost:8080/nc/tvshows.php"
favoritesFile = os.path.join(addon_data_dir, 'favorites.txt')
if not (os.path.isfile(favoritesFile)):
	common.SaveList(favoritesFile, [])
	
makeGroups = "true"
URLP="http://cubeplay.000webhostapp.com/"
#URLP="http://localhost:8080/"
URLNC=URLP+"nc/"
	
def getLocaleString(id):
	return Addon.getLocalizedString(id).encode('utf-8')

def Categories(): #70
	#AddDir("[B]{0}: {1}[/B] - {2} ".format(getLocaleString(30036), getLocaleString(30037) if makeGroups else getLocaleString(30038) , getLocaleString(30039)), "setting" ,50 ,os.path.join(iconsDir, "setting.png"), isFolder=False)
	AddDir("[COLOR Pink][B][Canais de TV RedeCanais.com][/B][/COLOR]" , "", 100, "https://walter.trakt.tv/images/movies/000/090/449/posters/thumb/eadfdc57aa.jpg", "https://walter.trakt.tv/images/movies/000/090/449/posters/thumb/eadfdc57aa.jpg", index=0, cacheMin = "0")
	AddDir("[COLOR blue][B][Filmes Dublado RedeCanais.com][/B][/COLOR]" , "", 90, "https://walter.trakt.tv/images/movies/000/222/254/fanarts/thumb/401d5f083e.jpg", "https://walter.trakt.tv/images/movies/000/222/254/fanarts/thumb/401d5f083e.jpg", index=0, cacheMin = "0")
	AddDir("[COLOR blue][B][Filmes Legendado RedeCanais.com][/B][/COLOR]" , "", 91, "https://walter.trakt.tv/images/movies/000/181/313/fanarts/thumb/cc9226edfe.jpg", "https://walter.trakt.tv/images/movies/000/181/313/fanarts/thumb/cc9226edfe.jpg", index=0, cacheMin = "0")
	AddDir("[COLOR blue][B][Filmes Nacional RedeCanais.com][/B][/COLOR]" , "", 92, "http://cdn.cinepop.com.br/2016/11/minhamaeeumapeca2_2-750x380.jpg", "http://cdn.cinepop.com.br/2016/11/minhamaeeumapeca2_2-750x380.jpg", index=0, cacheMin = "0")
	try:
		checa = urllib2.urlopen( URLNC + "version.txt" ).read()
		AddDir("[COLOR yellow][B][Series NetCine.us][/B][/COLOR]" , URLNC + "listTVshow.php", 60, "https://walter.trakt.tv/images/shows/000/098/898/fanarts/thumb/bca6f8bc3c.jpg", "https://walter.trakt.tv/images/shows/000/098/898/fanarts/thumb/bca6f8bc3c.jpg", index=0, cacheMin = "0")
		AddDir("[COLOR yellow][B][Filmes NetCine.us][/B][/COLOR]" , URLNC + "listMovies.php", 71, "https://walter.trakt.tv/images/movies/000/181/312/fanarts/thumb/e30b344522.jpg", "https://walter.trakt.tv/images/movies/000/181/312/fanarts/thumb/e30b344522.jpg", index=0, cacheMin = "0")
	except urllib2.URLError, e:
		AddDir("Server NETCINE offline, tente novamente em alguns minutos" , "setting", 50, "", "", 0, cacheMin = "0", isFolder=False)
		#AddDir("Verifique se o addon esta atualizado em:" , "setting", 50, "", "", 0, cacheMin = "0, isFolder=False")
		#AddDir("http://bit.ly/CUBEPLAY" , "setting", 50, "", "", 0, cacheMin = "0", isFolder=False)
	AddDir("[COLOR red][B][Genero dos Filmes]:[/B] " + Clista2[int(Cat)] +"[/COLOR]", "url" ,80 ,"https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", "https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", isFolder=False)
	AddDir("[COLOR green][B][Favoritos Cube Play][/B][/COLOR]", "favorites" ,30 , "http://icons.iconarchive.com/icons/royalflushxx/systematrix/256/Favorites-icon.png", "http://icons.iconarchive.com/icons/royalflushxx/systematrix/256/Favorites-icon.png")
	uversao = urllib2.urlopen( "https://raw.githubusercontent.com/RH1CK/CubePlay/master/version.txt" ).read().replace('\n','').replace('\r','')
	if uversao != Versao:
		AddDir("[B][COLOR pink][CLIQUE AQUI]\n[PARA ATUALIZAR O ADDON][/COLOR][/B]", "setting" ,130 ,"http://cdn.blog.hu/an/antivirus/image/201605/hav6.jpg" , "http://cdn.blog.hu/an/antivirus/image/201605/hav6.jpg", isFolder=False, info="Ha uma nova versao do addon\nClique aqui para atualizar")
	AddDir("[B][Sobre o Addon][/B]", "config" ,0 ,"http://www.iconsplace.com/icons/preview/orange/about-256.png", "http://www.iconsplace.com/icons/preview/orange/about-256.png", isFolder=False, info="Addon modificado do PlaylistLoader 1.2.0 por Avigdor\r https://github.com/avigdork/xbmc-avigdork.\r\nNao somos responsaveis por colocar o conteudo online, apenas indexamos.\r\nPara sugestoes e report de bugs nossa pagina no FB: [COLOR blue]http://fb.com/CubePlayKodi[/COLOR]")
	AddDir("[B][COLOR blue]http://fb.com/CubePlayKodi[/COLOR][/B]", "config" ,0 ,"https://cdn.pixabay.com/photo/2017/08/20/10/30/facebook-2661207_960_720.jpg", "https://cdn.pixabay.com/photo/2017/08/20/10/30/facebook-2661207_960_720.jpg", isFolder=False, info="Para sugestoes e report de bugs nossa pagina no FB: [COLOR blue]http://fb.com/CubePlayKodi[/COLOR]")
# --------------  NETCINE
def PlayS(): #62
	try:
		link = urllib2.urlopen(URLNC +  url ).read().replace('\n','').replace('\r','')
		match = re.compile('url="(.+?)".+?mg="(.+?)".+?ame="(.+?)".+?nfo="(.+?)"').findall(link)
		i= 0
		for url2,img2,name2,info2 in match:
			AddDir(name2 + name ,url2, 3, iconimage, iconimage, index=i, isFolder=False, IsPlayable=True, info=info2)
			i += 1
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "", 0, cacheMin = "0")

def EpisodioS(): #61
	try:
		link = urllib2.urlopen( URLNC + url ).read().replace('\n','').replace('\r','')
		match = re.compile('url="(.+?)".+?mg="(.+?)".+?ame="(.+?)".+?nfo="(.+?)"').findall(link)
		i= 0
		for url2,img2,name2,info2 in match:
			AddDir(name2 ,url2, 62, iconimage, iconimage, index=i, cacheMin = "0", info=info2)
			i += 1
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "", 0, cacheMin = "0")
	
def Series(): #60
	try:
		link = urllib2.urlopen(url).read().replace('\n','').replace('\r','')
		match = re.compile('url="(.+?)".+?mg="(.+?)".+?ame="(.+?)"').findall(link)
		i= 0
		for url2,img2,name2 in match:
			AddDir(name2, url2, 61, img2, img2, index=i, cacheMin = "0")
			i += 1
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "", 0, cacheMin = "0")

def MoviesNC(): #70
	AddDir("[COLOR red][B]Filtro: " + Clista2[int(Cat)] + "[/B][/COLOR]", "setting" ,90 ,"https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", isFolder=False)
	try:
		link = urllib2.urlopen( url +"?cat=" + Clista[int(Cat)]).read().replace('\n','').replace('\r','')
		match = re.compile('url="(.+?)".+?mg="(.+?)".+?ame="(.+?)"').findall(link)
		i= 0
		for url2,img2,name2 in match:
			AddDir(name2 ,url2, 79, img2, img2, index=i, cacheMin = "0", info="")
			i += 1
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "", 0, cacheMin = "0")

def Generos(): #80
	dialog = xbmcgui.Dialog()
	d = dialog.select("Escolha o Genero", Clista2)
	if d != -1:
		global Cat
		Addon.setSetting("Cat", str(d) )
		Cat = d
		#xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, str(Cat) , "Cat", ""))
		Addon.setSetting("cPage", "0" )
		xbmc.executebuiltin("XBMC.Container.Refresh()")

def PlayM(): #79
	try:
		link = urllib2.urlopen(URLNC + url ).read().replace('\n','').replace('\r','')
		match = re.compile('url="(.+?)".+?mg="(.+?)".+?ame="(.+?)".+?nfo="(.+?)"').findall(link)
		i= 0
		for url2,img2,name2,info2 in match:
			AddDir(name2 + name ,url2, 3, iconimage, iconimage, index=i, isFolder=False, IsPlayable=True, info=info2)
			i += 1
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "", 0, cacheMin = "0")
# --------------  FIM NETCINE
# --------------  REDECANAIS
def MoviesRCD(): #90 Filme dublado
	AddDir("[COLOR red][B]Filtro: " + Clista2[int(Cat)] + "[/B][/COLOR]", "setting" ,90 ,"https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", isFolder=False)
	try:
		p= 1
		if int(cPage) > 0:
			AddDir("[COLOR blue][B]<< Pagina Anterior ["+ str( int(cPage) ) +"[/B]][/COLOR]", "" , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False)
		l= int(cPage)*5
		for x in range(0, 5):
			l +=1
			link = common.OpenURL("http://www.redecanais.net/browse-filmes-dublado-videos-"+str(l)+"-date.html")
			if Clista2[int(Cat)] != "Sem filtro (Mostrar Todos)":
				link = common.OpenURL("http://www.redecanais.info/browse-"+Clista2[int(Cat)]+"-Filmes-videos-"+str(l)+"-date.html")
			match = re.compile('href\=\"(http:\/\/www.redecanais\.[^\"]+)\".+src=\"([^\"]+)\".alt=\"([^\"]+)\" width').findall(link)
			i= 0
			if match:
				for url2,img2,name2 in match:
					AddDir(name2 ,url2, 95, img2, img2, index=i, cacheMin = "0", info="")
					i += 1
					p += 1
		if p >= 60:
			AddDir("[COLOR blue][B]Proxima Pagina >> ["+ str( int(cPage) + 2) +"[/B]][/COLOR]", "" , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False)
	except e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "", 0, cacheMin = "0")
def MoviesRCL(): #91 Filme Legendado
	AddDir("[COLOR red][B]Filtro: " + Clista2[int(Cat)] + "[/B][/COLOR]", "setting" ,90 ,"https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", isFolder=False)
	try:
		p= 1
		if int(cPage) > 0:
			AddDir("[COLOR blue][B]<< Pagina Anterior ["+ str( int(cPage) ) +"[/B]][/COLOR]", "" , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False)
		l= int(cPage)*5
		for x in range(0, 5):
			l +=1
			link = common.OpenURL("http://www.redecanais.net/browse-filmes-legendado-videos-"+str(l)+"-date.html")
			if Clista2[int(Cat)] != "Sem filtro (Mostrar Todos)":
				link = common.OpenURL("http://www.redecanais.net/browse-"+Clista2[int(Cat)]+"-Filmes-Legendado-videos-"+str(l)+"-date.html")
			match = re.compile('href\=\"(http:\/\/www.redecanais\.[^\"]+)\".+src=\"([^\"]+)\".alt=\"([^\"]+)\" width').findall(link)
			i= 0
			if match:
				for url2,img2,name2 in match:
					AddDir(name2 ,url2, 95, img2, img2, index=i, cacheMin = "0", info="")
					i += 1
					p += 1
		if p >= 60:
			AddDir("[COLOR blue][B]Proxima Pagina >> ["+ str( int(cPage) + 2) +"[/B]][/COLOR]", "" , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False)
	except e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "", 0, cacheMin = "0")
def MoviesRCN(): #92 Filmes Nacional
	AddDir("[COLOR red][B]Filtro: " + Clista2[int(Cat)] + "[/B][/COLOR]", "setting" ,90 ,"https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", isFolder=False)
	try:
		p= 1
		if int(cPage) > 0:
			AddDir("[COLOR blue][B]<< Pagina Anterior ["+ str( int(cPage) ) +"[/B]][/COLOR]", "" , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False)
		l= int(cPage)*5
		for x in range(0, 5):
			l +=1
			link = common.OpenURL("http://www.redecanais.net/browse-filmes-nacional-videos-"+str(l)+"-date.html")
			match = re.compile('href\=\"(http:\/\/www.redecanais\.[^\"]+)\".+src=\"([^\"]+)\".alt=\"([^\"]+)\" width').findall(link)
			i= 0
			if match:
				for url2,img2,name2 in match:
					AddDir(name2 ,url2, 95, img2, img2, index=i, cacheMin = "0", info="")
					i += 1
					p += 1
		if p >= 60:
			AddDir("[COLOR blue][B]Proxima Pagina >> ["+ str( int(cPage) + 2) +"[/B]][/COLOR]", "" , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False)
	except e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "", 0, cacheMin = "0")
def PlayMRC(): #95 Play filmes
	try:
		link = common.OpenURL(url)
		desc = re.compile('<p itemprop=\"description\"><p>(.+)<\/p><\/p>').findall(link)
		if desc:
			desc = re.sub('&([^;]+);', lambda m: unichr(htmlentitydefs.name2codepoint[m.group(1)]), desc[0]).encode('utf-8')
		player = re.compile('<iframe name=\"Player\".+src=\"([^\"]+)\"').findall(link)
		link2 = common.OpenURL(player[0])
		urlp = re.compile('file: \"([^\"]+)\"').findall(link2)
		AddDir("[B][COLOR yellow]"+ name +" [/COLOR][/B]"  , urlp[0] + "?play|Referer=http://www.redecanais.com/", 3, iconimage, iconimage, index=0, isFolder=False, IsPlayable=True, info=desc)
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "", 0, cacheMin = "0")
# ----------------- FIM REDECANAIS
# ----------------- REDECANAIS TV
def TVRC(): # 100
	try:
		l= 0
		for x in range(0, 5):
			l +=1
			link = common.OpenURL("http://www.redecanais.info/browse-canais-videos-"+str(l)+"-title.html")
			match = re.compile('href\=\"(http:\/\/www.redecanais\.[^\"]+)\".+src=\"([^\"]+)\".alt=\"([^\"]+)\" width').findall(link)
			i= 0
			if match:
				for url2,img2,name2 in match:
					name2 = name2.replace("Assistir ", "").replace(" - Online - 24 Horas - Ao Vivo", "")
					#name2 = re.sub('&([^;]+);', lambda m: unichr(htmlentitydefs.name2codepoint[m.group(1)]), name2).encode('utf-8')
					AddDir(name2 ,url2, 101, img2, img2, index=i, cacheMin = "0", info="")
					i += 1
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "", 0, cacheMin = "0")
def PlayTVRC(): # 101
	try:
		link = common.OpenURL(url)
		#desc = re.compile('<p itemprop=\"description\"><p>(.+)<\/p><\/p>').findall(link)
		player = re.compile('<iframe name=\"Player\".+src=\"([^\"]+)\"').findall(link)
		link2 = common.OpenURL(player[0])
		urlp = re.compile('\"source\"\: \"([^\"]+)').findall(link2)
		AddDir("[B][COLOR yellow]"+ name +" [/COLOR][/B]"  , urlp[0] + "?play|Referer=http://www.redecanais.com/", 3, iconimage, iconimage, index=0, isFolder=False, IsPlayable=True, info="Play")
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "", 0, cacheMin = "0")
# ----------------- FIM REDECANAIS TV
def AddNewList():
	listName = GetKeyboardText(getLocaleString(30004)).strip()
	if len(listName) < 1:
		return
	listUrl = GetChoice(30002, 30005, 30006, 30016, 30017, fileType=1, fileMask='.plx|.m3u|.m3u8')
	if len(listUrl) < 1:
		return
	image = GetChoice(30022, 30022, 30022, 30024, 30025, 30021, fileType=2)
	logosUrl = '' if listUrl.endswith('.plx') else GetChoice(30018, 30019, 30020, 30019, 30020, 30021, fileType=0)
	if logosUrl.startswith('http') and not logosUrl.endswith('/'):
		logosUrl += '/'
	cacheInMinutes = GetNumFromUser(getLocaleString(30034), '0') if listUrl.startswith('http') else 0
	if cacheInMinutes is None:
		cacheInMinutes = 0
	chList = common.ReadURL(playlistsFile)
	for item in chList:
		if item["url"].lower() == listUrl.lower():
			xbmc.executebuiltin('Notification({0}, "{1}" {2}, 5000, {3})'.format(AddonName, item["name"].encode("utf-8"), getLocaleString(30007), icon))
			return
	chList.append({"name": listName.decode("utf-8"), "url": listUrl, "image": image, "logos": logosUrl, "cache": cacheInMinutes})
	if common.SaveList(playlistsFile, chList):
		xbmc.executebuiltin("XBMC.Container.Refresh()")

def GetChoice(choiceTitle, fileTitle, urlTitle, choiceFile, choiceUrl, choiceNone=None, fileType=1, fileMask=None, defaultText=""):
	choice = ''
	choiceList = [getLocaleString(choiceFile), getLocaleString(choiceUrl)]
	if choiceNone is not None:
		choiceList = [getLocaleString(choiceNone)] + choiceList
	method = GetSourceLocation(getLocaleString(choiceTitle), choiceList)	
	if choiceNone is None and method == 0 or choiceNone is not None and method == 1:
		if not defaultText.startswith('http'):
			defaultText = ""
		choice = GetKeyboardText(getLocaleString(fileTitle), defaultText).strip().decode("utf-8")
	elif choiceNone is None and method == 1 or choiceNone is not None and method == 2:
		if defaultText.startswith('http'):
			defaultText = ""
		choice = xbmcgui.Dialog().browse(fileType, getLocaleString(urlTitle), 'files', fileMask, False, False, defaultText).decode("utf-8")
	return choice
	
def RemoveFromLists(index, listFile):
	chList = common.ReadList(listFile) 
	if index < 0 or index >= len(chList):
		return
	del chList[index]
	common.SaveList(listFile, chList)
	xbmc.executebuiltin("XBMC.Container.Refresh()")
			
def PlxCategory(url, cache):
	tmpList = []
	chList = common.plx2list(url, cache)
	background = chList[0]["background"]
	for channel in chList[1:]:
		iconimage = "" if not channel.has_key("thumb") else common.GetEncodeString(channel["thumb"])
		name = common.GetEncodeString(channel["name"])
		if channel["type"] == 'playlist':
			AddDir("{0}".format(name) ,channel["url"].encode("utf-8"), 1, iconimage, background=background.encode("utf-8"))
		else:
			AddDir(name, channel["url"].encode("utf-8"), 3, iconimage, isFolder=False, IsPlayable=True, background=background)
			tmpList.append({"url": channel["url"], "image": iconimage.decode("utf-8"), "name": name.decode("utf-8")})
			
def m3uCategory(url, logos, cache, gListIndex=-1):	
	tmpList = []
	chList = common.m3u2list(url, cache)
	groupChannels = []
	for channel in chList:
		if makeGroups:
			matches = [groupChannels.index(x) for x in groupChannels if len(x) > 0 and x[0].get("group_title", x[0]["display_name"]) == channel.get("group_title", channel["display_name"])]
		if makeGroups and len(matches) == 1:
			groupChannels[matches[0]].append(channel)
		else:
			groupChannels.append([channel])
	for channels in groupChannels:
		idx = groupChannels.index(channels)
		if gListIndex > -1 and gListIndex != idx:
			continue
		isGroupChannel = gListIndex < 0 and len(channels) >= 1
		chs = [channels[0]] if isGroupChannel else channels
		for channel in chs:
			chUrl = common.GetEncodeString(channel["url"])
			name = common.GetEncodeString(channel["display_name"]) if not isGroupChannel else common.GetEncodeString(channel.get("group_title", channel["display_name"]))
			if isGroupChannel:
				name = '{0}'.format(name)
				chUrl = url
				image = channel.get("tvg_logo", channel.get("logo", ""))
				AddDir(name ,url, 10, image, index=idx)
			elif chUrl == "http://127.0.0.0":
				image = channel.get("tvg_logo", channel.get("logo", ""))
				if logos is not None and logos != ''  and image != "" and not image.startswith('http'):
					image = logos + image
			else:
				image = channel.get("tvg_logo", channel.get("logo", ""))
				if logos is not None and logos != ''  and image != "" and not image.startswith('http'):
					image = logos + image
				AddDir(name, chUrl, 60, image, index=-1, isFolder=True, IsPlayable=False)
			tmpList.append({"url": chUrl.decode("utf-8"), "image": image.decode("utf-8"), "name": name.decode("utf-8")})
		
def PlayUrl(name, url, iconimage=None, info='a'):
	if url.startswith('acestream://'):
		url = 'plugin://program.plexus/?mode=1&url={0}&name={1}&iconimage={2}'.format(url, name, iconimage)
	else:
		url = common.getFinalUrl(url)
	xbmc.log('--- Playing "{0}". {1}'.format(name, url), 2)
	listitem = xbmcgui.ListItem(path=url)
	listitem.setInfo(type="Video", infoLabels={"mediatype": "video", "Title": name, "Plot": info })
	if iconimage is not None:
		try:
			listitem.setArt({'thumb' : iconimage})
		except:
			listitem.setThumbnailImage(iconimage)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

def AddDir(name, url, mode, iconimage='', logos='', index=-1, move=0, isFolder=True, IsPlayable=False, background=None, cacheMin='0', info=''):
	urlParams = {'name': name, 'url': url, 'mode': mode, 'iconimage': iconimage, 'logos': logos, 'cache': cacheMin, 'info': info}
	liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage, )
	liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": info })
	#liz.setProperty("Fanart_Image", logos)
	liz.setArt({
	"poster": iconimage,
	"banner": logos,
	"fanart": logos
        })
	listMode = 21 # Lists
	if IsPlayable:
		liz.setProperty('IsPlayable', 'true')
	#if background != None:
	#	liz.setProperty('fanart_image', background)
	items = []
	if mode == 1 or mode == 2:
		items = []
	elif mode== 61:
		liz.addContextMenuItems(items = [('{0}'.format(getLocaleString(30009)), 'XBMC.RunPlugin({0}?url={1}&mode=31&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name)))])
	elif mode== 79:
		liz.addContextMenuItems(items = [('{0}'.format(getLocaleString(30009)), 'XBMC.RunPlugin({0}?url={1}&mode=72&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name)))])
	elif mode== 95:
		liz.addContextMenuItems(items = [('{0}'.format(getLocaleString(30009)), 'XBMC.RunPlugin({0}?url={1}&mode=93&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name)))])
	if info=="Favoritos":
		items = [("Remover dos favoritos", 'XBMC.RunPlugin({0}?index={1}&mode=33)'.format(sys.argv[0], index)),
		(getLocaleString(30030), 'XBMC.RunPlugin({0}?index={1}&mode={2}&move=-1)'.format(sys.argv[0], index, 38)),
		(getLocaleString(30031), 'XBMC.RunPlugin({0}?index={1}&mode={2}&move=1)'.format(sys.argv[0], index, 38)),
		(getLocaleString(30032), 'XBMC.RunPlugin({0}?index={1}&mode={2}&move=0)'.format(sys.argv[0], index, 38))]
		liz.addContextMenuItems(items)
	if mode == 10:
		urlParams['index'] = index
	u = '{0}?{1}'.format(sys.argv[0], urllib.urlencode(urlParams))
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)

def GetKeyboardText(title = "", defaultText = ""):
	keyboard = xbmc.Keyboard(defaultText, title)
	keyboard.doModal()
	text = "" if not keyboard.isConfirmed() else keyboard.getText()
	return text

def GetSourceLocation(title, chList):
	dialog = xbmcgui.Dialog()
	answer = dialog.select(title, chList)
	return answer
	
def AddFavorites(url, iconimage, name, mode):
	favList = common.ReadList(favoritesFile)
	for item in favList:
		if item["url"].lower() == url.decode("utf-8").lower():
			xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, name, getLocaleString(30011), icon))
			return
	chList = []	
	for channel in chList:
		if channel["name"].lower() == name.decode("utf-8").lower():
			url = channel["url"].encode("utf-8")
			iconimage = channel["image"].encode("utf-8")
			break
	if not iconimage:
		iconimage = ""
	data = {"url": url.decode("utf-8"), "image": iconimage.decode("utf-8"), "name": name.decode("utf-8"), "mode": mode}
	favList.append(data)
	common.SaveList(favoritesFile, favList)
	xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, name, getLocaleString(30012), icon))
	
def ListFavorites():
	chList = common.ReadList(favoritesFile)
	i = 0
	for channel in chList:
		AddDir(channel["name"].encode("utf-8"), channel["url"].encode("utf-8"), channel["mode"], channel["image"].encode("utf-8"), channel["image"].encode("utf-8"), index=i, isFolder=True, IsPlayable=False, info="Favoritos")
		i += 1
		
def AddNewFavorite():
	chName = GetKeyboardText(getLocaleString(30014))
	if len(chName) < 1:
		return
	chUrl = GetKeyboardText(getLocaleString(30015))
	if len(chUrl) < 1:
		return
	image = GetChoice(30023, 30023, 30023, 30024, 30025, 30021, fileType=2)
		
	favList = common.ReadList(favoritesFile)
	for item in favList:
		if item["url"].lower() == chUrl.decode("utf-8").lower():
			xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, chName, getLocaleString(30011), icon))
			return
			
	data = {"url": chUrl.decode("utf-8"), "image": image, "name": chName.decode("utf-8")}
	
	favList.append(data)
	if common.SaveList(favoritesFile, favList):
		xbmc.executebuiltin("XBMC.Container.Refresh()")

def ChangeKey(index, listFile, key, title):
	chList = common.ReadList(listFile)
	str = GetKeyboardText(getLocaleString(title), chList[index][key].encode("utf-8"))
	if len(str) < 1:
		return
	chList[index][key] = str.decode("utf-8")
	if common.SaveList(listFile, chList):
		xbmc.executebuiltin("XBMC.Container.Refresh()")
		
def ChangeChoice(index, listFile, key, choiceTitle, fileTitle, urlTitle, choiceFile, choiceUrl, choiceNone=None, fileType=1, fileMask=None):
	chList = common.ReadList(listFile)
	defaultText = chList[index].get(key, "")
	str = GetChoice(choiceTitle, fileTitle, urlTitle, choiceFile, choiceUrl, choiceNone, fileType, fileMask, defaultText.encode("utf-8"))
	if key == "url" and len(str) < 1:
		return
	elif key == "logos" and str.startswith('http') and not str.endswith('/'):
		str += '/'
	chList[index][key] = str.decode("utf-8")
	if common.SaveList(listFile, chList):
		xbmc.executebuiltin("XBMC.Container.Refresh()")
	
def MoveInList(index, step, listFile):
	theList = common.ReadList(listFile)
	if index + step >= len(theList) or index + step < 0:
		return
	if step == 0:
		step = GetIndexFromUser(len(theList), index)
	if step < 0:
		tempList = theList[0:index + step] + [theList[index]] + theList[index + step:index] + theList[index + 1:]
	elif step > 0:
		tempList = theList[0:index] + theList[index +  1:index + 1 + step] + [theList[index]] + theList[index + 1 + step:]
	else:
		return
	common.SaveList(listFile, tempList)
	xbmc.executebuiltin("XBMC.Container.Refresh()")

def GetNumFromUser(title, defaultt=''):
	dialog = xbmcgui.Dialog()
	choice = dialog.input(title, defaultt=defaultt, type=xbmcgui.INPUT_NUMERIC)
	return None if choice == '' else int(choice)

def GetIndexFromUser(listLen, index):
	dialog = xbmcgui.Dialog()
	location = GetNumFromUser('{0} (1-{1})'.format(getLocaleString(30033), listLen))
	return 0 if location is None or location > listLen or location <= 0 else location - 1 - index

def ChangeCache(index, listFile):
	chList = common.ReadList(listFile)
	defaultText = chList[index].get('cache', 0)
	cacheInMinutes = GetNumFromUser(getLocaleString(30034), str(defaultText)) if chList[index].get('url', '0').startswith('http') else 0
	if cacheInMinutes is None:
		return
	chList[index]['cache'] = cacheInMinutes
	if common.SaveList(listFile, chList):
		xbmc.executebuiltin("XBMC.Container.Refresh()")

def ToggleGroups():
	notMakeGroups = "false" if makeGroups else "true"
	Addon.setSetting("makeGroups", notMakeGroups)
	xbmc.executebuiltin("XBMC.Container.Refresh()")

def TogglePrevious():
	Addon.setSetting("cPage", str(int(cPage) - 1) )
	xbmc.executebuiltin("XBMC.Container.Refresh()")

def ToggleNext():
	Addon.setSetting("cPage", str(int(cPage) + 1) )
	xbmc.executebuiltin("XBMC.Container.Refresh()")

def Update():
	dialog = xbmcgui.Dialog()
	ret = dialog.yesno('Kodi', 'Quer atualizar o addon??')
	if ret:
		zip = os.path.join( Path, "default.py")
		f = urllib.urlopen("https://raw.githubusercontent.com/RH1CK/CubePlay/master/default.py")
		with open(zip, "wb") as subFile:
			subFile.write(f.read())
			subFile.close()
		xbmc.executebuiltin("XBMC.Container.Refresh()")

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))
url = params.get('url')
logos = params.get('logos', '')
name = params.get('name')
iconimage = params.get('iconimage')
cache = int(params.get('cache', '0'))
index = int(params.get('index', '-1'))
move = int(params.get('move', '0'))
mode = int(params.get('mode', '0'))
info = params.get('info')

if mode == 0:
	Categories()
	setViewM()
elif mode == 1:
	PlxCategory(url, cache)
elif mode == 2 or mode == 10:
	m3uCategory(url, logos, cache, index)
elif mode == 3 or mode == 32:
	PlayUrl(name, url, iconimage, info)
	#xbmc.executebuiltin('Notification({0}, "{1}", {2}, {3})'.format( str( info ) , str(info), 20000, ""))
elif mode == 20:
	AddNewList()
elif mode == 21:
	MoveInList(index, move, playlistsFile)
elif mode == 22:
	RemoveFromLists(index, playlistsFile)
elif mode == 23:
	ChangeKey(index, playlistsFile, "name", 30004)
elif mode == 24:
	ChangeChoice(index, playlistsFile, "url", 30002, 30005, 30006, 30016, 30017, None, 1, '.plx|.m3u|.m3u8')
elif mode == 25:
	ChangeChoice(index, playlistsFile, "image", 30022, 30022, 30022, 30024, 30025, 30021, 2)
elif mode == 26:
	ChangeChoice(index, playlistsFile, "logos", 30018, 30019, 30020, 30019, 30020, 30021, 0)
elif mode == 27:
	common.DelFile(playlistsFile)
	sys.exit()
elif mode == 28:
	ChangeCache(index, playlistsFile)
elif mode == 30:
	ListFavorites()
	setViewS()
elif mode == 31: 
	AddFavorites(url, iconimage, name, "61") 
elif mode == 72: 
	AddFavorites(url, iconimage, name, "79") 
elif mode == 93: 
	AddFavorites(url, iconimage, name, "95") 
elif mode == 33:
	RemoveFromLists(index, favoritesFile)
elif mode == 34:
	AddNewFavorite()
elif mode == 35:
	ChangeKey(index, favoritesFile, "name", 30014)
elif mode == 36:
	ChangeKey(index, favoritesFile, "url", 30015)
elif mode == 37:
	ChangeChoice(index, favoritesFile, "image", 30023, 30023, 30023, 30024, 30025, 30021, 2)
elif mode == 38:
	MoveInList(index, move, favoritesFile)
elif mode == 39:
	common.DelFile(favoritesFile)
	sys.exit()
elif mode == 50:
	ToggleGroups()
elif mode == 60:
	Series()
	setViewS()
elif mode == 61:
	EpisodioS()
	setViewS()
elif mode == 62:
	PlayS()
	setViewS()
elif mode == 71:
	MoviesNC()
	setViewM()
elif mode == 79:
	PlayM()
	setViewS()
elif mode == 80:
	Generos()
elif mode == 90:
	MoviesRCD()
	setViewM()
elif mode == 91:
	MoviesRCL()
	setViewM()
elif mode == 92:
	MoviesRCN()
	setViewM()
elif mode == 95:
	PlayMRC()
	setViewM()
elif mode == 100:
	TVRC()
	setViewM()
elif mode == 101:
	PlayTVRC()
	setViewM()
elif mode == 110:
	ToggleNext()
elif mode == 120:
	TogglePrevious()
elif mode == 130:
	Update()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
