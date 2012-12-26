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
import gntp.notifier

from libgreader import GoogleReader, ClientAuthMethod
from PyObjCTools import NibClassBuilder

class AppDelegate(NSObject):
    statusMenu = IBOutlet()
    
    prefWindow = IBOutlet()
    
    userText = IBOutlet()
    passText = IBOutlet()
    
    user = None
    password = None
    
    def applicationDidFinishLaunching_(self, sender):
        NSLog("Application did finish launching.")

    def testReader(self,readerUser, readerPassword):
        
        ca = ClientAuthMethod(readerUser,readerPassword)
        reader = GoogleReader(ca)
        if reader.buildSubscriptionList():
            NSLog("Google Reader connect ok")
        else:
            NSLog("Error retrieving subscriptions from Google Reader")
            return False
        
        NSLog("Getting Google Reader categories")
        categories = reader.getCategories()
        NSLog("%d categories",len(categories))
        for category in categories:
            NSLog(category.label)

    @IBAction
    def savePreferences_(self, sender):
        self.user = self.userText.stringValue()
        self.password = self.passText.stringValue()
                
        self.prefWindow.orderOut_(None)
    
    @IBAction
    def checkItems_(self, sender):
        gntp.notifier.mini("Checking items")

        self.testReader(self.user,self.password)
                        


    def awakeFromNib(self):
        bundle = NSBundle.mainBundle()
        
        statusbar = NSStatusBar.systemStatusBar()
        # Create the statusbar item
        self.statusitem = statusbar.statusItemWithLength_(NSVariableStatusItemLength)
        # Load all images
        
        self.statusImage = NSImage.alloc().initWithContentsOfFile_(bundle.pathForResource_ofType_("gricon","png"))
        
        # Set initial image
        self.statusitem.setImage_(self.statusImage)
        # Let it highlight upon clicking
        self.statusitem.setHighlightMode_(1)
        # Set a tooltip
        self.statusitem.setToolTip_('Google Reader Notifier')

        self.statusitem.setMenu_(self.statusMenu)
        
        
        if (self.user is None or self.password is None):
            self.prefWindow.makeKeyAndOrderFront_(None)
        
        print "awake"