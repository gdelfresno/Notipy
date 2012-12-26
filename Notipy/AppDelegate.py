#-*- coding: utf-8 -*-
#
#  NotipyAppDelegate.py
#  Notipy
#
#  Created by Guillermo del Fresno Herena on 26/12/12.
#  Copyright lomoLomo 2012. All rights reserved.
#

from Foundation import *
from AppKit import *

class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, sender):
        NSLog("Application did finish launching.")
