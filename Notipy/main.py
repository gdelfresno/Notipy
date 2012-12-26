#-*- coding: utf-8 -*-
#
#  main.py
#  Notipy
#
#  Created by Guillermo del Fresno Herena on 26/12/12.
#  Copyright lomoLomo 2012. All rights reserved.
#

#import modules required by application
import objc
import Foundation
import AppKit

from PyObjCTools import AppHelper

# import modules containing classes required to start application and load MainMenu.nib
import AppDelegate

# pass control to AppKit
AppHelper.runEventLoop()
