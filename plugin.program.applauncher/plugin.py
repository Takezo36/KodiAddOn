# -*- coding: utf8 -*-

# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details

import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import simplejson as json
import AppListerLinux
#import LibAutoCompletion
#import YouTubeAutoCompletion
#import LibSearch
#import YouTubeSearch
#import FileSystemAutoCompletion

ADDON = xbmcaddon.Addon()
ADDON_VERSION = ADDON.getAddonInfo('version')
ACTION = "action"
class AddCustomEntryDialog(xbmcgui.WindowDialog):
  
def createContextMenuEntries(sideCalls):
  result = []
  for sideCall in sideCalls:
    result.append((sideCall[AppListerLinux.NAME], "Notification(" + sideCall[AppListerLinux.EXEC] + ", "  + sideCall[AppListerLinux.EXEC] + ")"))
  result.append(("Add to start", "RunPlugin(plugin://plugin.program.applauncher?exec=addfav)"))
  return result

def createDirectories():
  entries = AppListerLinux.getAppsWithIcons()
  items = []
  for entry in sorted(entries, key=lambda k: k[AppListerLinux.NAME]):
    li = xbmcgui.ListItem(entry[AppListerLinux.NAME])
    if "icon" in entry:
      icon = entry[AppListerLinux.ICON]
      if icon:
        li.setArt({'icon' : icon,
                   'thumb':icon,
                   'poster':icon,
                   'banner':icon,
                   'fanart':icon,
                   'clearart':icon,
                   'clearlogo':icon,
                   'landscape':icon})
    contextMenuEntries = createContextMenuEntries(entry[AppListerLinux.SIDECALLS])
    if contextMenuEntries:
      li.addContextMenuItems(contextMenuEntries)
    li.setPath(path="plugin://plugin.program.applauncher?exec="+entry[AppListerLinux.EXEC])

    xbmcplugin.addDirectoryItem(handle, "plugin://plugin.program.applauncher/?exec="+entry[AppListerLinux.EXEC], li)
  xbmcplugin.endOfDirectory(handle, cacheToDisc=False)  

def addToStart(entry):
  pass
def addCustomEntry():
  dialog = 
def addCustomVariant():
  pass
def storeEntries(typeOfEntry, entries):

def loadEntries(typeOfEntry):
  

def parseArgs():
  handle = int(sys.argv[1])
  params = {}
  args = sys.argv[2][1:]
  if args:
    for argPair in args.split("&"):
      temp = argPair.split("=")
      param[temp[0]] = temp[1]
if (__name__ == "__main__"):
  parseArgs()
  if ACTION in params:
    action = params[ACTION]
    if action == "exec":
      executeApp(params[AppListerLinux.EXEC])
    elif action == "addtostart":
      
    elif action == "addcustomentry":
      
    elif action == "addcustomvariant":
       
  else:
    createDirectories()
    xbmc.log('finished')

