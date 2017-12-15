#!/usr/bin/env python3
#encoding:utf8


# 已有新的对应美术资源情况下删除老旧资源
import os
import io
import sys
import shutil
import hashlib
import sqlite3
from urllib.request import Request, urlopen
from urllib import error
import urllib
from base64 import b64encode
import threading


#复制的源文件

freshMan = ["../../../../../../FreshMan/Client/Client/res/ui",
            "../../../../../../FreshMan/Client/Client/res/animation",
            "../../../../../../FreshMan/Client/Client/res/audio",
            "../../../../../../FreshMan/Client/Client/res/fx",
            "../../../../../../FreshMan/Client/Client/res/header",
            "../../../../../../FreshMan/Client/Client/res/lt",
            "../../../../../../FreshMan/Client/Client/res/map",
]


