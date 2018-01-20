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
import subprocess
#import LibAutoCompletion
#import YouTubeAutoCompletion
#import LibSearch
#import YouTubeSearch
#import FileSystemAutoCompletion

ADDON = xbmcaddon.Addon()
ADDON_VERSION = ADDON.getAddonInfo('version')
ADDON_ID       = ADDON.getAddonInfo('id')
ADDON_USER_DATA_FOLDER = xbmc.translatePath("special://profile/addon_data/"+ADDON_ID)
ADDON_STORAGE_FILE = ADDON_USER_DATA_FOLDER + os.sep + "store.json"
ACTION = "action"
ACTION_SHOW_DIR = "showdir"
ACTION_ADD_CUSTOM_VARIANT = "addcustomvariant"
ACTION_ADD_CUSTOM_ENTRY = "addcustomentry"
ACTION_ADD_TO_START = "addtostart"
ACTION_EXEC = "exec"
DIR = "dir"
STARTMENU_IGNORE = "dshjkfhsd"
STARTMENU_ENTRY = "start"
ALL_APPS_STRING = "All Apps"
REMOVE_START = "removeStart"
handle = -1
PLUGIN_ACTION = "Container.Update(plugin://plugin.program.applauncher?"


class AddCustomEntryDialog(xbmcgui.WindowDialog):
  def __init__(self, *args, **kwargs):
    self.entryPath = kwargs.get("entryPath")
    self.addControl(xbmcgui.ControlLabel(100, 250, 125, 75, self.entryPath))
  
  
def createContextMenuEntries(sideCalls, entryPath):
  result = []
  for sideCall in sideCalls:
    result.append((sideCall[AppListerLinux.NAME], "Notification(" + sideCall[AppListerLinux.EXEC] + ", "  + sideCall[AppListerLinux.EXEC] + ")"))
  result.append(("Add to start", PLUGIN_ACTION+ACTION+"="+ACTION_ADD_TO_START+"&"+DIR+"="+entryPath+")"))
  return result

def createEntries(folderToShow = ""):
  entries = AppListerLinux.getAppsWithIcons()
  items = []
  if folderToShow != "" and folderToShow != STARTMENU_IGNORE:
    for folder in folderToShow.split("/"):
      entries = entries[folder]
  for key in entries.keys():#sorted(entries, key=lambda k: k[AppListerLinux.NAME]):
    entry = entries[key]
    if entry[AppListerLinux.TYPE] == AppListerLinux.TYPE_APP:
      li = createAppEntry(entry, folderToShow+"/"+key)
      xbmcplugin.addDirectoryItem(handle, li.getPath(), li)
    elif entry[AppListerLinux.TYPE] == AppListerLinux.TYPE_FOLDER:
      li = createFolder(key,"plugin://plugin.program.applauncher?"+ACTION+"="+ACTION_SHOW_DIR+"&"+DIR+"="+folderToShow+"/"+key, folderToShow+"/"+key)
      xbmcplugin.addDirectoryItem(handle, li.getPath(), li, isFolder=True)
  xbmcplugin.endOfDirectory(handle, cacheToDisc=False)  

def createFolder(name, target, addToStartPath, isStart = False):
  li = xbmcgui.ListItem(name)
  li.setPath(path=target)
  #li.setIsFolder(True)
  if not isStart:
    contextMenuEntries = createContextMenuEntries([], addToStartPath)
  else:
    contextMenuEntries = createRemoveStartContextMenu(addToStartPath)
  if contextMenuEntries:
      li.addContextMenuItems(contextMenuEntries)
  return li

def createAppEntry(entry, addToStartPath, isStart = False):
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
  if not isStart:
    contextMenuEntries = createContextMenuEntries(entry[AppListerLinux.SIDECALLS], addToStartPath)
  else:
    contextMenuEntries =  createRemoveStartContextMenu(addToStartPath)
  if contextMenuEntries:
    li.addContextMenuItems(contextMenuEntries)
  li.setPath(path="plugin://plugin.program.applauncher?"+ACTION+"="+ACTION_EXEC+"&"+ACTION_EXEC+"="+entry[AppListerLinux.EXEC])
  return li
def addToStart(entry):
  if os.path.isfile(ADDON_STORAGE_FILE):
    with open(ADDON_STORAGE_FILE, 'r') as fp:
      data = json.load(fp)
  if not "data" in locals():
    data = {}
  if STARTMENU_ENTRY not in data:
    data[STARTMENU_ENTRY] = []
  if entry in data[STARTMENU_ENTRY]:
    data[STARTMENU_ENTRY].remove(entry)
  data[STARTMENU_ENTRY].append(entry)
  with open(ADDON_STORAGE_FILE, 'w') as fp:  
    json.dump(data, fp)

def addCustomEntry():
  pass
def addCustomVariant():
  pass
def storeEntries(typeOfEntry, entries):
  pass
def loadEntries(typeOfEntry):
  pass
def executeApp(command):
  killKodi = False
  minimize = False
  if killKodi:
    pass
  else:
    if minimize:
      xbmc.executebuiltin("Minimize")
    subprocess.call(command.strip().split(" "))
    

def addSortingMethods():
  xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_LABEL)

def findEntries(entries, searchItems):
  result = []
  for item in searchItems:
    entry = entries
    if item[0] == "/":
      item=item[1:]
    for key in item.split("/"):
      entry = entry[key]
    entry[REMOVE_START] = item
    result.append(entry)
  return result
  #for key in entries.keys():
  #  if key == AppListerLinux.TYPE:
  #    continue
  #  if key in searchItems:
  #    result.append(entries[key])
  #  elif entries[key][AppListerLinux.TYPE] == AppListerLinux.TYPE_FOLDER:
  #    result.expand(findEntries(entries[key], searchItems)
  #return result

def createRemoveStartContextMenu(path):
  return [(REMOVE_START, path)]

def createStartMenu(startItems):
  li = createFolder(ALL_APPS_STRING,"plugin://plugin.program.applauncher?"+ACTION+"="+ACTION_SHOW_DIR+"&"+DIR+"="+STARTMENU_IGNORE, STARTMENU_IGNORE, True)
  xbmcplugin.addDirectoryItem(handle, li.getPath(), li, isFolder=True)
  entries = AppListerLinux.getAppsWithIcons()
  entries = findEntries(entries, startItems)
  for entry in entries:
    if entry[AppListerLinux.TYPE] == AppListerLinux.TYPE_FOLDER:
      isFolder = True
      li = createFolder(entry, "target", entry[REMOVE_START], True)
    else:
      isFolder = False
      li = createAppEntry(entry, entry[REMOVE_START], True)
    xbmcplugin.addDirectoryItem(handle, li.getPath(), li, isFolder=isFolder)
  xbmcplugin.endOfDirectory(handle, cacheToDisc=False)
def loadStartMenuItems():
  if not os.path.isfile(ADDON_STORAGE_FILE):
    return None
  with open(ADDON_STORAGE_FILE, 'r') as fp:
    data = json.load(fp)
  if not data or STARTMENU_ENTRY not in data or not data[STARTMENU_ENTRY]:
    return None
  return data[STARTMENU_ENTRY]

def parseArgs():
  global handle
  handle = int(sys.argv[1])
  params = {}
  args = sys.argv[2][1:]
  if args:
    for argPair in args.split("&"):
      temp = argPair.split("=")
      params[temp[0]] = temp[1]
  return params
if (__name__ == "__main__"):
  params = parseArgs()
  print params
#  if handle == -1:
#    global handle
#    handle = params["handle"]
  if not os.path.exists(ADDON_USER_DATA_FOLDER):
    os.makedirs(ADDON_USER_DATA_FOLDER)
  if ACTION in params:
    action = params[ACTION]
    if action == ACTION_EXEC:
      executeApp(params[ACTION_EXEC])
    elif action == ACTION_ADD_TO_START:
      addToStart(params[DIR])      
      #AddCustomEntryDialog(entryPath = params[DIR]).doModal()
    elif action == ACTION_ADD_CUSTOM_ENTRY:
      pass
    elif action == ACTION_ADD_CUSTOM_VARIANT:
      pass
    elif action == ACTION_SHOW_DIR:
      createEntries(params[DIR])
      addSortingMethods()
  else:
    startItems = loadStartMenuItems()
    if startItems:
      createStartMenu(startItems)
    else:
      createEntries()
    addSortingMethods()
    xbmc.log('finished')

