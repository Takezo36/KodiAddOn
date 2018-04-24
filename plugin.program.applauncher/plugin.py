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
import AppLister
import Constants
import subprocess
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
APP_LAUNCHER = xbmc.translatePath("special://home")+ os.sep + "addons" + os.sep + ADDON_ID + os.sep + "resources" + os.sep + "lib" + os.sep + "AppLauncher.py"
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
  if isRoot:
    addAddCustomEntry(handle)
  xbmcplugin.endOfDirectory(handle, cacheToDisc=False)  

def addAddCustomEntry(handle):
  li = xbmcgui.ListItem(CUSTOM_ENTRY_CONTEXT_STRING)
  li.setPath(path="plugin://plugin.program.applauncher?"+ACTION+"="+ACTION_ADD_CUSTOM_ENTRY)
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

def addBaseContextMenu(contextMenu, addToStartPath, name, isStart, isRoot, isCustom = False):
  if not isStart and not isRoot:
    addAddToStartEntry(contextMenu, addToStartPath)
  if isStart:
    addRemoveStartEntry(contextMenu, addToStartPath)
  if isCustom:
    addRemoveCustomEntry(contextMenu, name)

def createAppEntry(entry, addToStartPath, isStart, isRoot, isCustom = False):
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
  addSideCallEntries(contextMenu, entry[Constants.SIDECALLS])
  addBaseContextMenu(contextMenu, addToStartPath, entry[Constants.NAME], isStart, isRoot, isCustom)
  if not isStart and not isCustom:
    contextMenu.append(createCustomVariantContextMenuEntry(addToStartPath))
  if contextMenu:
    li.addContextMenuItems(contextMenu)
  li.setPath(path="plugin://plugin.program.applauncher?"+ACTION+"="+ACTION_EXEC+"&"+ACTION_EXEC+"="+entry[Constants.EXEC])
  return li
def addToStart(entry):
  data = loadData()
  data[STARTMENU_ENTRY].append(entry)
  writeData(data)

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
  entry = {}
  entry[Constants.NAME] = name
  entry[Constants.EXEC] = fileName + " " + params
  entry[Constants.ICON] = icon
  entry[Constants.TYPE] = Constants.TYPE_APP
  entry[Constants.SIDECALLS] = []
  data = loadData()
  data[CUSTOM_ENTRIES][name] = entry
  writeData(data)

def addCustomVariant(path):
  entry = AppLister.getAppsWithIcons()
  for key in path.split("/"):
    entry = entry[key]
  showCustomDialog(entry[Constants.EXEC], entry[Constants.ICON], entry[Constants.NAME])

def executeApp(command):
  killKodi = True
  minimize = False
  if killKodi:
    kodiExe = xbmc.translatePath("special://xbmc") + "kodi"
    subprocess.Popen((sys.executable + " " + APP_LAUNCHER + " " + command + " " + kodiExe).split(" "))
#    xbmc.executebuiltin("Quit")
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
  #  if key == Constants.TYPE:
  #    continue
  #  if key in searchItems:
  #    result.append(entries[key])
  #  elif entries[key][Constants.TYPE] == Constants.TYPE_FOLDER:
  #    result.expand(findEntries(entries[key], searchItems)
  #return result



def createStartMenu(startItems, entries):
  if STARTMENU_ENTRY in startItems and startItems[STARTMENU_ENTRY]:
    foundEntries = findEntries(entries, startItems[STARTMENU_ENTRY])
    for entry in foundEntries:
      if entry[Constants.TYPE] == Constants.TYPE_FOLDER:
        isFolder = True
        li = createFolder(entry, "target", entry[REMOVE_START], True, True)
      else:
        isFolder = False
        li = createAppEntry(entry, entry[REMOVE_START], True, True)
      xbmcplugin.addDirectoryItem(handle, li.getPath(), li, isFolder=isFolder)
  if CUSTOM_ENTRIES in startItems and startItems[CUSTOM_ENTRIES]:
    for key in startItems[CUSTOM_ENTRIES].keys():
      li = createAppEntry(startItems[CUSTOM_ENTRIES][key], "blaa", False, True, True)
      xbmcplugin.addDirectoryItem(handle, li.getPath(), li)

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
  if STARTMENU_ENTRY not in data:
    data[STARTMENU_ENTRY] = []
  if CUSTOM_ENTRIES not in data:
    data[CUSTOM_ENTRIES] = {}
  return data

def removeStartEntry(data, path):
  if path in data[STARTMENU_ENTRY]:
    data[STARTMENU_ENTRY].remove(path)
  
def removeFromStart(path):
  data = loadData()
  removeStartEntry(data, path)
  writeData(data)

def removeFromCustoms(name):
  data = loadData()
  data[CUSTOM_ENTRIES].pop(name, None)
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

