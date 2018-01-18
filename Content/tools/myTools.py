import os
import sys
import base64
import hashlib
import tkinter as tk
import tkinter.ttk as ttk
import subprocess 
import time
from tkinter import scrolledtext
import threading
import re
import sqlite3
import importlib
import queue
from tkinter.filedialog import askdirectory
from tkinter import messagebox
from tkinter import Toplevel
import math
import traceback


class ThreadExcept(threading.Thread):
    def __init__(self, **arvgs):
        super(ThreadExcept, self).__init__()
        self.func = arvgs['target']
        self.gui = arvgs['gui']
        self.exitcode = 0
        self.exception = None
        self.exc_traceback = ''
    def run(self):
        try:
            self.func()
        except Exception as e:
            self.exitcode = 1
            self.exception = e
            self.exc_traceback = ''.join(traceback.format_exception(*sys.exc_info()))
            self.gui.insertInfoToScr(self.gui.art_ui.scr,tk.END,self.exc_traceback,'red')
            print(self.exc_traceback)



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
    #
    # command hooks
    def validate(self):
        return 1 # override

    def apply(self):
        pass # override


#tkinter Ui部分
class TkinterGui():  
    def __init__(self,**arvg):
        self.tkRoot =  arvg['tkRoot']
        self.prams = arvg
        self.crateMianPage()
    
    def crateMianPage(self):
        # Tab Control introduced here --------------------------------------  
        tabControl = ttk.Notebook(self.tkRoot)   # Create Tab Control  
        self.tabControl = tabControl

        self.art_ui = ttk.Frame(tabControl)            # Create a tab   
        tabControl.add(self.art_ui, text='tools')      # Add the tab
        self.crateHandArtUi()
  
        self.git_ui = ttk.Frame(tabControl)            # Add a second tab  
        tabControl.add(self.git_ui, text='git')      # Make second tab visible 
        self.crateHandelDesionUi() 
  
        self.tab3 = ttk.Frame(tabControl)            # Add a third tab  
        tabControl.add(self.tab3, text='test')      # Make second tab visible  
        self.crateHandelProtobufUi()
        
        tabControl.pack(expand=1, fill="both")  # Pack to make visible 
        tabControl.bind('<<NotebookTabChanged>>',self.updateCurrentUi)
        
        # print(tabControl.keys())  #获取控件参数关键字
        # print(tabControl.config())#获取控件参数设置
    #刷新界面元素
    def refreshUiElemect(self):

        self.setScript_path()
        self.getBranchAllName()
    

    #保存当前操作类型
    def updateCurrentUi(self,event):
        tmpPath = self.prams['getScriptPath'](self.art_ui.mPName)
        if tmpPath !=None:
            self.art_ui.path.set(tmpPath)
        else:
            self.art_ui.path.set("") 
        #解决页面部分不刷新问题
        currentIndex = self.art_ui.scr.index('current')
        indexfloat = float(currentIndex) + math.floor(21/2) + 1
        self.art_ui.scr.see('1.end')
        self.art_ui.scr.see(tk.END)
        self.art_ui.scr.see(str.format('%f' % indexfloat))

        self.refreshUiElemect()
    
    #设置路径
    def setScript_path(self,*arvg):
        self.art_ui.mPName = self.art_ui.bookChosen.get()
        # self.art_ui.mType = self.tabControl.tab('current')['text']
        tmpPath = self.prams['getScriptPath'](self.art_ui.mPName)
        if tmpPath !=None:
            self.art_ui.path.set(tmpPath)
        else:
            self.art_ui.path.set("")
       

    #设置历史路径
    def crateHandArtUi(self):

        scrolW  = 109; scrolH  = 21  
        scr = scrolledtext.ScrolledText(self.art_ui, width=scrolW, height=scrolH, wrap=tk.WORD,bg = '#f2f2f2',state = 'disabled') 
        scr.grid(column=0, row=12,columnspan=10,rowspan=6,padx = 0,sticky=tk.W +tk.N)
        scr.grid_propagate(0)

        self.art_ui.scr = scr
        
        # #遍历子对象
        # for child in self.art_ui.scr.frame.children.values():
        #     if child.winfo_class() == 'Text':
        #         child.configure(state = 'disabled')
        #     print(child.winfo_class())
        
            
        tmpFrame = tk.Frame(self.art_ui, width=800, height=160,bg='#ffffe0')
        tmpFrame.grid(row=2, column=0,columnspan=10,sticky=tk.W)
       
        style = ttk.Style()
        style.map("C.TButton",
            foreground=[('pressed', 'black'), ('active', 'black')],
            background=[('pressed', '!disabled', 'blue'), ('active', 'blue')],
            width = [('pressed', 120), ('active', 120)],
            height = [('pressed', '!disabled', 50), ('active', 50)],
        )

        colored_btn = ttk.Button(self.art_ui,text="执行操作", style="C.TButton",command = lambda:self.prams['handleArtFunc']())
        colored_btn.grid(column=6, row=0)

        self.art_ui.path = tk.StringVar()
        tk.Label(self.art_ui,text = "脚本路径:",width = 6).grid(row = 1, column = 0,columnspan = 1,sticky = tk.W + tk.E)
        tk.Entry(self.art_ui, textvariable = self.art_ui.path,width = 65,state = 'readonly').grid(row = 1, column = 1,padx = 10,columnspan = 5)
        ttk.Button(self.art_ui, text = "路径选择",style="C.TButton",command = lambda :self.prams['selectPath']()).grid(row = 1, column = 6)

        def tmprefreshUiElemect(*args):
            self.refreshUiElemect()

        #项目选择
        tk.Label(self.art_ui,text = "项目名称:",width = 6).grid(row = 0, column = 0,columnspan = 1,sticky = tk.W + tk.E,)
        self.art_ui.book = tk.StringVar()  
        bookChosen = ttk.Combobox(self.art_ui, width=13, textvariable=self.art_ui.book)  
        bookChosen['values'] = ('校花1', '校花2','校花N')  
        bookChosen.grid(column=1, row=0,padx = 10,sticky = tk.W)
        bookChosen.current(0)  #设置初始显示值，值为元组['values']的下标
        self.art_ui.mPName = bookChosen.get()
        bookChosen.config(state='readonly')  #设为只读模式 
        bookChosen.bind('<<ComboboxSelected>>',tmprefreshUiElemect)
        self.art_ui.bookChosen = bookChosen            


        def setBranchName(*args):
            branchName = bookChosen1.get()
            self.insertInfoToScr(self.art_ui.scr,tk.END,branchName + '\n','green')
            
        #项目选择
        tk.Label(self.art_ui,text = "项目分支:",width = 6,anchor= tk.E).grid(row = 0, column = 2,columnspan = 1,sticky =tk.E)
        self.art_ui.book1 = tk.StringVar()  
        bookChosen1 = ttk.Combobox(self.art_ui, width=13, textvariable=self.art_ui.book1)
        bookChosen1['values'] = ()
        bookChosen1.grid(column=3, row=0,sticky = tk.W,padx = 5)
        bookChosen1.config(state='readonly')  #设为只读模式 
        bookChosen1.bind('<<ComboboxSelected>>',setBranchName)
        self.art_ui.bookChosen1 = bookChosen1

        
        def setHandleType(*args):
            branchName = bookChosen1.get()
            self.insertInfoToScr(self.art_ui.scr,tk.END,branchName + '\n','green')

         #项目选择
        tk.Label(self.art_ui,text = "工作类型:",width = 6,anchor= tk.E).grid(row = 0, column = 4,columnspan = 1,sticky =tk.E)
        self.art_ui.book2 = tk.StringVar()  
        bookChosen2 = ttk.Combobox(self.art_ui, width=13, textvariable=self.art_ui.book2)
        bookChosen2['values'] = ('导图','导表')
        bookChosen2.grid(column=5, row=0,sticky = tk.W,padx = 5)
        bookChosen2.config(state='readonly')  #设为只读模式 
        bookChosen2.current(0)
        bookChosen2.bind('<<ComboboxSelected>>',setHandleType)
        self.art_ui.bookChosen2 = bookChosen2

        self.refreshUiElemect()


    def getBranchAllName(self):
        #需要手动设置路径才可获取状态
        self.art_ui.mPName = self.art_ui.bookChosen.get()
        tmpPath = self.prams['getScriptPath'](self.art_ui.mPName)
        if tmpPath == None:
            self.art_ui.bookChosen1['values'] = ('',)
            self.art_ui.bookChosen1.current(0)
            return

        tempValues = self.prams['getAllBranchName'](tmpPath)
        if tempValues == None:
            self.art_ui.bookChosen1['values'] = ('',)
            self.art_ui.bookChosen1.current(0)
        else:
            a = tempValues.split('\n')
            tRe = re.compile(r"\s*\*\s*")
            for i in range(len(a)):
                match = tRe.match(a[i])
                if match:
                    index = i
                    a[i] = re.sub(tRe,' ',a[i],1)
                else:
                    a[i] = re.sub(' ','',a[i],1)

            self.art_ui.bookChosen1['values'] = a
            self.art_ui.bookChosen1.current(index)


    def insertInfoToScr(self,scrObj,pos,text,color = None):
        scrObj.configure(state='normal',foreground = 'black')
        scrObj.update_idletasks()
        if color!=None:
            scrObj.tag_add(color,pos)
            scrObj.tag_config(color,foreground = color)
            scrObj.insert(pos,text,(color,))
        else:
            scrObj.insert(pos,text)
        scrObj.see(pos)
        scrObj.configure(state='disabled',foreground = 'black')
        # scrObj.mark_set("insert", '1.0')        
       

    def lockhandelUi(self,addLock):
        if addLock:
            tmpState = 'disabled'
            self.git_ui.entry.configure(state = 'readonly')
        else:
            tmpState = 'normal'
            self.git_ui.entry.configure(state = tmpState)

        for x in range(0,self.tabControl.index('end')):
            if self.tabControl.index('current') != x:
                tmptab = self.tabControl.tab(x,state = tmpState)
        self.art_ui.bookChosen.configure(state = tmpState)
        self.art_ui.bookChosen1.configure(state = tmpState)
        self.art_ui.bookChosen2.configure(state = tmpState)
        


    def crateHandelDesionUi(self):
        frame = self.git_ui
        tpath = self.art_ui.path.get()
        self.git_ui.path = tk.StringVar()
        self.git_ui.entryC = tk.StringVar()
        self.git_ui.path.set(tpath)


        def handCmdFunc(sourceCmd):
            pattern = re.compile(r"\s+")
            a = re.sub(pattern,' ',sourceCmd)
            b = a.split(' ')
            return b
      
        def myinsertInfo_des(cmd):
            cmdarvg = handCmdFunc(cmd)

            if cmdarvg[0] == 'cd' and len(cmdarvg) > 1 and cmdarvg[1] != '':

                pattern1 = re.compile(r"\.+")
                pattern2 = re.compile(r"/+")
                tmpst1 = '/' + cmdarvg[1]
                normalPath = re.sub(pattern2,'/',tmpst1)
                tmpStr2 = self.git_ui.path.get() + normalPath
                a = normalPath.split('/')

                if pattern1.match(a[1]):
                    # print('有点')
                    if os.path.exists(tmpStr2):
                        absPath = os.path.abspath(tmpStr2)
                        self.git_ui.path.set(absPath)
                        return
                else:
                    if os.path.exists(normalPath):
                        # print('存在')
                        absPath = os.path.abspath(normalPath)
                        self.git_ui.path.set(absPath)
                        return
                    else:
                        #检查当前路径
                        handNormalPath = self.git_ui.path.get() + normalPath
                        if os.path.exists(handNormalPath):
                            absPath = os.path.abspath(handNormalPath)
                            self.git_ui.path.set(absPath)
                            return
            isgitState = False 
            if cmdarvg[0] == 'git':
                isgitState = True
            
            self.lockhandelUi(True)

            print(self.git_ui.path.get())
            obj1 = subprocess.Popen(cmd,
                            shell = True,
                            cwd = self.git_ui.path.get(),
                            stdin = subprocess.PIPE,
                            stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE,
                            universal_newlines = True)
                
            obj1.wait()
            self.insertInfoToScr(frame.scr,tk.END,obj1.stdout.read())
            errcode = obj1.stderr.read()
            obj1.stdin.close()
            obj1.stdout.close()
            obj1.stderr.close()

            if errcode !=None:
                self.insertInfoToScr(frame.scr,tk.END,errcode,'red')
            else:
                self.insertInfoToScr(frame.scr,tk.END,'done.','red')

            self.lockhandelUi(False)

        scrolW  = 108; scrolH  = 31  
        frame.scr = scrolledtext.ScrolledText(frame, width=scrolW, height=scrolH, wrap=tk.WORD,bg = '#f2f2f2',state='disabled') 
        frame.scr.grid(column=0, row=2,columnspan=10,rowspan=6,sticky=tk.W + tk.E)

  
        tk.Frame(frame, width=777, height=5,bg='#fffacd').grid(row=1, column=0,columnspan=10,sticky=tk.W + tk.E)
        tk.Frame(frame, width=777, height=5,bg='#fffacd').grid(row=10, column=0,columnspan=10,sticky=tk.W + tk.E)
        

        style = ttk.Style()
        style.map("C.TButton",
            foreground=[('pressed', 'black'), ('active', 'black')],
            background=[('pressed', '!disabled', 'blue'), ('active', 'blue')],
            width = [('pressed', 120), ('active', 120)],
            height = [('pressed', '!disabled', 50), ('active', 50)],
        )
        
        def actionCmd(event):
            c = entry1.get()
            pattern = re.compile(r"\s*clear\s*")
            if pattern.match(c):
                entry1.delete(0, tk.END)
                frame.scr.configure(state='normal',foreground = 'black')
                frame.scr.delete(1.0,tk.END)
                frame.scr.configure(state='disabled',foreground = 'black')
                return
            entry1.delete(0, tk.END)
            self.insertInfoToScr(frame.scr,tk.END,c + '\n','green')
            a = c.split('\n')
            cmd = a[len(a) - 2]

            if cmd == '':
                return
            else:
                print(cmd)

            t = threading.Thread(target=myinsertInfo_des,args=(cmd,))
            t.setDaemon(True)
            t.start()

        def tabAction(event):
            cmdarvg = handCmdFunc(entry1.get())
            endPath = cmdarvg[len(cmdarvg) - 1]

            if endPath == '':
                c = os.listdir(self.git_ui.path.get())
                for x in c:
                    showC = x + '\n'
                    self.insertInfoToScr(frame.scr,tk.END,showC,'blue')
            else:
                #tab 自动补齐
                c = os.walk(self.git_ui.path.get(),True)
                b = []
                pattern = re.compile(r"%s.*" % (self.git_ui.path.get() + '/' + endPath))

                for dir_path,subpaths,files in c:

                    if dir_path == self.git_ui.path.get():#文件路径
                        pattern3 = re.compile(r"%s.*" % endPath)
                        for f in files:
                            if re.match(pattern3,f):
                                b.append(f)
                                showC = f +'\n'
                                self.insertInfoToScr(frame.scr,tk.END,showC,'blue')

                    if re.match(pattern,dir_path): #文件夹路径
                        showC = os.path.relpath(dir_path,self.git_ui.path.get())
                        pattern2 = re.compile(r".*/.*")
                        if re.match(pattern2,showC):
                            pass
                        else:
                            b.append(showC)
                            showC = showC + '\n'
                            self.insertInfoToScr(frame.scr,tk.END,showC,'blue')
                
                if len(b) == 1:
                    if os.path.isdir(self.git_ui.path.get() + '/' + b[0]):
                        b[0] = b[0] + '/'
                    cmdarvg[len(cmdarvg) - 1] = b[0]
                    self.git_ui.entryC.set(cmdarvg)
                    entry1.icursor(tk.END)

                    
            return 'break'

        entry1 = tk.Entry(frame, textvariable = self.git_ui.entryC,width = 85)
        entry1.grid(row = 11, column = 0,columnspan = 10,sticky = tk.W+ tk.E)
        entry1.bind('<Return>',actionCmd)
        entry1.bind('<Tab>',tabAction)

        self.git_ui.entry = entry1

        #当前路径工作路径
        tk.Label(frame,textvariable = self.git_ui.path,width = 86,anchor= tk.W).grid(row = 0, column = 0,columnspan = 10,sticky =tk.W)
        

    def crateHandelProtobufUi(self):

        frame = self.tab3
        scrolW  = 102; scrolH  = 24  
        frame.scr = scrolledtext.ScrolledText(frame, width=scrolW, height=scrolH, wrap=tk.WORD,bg = '#f2f2f2') 
        frame.scr.grid(column=0, row=12,columnspan=10,rowspan=6,padx = 10,sticky=tk.E + tk.W + tk.S)
        
        tmpFrame = tk.Frame(frame, width=800, height=160,bg='#fff0f5')
        tmpFrame.grid(row=2, column=0,columnspan=10,sticky=tk.W)

        style = ttk.Style()
        style.map("C.TButton",
            foreground=[('pressed', 'black'), ('active', 'black')],
            background=[('pressed', '!disabled', 'blue'), ('active', 'blue')],
            width = [('pressed', 120), ('active', 120)],
            height = [('pressed', '!disabled', 50), ('active', 50)],
        )
        

        def myTestFunc():
            print(frame.scr.get(1.0,tk.END))
            tmpStr = frame.scr.get(1.0,tk.END)
            pattern = re.compile(r"\s+")
            a = re.sub(pattern,' ',tmpStr)
            b = a.split(' ')
            


        self.colored_btn = ttk.Button(frame,text="测试", style="C.TButton",command = lambda:myTestFunc())
        self.colored_btn.grid(column=9, row=0,rowspan=3)

class MyTools():
    def __init__(self,root):
        self.root = root
        self.mtPath = None
        self.dbName = 'historyPath.db'
        self.initdbData()
        arvg = {}
        arvg["tkRoot"] = root
        arvg["handleArtFunc"] = self.myTools_handleArt
        arvg["handleDesFunc"] = self.myToolsPrint
        arvg["handleProtoFunc"] = self.myToolsPrint
        arvg["myPrintFunc"] = self.myToolsPrint
        arvg["selectPath"] = self.myTools_selectPath
        arvg["getScriptPath"] = self.myTools_getScriptPath
        arvg["saveScriptPath"] = self.myTools_saveScriptPath 
        arvg["getAllBranchName"] = self.getAllBranchName
        self.gui = TkinterGui(**arvg)
        self.art = handleArtResource(root,self.gui)

    #初始化数据库
    def initdbData(self):
        if os.path.exists(self.dbName):
            # print('已有历史记录')
            return
        # 初始化数据库
        db = sqlite3.connect(self.dbName)
        db.execute("CREATE TABLE IF NOT EXISTS HistoryPath (projectName varchar(20), scriptPath varchar(100))")
        db.close()

    #获得StrPath路径
    def myTools_getScriptPath(self,pName):
        db = sqlite3.connect(self.dbName)
        dbresult = db.execute("select * from HistoryPath where projectName = '%s' " % (pName)).fetchone()
        db.close()
        if dbresult == None:
            return None
        else:
            self.mtPath = dbresult[1]
            return dbresult[1]    
    #保存路径
    def myTools_saveScriptPath(self,pName,scriptPath):
        db = sqlite3.connect(self.dbName)
        dbresult = db.execute("select * from HistoryPath where projectName = '%s' " % (pName)).fetchone()
        if dbresult!=None:
            sql = "update HistoryPath set scriptPath = '%s' where projectName = '%s' " % (scriptPath,pName)
            db.execute(sql)
            db.commit()
        else:
            sql = "insert into HistoryPath values('%s', '%s')" % (pName,scriptPath)
            db.execute(sql)
            db.commit()
        db.close()

    def myToolsPrint(self):
        self.art.myPrintFunc()
    def myToolsTest(self):
        print("test")
    def myTools_selectPath(self):
        if self.art.workStatus:
            Dialog(self.root,'提示','导图进行中,请耐心等待...')
            return
        path_ = askdirectory(initialdir = self.mtPath)
        self.gui.art_ui.path.set(path_)
        self.myTools_saveScriptPath(self.gui.art_ui.mPName,path_)
        self.mtPath = path_

    #获取当前项目的所有分支
    def getAllBranchName(self,scriptPath):
        if self.mtPath == None:
            return None
        path = scriptPath + '/../../Client/'
        
        if not os.path.exists(path):
            return None

        obj1 = subprocess.Popen('git branch',
                            shell = True,
                            cwd = path,
                            stdin = subprocess.PIPE,
                            stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE,
                            universal_newlines = True)
        obj1.wait()
        content = obj1.stdout.read()
        obj1.stdin.close()
        obj1.stdout.close()
        obj1.stderr.close()
        return content
        

    #导图
    def myTools_handleArt(self):

        if self.mtPath == None:
            Dialog(self.root,'提示','目标路径不能为空。')
            return
        print(self.mtPath)
        if not os.path.exists('%s/copy_files.py' % self.mtPath):
            Dialog(self.root,'提示','请检查目标路径是否正确。')
            return
        sys.path.append(self.mtPath)
        self.art.handleArt(self.mtPath)
        
        
#处理美术资源类
class handleArtResource():
    def __init__(self,root,gui):
        self.num = 100
        self.root = root
        self.gui = gui
        self.workStatus = False   #是否工作中
        self.scriptPath = None
        
    def myPrintFunc(self):
        if self.workStatus:
            Dialog(self.root,'提示','正在打印中...')
            return
        t2 = ThreadExcept(target = self.myworker,gui = self.gui)
        t2.setDaemon(True) 
        t2.start()
        

        # print(dir(t2))

    def myworker(self):
        self.workStatus = True
        # for x in range(1,self.num):
        #     time.sleep(0.01)
        #     self.gui.insertInfoToScr(self.gui.art_ui.scr,tk.END,str.format('%d' % x + '\n'))
        for x in range(5,-1,-1):
            time.sleep(0.3)
            self.gui.insertInfoToScr(self.gui.art_ui.scr,tk.END,str.format('%f' % (100/x)) + '\n')
        self.workStatus = False

    def myShowInfoThreader(self):
        while art_threaderState==0:
            time.sleep(0.01)
            if tmpScriptObj.messageQueue.empty():
                pass
            self.gui.insertInfoToScr(self.gui.art_ui.scr,tk.END,tmpScriptObj.messageQueue.get() + '\n')
        
    #处理导图文件
    def opeaterCopyfile(self):
        instertProess = """
import queue

#显示用数据库
messageQueue = queue.Queue()
def myQueueData(strdata):
    messageQueue.put(strdata)
"""
        if os.path.exists('%s/temp_copy_files.py' % self.scriptPath):
            print("已删除")
            os.system('rm %s/temp_copy_files.py' % self.scriptPath)
        print("新建")
        os.system('cp %s/copy_files.py %s/temp_copy_files.py' % (self.scriptPath,self.scriptPath))

        # 导入存数据库代码
        pattern2 = re.compile(r"\s*import\s*")
        file = open('%s/temp_copy_files.py' % self.scriptPath,'r+')
        content = file.read()
        file.close()

        a = content.split('\n')
        tmpIndex = -1
        for i in range(len(a)):
            match = pattern2.match(a[i])
            if match:
                tmpIndex = i
        a[tmpIndex] = a[tmpIndex] + instertProess
       
        #导入提示存入数据库代码
        pattern3 = re.compile(r"\s*print\s*\(")
        pattern4 = re.compile(r".*拷贝目录:.*")
        pattern5 = re.compile(r"# 拷贝资源\s*")
        pattern6 = re.compile(r".*压缩目录:.*")
        deleteStatus = 0
        for i in range(len(a)):
            match = pattern3.match(a[i])
            match5 = pattern5.match(a[i])
            if match5:
                deleteStatus = 1
            if deleteStatus == 1:
                a[i] = '# ' + a[i]
            if match and deleteStatus==0:
                matc4 = pattern4.match(a[i])
                if matc4:#文件有语法诟病 此处是为了 在不动源文件基础下进行操作
                    a[i] = re.sub('\"拷贝目录:\",','\"拷贝目录:%s\" %',a[i],1)
                match6 = pattern6.match(a[i])
                if match6:
                    a[i] = re.sub('\"压缩目录:\",','\"压缩目录:%s\" %',a[i],1)

                testc = re.sub(pattern3,'(',a[i],1)
                #空格
                spece = re.sub(r"print*.*","",a[i])
                testc2 = "\n" + spece + "tmpData = str.format" + testc
                a[i] = a[i] + testc2 + "\n" + spece + "myQueueData(tmpData)"

        s = '\n'.join(a)
        fp = open('%s/temp_copy_files.py' % self.scriptPath, 'w')
        fp.write(s)
        fp.close()

    def myHandleArtThreader(self,cacPath):
        self.workStatus = True
        self.gui.lockhandelUi(True)
        self.gui.insertInfoToScr(self.gui.art_ui.scr,tk.END,"开始更新美术资源\n")
        obj1 = subprocess.Popen('git svn rebase',
                                shell = True,
                                cwd = cacPath,
                                stdin = subprocess.PIPE,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE,
                                universal_newlines = True)
        while True:
            if obj1.poll() != None:
                break
            time.sleep(0.01)
            self.gui.insertInfoToScr(self.gui.art_ui.scr,tk.END,obj1.stdout.readline())
            
        obj1.stdin.close()
        obj1.stdout.close()
        obj1.stderr.close()
        
        self.gui.insertInfoToScr(self.gui.art_ui.scr,tk.END,"美术资源更新完成\n")

        oldPath = os.getcwd()    #获取当前工作目录
        tmpScriptObj.messageQueue.put(oldPath)
        os.chdir(self.scriptPath)   #修改当前工作目录
        for item in tmpScriptObj.copy_dirs_map.items():
            tmpScriptObj.copy_dir_reverse(item[0], item[1])
        if tmpScriptObj.is_compress_file == True:
            t = ThreadExcept(target = tmpScriptObj.compress_dirs,gui = self.gui)
            t.setDaemon(True)
            t.start()
            t.join()

        art_threaderState = 1
        tmpScriptObj.messageQueue.put("更新了:(%d)个资源, 压缩了:(%d)个资源."%(tmpScriptObj.totalCopyFileCount, tmpScriptObj.totalCompressFileCount))
        tmpScriptObj.messageQueue.put(oldPath)
        os.chdir(oldPath)
        if os.path.exists('%s/temp_copy_files.py' % self.scriptPath):
            print("已删除")
            os.system('rm %s/temp_copy_files.py' % self.scriptPath)
        self.workStatus = False
        self.gui.lockhandelUi(False)
   
    def handleArt(self,scriptpath):
        if self.workStatus:
            Dialog(self.root,'提示','导图进行中,请耐心等待...')
            return
        self.gui.art_ui.scr.delete(1.0, tk.END)
        self.scriptPath = scriptpath
        cacPath = scriptpath + '/../../CACommon/'
        self.opeaterCopyfile()
        global tmpScriptObj  #脚本对象
        global art_threaderState #描述线程阻塞状态
        tmpScriptObj = importlib.import_module('temp_copy_files')
        art_threaderState = 0
        t2 = threading.Thread(target = self.myShowInfoThreader)
        t2.setDaemon(True)
        t2.start()

        t3 = threading.Thread(target = self.myHandleArtThreader,args=(cacPath,))
        t3.setDaemon(True)
        t3.start()

def main():
    root = tk.Tk() # 这里
    #fix the root window size
    root.minsize(840, 600)
    root.maxsize(840, 600) #这里主要是控制窗口的大小，让窗口大小不能改变
    root.title('赵日天大魔王的工具箱') #设置主窗口的标题
    mytools = MyTools(root)
    root.mainloop()   # 这里进入顶层窗口的循环
if __name__ == '__main__':
    main()

    

 
    

   