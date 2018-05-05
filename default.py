﻿# -*- coding: utf-8 -*-
import urllib, urlparse, sys, xbmcplugin ,xbmcgui, xbmcaddon, xbmc, os, json, hashlib, re, urllib2, htmlentitydefs, random

Versao = "18.05.05a"

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
cPageser = Addon.getSetting("cPageser")
cPageani = Addon.getSetting("cPageani")
cPagedes = Addon.getSetting("cPagedes")
cPagefo1 = Addon.getSetting("cPagefo1")
cPageMMf = Addon.getSetting("cPageMMf")

cEPG = Addon.getSetting("cEPG")
cOrdFO = "date" if Addon.getSetting("cOrdFO")=="0" else "title"
cOrdRCF = "date" if Addon.getSetting("cOrdRCF")=="0" else "title"
cOrdRCS = "date" if Addon.getSetting("cOrdRCS")=="0" else "title"
cOrdNCF = Addon.getSetting("cOrdNCF")
cOrdNCS = Addon.getSetting("cOrdNCS")

Cat = Addon.getSetting("Cat")
Catfo = Addon.getSetting("Catfo")
CatMM = Addon.getSetting("CatMM")
Clista=[ "todos",                     "acao", "animacao", "aventura", "comedia", "drama", "fantasia", "ficcao-cientifica", "romance", "suspense", "terror"]
Clista2=["Sem filtro (Mostrar Todos)","Acao", "Animacao", "Aventura", "Comedia", "Drama", "Fantasia", "Ficcao-Cientifica", "Romance", "Suspense", "Terror"]
Clistafo0=[ "0",                        "48",         "3",    "7",        "8",        "5",       "4",      "14",                "16",      "15",       "11"]
Clistafo1=["Sem filtro (Mostrar Todos)","Lançamentos","Ação", "Animação", "Aventura", "Comédia", "Drama",  "Ficção-Científica", "Romance", "Suspense", "Terror"]
ClistaMM0=["lancamentos","acao","animacao","aventura","comedia","drama","fantasia","ficcao-cientifica","guerra","policial","romance","suspense","terror"]
ClistaMM1=["Lançamentos","Ação","Animação","Aventura","Comédia","Drama","Fantasia","F. Científica",    "Guerra","Policial","Romance","Suspense","Terror"]
def setViewS():
	xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
def setViewM():
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	
favoritesFile = os.path.join(addon_data_dir, 'favorites.txt')
historicFile = os.path.join(addon_data_dir, 'historic.txt')
if not (os.path.isfile(favoritesFile)):
	common.SaveList(favoritesFile, [])
if not (os.path.isfile(historicFile)):
	common.SaveList(historicFile, [])
	
makeGroups = "true"
URLP="http://cubeplay.000webhostapp.com/"
#URLP="http://localhost:8080/"
URLNC=URLP+"nc/"
URLFO=URLP+"fo/"
	
def getLocaleString(id):
	return Addon.getLocalizedString(id).encode('utf-8')

def Categories(): #70
	#xbmcgui.Dialog().ok('Kodi', str(cPagenac))
	#AddDir("[B]!{0}: {1}[/B] - {2} ".format(getLocaleString(30036), getLocaleString(30037) if makeGroups else getLocaleString(30038) , getLocaleString(30039)), "setting" ,50 ,os.path.join(iconsDir, "setting.png"), isFolder=False)
	AddDir("[COLOR white][B][Canais de TV CubePlay][/B][/COLOR]" , "", 102, "http://oi68.tinypic.com/116jn69.jpg", "http://oi68.tinypic.com/116jn69.jpg")
	AddDir("[COLOR white][B][Canais de TV RedeCanais.com][/B][/COLOR]" , "", 100, "http://oi68.tinypic.com/116jn69.jpg", "http://oi68.tinypic.com/116jn69.jpg")
	AddDir("[B][COLOR cyan][Filmes MMFilmes.tv][/COLOR][/B]", "config" , 180,"https://walter.trakt.tv/images/movies/000/191/797/fanarts/thumb/6049212229.jpg", "https://walter.trakt.tv/images/movies/000/191/797/fanarts/thumb/6049212229.jpg", isFolder=True)
	AddDir("[COLOR yellow][B][Séries NetCine.us][/B][/COLOR]" , "", 60, "https://walter.trakt.tv/images/shows/000/098/898/fanarts/thumb/bca6f8bc3c.jpg", "https://walter.trakt.tv/images/shows/000/098/898/fanarts/thumb/bca6f8bc3c.jpg")
	AddDir("[COLOR yellow][B][Filmes NetCine.us][/B][/COLOR]" , "", 71, "https://walter.trakt.tv/images/movies/000/181/312/fanarts/thumb/e30b344522.jpg", "https://walter.trakt.tv/images/movies/000/181/312/fanarts/thumb/e30b344522.jpg")
	
	AddDir("[COLOR blue][B][Filmes Dublado RedeCanais.com][/B][/COLOR]" , cPage, 90, "https://walter.trakt.tv/images/movies/000/222/254/fanarts/thumb/401d5f083e.jpg", "https://walter.trakt.tv/images/movies/000/222/254/fanarts/thumb/401d5f083e.jpg", background="cPage")
	AddDir("[COLOR blue][B][Filmes Legendado RedeCanais.com][/B][/COLOR]" , cPageleg, 91, "https://walter.trakt.tv/images/movies/000/181/313/fanarts/thumb/cc9226edfe.jpg", "https://walter.trakt.tv/images/movies/000/181/313/fanarts/thumb/cc9226edfe.jpg", background="cPageleg")
	AddDir("[COLOR blue][B][Filmes Nacional RedeCanais.com][/B][/COLOR]" , cPagenac, 92, "http://cdn.cinepop.com.br/2016/11/minhamaeeumapeca2_2-750x380.jpg", "http://cdn.cinepop.com.br/2016/11/minhamaeeumapeca2_2-750x380.jpg", background="cPagenac")
	AddDir("[COLOR blue][B][Séries RedeCanais.com][/B][/COLOR]" , cPageser, 130, "https://walter.trakt.tv/images/shows/000/001/393/fanarts/thumb/fc68b3b649.jpg", "https://walter.trakt.tv/images/shows/000/001/393/fanarts/thumb/fc68b3b649.jpg", background="cPageser")
	AddDir("[COLOR purple][B][Filmes FilmesOnline.online][/B][/COLOR]" , "", 170, "https://walter.trakt.tv/images/movies/000/167/163/fanarts/thumb/23ecb5f950.jpg.webp", "https://walter.trakt.tv/images/movies/000/167/163/fanarts/thumb/23ecb5f950.jpg.webp")
	#AddDir("[COLOR red][B][Genero dos Filmes]:[/B] " + Clista2[int(Cat)] +"[/COLOR]", "url" ,80 ,"https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", "https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", isFolder=False)
	AddDir("[COLOR blue][B][Animes RedeCanais.com][/B][/COLOR]" , cPageser, 140, "https://walter.trakt.tv/images/shows/000/098/580/fanarts/thumb/d48b65c8a1.jpg", "https://walter.trakt.tv/images/shows/000/098/580/fanarts/thumb/d48b65c8a1.jpg", background="cPageser")
	AddDir("[COLOR blue][B][Desenhos RedeCanais.com][/B][/COLOR]" , cPageani, 150, "https://walter.trakt.tv/images/shows/000/069/829/fanarts/thumb/f0d18d4e1d.jpg", "https://walter.trakt.tv/images/shows/000/069/829/fanarts/thumb/f0d18d4e1d.jpg", background="cPageser")
	AddDir("[COLOR green][B][Favoritos Cube Play][/B][/COLOR]", "favorites" ,30 , "http://icons.iconarchive.com/icons/royalflushxx/systematrix/256/Favorites-icon.png", "http://icons.iconarchive.com/icons/royalflushxx/systematrix/256/Favorites-icon.png")
	AddDir("[COLOR green][B][Histórico Filmes][/B][/COLOR]", "historic" ,333 , "https://cdn2.iconfinder.com/data/icons/business-office-icons/256/To-do_List-512.png", "https://cdn2.iconfinder.com/data/icons/business-office-icons/256/To-do_List-512.png")
	AddDir("[COLOR pink][B][Busca][/B][/COLOR]" , "", 160, "https://azure.microsoft.com/svghandler/search/?width=400&height=315", "https://azure.microsoft.com/svghandler/search/?width=400&height=315")
	AddDir("[B][Sobre o Addon][/B]", "config" ,0 ,"http://www.iconsplace.com/icons/preview/orange/about-256.png", "http://www.iconsplace.com/icons/preview/orange/about-256.png", isFolder=False, info="Addon modificado do PlaylistLoader 1.2.0 por Avigdor\r https://github.com/avigdork/xbmc-avigdork.\r\nNao somos responsaveis por colocar o conteudo online, apenas indexamos.\r\nPara sugestoes e report de bugs nossa pagina no FB: [COLOR blue]http://fb.com/CubePlayKodi[/COLOR]\nVersão: "+Versao)
	AddDir("[B][COLOR blue]http://fb.com/CubePlayKodi[/COLOR][/B]", "config" ,0 ,"https://cdn.pixabay.com/photo/2017/08/20/10/30/facebook-2661207_960_720.jpg", "https://cdn.pixabay.com/photo/2017/08/20/10/30/facebook-2661207_960_720.jpg", isFolder=False, info="Para sugestoes e report de bugs nossa pagina no FB: [COLOR blue]http://fb.com/CubePlayKodi[/COLOR]")
	AddDir("[B][COLOR orange][Checar Atualizações][/COLOR][/B]", "config" , 200,"https://accelerator-origin.kkomando.com/wp-content/uploads/2015/04/update2-970x546.jpg", "https://accelerator-origin.kkomando.com/wp-content/uploads/2015/04/update2-970x546.jpg", isFolder=False, info="Checar se ha atualizacoes\n\nAs atualizacoes normalmente sao automaticas\nUse esse recurso caso nao esteja recebendo automaticamente")
# --------------  NETCINE
def PlayS(): #62
	try:
		link = urllib2.urlopen(URLNC +  url).read().replace('\n','').replace('\r','')
		match = re.compile('url="(.+?)".+?mg="(.+?)".+?ame="(.+?)".+?nfo="(.+?)"').findall(link)
		listau=[]
		listan=[]
		listai=[]
		for url2,img2,name2,info2 in match:
			listau.append(url2)
			listan.append(name2 + name)
			listai.append(info2)
		d = xbmcgui.Dialog().select("Cube Play", listan)
		if d!= -1:
			PlayUrl(listan[d], listau[d], iconimage, listai[d])
	except urllib2.URLError, e:
		xbmcgui.Dialog().ok("Cube Play" , "Server error, tente novamente em alguns minutos")

def EpisodioS(): #61
	try:
		link = urllib2.urlopen( URLNC + url ).read().replace('\n','').replace('\r','')
		match = re.compile('url="(.+?)".+?mg="(.+?)".+?ame="(.+?)".+?nfo="(.+?)"').findall(link)
		for url2,img2,name2,info2 in match:
			AddDir(name2 ,url2, 62, iconimage, iconimage, isFolder=False, IsPlayable=True, info=info2)
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, isFolder=False)
	
def Series(): #60
	try:
		link = urllib2.urlopen(URLNC + "listTVshow.php?o="+cOrdNCS).read().replace('\n','').replace('\r','')
		match = re.compile('url="(.+?)".+?mg="(.+?)".+?ame="(.+?)"').findall(link)
		for url2,img2,name2 in match:
			AddDir(name2, url2, 61, img2, img2)
	except urllib2.URLError, e:
		AddDir("Server NETCINE offline, tente novamente em alguns minutos" , "", 0, isFolder=False)

def MoviesNC(): #70
	AddDir("[COLOR yellow][B][Genero dos Filmes]:[/B] " + Clista2[int(Cat)] +"[/COLOR]", "url" ,80 ,"https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", "https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", isFolder=False)
	try:
		link = urllib2.urlopen(URLNC + "listMovies.php?o="+cOrdNCF +"&cat=" + Clista[int(Cat)]).read().replace('\n','').replace('\r','')
		match = re.compile('url="(.+?)".+?mg="(.+?)".+?ame="(.+?)"').findall(link)
		for url2,img2,name2 in match:
			AddDir(name2 ,url2, 79, img2, img2)
	except urllib2.URLError, e:
		AddDir("Server NETCINE offline, tente novamente em alguns minutos" , "", 0, isFolder=False)

def Generos(): #80
	d = xbmcgui.Dialog().select("Escolha o Genero", Clista2)
	if d != -1:
		global Cat
		Addon.setSetting("Cat", str(d) )
		Cat = d
		Addon.setSetting("cPage", "0" )
		Addon.setSetting("cPageleg", "0" )
		xbmc.executebuiltin("XBMC.Container.Refresh()")

def PlayM(): #79
	try:
		link = urllib2.urlopen(URLNC + url ).read().replace('\n','').replace('\r','')
		match = re.compile('url="(.+?)".+?mg="(.+?)".+?ame="(.+?)".+?nfo="(.+?)"').findall(link)
		for url2,img2,name2,info2 in match:
			AddDir(name2 + name ,url2, 3, iconimage, iconimage, isFolder=False, IsPlayable=True, info=info2, background=url+";;;"+name)
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, isFolder=False)
# --------------  FIM NETCINE
# --------------  REDECANAIS FILMES
def MoviesRCD(): #90 Filme dublado
	AddDir("[COLOR yellow][B][Genero dos Filmes]:[/B] " + Clista2[int(Cat)] +"[/COLOR]", "url" ,80 ,"https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", "https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", isFolder=False)
	try:
		p= 1
		if int(cPage) > 0:
			AddDir("[COLOR blue][B]<< Pagina Anterior ["+ str( int(cPage) ) +"[/B]][/COLOR]", cPage , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False, background="cPage")
		l= int(cPage)*5
		for x in range(0, 5):
			l +=1
			link = common.OpenURL("http://www.redecanais.info/browse-filmes-dublado-videos-"+str(l)+"-"+cOrdRCF+".html")
			if Clista2[int(Cat)] != "Sem filtro (Mostrar Todos)":
				link = common.OpenURL("http://www.redecanais.info/browse-"+Clista2[int(Cat)]+"-Filmes-videos-"+str(l)+"-"+cOrdRCF+".html")
			match = re.compile('href=\"(https:\/\/www.redecanais[^\"]+).+?src=\"([^\"]+)\".alt=\"([^\"]+)\" wi').findall(link)
			if match:
				for url2,img2,name2 in match:
					AddDir(name2 ,url2, 95, img2, img2, info="")
					p += 1
			else:
				break
		if p >= 60:
			AddDir("[COLOR blue][B]Proxima Pagina >> ["+ str( int(cPage) + 2) +"[/B]][/COLOR]", cPage , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False, background="cPage")
	except e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "")
def MoviesRCL(): #91 Filme Legendado
	AddDir("[COLOR yellow][B][Genero dos Filmes]:[/B] " + Clista2[int(Cat)] +"[/COLOR]", "url" ,80 ,"https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", "https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", isFolder=False)
	try:
		p= 1
		if int(cPageleg) > 0:
			AddDir("[COLOR blue][B]<< Pagina Anterior ["+ str( int(cPageleg) ) +"[/B]][/COLOR]", cPageleg , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False, background="cPageleg")
		l= int(cPageleg)*5
		for x in range(0, 5):
			l +=1
			link = common.OpenURL("http://www.redecanais.info/browse-filmes-legendado-videos-"+str(l)+"-"+cOrdRCF+".html")
			if Clista2[int(Cat)] != "Sem filtro (Mostrar Todos)":
				link = common.OpenURL("http://www.redecanais.info/browse-"+Clista2[int(Cat)]+"-Filmes-Legendado-videos-"+str(l)+"-"+cOrdRCF+".html")
			match = re.compile('href=\"(https:\/\/www.redecanais[^\"]+).+?src=\"([^\"]+)\".alt=\"([^\"]+)\" wi').findall(link)
			if match:
				for url2,img2,name2 in match:
					AddDir(name2 ,url2, 95, img2, img2, info="")
					p += 1
			else:
				break
		if p >= 60:
			AddDir("[COLOR blue][B]Proxima Pagina >> ["+ str( int(cPageleg) + 2) +"[/B]][/COLOR]", cPageleg , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False, background="cPageleg")
	except e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "")
def MoviesRCN(): #92 Filmes Nacional
	try:
		p= 1
		if int(cPagenac) > 0:
			AddDir("[COLOR blue][B]<< Pagina Anterior ["+ str( int(cPagenac) ) +"[/B]][/COLOR]", cPagenac , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False, background="cPagenac")
		l= int(cPagenac)*5
		for x in range(0, 5):
			l +=1
			link = common.OpenURL("http://www.redecanais.info/browse-filmes-nacional-videos-"+str(l)+"-"+cOrdRCF+".html")
			match = re.compile('href=\"(https:\/\/www.redecanais[^\"]+).+?src=\"([^\"]+)\".alt=\"([^\"]+)\" wi').findall(link)
			if match:
				for url2,img2,name2 in match:
					AddDir(name2 ,url2, 95, img2, img2, info="")
					p += 1
			else:
				break
		if p >= 60:
			AddDir("[COLOR blue][B]Proxima Pagina >> ["+ str( int(cPagenac) + 2) +"[/B]][/COLOR]", cPagenac , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False, background="cPagenac")
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "", 0)
def PlayMRC(): #95 Play filmes
	try:
		link = common.OpenURL(url.replace("https","http"))
		desc = re.compile('<p itemprop=\"description\"><p>(.+)<\/p><\/p>').findall(link)
		if desc:
			desc = re.sub('&([^;]+);', lambda m: unichr(htmlentitydefs.name2codepoint[m.group(1)]), desc[0]).encode('utf-8')
		player = re.compile('<iframe name=\"Player\".+src=\"([^\"]+)\"').findall(link)
		if player:
			link2 = common.OpenURL(player[0])
			urlp = re.compile('file: \"([^\"]+)\"').findall(link2)
			AddDir("[B][COLOR yellow]"+ name +" [/COLOR][/B]"  , urlp[0] + "?play|Referer=http://www.redecanais.com/", 3, iconimage, iconimage, index=0, isFolder=False, IsPlayable=True, info=desc, background=url+";;;"+name)
		else:
			AddDir("[B]Ocorreu um erro[/B]"  , "", 0, iconimage, iconimage, index=0, isFolder=False, IsPlayable=False, info="Erro")
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "")
# ----------------- FIM REDECANAIS
# --------------  REDECANAIS SERIES,ANIMES,DESENHOS
def PlaySRC(): #131 Play series
	try:
		url2 = re.sub('(\.link|\.com|\.net)', ".info", url.replace("https","http") )
		link = common.OpenURL(url2)
		desc = re.compile('<p itemprop=\"description\"><p>(.+)<\/p><\/p>').findall(link)
		if desc:
			desc = re.sub('&([^;]+);', lambda m: unichr(htmlentitydefs.name2codepoint[m.group(1)]), desc[0]).encode('utf-8')
		player = re.compile('<iframe name=\"Player\".+src=\"([^\"]+)\"').findall(link)
		if player:
			link2 = common.OpenURL(player[0])
			urlp = re.compile('file: \"([^\"]+)\"').findall(link2)
			PlayUrl(name, urlp[0] + "?play|Referer=http://www.redecanais.com/", iconimage, name)
		else:
			xbmcgui.Dialog().ok('Cube Play', 'Erro, tente novamente em alguns minutos')
	except urllib2.URLError, e:
		xbmcgui.Dialog().ok('Cube Play', 'Erro, tente novamente em alguns minutos')
def TemporadasRC(): #135 Temporadas
	url2 = re.sub('(\.link|\.com|\.net)', ".info", url.replace("https","http") )
	link = common.OpenURL(url2).replace('\n','').replace('\r','').replace('</html>','<span style="font').replace("https","http")
	temps = re.compile('size: x-large;\">.+?<span style\=\"font').findall(link)
	if temps:
		i= 0
		epi = re.compile('<strong>(E.+?)<\/strong>(.+?)(<br|<\/p)').findall(temps[0])
		temps = re.compile('(<span style="font-size: x-large;">(.+?)<\/span>)').findall(link)
		if temps:
			for a,tempname in temps:
				tempname = re.sub('<[\/]{0,1}strong>', "", tempname)
				try:
					tempname = re.sub('&([^;]+);', lambda m: unichr(htmlentitydefs.name2codepoint[m.group(1)]), tempname).encode('utf-8')
				except:
					tempname = tempname
				if not "ilme" in tempname:
					AddDir("[B]["+tempname+"][/B]" , url, 136, iconimage, iconimage, info="", isFolder=True, background=i)
				i+=1
	AddDir("[B][Todos Episódios][/B]" ,url, 139, iconimage, iconimage, info="")
def EpisodiosRC(x): #136 Episodios
	url2 = re.sub('(\.link|\.com|\.net)', ".info", url.replace("https","http") )
	link = common.OpenURL(url2).replace('\n','').replace('\r','').replace('</html>','<span style="font')
	temps = re.compile('size: x-large;\">.+?<span style\=\"font').findall(link)
	if temps:
		i= 0
		epi = re.compile('<strong>(E.+?)<\/strong>(.+?)(<br|<\/p)').findall(temps[ int(x) ])
	else:
		epi = re.compile('<strong>(E.+?)<\/strong>(.+?)(<br|<\/p)').findall(link)
	S= 0
	if epi:
		for name2,url2,brp in epi:
			name3 = re.compile('\d+').findall(name2)
			if name3:
				name3=name3[0]
			else:
				name3=name2
			urlm = re.compile('href\=\"(.+?)\"').findall(url2)
			try:
				namem = re.sub('&([^;]+);', lambda m: unichr(htmlentitydefs.name2codepoint[m.group(1)]), re.compile('([^\-]+)').findall(url2)[0] ).encode('utf-8')
			except:
				namem = re.compile('([^\-]+)').findall(url2)[0]
			namem = re.sub('<[\/]{0,1}strong>', "", namem)
			if "<" in namem:
				namem = ""
			if urlm:
				urlm[0] = "http://www.redecanais.info/" + urlm[0] if "http" not in urlm[0] else urlm[0]
			if len(urlm) > 1:
				urlm[1] = "http://www.redecanais.info/" + urlm[1] if "http" not in urlm[1] else urlm[1]
				AddDir("[COLOR yellow][Dub][/COLOR] "+ name3 +" "+namem ,urlm[0], 133, iconimage, iconimage, info="", isFolder=False, IsPlayable=True)
				AddDir("[COLOR blue][Leg][/COLOR] "+ name3 +" "+namem ,urlm[1], 133, iconimage, iconimage, info="", isFolder=False, IsPlayable=True)
			elif urlm:
				AddDir(name3 +" "+namem ,urlm[0], 133, iconimage, iconimage, info="", isFolder=False, IsPlayable=True)

def SeriesRC(urlrc,pagina2): #130 Lista as Series RC
	try:
		pagina=eval(pagina2)
		p= 1
		if int(pagina) > 0:
			AddDir("[COLOR blue][B]<< Pagina Anterior ["+ str( int(pagina) ) +"[/B]][/COLOR]", pagina , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False, background=pagina2)
		l= int(pagina)*5
		for x in range(0, 5):
			l +=1
			link = common.OpenURL("http://www.redecanais.info/browse-"+urlrc+"-videos-"+str(l)+"-"+cOrdRCS+".html")
			match = re.compile('href=\"(https:\/\/www.redecanais[^\"]+).+?src=\"([^\"]+)\".alt=\"([^\"]+)\" wi').findall(link)
			if match:
				for url2,img2,name2 in match:
					AddDir(name2 ,url2, 135, img2, img2, info="")
					p += 1
			else:
				break
		if p >= 60:
			AddDir("[COLOR blue][B]Proxima Pagina >> ["+ str( int(pagina) + 2) +"[/B]][/COLOR]", pagina , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False, background=pagina2)
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , url, 0, "", "")
def AllEpisodiosRC(): #139 Mostrar todos Epi
	link = common.OpenURL(url)
	match = re.compile('<strong>(E.+?)<\/strong>(.+?)(<br|<\/p)').findall(link)
	S= 0
	if match:
		for name2,url2,brp in match:
			name3 = re.compile('\d+').findall(name2)
			if name3:
				name3=name3[0]
				if int(name3) == 1:
					S = S + 1
			else:
				name3=name2

			urlm = re.compile('href\=\"(.+?)\"').findall(url2)
			try:
				namem = re.sub('&([^;]+);', lambda m: unichr(htmlentitydefs.name2codepoint[m.group(1)]), re.compile('([^\-]+)').findall(url2)[0] ).encode('utf-8')
			except:
				namem = re.compile('([^\-]+)').findall(url2)[0]
			if "<" in namem:
				namem = ""
			if urlm:
				if "http" not in urlm[0]:
					urlm[0] = "http://www.redecanais.net/" + urlm[0]
			if len(urlm) > 1:
				if "http" not in urlm[1]:
					urlm[1] = "http://www.redecanais.net/" + urlm[1]
				AddDir("[COLOR yellow][Dub][/COLOR] S"+str(S)+" E"+ name3 +" "+namem ,urlm[0], 133, iconimage, iconimage, info="", isFolder=False, IsPlayable=True)
				AddDir("[COLOR blue][Leg][/COLOR] S"+str(S)+" E"+ name3 +" "+namem ,urlm[1], 133, iconimage, iconimage, info="", isFolder=False, IsPlayable=True)
			elif urlm:
				AddDir("S"+str(S)+" E"+ name3 +" "+namem ,urlm[0], 133, iconimage, iconimage, info="", isFolder=False, IsPlayable=True)
# ----------------- FIM REDECANAIS SERIES,ANIMES,DESENHOS
# ----------------- BUSCA
def Busca(): # 160
	AddDir("[COLOR pink][B][Nova Busca][/B][/COLOR]", "" , 50 ,"", isFolder=False)
	d = xbmcgui.Dialog().input("Busca (poder demorar a carregar os resultados)").replace(" ", "+")
	try:
		p= 1
		AddDir("[COLOR blue][B][RedeCanais.com][/B][/COLOR]", "" , 0 ,"", isFolder=False)
		l= 0
		for x in range(0, 7):
			l +=1
			link = common.OpenURL("http://www.redecanais.info/search.php?keywords="+d+"&page="+str(l))
			match = re.compile('href=\"(https:\/\/www.redecanais[^\"]+).+?src=\"([^\"]+)\".alt=\"([^\"]+)\" wi').findall(link)
			if match:
				for url2,img2,name2 in match:
					if re.compile('\d+p').findall(name2):
						AddDir(name2 ,url2, 95, img2, img2)
					elif "Lista" in name2:
						AddDir(name2 ,url2, 135, img2, img2)
			else:
				break
	except urllib2.URLError, e:
		AddDir("Nada encontrado" , "", 0, "", "", 0)
	try:
		AddDir("[COLOR yellow][B][NetCine.us][/B][/COLOR]", "" , 0 ,"", isFolder=False)
		link = urllib2.urlopen(URLNC+"listBusca.php?b="+d).read().replace('\n','').replace('\r','')
		match = re.compile('url="(.+?)".+?mg="(.+?)".+?ame="(.+?)".+?ode="(.+?)"').findall(link)
		for url2,img2,name2,mode2 in match:
			AddDir(name2 ,url2, int(mode2), img2, img2)
	except urllib2.URLError, e:
		AddDir("Nada encontrado" , "", 0, "", "", 0)
# ----------------- FIM BUSCA
# ----------------- TV Cubeplay
def TVCB(): #102
	try:
		AddDir("[B][COLOR yellow]Carregar lista EPG (epg.com.br)[/COLOR][/B]", "", 105, "", "", isFolder=False)
		if(cEPG=="1"):
			epg = eval(EPG())
		link = urllib2.urlopen(URLP+"epg/iptv.php?adulto="+cadulto).read().replace('\n','').replace('\r','')
		m = re.compile('name="(.+?)".+?mg="(.+?)".+?pg="(.+?)"').findall(link)
		i=0
		for name2,img2,epg2 in m:
			try:
				info2=epg[epg2].replace(";;;","\n")
				if not epg2=="none" and cEPG=="1":
					name2 = "[COLOR yellow]"+name2+"[/COLOR]"
			except:
				info2=""
			AddDir(name2, str(i), 103, img2, img2, isFolder=False, IsPlayable=True, info = info2)
			i+=1
	except urllib2.URLError, e:
		AddDir("Servidor offline, tente novamente em alguns minutos" , "", 0, "", "", 0)
	Addon.setSetting("cEPG", "0")
def PlayTVCB(): #103
	try:
		link = urllib2.urlopen(URLP+"epg/iptv.php?c="+url).read().replace('\n','').replace('\r','')
		PlayUrl(name, link, iconimage, info)
	except urllib2.URLError, e:
		xbmcgui.Dialog().ok('Cube Play', "Servidor offline, tente novamente em alguns minutos")
# ----------------- Fim TV Cubeplay
# ----------------- REDECANAIS TV
def Acento(x):
	x = x.replace("\xe7","ç").replace("\xe0","à").replace("\xe1","á").replace("\xe2","â").replace("\xe3","ã").replace("\xe8","è").replace("\xe9","é").replace("\xea","ê").replace("\xed","í").replace("\xf3","ó").replace("\xf4","ô").replace("\xf5","õ").replace("\xfa","ú")
	return x
def EPG():
	epg1 = "{"
	try:
		xbmc.executebuiltin("Notification({0}, {1}, 7000, {2})".format(AddonName, "Carregando lista EPG. Aguarde um momento!", icon))
		link = common.OpenURL("http://www.epg.com.br/~mysql41/vertv.php").replace('	','')
		m = re.compile('javascript:toggleCanal\(\d+,.([^\']+)\h*(?s)(.+?)\<\!-- orig').findall(link)
		for c,f in m:
			hora = ""
			m2 = re.compile('(.+)(\(\d+.\d+\))\s').findall(f)
			if m2:
				for prog1,prog2 in m2:
					hora += prog2 +" "+ prog1 + ";;;"
					try:
						hora= Acento(hora)
					except:
						hora = hora
			hora = hora.replace("'","")
			epg1 += "'"+c+"' : '"+hora+"' , "
		return epg1+"'none':''}"
	except urllib2.URLError, e:
		return ""
		xbmc.executebuiltin("Notification({0}, {1}, 7000, {2})".format(AddonName, "Erro. tente novamente!", icon))
def TVRC(): #100
	AddDir("[B][COLOR yellow]Carregar lista EPG (epg.com.br)[/COLOR][/B]", "", 105, "", "", isFolder=False)
	if(cEPG=="1"):
		epg = eval(EPG())
	link = urllib2.urlopen("https://pastebin.com/raw/QaYHY3Nf").read().replace('\n','').replace('\r','')
	match = re.compile('url="(.+?)".+?mg="(.+?)".+?ame="(.+?)".+?pg="(.+?)"').findall(link)
	for url2,img2,name2,epg2 in match:
		try:
			info2=epg[epg2].replace(";;;","\n")
			if not epg2=="none" and cEPG=="1":
				name2 = "[COLOR yellow]"+name2+"[/COLOR]"
		except:
			info2=""
		if cadulto=="8080":
			AddDir(name2, url2, 101, img2, img2, isFolder=False, IsPlayable=True, info = info2)
		elif not "dulto" in name2:
			AddDir(name2, url2, 101, img2, img2, isFolder=False, IsPlayable=True, info = info2)
	Addon.setSetting("cEPG", "0")
def PlayTVRC(): # 101
	url2 = re.sub('(\.link|\.com|\.net)', ".info", url.replace("https","http") )
	try:
		link = common.OpenURL(url2)
		player = re.compile('<iframe name=\"Player\".+src=\"([^\"]+)\"').findall(link)
		link2 = common.OpenURL(player[0])
		urlp = re.compile('(http[^\"]+m3u[^\"]+)').findall(link2)
		if urlp:
			PlayUrl(name, urlp[0] + "?play|Referer=http://www.redecanais.com/", iconimage, info)
		else:
			xbmcgui.Dialog().ok('Cube Play', "Erro, aguarde atualização")
	except urllib2.URLError, e:
		xbmcgui.Dialog().ok('Cube Play', 'Erro, tente novamente em alguns minutos')
# ----------------- FIM REDECANAIS TV
# ----------------- Inicio Filmes Online
def GenerosFO(): #85
	d = xbmcgui.Dialog().select("Escolha o Genero", Clistafo1)
	if d != -1:
		global Cat
		Addon.setSetting("Catfo", str(d) )
		Cat = d
		Addon.setSetting("cPagefo1", "0" )
		xbmc.executebuiltin("XBMC.Container.Refresh()")
		
def MoviesFO(urlfo,pagina2): #170
	AddDir("[COLOR yellow][B][Gênero dos Filmes]:[/B] " + Clistafo1[int(Catfo)] +"[/COLOR]", "url" ,85 ,"https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", "https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", isFolder=False)
	try:
		pagina=eval(pagina2)
		l= int(pagina)*5
		p= 1
		if int(pagina) > 0:
			AddDir("[COLOR blue][B]<< Pagina Anterior ["+ str( int(pagina) ) +"[/B]][/COLOR]", pagina , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False, background=pagina2)
		for x in range(0, 5):
			l +=1
			ordem = "desc" if cOrdFO=="1" else "asc"
			link = common.OpenURL("https://filmesonline.online/index.php?do=search&subaction=search&search_start="+str(l)+"&story="+urlfo+"&sortby="+cOrdFO+"&resorder="+ordem+"&catlist[]="+Clistafo0[int(Catfo)]).replace("\r","").replace("\n","")
			link = re.sub('Novos Filmes.+', '', link)
			m = re.compile('src=\"(.upload[^\"]+).+?alt=\"([^\"]+).+?href=\"([^\"]+)').findall(link)
			m2 = re.compile('numb-serial..(.+?)\<.+?afd..(\d+)').findall(link)
			i=0
			if m:
				#xbmcgui.Dialog().ok('Cube Play', str(m))
				for img2,name2,url2 in m:
					AddDir(name2 + " ("+m2[i][0]+") - " + m2[i][1], url2, 171, "https://filmesonline.online/"+img2, "https://filmesonline.online/"+img2, info="")
					p+=1
					i+=1
		if p >= 80:
			AddDir("[COLOR blue][B]Proxima Pagina >> ["+ str( int(pagina) + 2) +"[/B]][/COLOR]", pagina , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False, background=pagina2)
	except urllib2.URLError, e:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "")
		
def PlayMFO1(): #172
	global background
	if re.compile('\d+').findall(str ( background )) :
		s = background.split(",")
		sel = xbmcgui.Dialog().select("Selecione a resolução", s)
		if sel!=-1:
			link = common.OpenURL( url+"?q="+s[sel] )
			m = re.compile('https[^\"]+\.mp4').findall(link)
			background = "None"
			PlayUrl(name, m[0],"",info)
	else:
		link = common.OpenURL(url)
		m = re.compile('https[^\"]+\.mp4').findall(link)
		background = "None"
		PlayUrl(name, m[0],"",info)
		
def GetMFO1(): #171
	try:
		link = common.OpenURL( url )
		m = re.compile('href\=\"(.+?\#Rapid)').findall(link)
		t = re.compile('class=\"titleblock\"\>\s\<h1\>([^\<]+)').findall(link)
		i = re.compile('class=\"p-info-text\"\>\s\<span\>([^\<]+)').findall(link)
		if m:
			link2 = common.OpenURL( "https://filmesonline.online"+m[0] )
			m2 = re.compile('iframe.+?src\=\"([^\"]+)').findall(link2)
			if m2:
				title = t[0] if t else name
				info = i[0] if i else ""
				link3 = common.OpenURL( "https:"+m2[0] )
				m3 = re.compile('https[^\"]+\.mp4').findall(link3)
				if m3:
					pp = re.compile('q=(\d+p)').findall(link3)
					pp = list(reversed(pp))
					AddDir( title , "https:"+m2[0], 172, iconimage, iconimage, isFolder=False, IsPlayable=True, info=info, background= ",".join(pp))
					AddDir( "Resoluções: "+", ".join(pp), "https:"+m2[0], 0, iconimage, iconimage, isFolder=False, info="Clique no título do filme para dar play")
				else:
					AddDir( "Video offline!!" ,"", 0, "", "", isFolder=False)
	except urllib2.URLError, e:
		AddDir( "Video offline" ,"", 0, "", "", isFolder=False)
# ----------------- FIM Filmes Online
# ----------------- Inicio MM filmes
def GenerosMM(): #189
	d = xbmcgui.Dialog().select("Escolha o Genero", ClistaMM1)
	if d != -1:
		global Cat
		Addon.setSetting("CatMM", str(d) )
		Cat = d
		Addon.setSetting("cPageMMf", "0" )
		xbmc.executebuiltin("XBMC.Container.Refresh()")
def ListFilmeMM(pagina2): #180
	AddDir("[COLOR yellow][B][Gênero dos Filmes]:[/B] " + ClistaMM1[int(CatMM)] +"[/COLOR]", "url" ,189 ,"https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", "https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", isFolder=False)
	pagina=eval(pagina2)
	l= int(pagina)*5
	p=1
	i=0
	if int(pagina) > 0:
		AddDir("[COLOR blue][B]<< Pagina Anterior ["+ str( int(pagina) ) +"[/B]][/COLOR]", pagina , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False, background=pagina2)
	try:
		links = common.OpenURL("http://www.mmfilmes.tv/series/")
		ms = re.compile('href\=\"(.+?www.mmfilmes.tv.+?)\" rel\=\"bookmark\"').findall(links)
		for x in range(0, 5):
			l+=1
			link = common.OpenURL("http://www.mmfilmes.tv/category/"+ ClistaMM0[int(CatMM)] +"/page/"+str(l)+"/")
			m = re.compile('id\=\"post\-\d+\".+?\=.([^\"]+)\h*(?s)(.+?)(http[^\"]+)').findall(link)
			res = re.compile('audioy..([^\<]*)').findall(link)
			jpg = re.compile('src=\"(http.+?www.mmfilmes.tv\/wp-content\/uploads[^\"]+)').findall(link)
			dubleg = re.compile('boxxer.+\s.+boxxer..([^\<]*)').findall(link)
			if m:
				for name2,b,url2 in m:
					name2 = name2.replace("&#8211;","-").replace("&#038;","&").replace("&#8217;","\'")
					if not url2 in ms:
						AddDir(name2+ " [COLOR yellow]"+res[i]+"[/COLOR] [COLOR blue]"+dubleg[i]+"[/COLOR]", url2, 181, jpg[i], jpg[i],isFolder=True,IsPlayable=False,background=name2)
					i+=1
					p+=1
			i=0
			if p >= 50:
				AddDir("[COLOR blue][B]Proxima Pagina >> ["+ str( int(pagina) + 2) +"[/B]][/COLOR]", pagina , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False, background=pagina2)
	except:
		pass
def OpenLinkMM(): #181
	link = common.OpenURL(url)
	m = re.compile('boxp\(.([^\']+)').findall(link)
	info2 = re.compile('mCSB_container..\s(\h*(?s)(.+?))\<\/div').findall(link)
	if info2:
		info2=info2[0][0].replace("\t","")
	else:
		info2=""
	if m:
		link2 = common.OpenURL(m[0],headers={'referer': "http://www.mmfilmes.tv/"})
		m2 = re.compile('opb\(.([^\']+).+?.{3}.+?[^\\>]+.([^\<]+)').findall(link2)
		if m2:
			for link,dubleg in m2:
				AddDir( background +" [COLOR blue]("+dubleg+")[/COLOR]" ,link, 182, iconimage, iconimage, isFolder=False, IsPlayable=True, info=info2)
def PlayLinkMM(): #182
	#xbmcgui.Dialog().ok(background, url + " " +background)
	link = common.OpenURL(url,headers={'referer': "http://www.mmfilmes.tv/"})
	m = re.compile('addiframe\(\'([^\']+)').findall(link)
	if m:
		link2 = common.OpenURL(m[0],headers={'referer': "http://www.mmfilmes.tv/"}).replace("file","\nfile")
		m2 = re.compile('file.+?(h[^\']+).+?(\d+p)\'').findall(link2)
		legenda = re.compile('(http[^\']+\.(vtt|srt|sub|ssa|txt|ass))').findall(link2)
		listar=[]
		listal=[]
		for link,res in m2:
			listal.append(link)
			listar.append(res)
		if len(listal) <1:
			xbmcgui.Dialog().ok('Cube Play', 'Erro, video não encontrado')
			sys.exit(int(sys.argv[1]))
		d = xbmcgui.Dialog().select("Selecione a resolução", listar)
		if d!= -1:
			#PlayUrl(listal[d], listal[d], iconimage, "")
			if legenda:
				PlayUrl(name, listal[d], iconimage, info, sub=legenda[0][0])
			else:
				PlayUrl(name, listal[d], iconimage, info)
# ----------------- Fim MM filmes
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
			
def PlayUrl(name, url, iconimage=None, info='', sub=''):
	#xbmcgui.Dialog().ok(background, url + " " +background)
	if background != "None":
		b = background.split(";;;")
		if "redecanais" in background:
			AddFavorites(b[0], iconimage, b[1], "95", "historic.txt")
		else:
			AddFavorites(b[0], iconimage, b[1], "79", "historic.txt")
	url = common.getFinalUrl(url)
	xbmc.log('--- Playing "{0}". {1}'.format(name, url), 2)
	listitem = xbmcgui.ListItem(path=url)
	listitem.setInfo(type="Video", infoLabels={"mediatype": "video", "Title": name, "Plot": info })
	if sub!='':
		listitem.setSubtitles(['special://temp/example.srt', sub ])
	if iconimage is not None:
		try:
			listitem.setArt({'thumb' : iconimage})
		except:
			listitem.setThumbnailImage(iconimage)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

def AddDir(name, url, mode, iconimage='', logos='', index=-1, move=0, isFolder=True, IsPlayable=False, background=None, cacheMin='0', info=''):
	urlParams = {'name': name, 'url': url, 'mode': mode, 'iconimage': iconimage, 'logos': logos, 'cache': cacheMin, 'info': info, 'background': background}
	liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage )
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
	items = []
	if mode == 1 or mode == 2:
		items = []
	elif mode== 61 or info=="series nc":
		liz.addContextMenuItems(items = [("Add ao fav. do Cube Play", 'XBMC.RunPlugin({0}?url={1}&mode=31&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name)))])
	elif mode== 79:
		liz.addContextMenuItems(items = [("Add ao fav. do Cube Play", 'XBMC.RunPlugin({0}?url={1}&mode=72&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name)))])
	elif mode== 95:
		liz.addContextMenuItems(items = [("Add ao fav. do Cube Play", 'XBMC.RunPlugin({0}?url={1}&mode=93&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name)))])
	elif mode== 135:
		liz.addContextMenuItems(items = [("Add ao fav. do Cube Play", 'XBMC.RunPlugin({0}?url={1}&mode=131&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name)))])
	elif mode== 171:
		liz.addContextMenuItems(items = [("Add ao fav. do Cube Play", 'XBMC.RunPlugin({0}?url={1}&mode=175&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name)))])
	elif mode== 181:
		liz.addContextMenuItems(items = [("Add ao fav. do Cube Play", 'XBMC.RunPlugin({0}?url={1}&mode=185&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(name)))])
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

def CheckUpdate(msg): #200
	try:
		uversao = urllib2.urlopen( "https://raw.githubusercontent.com/RH1CK/CubePlay/master/version.txt?r="+str(random.random() *100) ).read().replace('\n','').replace('\r','')
		if uversao != Versao or not cadulto:
			Update()
			#xbmc.executebuiltin("XBMC.Container.Refresh()")
		elif msg==True:
			xbmcgui.Dialog().ok('Cube Play', "O addon ja esta na ultima versao: "+Versao+"\nAs atualizacoes normalmente sao automaticas\nUse esse recurso caso nao esteja recebendo automaticamente")
			xbmc.executebuiltin("XBMC.Container.Refresh()")
	except urllib2.URLError, e:
		if msg==True:
			xbmcgui.Dialog().ok('Cube Play', "Nao foi possivel checar")

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
	except urllib2.URLError, e:
		fonte = ""
	try:
		fonte = urllib2.urlopen( "https://raw.githubusercontent.com/RH1CK/CubePlay/master/resources/settings.xml" ).read().replace('\n','')
		prog = re.compile('</settings>').findall(fonte)
		if prog:
			py = os.path.join( Path, "resources/settings.xml")
			file = open(py, "w")
			file.write(fonte)
			file.close()
	except urllib2.URLError, e:
		fonte = ""
	xbmc.executebuiltin("Notification({0}, {1}, 9000, {2})".format(AddonName, "Atualizando o addon. Feche e abra para ver as alterações!", icon))
	xbmc.sleep(2000)

def study(x):
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

if mode == 0:
	Categories()
	setViewM()
	if cadulto!="update":
		CheckUpdate(False)	
elif mode == 3 or mode == 32:
	PlayUrl(name, url, iconimage, info)
elif mode == 30:
	ListFavorites('favorites.txt', "Favoritos")
	setViewS()
elif mode == 333:
	ListHistoric('historic.txt', "Historico")
	setViewM()
elif mode == 31: 
	AddFavorites(url, iconimage, name, "61", 'favorites.txt')
elif mode == 72: 
	AddFavorites(url, iconimage, name, "79", 'favorites.txt')
elif mode == 93: 
	AddFavorites(url, iconimage, name, "95", 'favorites.txt')
elif mode == 131: 
	AddFavorites(url, iconimage, name, "135", 'favorites.txt')
elif mode == 175: 
	AddFavorites(url, iconimage, name, "171", 'favorites.txt')
elif mode == 185: 
	AddFavorites(url, iconimage, name, "181", 'favorites.txt')
elif mode == 33:
	RemoveFromLists(index, favoritesFile)
elif mode == 34:
	AddNewFavorite()
elif mode == 38:
	MoveInList(index, move, favoritesFile)
elif mode == 39:
	dialog = xbmcgui.Dialog()
	ret = dialog.yesno('Cube Play', 'Deseja mesmo deletar todos os favoritos?')
	if ret:
		common.DelFile(favoritesFile)
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
elif mode == 102:
	TVCB()
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
	TemporadasRC()
	setViewS()
elif mode == 136:
	EpisodiosRC(background)
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
elif mode == 189:
	GenerosMM()
elif mode == 200:
	CheckUpdate(True)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
#checkintegrity25852