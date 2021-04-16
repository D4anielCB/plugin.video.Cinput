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

def Categories(): #0
	AddDir("Play", "", 1, isFolder=False, IsPlayable=True)

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
	url = "https://lh3.googleusercontent.com/proxy/p2mr6yBl2Bn1S-yr0-eONst-nYtOUadBbNVO-t5Nh_GL5qZOYF9sVVZfWZO1UaMxjUGd5r3qwqSb3iLN9HNS6IH4WB9yp5vwD34034cBMIlKJq67oQ=s0"
	xbmc.log('--- Playing "{0}". {1}'.format(name, url), 2)
	listitem = xbmcgui.ListItem(path=url)
	listitem.setMimeType('video/mp2t')
	listitem.setProperty('mimetype', 'video/mp2t')
	listitem.setProperty('inputstream', 'inputstream.ffmpegdirect')
	listitem.setProperty('inputstream.ffmpegdirect.mime_type', 'video/mp2t')
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
	
params = urllib.parse.parse_qs(sys.argv[2][1:]) 
name = params.get('name',[None])[0]
url = params.get('url',[None])[0]
mode = int(params.get('mode', '0')[0]) if params.get('mode') else 0

if mode == 0:
	Categories()
elif mode == 1:
	PlayUrl(name, url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))