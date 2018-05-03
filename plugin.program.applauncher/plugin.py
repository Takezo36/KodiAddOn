# -*- coding: utf8 -*-

# Copyright (C) 2018 - Benjamin Hebgen <mail>
# This program is Free Software see LICENSE file for details

import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import simplejson as json
import AppLister
import Constants
import subprocess
from distutils.util import strtobool
#import AddCustomDialog
#import LibAutoCompletion
#import YouTubeAutoCompletion
#import LibSearch
#import YouTubeSearch
#import FileSystemAutoCompletion

ADDON = xbmcaddon.Addon()
ADDON_VERSION = ADDON.getAddonInfo('version')
ADDON_ID       = ADDON.getAddonInfo('id')
ADDON_USER_DATA_FOLDER = xbmc.translatePath("special://profile/addon_data/"+ADDON_ID)
APP_LAUNCHER = xbmc.translatePath("special://home")+ "addons" + os.sep + ADDON_ID + os.sep + "resources" + os.sep + "lib" + os.sep + "AppLauncher.py"
ADDON_STORAGE_FILE = ADDON_USER_DATA_FOLDER + os.sep + "store.json"
ACTION = "action"
ACTION_SHOW_DIR = "showdir"
ACTION_ADD_CUSTOM_VARIANT = "addcustomvariant"
ACTION_ADD_CUSTOM_ENTRY = "addcustomentry"
ACTION_ADD_TO_START = "addtostart"
ACTION_REMOVE_FROM_START = "removetostart"
ACTION_REMOVE_FROM_CUSTOMS = "removefromcustoms"
ACTION_EXEC = "exec"
CUSTOM_ENTRIES = "custom"
DIR = "dir"
STARTMENU_IGNORE = "dshjkfhsd"
STARTMENU_ENTRY = "start"
handle = -1
PLUGIN_ACTION = "Container.Update(plugin://plugin.program.applauncher?"

CUSTOM_ENTRY_CONTEXT_STRING = "Create custom entry"
CUSTOM_VARIANT = "Create custom variant"
ADD_TO_START = "Add to start"
ALL_APPS_STRING = "All Apps"
REMOVE_START = "Remove from start"



def addSideCallEntries(contextMenu, sideCalls):
  for sideCall in sideCalls:
    contextMenu.append((sideCall[Constants.NAME], PLUGIN_ACTION+ACTION+"="+ACTION_EXEC+"&"+ACTION_EXEC+"="+sideCall[Constants.EXEC]+")"))
  return contextMenu

def addRemoveStartEntry(contextMenu, path):
  contextMenu.append((REMOVE_START, PLUGIN_ACTION+ACTION+"="+ACTION_REMOVE_FROM_START+"&"+DIR+"="+path+")"))
  return contextMenu
def addRemoveCustomEntry(contextMenu, name):
  contextMenu.append((REMOVE_START, PLUGIN_ACTION+ACTION+"="+ACTION_REMOVE_FROM_CUSTOMS+"&"+DIR+"="+name+")"))
  return contextMenu
def addAddToStartEntry(contextMenu, entryPath):
  contextMenu.append((ADD_TO_START, PLUGIN_ACTION+ACTION+"="+ACTION_ADD_TO_START+"&"+DIR+"="+entryPath+")"))
  return contextMenu
def createCustomVariantContextMenuEntry(entryPath):
  return (CUSTOM_VARIANT, PLUGIN_ACTION+ACTION+"="+ACTION_ADD_CUSTOM_VARIANT+"&"+DIR+"="+entryPath+")")


def createEntries(folderToShow = ""):
  entries = AppLister.getAppsWithIcons()
  items = []
  if folderToShow != "":
    isRoot = False
    #sucks do proper url decoding
    folderToShow = folderToShow.replace("%2f", "/")
    folderToShow = folderToShow.replace("%2F", "/")
    folderToShow = folderToShow.replace("%20", " ")
    for folder in folderToShow.split("/"):
      entries = entries[folder]
  else:
    isRoot = True
    startItems = loadData()
    createStartMenu(startItems,entries)
  if not strtobool(ADDON.getSetting("dontshowstart")):
    addStartEntries(entries)
  addAddCustomEntry(handle, folderToShow)
  xbmcplugin.endOfDirectory(handle, cacheToDisc=False)  
def addStartEntries(entries):
  for key in entries.keys():#sorted(entries, key=lambda k: k[Constants.NAME]):
    if key == Constants.TYPE:
      continue
    entry = entries[key]
    if entry[Constants.TYPE] == Constants.TYPE_APP:
      li = createAppEntry(entry, folderToShow+"/"+key, False, isRoot)
      xbmcplugin.addDirectoryItem(handle, li.getPath(), li)
    elif entry[Constants.TYPE] == Constants.TYPE_FOLDER:
      if not isRoot:
        folderLink = folderToShow + "/" + key
      else:
        folderLink = key
      li = createFolder(key,"plugin://plugin.program.applauncher?"+ACTION+"="+ACTION_SHOW_DIR+"&"+DIR+"="+folderLink, folderLink, False, isRoot)
      xbmcplugin.addDirectoryItem(handle, li.getPath(), li, isFolder=True)
  
def addAddCustomEntry(handle, path):
  li = xbmcgui.ListItem(CUSTOM_ENTRY_CONTEXT_STRING)
  li.setPath(path="plugin://plugin.program.applauncher?"+ACTION+"="+ACTION_ADD_CUSTOM_ENTRY+"&"+DIR+"="+path)
  xbmcplugin.addDirectoryItem(handle, li.getPath(), li)
def createFolder(name, target, addToStartPath, isStart, isRoot):
  #print target
  li = xbmcgui.ListItem(name)
  li.setPath(path=target)
  #li.setIsFolder(True)
  contextMenu = []
  addBaseContextMenu(contextMenu, addToStartPath, None, isStart, isRoot)
  if contextMenu:
      li.addContextMenuItems(contextMenu)
  return li

def addBaseContextMenu(contextMenu, addToStartPath, name, isCustom = False):
  if isCustom:
    addRemoveCustomEntry(contextMenu, addToStartPath)

def createAppEntry(entry, addToStartPath, isCustom = False):
  li = xbmcgui.ListItem(entry[Constants.NAME])
  print entry[Constants.EXEC]
  if "icon" in entry:
    icon = entry[Constants.ICON]
    if icon:
      li.setArt({'icon' : icon,
                 'thumb':icon,
                 'poster':icon,
                 'banner':icon,
                 'fanart':icon,
                 'clearart':icon,
                 'clearlogo':icon,
                 'landscape':icon})
  contextMenu = []
  if Constants.SIDECALLS in entry.keys():
    addSideCallEntries(contextMenu, entry[Constants.SIDECALLS])
  addBaseContextMenu(contextMenu, addToStartPath, entry[Constants.NAME], isCustom)
  if not isCustom:
    contextMenu.append(createCustomVariantContextMenuEntry(addToStartPath))
  if contextMenu:
    li.addContextMenuItems(contextMenu)
  li.setPath(path="plugin://plugin.program.applauncher?"+ACTION+"="+ACTION_EXEC+"&"+ACTION_EXEC+"="+entry[Constants.EXEC])
  return li
def addToStart(path):
  entry = AppLister.getAppsWithIcons()
  for key in path.split("/"):
    entry = entry[key]
  storeEntry(entry[Constants.EXEC], entry[Constants.ICON], entry[Constants.NAME])

def addCustomEntry(exe="/", icon="/", name=""):
  dialog = xbmcgui.Dialog()
  fileName = dialog.browseSingle(1, 'Select Execution File', 'files', '', False, False, exe)
  if fileName == "":
    return
  params = dialog.input("Add parameters")
  icon = dialog.browseSingle(1, 'Select Icon', 'files', '', False, False, icon)
  if icon == "":
    return
  name = dialog.input("Set name", name)
  if name == "":
    return
  storeEntry(fileName + " " + params, icon, name)

def storeEntry(exe="/", icon="/", name="", path="/"):
  entry = {}
  entry[Constants.NAME] = name
  entry[Constants.EXEC] = exe
  entry[Constants.ICON] = icon
  entry[Constants.TYPE] = Constants.TYPE_APP
  entry[REMOVE_START] = path+name
  data = loadData()
  storepoint = data[CUSTOM_ENTRIES]
  for key in path.split("/"):
    if key in storepoint.keys() and storepoint[key][Constants.TYPE] == Constants.TYPE_FOLDER:
      storepoint = storepoint[key]
    else:
      storepoint[key] = {}
      storepoint[key].[Constants.TYPE] == Constants.TYPE_FOLDER
      storepoint[key].[Constants.NAME] == key
      storepoint = storepoint[key]
  storepoint[name] = entry
  writeData(data)

def addCustomVariant(path):
  entry = AppLister.getAppsWithIcons()
  for key in path.split("/"):
    entry = entry[key]
  addCustomEntry(entry[Constants.EXEC], entry[Constants.ICON], entry[Constants.NAME])

def executeApp(command):
  killKodi = strtobool(ADDON.getSetting("killkodi"))
  minimize = strtobool(ADDON.getSetting("minimize"))  
  if killKodi:
    kodiExe = xbmc.translatePath("special://xbmc") + "kodi"
    subprocess.Popen((sys.executable + " " + APP_LAUNCHER + " " + command + " " + kodiExe).split(" "))
    xbmc.executebuiltin("Quit")
  else:
    if minimize:
      xbmc.executebuiltin("Minimize")
    print command
    subprocess.call(command.strip().split(" "))
    

def addSortingMethods():
  xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_LABEL)

def createStartMenu(startItems, entries):
  if CUSTOM_ENTRIES in startItems and startItems[CUSTOM_ENTRIES]:
    for key in startItems[CUSTOM_ENTRIES].keys():
      entry = startItems[CUSTOM_ENTRIES][key]
      if entry[Constants.TYPE] == Constants.TYPE_FOLDER:
        isFolder = True
        li = createFolder(entry, "target", entry[REMOVE_START], True, False)
      else:
        isFolder = False
        li = createAppEntry(entry, entry[REMOVE_START], True, False)
      xbmcplugin.addDirectoryItem(handle, li.getPath(), li, isFolder=isFolder)
  
  
def loadStartMenuItems():
  if not os.path.isfile(ADDON_STORAGE_FILE):
    return None
  with open(ADDON_STORAGE_FILE, 'r') as fp:
    data = json.load(fp)
  return data

def writeData(data):
  with open(ADDON_STORAGE_FILE, 'w') as fp:  
    json.dump(data, fp)

def loadData():
  if os.path.isfile(ADDON_STORAGE_FILE):
    with open(ADDON_STORAGE_FILE, 'r') as fp:
      data = json.load(fp)
  if not "data" in locals():
    data = {}
  if CUSTOM_ENTRIES not in data:
    data[CUSTOM_ENTRIES] = {}
  return data

def removeFromCustoms(path):
  data = loadData()
  deleteName = path.split("/")[:-1]
  entries = data[CUSTOM_ENTRIES]
  for key in path.split("/"):
    if key == deleteName:
      entries.pop(key, None)
    else:
      entries = entries[key]
  writeData(data)

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
  print xbmc.translatePath("special://xbmc")
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
      addCustomEntry()
    elif action == ACTION_ADD_CUSTOM_VARIANT:
      addCustomVariant(params[DIR])
    elif action == ACTION_REMOVE_FROM_START:
      removeFromStart(params[DIR])
    elif action == ACTION_REMOVE_FROM_CUSTOMS:
      removeFromCustoms(params[DIR])
    elif action == ACTION_SHOW_DIR:
      createEntries(params[DIR])
      addSortingMethods()
  else:
    createEntries()
    addSortingMethods()
    xbmc.log('finished')

