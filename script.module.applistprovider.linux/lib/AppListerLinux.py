# -*- coding: utf8 -*-

# Copyright (C) 2015 - Benjamin Hebgen
# This program is Free Software see LICENSE file for details

import xbmc
import xbmcaddon
import os


ADDON = xbmcaddon.Addon()
ADDON_VERSION = ADDON.getAddonInfo('version')
EXEC = "exec"
NAME = "name"
ICON = "icon"

 
def discoverIcon(dirName, icon):
  allowedIconType = [".jpg", ".png"]
  for theme in os.listdir(dirName):
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
  result = []
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
          for line in open(appDir+os.sep+file):
            if line.startswith("Exec"):
              entry[EXEC]=line.split("=")[1][:-1]
            elif line.startswith("Name") and NAME not in entry:
              entry[NAME]=line.split("=")[1][:-1]
            elif line.startswith("Name["+language+"]"):
              entry[NAME]=line.split("=")[1][:-1]
            elif line.startswith("Icon"):
              entry[ICON]=line.split("=")[1][:-1]
          if ICON in entry:
            entry[ICON]=getBestIcon(entry[ICON])
          result.append(entry)
  return result  

if (__name__ == "__main__"):
  xbmc.log("version %s started" % ADDON_VERSION)
  ADDON.openSettings()
  xbmc.log('finished')

