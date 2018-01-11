#!/usr/bin/env python3

# A simple demonstration of GUI Scripting

import appscript
from appscript import *

# texteditgui = app('System Events').processes['Xcode']

# app('Xcode').activate()
# # mref = texteditgui.menu_bars[1].menus
# # # mref['Help'].menu_items['Xcode Help'].click()
# # mref['New'].menu_items['File'].click()
# # # mref['File'].menu_items['Save'].click()

# # print(texteditgui.schemes.get())
# print(texteditgui.help("-o"))


str1 = "Xcode"
ituns = appscript.app(str1)
ituns.open("/Users/moqikaka_zb/Documents/Projects/NewFreshMan/Client/Client/frameworks/runtime-src/proj.ios_mac/NewXiaoHua.xcodeproj")
ituns.activate()
print(ituns.help("-h"))
print(ituns.help("-o"))
print(ituns.help("-t run_"))
# print(ituns.help("-t scheme"))
# print(ituns.help("-t workspace_document"))
# print(ituns.workspace_documents['NewXiaoHua.xcodeproj'].run_destinations.get())
# ituns.workspace_documents['NewXiaoHua.xcodeproj'].run_()


