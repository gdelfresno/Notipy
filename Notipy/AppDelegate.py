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
from objc import YES, NO, IBAction, IBOutlet

from PyObjCTools import NibClassBuilder

class AppDelegate(NSObject):
    statusMenu = IBOutlet()

    def applicationDidFinishLaunching_(self, sender):
        NSLog("Application did finish launching.")

    @IBAction
    def doSomething_(self, sender):
        NSLog("It's doing something.")
    
    def awakeFromNib(self):
        bundle = NSBundle.mainBundle()
        
        statusbar = NSStatusBar.systemStatusBar()
        # Create the statusbar item
        self.statusitem = statusbar.statusItemWithLength_(NSVariableStatusItemLength)
        # Load all images
        
        self.statusImage = NSImage.alloc().initWithContentsOfFile_(bundle.pathForResource_ofType_("icon","png"))
        
        # Set initial image
        self.statusitem.setImage_(self.statusImage)
        # Let it highlight upon clicking
        self.statusitem.setHighlightMode_(1)
        # Set a tooltip
        self.statusitem.setToolTip_('Sync Trigger')

        self.statusitem.setMenu_(self.statusMenu)
        print "awake"