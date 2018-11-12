# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 00:00:37 2018

@author: sanket
"""

import os
import threading

def fun(command):
    os.system(command)

for i in range(0, 3 ):
    (threading.Thread(target=fun, args=("python node"+str(i)+".py",))).start()