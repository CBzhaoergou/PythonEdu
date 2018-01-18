#!/usr/bin/env python3

# A simple demonstration of GUI Scripting

from appscript import *

texteditgui = app('System Events').processes['Sublime Text 2']

app('Sublime Text 2').activate()

mref = texteditgui.menu_bars[1].menus
mref['File'].menu_items['New File'].click()
mref['File'].menu_items['Save'].click()

# print(texteditgui.help("-o"))
print(texteditgui.help("-t browser"))
# print(texteditgui.help("-t click"))
src = texteditgui.browsers["Save"].quit()
print(src)

# mref['Window'].menu_items['Zoom'].click()

# Note: TextEdit's 'Zoom' menu item has a different name in OS X 10.4:
# mref['Window'].menu_items['Zoom Model'].click()

# Note: the System Events object model is slightly different in OS X 10.3,
# so 10.3 users should change the last three lines to:
# mref['File'].menu_bar_items['File'].menu_items['New'].click()
# mref['Edit'].menu_bar_items['Edit'].menu_items['Paste'].click()
# mref['Window'].menu_bar_items['Window'].menu_items['Zoom Window'].click()