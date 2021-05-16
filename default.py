# -*- coding: utf-8 -*-
import xbmc
import sys
import xbmcplugin 
import xbmcgui
import xbmcaddon
import os
import urllib.parse 
import json
import inputstreamhelper

from urllib.parse import urlparse, quote_plus, unquote
from urllib.request import urlopen, Request
import urllib.request, urllib.parse, urllib.error
import urllib.parse
import re

#AddonID = 'plugin.video.Cinput'
Addon = xbmcaddon.Addon('plugin.video.Cinput')

test = Addon.getSetting("cDownload")

def Categories(): #0
	AddDir("Play", "", 1, isFolder=False, IsPlayable=True)
	AddDir("Iniciar Download", "", 2, isFolder=False, IsPlayable=False)
	AddDir("Parar Download", "", 3, isFolder=False, IsPlayable=False)
	
def StartDownload(url="", ref=""):
	if Addon.getSetting("cDownload") == "True":
		d = xbmcgui.Dialog().yesno("", "Stop Downloading and start this one?")
		if d:
			Addon.setSetting("cDownload", "False")
			xbmc.sleep(6000)
			Addon.setSetting("cDownload", "True")
			Download(url, ref)
	else:
		Addon.setSetting("cDownload", "True")
		Download(url, ref)
	#Download("https://s1.movies.futbol/web-sources/download/475DC76CEA238433/275941/Chernobyl+-+Season+1%3a+miniseries+-+1%3a23%3a45+(Trailers.to).mp4", "http://trailers.to")
	
def StopDownload():
	d = xbmcgui.Dialog().yesno("", "Stop Downloading?")
	if d:
		Addon.setSetting("cDownload", "False")
	
def Download(url="", ref=""):
	if not url: return
	Path = xbmc.translatePath( xbmcaddon.Addon().getAddonInfo('path') )
	file = os.path.join( Path, "video.mp4")
	req = Request(url)
	if ref:
		req.add_header('referer', ref)
	req.add_header('Content-Type', 'video/mp4')
	req.add_header('Accept-Ranges', 'bytes')
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/248.65')
	#req.add_header('Content-Range', 'bytes 96242530-962425304/4')
	sizechunk = 10 * 1024 * 1024
	totalsize = 0
	#req.add_header('Range', 'bytes=1000000000-')
	req.add_header('Range', 'bytes=104857601-209715202')
	resp = urlopen(req)
	length = re.compile('ength\: ?(\d+)').findall(str(resp.headers))
	ST(resp.headers)
	#return
	#resp2 = urlopen(req)
	prog=0
	progress = xbmcgui.DialogProgressBG()
	progress.create('Loading... '+length[0])
	with open(file, 'ab+') as f:
		while Addon.getSetting("cDownload") == "True":
			progtotal = int( 100*totalsize/(int(length[0])) )
			progress.update(progtotal, "")
			prog+=1
			chunk = resp.read(sizechunk)
			if not chunk:
				Addon.setSetting("cDownload", "False")
				progress.close()
				break
			f.write(chunk)
			totalsize+=sizechunk
	progress.close()

def AddDir(name, url, mode, isFolder=True, IsPlayable=False):
	urlParams = {'name': name, 'url': url, 'mode': mode}
	liz = xbmcgui.ListItem(name)
	liz.setContentLookup(False)
	liz.setInfo(type="video", infoLabels={})
	if IsPlayable:
		liz.setProperty('IsPlayable', 'true')
	u = '{0}?{1}'.format(sys.argv[0], urllib.parse.urlencode(urlParams))
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)

def PlayUrl(name, url): #1
	#Download()
	#url = "https://s0.blogspotting.art/web-sources/9B17BA576A73C731/4059907/demon-slayer-kimetsu-no-yaiba-the-movie-mugen-train-2020|referer=https://trailers.to/"
	#url = "http://localhost:8080/mac/m3u.m3u8|referer=https://trailers.to/"
	UA = quote_plus("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/677.98")
	#url = "D:\\Kodi19.0\\portable_data\\addons\\plugin.video.Cinput\\video.mp4"
	url = "https://s0.blogspotting.art/web-sources/download/FF64E07E2C2DDC97/933789/file.mp4|referer=https://trailers.to/&User-Agent="+UA
	xbmc.log('--- Playing "{0}". {1}'.format(name, url), 2)
	listitem = xbmcgui.ListItem(path=url)
	listitem.setMimeType('video/mp2t')
	listitem.setProperty('mimetype', 'video/mp2t')
	listitem.setProperty('inputstream', 'inputstream.ffmpegdirect')
	listitem.setProperty('inputstream.ffmpegdirect.mime_type', 'video/mp2t')
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
#---------------------
def ST(x="", o="w"):
	if o == "1":
		o = "a+"
	if type(x) == type({}) or type(x) == type([]):
		y = json.dumps(x, indent=4, ensure_ascii=True)
	else:
		try:
			y = str(x)
		except:
			y = str(str(x).encode("utf-8"))
	Path = xbmc.translatePath( xbmcaddon.Addon().getAddonInfo('path') )
	py = os.path.join( Path, "study.txt")
	#file = open(py, "a+")
	file = open(py, o)
	file.write(y+"\n"+str(type(x)))
	file.close()
	
params = urllib.parse.parse_qs(sys.argv[2][1:]) 
name = params.get('name',[None])[0]
url = params.get('url',[None])[0]
mode = int(params.get('mode', '0')[0]) if params.get('mode') else 0

if mode == 0:
	Categories()
elif mode == 1:
	PlayUrl(name, url)
elif mode == 2:
	#StartDownload("https://s0.blogspotting.art/web-sources/download/A1767B4A56E1EF57/933789/file.mp4", "http://trailers.to")
	StartDownload("https://s0.blogspotting.art/web-sources/9FD853F9D67AABFF/933789/Tom+Clancy%27s+Without+Remorse+(2021)+(Trailers.to).mp4", "http://trailers.to")
	#StartDownload("http://cdn.netcine.biz/html/content/conteudolb4/walker/01leg/01-ALTO.mp4?token=htKgCi5A1dEGZFTUK1fHXQ&expires=1621223898&ip=189.5.231.128", "http://cdn.netcine.info")
elif mode == 3:
	StopDownload()


xbmcplugin.endOfDirectory(int(sys.argv[1]))