#!/usr/bin/env python3

#描述:消息对话框简单封装
#创建人:cbZhaoErGou
#创建时间:2018.1.11

import hashlib
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Toplevel


#参数说明:
"""
   parent:父窗口(必要)
   title:标题名(可选)
   message:消息内容(可选)
    
"""

class Dialog(Toplevel):
    def __init__(self, parent, title = None,message = None):
        Toplevel.__init__(self, parent)
        self.transient(parent)
        if title:
            self.title(title)
        if message:
            self.message = message
        self.parent = parent
        self.result = None

        frameW = 300
        frameH = 100
        body = tk.Frame(self,width = frameW, height = frameH)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)
      
        self.buttonbox()
        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (parent.winfo_rootx()+ parent.winfo_width()*0.5 - frameW*0.5,
                                  parent.winfo_rooty()+ parent.winfo_height()*0.5 - frameH*0.9))
        self.initial_focus.focus_set()
        self.wait_window(self)
    #
    # construction hooks

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden
        tk.Label(master,text = self.message).grid(row = 0, column = 0)
        master.pack_propagate(0)
        master.grid_propagate(0)
        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons
        box = tk.Frame(self)
        w = tk.Button(box, text="确定", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack()

    #
    # standard button semantics
    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    # command hooks
    def validate(self):
        return 1 # override

    def apply(self):
        pass # override
    

 
    

   