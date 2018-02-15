# -*- coding: utf8 -*-

# Copyright (C) 2015 - Benjamin Hebgen
# This program is Free Software see LICENSE file for details

import xbmc
import xbmcaddon
import os
import Constants



ADDON = xbmcaddon.Addon()
ADDON_VERSION = ADDON.getAddonInfo('version')

 
def discoverIcon(dirName, icon):
  allowedIconType = [".jpg", ".png"]
  if os.path.isfile("/usr/share/pixmaps/"+icon+".png"):
    return "/usr/share/pixmaps/"+icon+".png"
  if os.path.isdir(dirName):
    themeList = os.listdir(dirName)
    #moving hicolor to front
    if "hicolor" in themeList:
      themeList.remove("hicolor")
      themeList.insert(0, "hicolor")
    for theme in themeList:
      if os.path.isdir(dirName+theme):
        for iconfolder in sorted(os.listdir(dirName+theme), reverse=True):
          if os.path.isfile(dirName+theme+os.sep+iconfolder+os.sep+"apps"+os.sep+icon+".png"):
            return dirName+theme+os.sep+iconfolder+os.sep+"apps"+os.sep+icon+".png"
          if os.path.isfile(dirName+theme+os.sep+iconfolder+os.sep+"actions"+os.sep+icon+".png"):
            return dirName+theme+os.sep+iconfolder+os.sep+"actions"+os.sep+icon+".png"
  return None
#this is fucking slow find better way to look up the icons  
#  if os.path.isfile(dirName) and dirName[-4:] in allowedIconType and icon in dirName:
   # return dirName
  #if os.path.isdir(dirName):
 #   for entry in sorted(os.listdir(dirName), reverse=True):
#      if os.path.isdir(dirName+entry):
     #   discovered = discoverIcon(dirName+entry+os.sep, icon)
    #  else:
   #     discovered = discoverIcon(dirName+entry, icon)
  #    if discovered is not None:
 #       return discovered
#  return None

def getBestIcon(icon):
  if os.path.isfile(icon):
    return icon
  return discoverIcon("/usr/share/icons/", icon)
  

def getAppsWithIcons(additionalDir=""):
  result = {}
  language = xbmc.getLanguage(xbmc.ISO_639_1)
  defaultDirs = ["/usr/share/applications/", "~/.local/share/applications/"]
  if additionalDir and additionalDir[-1:]!="/":
    additionalDir += "/"
  if additionalDir:
    defaultDirs.append(additionalDir)
  for appDir in defaultDirs:
    if os.path.isdir(appDir):
      for file in sorted(os.listdir(appDir)):
        if file.endswith(".desktop"):
          entry = {}
          desktopEntry = False
          sideCalls = []
          sideCall = {}
          entry[Constants.SIDECALLS] = sideCalls
          entry[Constants.TYPE] = Constants.TYPE_APP
          for line in open(appDir+os.sep+file):
            
            if line.startswith("[Desktop Entry"):
              #main entry entrance
              desktopEntry = True
            if line.startswith("[Desktop Action"):
              sideCall = {}
              desktopEntry = False
              sideCalls.append(sideCall)
            if line.startswith("Exec"):
              if desktopEntry:
                entry[Constants.EXEC]=line.split("=")[1][:-1]
                if "%" in entry[Constants.EXEC]:
                  entry[Constants.EXEC] = entry[Constants.EXEC][:entry[Constants.EXEC].find("%")]
              else:
                sideCall[Constants.EXEC]=line.split("=")[1][:-1]
                if "%" in sideCall[Constants.EXEC]:
                  sideCall[Constants.EXEC] = sideCall[Constants.EXEC][:sideCall[Constants.EXEC].find("%")]
            elif line.startswith("Name"):
              if desktopEntry:
                if Constants.NAME not in entry:
                  entry[Constants.NAME]=line.split("=")[1][:-1]
              else:
                if Constants.NAME not in sideCall:
                  sideCall[Constants.NAME]=line.split("=")[1][:-1]
            elif line.startswith("Name["+language+"]"):
              if desktopEntry:
                entry[Constants.NAME]=line.split("=")[1][:-1]
              else:
                sideCall[Constants.NAME]=line.split("=")[1][:-1]
            elif line.startswith("Icon"):
              if desktopEntry:
                entry[Constants.ICON]=line.split("=")[1][:-1]
              else:
                sideCall[Constants.ICON]=line.split("=")[1][:-1]
          if Constants.ICON in entry:
            entry[Constants.ICON]=getBestIcon(entry[Constants.ICON])
          if entry[Constants.SIDECALLS]:
            for sideCall in entry[Constants.SIDECALLS]:
              if Constants.ICON in sideCall:
                sideCall[Constants.ICON]=getBestIcon(sideCall[Constants.ICON])
          result[entry[Constants.NAME]] = entry
  return result

if (__name__ == "__main__"):
  xbmc.log("version %s started" % ADDON_VERSION)
  ADDON.openSettings()
  xbmc.log('finished')

