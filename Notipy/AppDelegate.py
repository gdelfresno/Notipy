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
from threading import Timer

from libgreader import GoogleReader, ClientAuthMethod, ReaderUrl
from PyObjCTools import NibClassBuilder
class RepeatingTimer(object):
	def __init__(self,interval, function, *args, **kwargs):
		super(RepeatingTimer, self).__init__()
		self.args = args
		self.kwargs = kwargs
		self.function = function
		self.interval = interval
    
	def start(self):
		self.callback()
    
	def stop(self):
		self.interval = False
    
	def callback(self):
		if self.interval:
			self.function(*self.args, **self.kwargs)
			Timer(self.interval, self.callback, ).start()


class AppDelegate(NSObject):
    statusMenu = IBOutlet()
    
    prefWindow = IBOutlet()
    
    userText = IBOutlet()
    passText = IBOutlet()
    
    user = None
    password = None
    
    lastId = None
    growl = None
    
    def applicationDidFinishLaunching_(self, sender):
        appName = "Notipy" #bundle.localizedStringForKey_value_table_(kCFBundleNameKey,'Notipy',None)
        self.growl = gntp.notifier.GrowlNotifier(
                                                 applicationName = appName,
                                                 notifications = ["New Article","Configuration Missing"],
                                                 defaultNotifications = ["New Article"],
                                                 )
        try:
            self.growl.register()
        except:
            print "Error registering Growl"

        if (self.user is None or self.password is None):
            self.growl.notify(
                              noteType = "Configuration Missing",
                              title = "Configuration missing",
                              description = "Google Reader Account not configured",
                              sticky = False,
                              priority = 1,
                              )
            self.prefWindow.makeKeyAndOrderFront_(None)
        
        
        timer = RepeatingTimer(60.0*5,self.checkItems_,None)
        timer.start()
        NSLog("Application did finish launching.")
    
    def notifyNewItem(self,item):
        if item is None:
            return
        
        url = None
        if 'canonical' in item.data:
            url = item.data['canonical'][0]['href']
        elif 'alternate' in item.data:
            url = item.data['alternate'][0]['href']
                
        self.growl.notify(
            noteType = "New Article",
            title = item.origin['title'] + " published",
            description = item.title,
            sticky = False,
            priority = 1,
            callback = url
        )

        

    @IBAction
    def savePreferences_(self, sender):
        self.user = self.userText.stringValue()
        self.password = self.passText.stringValue()
                
        self.prefWindow.orderOut_(None)
    
    @IBAction
    def checkItems_(self, sender):

        NSLog("Checking items")
        if self.user is None or self.password is None:
            return
        
        #Retrieve all items
        ca = ClientAuthMethod(self.user,self.password)
        reader = GoogleReader(ca)
        reader.makeSpecialFeeds()
        specials = reader.getSpecialFeed(ReaderUrl.READING_LIST)
        specials.loadItems()
        
        if self.lastId is None:
            item = specials.items[0]

            self.lastId = item.id
            self.notifyNewItem(item)
        else:
            if len(specials.items) > 0:
                lastItem = specials.items[0].id
                for item in specials.items:
                    if item.id == self.lastId:
                        break
                    self.notifyNewItem(item)
                self.lastId = lastItem
        NSLog("Finished Checking items")

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
        
        
        
    
    
