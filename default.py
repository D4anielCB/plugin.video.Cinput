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
	sizechunk = 10 * 1024 * 1024
	totalsize = 0
	resp = urlopen(req)
	length = re.compile('ength\: ?(\d+)').findall(str(resp.headers))
	prog=0
	progress = xbmcgui.DialogProgressBG()
	progress.create('Loading... '+length[0])
	with open(file, 'wb') as f:
		while Addon.getSetting("cDownload") == "True":
			progtotal = int( 100*totalsize/(int(length[0])) )
			progress.update(progtotal, "")
			prog+=1
			chunk = resp.read(sizechunk)
			if not chunk:
				Addon.setSetting("cDownload", "False")
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
	url = "D:\\Kodi19.0\\portable_data\\addons\\plugin.video.Cinput\\video.mp4"
	xbmc.log('--- Playing "{0}". {1}'.format(name, url), 2)
	listitem = xbmcgui.ListItem(path=url)
	#listitem.setMimeType('video/mp2t')
	#listitem.setProperty('mimetype', 'video/mp2t')
	#listitem.setProperty('inputstream', 'inputstream.ffmpegdirect')
	#listitem.setProperty('inputstream.ffmpegdirect.mime_type', 'video/mp2t')
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
	StartDownload("https://s0.blogspotting.art/web-sources/download/8D841518CB161818/933789/file.mp4", "http://trailers.to")
elif mode == 3:
	StopDownload()


xbmcplugin.endOfDirectory(int(sys.argv[1]))