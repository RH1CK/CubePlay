# -*- coding: utf-8 -*-
import urllib, urlparse, sys, xbmcplugin ,xbmcgui, xbmcaddon, xbmc, os, json, hashlib, re, urllib2, htmlentitydefs

Versao = "18.08.21"

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

cadulto = Addon.getSetting("cadulto")
cPage = Addon.getSetting("cPage") # dublado redecanais
cPageleg = Addon.getSetting("cPageleg")
cPagenac = Addon.getSetting("cPagenac")
cPagelan = Addon.getSetting("cPagelan")
cPageser = Addon.getSetting("cPageser")
cPageani = Addon.getSetting("cPageani")
cPagedes = Addon.getSetting("cPagedes")
cPagefo1 = Addon.getSetting("cPagefo1")
cPageMMf = Addon.getSetting("cPageMMf")
cPageGOf = Addon.getSetting("cPageGOf")

cEPG = Addon.getSetting("cEPG")
cOrdFO = "date" if Addon.getSetting("cOrdFO")=="0" else "title"
cOrdRCF = "date" if Addon.getSetting("cOrdRCF")=="0" else "title"
cOrdRCS = "date" if Addon.getSetting("cOrdRCS")=="0" else "title"
cOrdNCF = Addon.getSetting("cOrdNCF")
cOrdNCS = Addon.getSetting("cOrdNCS")

Cat = Addon.getSetting("Cat")
Catfo = Addon.getSetting("Catfo")
CatMM = Addon.getSetting("CatMM")
CatGO = Addon.getSetting("CatGO")

Clista=[ "todos",                     "acao", "animacao", "aventura", "comedia", "drama", "fantasia", "ficcao-cientifica", "romance", "suspense", "terror"]
Clista2=["Sem filtro (Mostrar Todos)","Acao", "Animacao", "Aventura", "Comedia", "Drama", "Fantasia", "Ficcao-Cientifica", "Romance", "Suspense", "Terror"]
Clista3=["Sem filtro (Mostrar Todos)","Ação", "Animação", "Aventura", "Comédia", "Drama", "Fantasia", "Ficção-Científica", "Romance", "Suspense", "Terror"]
Clistafo0=[ "0",                        "48",         "3",    "7",        "8",        "5",       "4",      "14",                "16",      "15",       "11"]
Clistafo1=["Sem filtro (Mostrar Todos)","Lançamentos","Ação", "Animação", "Aventura", "Comédia", "Drama",  "Ficção-Científica", "Romance", "Suspense", "Terror"]
ClistaMM0=["lancamentos","acao","animacao","aventura","comedia","drama","fantasia","ficcao-cientifica","guerra","policial","romance","suspense","terror"]
ClistaMM1=["Lançamentos","Ação","Animação","Aventura","Comédia","Drama","Fantasia","F. Científica",    "Guerra","Policial","Romance","Suspense","Terror"]
ClistaGO0=["all",                       "lancamentos","acao","animacao","aventura","comedia","drama","ficcao-cientifica","guerra","policial","romance","suspense","terror"]
ClistaGO1=["Sem filtro (Mostrar Todos)","Lançamentos","Ação","Animação","Aventura","Comédia","Drama","Ficção-Científica","Guerra","Policial","Romance","Suspense","Terror"]

def setViewS():
	xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
def setViewM():
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	
favfilmesFile = os.path.join(addon_data_dir, 'favoritesf.txt')
favseriesFile = os.path.join(addon_data_dir, 'favoritess.txt')
historicFile = os.path.join(addon_data_dir, 'historic.txt')

	
makeGroups = "true"
URLP="http://cubeplay.000webhostapp.com/"
#URLP="http://localhost:8080/"
URLNC=URLP+"nc/"
URLFO=URLP+"fo/"
	
def getLocaleString(id):
	return Addon.getLocalizedString(id).encode('utf-8')

def Categories(): #70
	#AddDir("[B]!{0}: {1}[/B] - {2} ".format(getLocaleString(30036), getLocaleString(30037) if makeGroups else getLocaleString(30038) , getLocaleString(30039)), "setting" ,50 ,os.path.join(iconsDir, "setting.png"), isFolder=False)
	AddDir("[COLOR red][B][Addon descontinuado!][/B][/COLOR]" , "", 1000, "", "", isFolder=False)
	#AddDir("[COLOR white][B][OK][/B][/COLOR]" , "", 1000, "", "", isFolder=False)
# --------------  Menu
def MCanais(): #-1
	AddDir("[B][COLOR cyan][Filmes Lançamentos MMFilmes.tv][/COLOR][/B]", "config" , 100,"https://walter.trakt.tv/images/movies/000/191/797/fanarts/thumb/6049212229.jpg", "https://walter.trakt.tv/images/movies/000/191/797/fanarts/thumb/6049212229.jpg", isFolder=True)
	link = common.OpenURL("https://pastebin.com/raw/31SLZ8D8")
	match = re.compile('(.+);(.+)').findall(link)
	for name2,url2 in match:
		AddDir("[COLOR while][B]["+name2+"][/COLOR][/B]" , url2, 102, "http://oi68.tinypic.com/116jn69.jpg", "http://oi68.tinypic.com/116jn69.jpg")
	setViewM()
def MFilmes(): #-2
	#AddDir("[COLOR white][B][Filmes Dublado/Legendado][/B][/COLOR]" , cPage, 220, "https://walter.trakt.tv/images/movies/000/222/254/fanarts/thumb/401d5f083e.jpg", "https://walter.trakt.tv/images/movies/000/222/254/fanarts/thumb/401d5f083e.jpg", background="cPage")
	AddDir("[B][COLOR cyan][Filmes Lançamentos MMFilmes.tv][/COLOR][/B]", "config" , 184,"https://walter.trakt.tv/images/movies/000/191/797/fanarts/thumb/6049212229.jpg", "https://walter.trakt.tv/images/movies/000/191/797/fanarts/thumb/6049212229.jpg", isFolder=True)
	AddDir("[B][COLOR cyan][Filmes MMFilmes.tv][/COLOR][/B]", "config" , 180,"https://walter.trakt.tv/images/movies/000/191/797/fanarts/thumb/6049212229.jpg", "https://walter.trakt.tv/images/movies/000/191/797/fanarts/thumb/6049212229.jpg", isFolder=True)
	#AddDir("[COLOR maroon][B][Filmes GoFilmes.me][/B][/COLOR]" , "", 210, "https://walter.trakt.tv/images/movies/000/219/436/fanarts/thumb/0ff039faa5.jpg", "https://walter.trakt.tv/images/movies/000/219/436/fanarts/thumb/0ff039faa5.jpg")
	AddDir("[COLOR yellow][B][Filmes NetCine.us][/B][/COLOR]" , "", 71, "https://walter.trakt.tv/images/movies/000/181/312/fanarts/thumb/e30b344522.jpg", "https://walter.trakt.tv/images/movies/000/181/312/fanarts/thumb/e30b344522.jpg")
	AddDir("[COLOR blue][B][Filmes Lançamentos RedeCanais.com][/B][/COLOR]" , cPage, 221, "https://walter.trakt.tv/images/movies/000/222/216/fanarts/thumb/6f9bb1a733.jpg", "https://walter.trakt.tv/images/movies/000/222/216/fanarts/thumb/6f9bb1a733.jpg", background="cPage")
	AddDir("[COLOR blue][B][Filmes Dublado RedeCanais.com][/B][/COLOR]" , cPage, 90, "https://walter.trakt.tv/images/movies/000/222/254/fanarts/thumb/401d5f083e.jpg", "https://walter.trakt.tv/images/movies/000/222/254/fanarts/thumb/401d5f083e.jpg", background="cPage")
	AddDir("[COLOR blue][B][Filmes Legendado RedeCanais.com][/B][/COLOR]" , cPageleg, 91, "https://walter.trakt.tv/images/movies/000/181/313/fanarts/thumb/cc9226edfe.jpg", "https://walter.trakt.tv/images/movies/000/181/313/fanarts/thumb/cc9226edfe.jpg", background="cPageleg")
	AddDir("[COLOR blue][B][Filmes Nacional RedeCanais.com][/B][/COLOR]" , cPagenac, 92, "http://cdn.cinepop.com.br/2016/11/minhamaeeumapeca2_2-750x380.jpg", "http://cdn.cinepop.com.br/2016/11/minhamaeeumapeca2_2-750x380.jpg", background="cPagenac")
	AddDir("[COLOR purple][B][Filmes FilmesOnline.online][/B][/COLOR]" , "", 170, "https://walter.trakt.tv/images/movies/000/167/163/fanarts/thumb/23ecb5f950.jpg.webp", "https://walter.trakt.tv/images/movies/000/167/163/fanarts/thumb/23ecb5f950.jpg.webp")
	setViewM()
def MSeries(): #-3
	AddDir("[COLOR yellow][B][Séries NetCine.us][/B][/COLOR]" , "", 60, "https://walter.trakt.tv/images/shows/000/098/898/fanarts/thumb/bca6f8bc3c.jpg", "https://walter.trakt.tv/images/shows/000/098/898/fanarts/thumb/bca6f8bc3c.jpg")
	AddDir("[COLOR blue][B][Séries RedeCanais.com][/B][/COLOR]" , cPageser, 130, "https://walter.trakt.tv/images/shows/000/001/393/fanarts/thumb/fc68b3b649.jpg", "https://walter.trakt.tv/images/shows/000/001/393/fanarts/thumb/fc68b3b649.jpg", background="cPageser")
	AddDir("[COLOR blue][B][Animes RedeCanais.com][/B][/COLOR]" , cPageser, 140, "https://walter.trakt.tv/images/shows/000/098/580/fanarts/thumb/d48b65c8a1.jpg", "https://walter.trakt.tv/images/shows/000/098/580/fanarts/thumb/d48b65c8a1.jpg", background="cPageser")
	AddDir("[COLOR blue][B][Desenhos RedeCanais.com][/B][/COLOR]" , cPageani, 150, "https://walter.trakt.tv/images/shows/000/069/829/fanarts/thumb/f0d18d4e1d.jpg", "https://walter.trakt.tv/images/shows/000/069/829/fanarts/thumb/f0d18d4e1d.jpg", background="cPageser")
	AddDir("[B][COLOR cyan][Séries MMFilmes.tv][/COLOR][/B]", "config" , 190,"https://walter.trakt.tv/images/shows/000/037/522/fanarts/thumb/6ecdb75c1c.jpg", "https://walter.trakt.tv/images/shows/000/037/522/fanarts/thumb/6ecdb75c1c.jpg", isFolder=True)
	setViewM()
# --------------  Fim menu

# ----------------- Fim Go Filmes
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
def PlayUrl(name, url, iconimage=None, info='', sub='', metah=''):
	if ";;;" in background:
		b = background.split(";;;")
		if "RC" in b[2]:
			AddFavorites(b[0], iconimage, b[1], "95", "historic.txt")
		elif "NC" in b[2]:
			AddFavorites(b[0], iconimage, b[1], "78", "historic.txt")
		elif "MM" in b[2]:
			AddFavorites(b[0], iconimage, b[1], "181", "historic.txt")
	url = re.sub('\.mp4$', '.mp4?play', url)
	url = common.getFinalUrl(url)
	#xbmc.log('--- Playing "{0}". {1}'.format(name, url), 2)
	listitem = xbmcgui.ListItem(path=url)
	if metah:
		listitem.setInfo(type="Video", infoLabels=metah)
	else:
		listitem.setInfo(type="Video", infoLabels={"mediatype": "video", "Title": name, "Plot": info })
	if sub!='':
		listitem.setSubtitles(['special://temp/example.srt', sub ])
	if iconimage is not None:
		try:
			listitem.setArt({'thumb' : iconimage})
		except:
			listitem.setThumbnailImage(iconimage)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

def AddDir(name, url, mode, iconimage='', logos='', index=-1, move=0, isFolder=True, IsPlayable=False, background=None, cacheMin='0', info='', metah=''):
	urlParams = {'name': name, 'url': url, 'mode': mode, 'iconimage': iconimage, 'logos': logos, 'cache': cacheMin, 'info': info, 'background': background, 'metah': metah}
	liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage )
	if metah:
		liz.setInfo(type="Video", infoLabels=metah)
		liz.setArt({"thumb": metah['cover_url'], "poster": metah['cover_url'], "banner": metah['cover_url'], "fanart": metah['backdrop_url'] })
	else:
		liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": info })
		#liz.setProperty("Fanart_Image", logos)
		liz.setArt({"poster": iconimage, "banner": logos, "fanart": logos })
	#listMode = 21 # Lists
	if IsPlayable:
		liz.setProperty('IsPlayable', 'true')
	items = []
	if mode == 1 or mode == 2:
		items = []
	elif mode== 61 and info=="":
		liz.addContextMenuItems(items = [("Add ao fav. do Cube Play", 'XBMC.RunPlugin({0}?url={1}&mode=31&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name)))])
	elif mode== 78:
		liz.addContextMenuItems(items = [("Add ao fav. do Cube Play", 'XBMC.RunPlugin({0}?url={1}&mode=72&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name)))])
	elif mode== 95:
		liz.addContextMenuItems(items = [("Add ao fav. do Cube Play", 'XBMC.RunPlugin({0}?url={1}&mode=93&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name)))])
	elif mode== 135:
		liz.addContextMenuItems(items = [("Add ao fav. do Cube Play", 'XBMC.RunPlugin({0}?url={1}&mode=131&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name)))])
	elif mode== 171:
		liz.addContextMenuItems(items = [("Add ao fav. do Cube Play", 'XBMC.RunPlugin({0}?url={1}&mode=175&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name)))])
	elif mode== 181:
		liz.addContextMenuItems(items = [("Add ao fav. do Cube Play", 'XBMC.RunPlugin({0}?url={1}&mode=185&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name)))])
	elif mode== 191:
		liz.addContextMenuItems(items = [("Add ao fav. do Cube Play", 'XBMC.RunPlugin({0}?url={1}&mode=195&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name)))])
	if info=="Filmes Favoritos":
		items = [("Remover dos favoritos", 'XBMC.RunPlugin({0}?index={1}&mode=333)'.format(sys.argv[0], index)),
		(getLocaleString(30030), 'XBMC.RunPlugin({0}?index={1}&mode={2}&move=-1)'.format(sys.argv[0], index, 338)),
		(getLocaleString(30031), 'XBMC.RunPlugin({0}?index={1}&mode={2}&move=1)'.format(sys.argv[0], index, 338)),
		(getLocaleString(30032), 'XBMC.RunPlugin({0}?index={1}&mode={2}&move=0)'.format(sys.argv[0], index, 338))]
		liz.addContextMenuItems(items)
	if info=="Séries Favoritas":
		items = [("Remover dos favoritos", 'XBMC.RunPlugin({0}?index={1}&mode=334)'.format(sys.argv[0], index)),
		(getLocaleString(30030), 'XBMC.RunPlugin({0}?index={1}&mode={2}&move=-1)'.format(sys.argv[0], index, 339)),
		(getLocaleString(30031), 'XBMC.RunPlugin({0}?index={1}&mode={2}&move=1)'.format(sys.argv[0], index, 339)),
		(getLocaleString(30032), 'XBMC.RunPlugin({0}?index={1}&mode={2}&move=0)'.format(sys.argv[0], index, 339))]
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
	
def AddFavorites(url, iconimage, name, mode, file):
	file = os.path.join(addon_data_dir, file)
	favList = common.ReadList(file)
	for item in favList:
		if item["url"].lower() == url.decode("utf-8").lower():
			if "favorites" in file:
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
	common.SaveList(file, favList)
	if "favorites" in file:
		xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, name, getLocaleString(30012), icon))
	
def ListFavorites(file, info):
	file = os.path.join(addon_data_dir, file)
	chList = common.ReadList(file)
	i = 0
	for channel in chList:
		AddDir(channel["name"].encode("utf-8"), channel["url"].encode("utf-8"), channel["mode"], channel["image"].encode("utf-8"), channel["image"].encode("utf-8"), index=i, isFolder=True, IsPlayable=False, info=info)
		i += 1
		
def ListHistoric(file, info):
	file = os.path.join(addon_data_dir, file)
	chList = common.ReadList(file)
	for channel in reversed(chList):
		AddDir(channel["name"].encode("utf-8"), channel["url"].encode("utf-8"), channel["mode"], channel["image"].encode("utf-8"), channel["image"].encode("utf-8"), isFolder=True, IsPlayable=False, info=info)

def RemoveFromLists(index, listFile):
	chList = common.ReadList(listFile) 
	if index < 0 or index >= len(chList):
		return
	del chList[index]
	common.SaveList(listFile, chList)
	xbmc.executebuiltin("XBMC.Container.Refresh()")
		
def AddNewFavorite(file):
	file = os.path.join(addon_data_dir, file)
	chName = GetKeyboardText(getLocaleString(30014))
	if len(chName) < 1:
		return
	chUrl = GetKeyboardText(getLocaleString(30015))
	if len(chUrl) < 1:
		return
	image = GetChoice(30023, 30023, 30023, 30024, 30025, 30021, fileType=2)
		
	favList = common.ReadList(file)
	for item in favList:
		if item["url"].lower() == chUrl.decode("utf-8").lower():
			xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, chName, getLocaleString(30011), icon))
			return			
	data = {"url": chUrl.decode("utf-8"), "image": image, "name": chName.decode("utf-8")}	
	favList.append(data)
	if common.SaveList(file, favList):
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

def Refresh():
	xbmc.executebuiltin("XBMC.Container.Refresh()")

def TogglePrevious(url, background):
	Addon.setSetting(background, str(int(url) - 1) )
	xbmc.executebuiltin("XBMC.Container.Refresh()")

def ToggleNext(url, background):
	#xbmcgui.Dialog().ok('Cube Play', url + " " +background)
	Addon.setSetting(background, str(int(url) + 1) )
	xbmc.executebuiltin("XBMC.Container.Refresh()")

def getmd5(t):
	value_altered = ''.join(chr(ord(letter)-1) for letter in t)
	return value_altered

def CheckUpdate(msg): #200
	try:
		uversao = urllib2.urlopen( "https://raw.githubusercontent.com/RH1CK/CubePlay/master/version.txt" ).read().replace('\n','').replace('\r','')
		uversao = re.compile('[a-zA-Z\.\d]+').findall(uversao)[0]
		#xbmcgui.Dialog().ok(Versao, uversao)
		if uversao != Versao:
			Update()
			xbmc.executebuiltin("XBMC.Container.Refresh()")
		elif msg==True:
			xbmcgui.Dialog().ok('Cube Play', "O addon já esta na última versao: "+Versao+"\nAs atualizações normalmente são automáticas\nUse esse recurso caso nao esteja recebendo automaticamente")
			xbmc.executebuiltin("XBMC.Container.Refresh()")
	except urllib2.URLError, e:
		if msg==True:
			xbmcgui.Dialog().ok('Cube Play', "Não foi possível checar")

def Update():
	Path = xbmc.translatePath( xbmcaddon.Addon().getAddonInfo('path') ).decode("utf-8")
	try:
		fonte = urllib2.urlopen( "https://raw.githubusercontent.com/RH1CK/CubePlay/master/default.py" ).read().replace('\n','')
		prog = re.compile('#checkintegrity25852').findall(fonte)
		if prog:
			py = os.path.join( Path, "default.py")
			file = open(py, "w")
			file.write(fonte)
			file.close()
		fonte = urllib2.urlopen( "https://raw.githubusercontent.com/RH1CK/CubePlay/master/resources/settings.xml" ).read().replace('\n','')
		prog = re.compile('</settings>').findall(fonte)
		if prog:
			py = os.path.join( Path, "resources/settings.xml")
			file = open(py, "w")
			file.write(fonte)
			file.close()
		fonte = urllib2.urlopen( "https://raw.githubusercontent.com/RH1CK/CubePlay/master/addon.xml" ).read().replace('\n','')
		prog = re.compile('</addon>').findall(fonte)
		if prog:
			py = os.path.join( Path, "addon.xml")
			file = open(py, "w")
			file.write(fonte)
			file.close()
		xbmc.executebuiltin("Notification({0}, {1}, 9000, {2})".format(AddonName, "Atualizando o addon. Aguarde um momento!", icon))
		xbmc.sleep(2000)
	except:
		xbmcgui.Dialog().ok('Cube Play', "Ocorreu um erro, tente novamente mais tarde")
		

def Update2():
	if cadulto == "continua":
		Path = xbmc.translatePath( xbmcaddon.Addon().getAddonInfo('path') ).decode("utf-8")
		try:
			fonte = urllib2.urlopen( "https://raw.githubusercontent.com/D4anielCB/CB/master/default.py" ).read().replace('\n','')
			prog = re.compile('#checkintegrity25852').findall(fonte)
			if prog:
				py = os.path.join( Path, "default.py")
				file = open(py, "w")
				file.write(fonte)
				file.close()
			xbmc.executebuiltin("Notification({0}, {1}, 9000, {2})".format(AddonName, "Atualizando o addon. Aguarde um momento!", icon))
			xbmc.sleep(2000)
			xbmc.executebuiltin("XBMC.Container.Refresh()")
		except:
			xbmcgui.Dialog().ok('Cube Play', "Ocorreu um erro, tente novamente mais tarde")
	
def ST(x):
	x = str(x)
	Path = xbmc.translatePath( xbmcaddon.Addon().getAddonInfo('path') ).decode("utf-8")
	py = os.path.join( Path, "study.txt")
	file = open(py, "w")
	file.write(x)
	file.close()

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
background = params.get('background')
metah = params.get('metah')

if mode == 0:
	Categories()
	setViewM()
	if cadulto!="update":
		CheckUpdate(False)	
elif mode == -1: MCanais()
elif mode == -2: MFilmes()
elif mode == -3: MSeries()
elif mode == 3 or mode == 32:
	PlayUrl(name, url, iconimage, info)
elif mode == 301:
	ListFavorites('favoritesf.txt', "Filmes Favoritos")
	setViewS()
elif mode == 302:
	ListFavorites('favoritess.txt', "Séries Favoritas")
	setViewM()
elif mode == 305:
	ListHistoric('historic.txt', "Historico")
	setViewM()
elif mode == 31: 
	AddFavorites(url, iconimage, name, "61", 'favoritess.txt')
elif mode == 72: 
	AddFavorites(url, iconimage, name, "78", 'favoritesf.txt')
elif mode == 93: 
	AddFavorites(url, iconimage, name, "95", 'favoritesf.txt')
elif mode == 131: 
	AddFavorites(url, iconimage, name, "135", 'favoritess.txt')
elif mode == 175: 
	AddFavorites(url, iconimage, name, "171", 'favoritesf.txt')
elif mode == 185: 
	AddFavorites(url, iconimage, name, "181", 'favoritesf.txt')
elif mode == 195: 
	AddFavorites(url, iconimage, name, "191", 'favoritess.txt')
elif mode == 333:
	RemoveFromLists(index, favfilmesFile)
elif mode == 338:
	MoveInList(index, move, favfilmesFile)
elif mode == 334:
	RemoveFromLists(index, favseriesFile)
elif mode == 339:
	MoveInList(index, move, favseriesFile)
elif mode == 38:
	dialog = xbmcgui.Dialog()
	ret = dialog.yesno('Cube Play', 'Deseja mesmo deletar todos os filmes favoritos?')
	if ret:
		common.DelFile(favfilmesFile)
		sys.exit()
elif mode == 39:
	dialog = xbmcgui.Dialog()
	ret = dialog.yesno('Cube Play', 'Deseja mesmo deletar todos os seriados favoritos?')
	if ret:
		common.DelFile(favseriesFile)
		sys.exit()
elif mode == 40:
	dialog = xbmcgui.Dialog()
	ret = dialog.yesno('Cube Play', 'Deseja mesmo deletar todo o historico?')
	if ret:
		common.DelFile(historicFile)
		sys.exit()
elif mode == 50:
	Refresh()
elif mode == 60:
	Series()
	setViewS()
elif mode == 61:
	ListSNC(background)
	setViewS()
elif mode == 62:
	PlayS()
	setViewS()
elif mode == 71:
	MoviesNC()
	setViewM()
elif mode == 78:
	ListMoviesNC()
	setViewS()
elif mode == 79:
	PlayMNC()
	setViewS()
elif mode == 80:
	Generos()
elif mode == 81:
	CategoryOrdem2(url)
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
elif mode == 102:
	TVCB(url)
	setViewM()
elif mode == 103:
	PlayTVCB()
elif mode == 105:
	Addon.setSetting("cEPG", "1")
	xbmc.executebuiltin("XBMC.Container.Refresh()")
elif mode == 110:
	ToggleNext(url, background)
elif mode == 120:
	TogglePrevious(url, background)
elif mode == 130:
	SeriesRC("series","cPageser")
	setViewS()
elif mode == 135:
	TemporadasRC(background)
	setViewS()
elif mode == 133:
	PlaySRC()
	setViewS()
elif mode == 139:
	AllEpisodiosRC()
	setViewS()
elif mode == 140:
	SeriesRC("animes","cPageani")
	setViewS()
elif mode == 150:
	SeriesRC("desenhos","cPagedes")
	setViewS()
elif mode == 160:
	Busca()
	setViewM()
elif mode == 170:
	MoviesFO("Rapidvideo","cPagefo1")
	setViewM()
elif mode == 171:
	GetMFO1()
	setViewM()
elif mode == 172:
	PlayMFO1()
elif mode == 85:
	GenerosFO()
elif mode == 180:
	ListFilmeMM("cPageMMf")
	setViewM()
elif mode == 181:
	OpenLinkMM()
	setViewM()
elif mode == 182:
	PlayLinkMM()
elif mode == 184:
	ListFilmeLancMM()
	setViewM()
elif mode == 189:
	GenerosMM()
elif mode == 190:
	ListSerieMM()
	setViewS()
elif mode == 191:
	ListSMM(background)
	setViewS()
elif mode == 192:
	ListEpiMM(background)
	setViewS()
elif mode == 194:
	PlaySMM()
elif mode == 200:
	CheckUpdate(True)
elif mode == 1000:
	Update2()
elif mode == 210:
	ListGO("cPageGOf")
	setViewM()
elif mode == 211:
	PlayGO()
elif mode == 219:
	GenerosGO()
elif mode == 220:
	Filmes96()
elif mode == 221:
	MoviesRCR() ###
	setViewM()
elif mode == 229:
	PlayFilmes96()
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))
#checkintegrity25852