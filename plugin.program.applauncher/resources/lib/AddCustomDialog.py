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


class AddCustomEntryDialog(xbmcgui.WindowXML):
  def __init__(self, *args, **kwargs):
    xbmcgui.WindowXML(args, kwargs)
    self.addControl(xbmcgui.ControlLabel(100, 250, 125, 75, "test"))
  
  

