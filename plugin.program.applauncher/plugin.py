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

if (__name__ == "__main__"):
  if sys.argv[2][1:]:
    print(xbmc.executebuiltin("System.Exec("+sys.argv[2][1:].split("=")[1]+")"))
  else:
    entries = AppListerLinux.getAppsWithIcons()
    handle = int(sys.argv[1])
    items = []
    for entry in sorted(entries, key=lambda k: k['name']):
      li = xbmcgui.ListItem(entry["name"])
      if "icon" in entry:
        icon = entry["icon"]
        if icon:
          li.setArt({'icon' : icon,
                     'thumb':icon,
                     'poster':icon,
                     'banner':icon,
                     'fanart':icon,
                     'clearart':icon,
                     'clearlogo':icon,
                     'landscape':icon})
      li.setPath(path="plugin://plugin.program.applauncher?exec="+entry["exec"])

      xbmcplugin.addDirectoryItem(handle, "plugin://plugin.program.applauncher/?exec="+entry["exec"], li)
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)  
xbmc.log('finished')

