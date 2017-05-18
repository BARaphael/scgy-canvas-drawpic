#!/usr/bin/env python3
# encoding: utf-8

# Usage:
# canvas.py pic start_x start_y
# canvas.py 1.jpg 0 0

import requests
from PIL import Image
import random
import sys
import time

class Canvas:
    def __init__(self):
        self.data=[]
        for i in range(300):
            self.data.append([])
            for j in range(300):
                self.data[i].append((255,255,255))
        self.count=-1
        self.update()

    def update(self):
        d=update(self.count)
        for p in d["data"]:
            self.data[p["x"]][p["y"]]=int_to_color(p["color"])
        self.count=d["count"]

    def show(self):
        #i=Image.new('RGB',(300,300))
        #i.putdata(sum(self.data,[]))
        pass

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'}

def modify(x,y,color,count):
    print(x,y,color,count)
    #return
    url='http://canvas.ourscgy.ustc.edu.cn/canvas/modify'
    json={"canvas":[{"x":x,"y":y,"color":color}],"count":count}
    r=requests.post(url,json=json,headers=headers,timeout=5)
    print(r.json())
    return r.json()

def update(count):
    url='http://canvas.ourscgy.ustc.edu.cn/canvas/update'
    r=requests.get(url,params={"count":count},headers=headers,timeout=5)
    return r.json()

def color_to_int(color):
    return (color[0]<<16)+(color[1]<<8)+color[2]

def int_to_color(n):
    return n>>16,(n>>8)%256,n%256

def diff(c1,c2):
    return max(0,c1[0]-c2[0])+max(0,c1[1]-c2[1])+max(0,c1[2]-c2[2])

def modify_to(pic,x,y):
    c=Canvas()
    while True:
        diffs=[]
        for i in range(pic.width):
            for j in range(pic.height):
                if x+i>=0 and x+i<300 and y+j>=0 and y+j<300:
                    if c.data[x+i][y+j]!=pic.getpixel((i,j)):
                        diffs.append((i,j,diff(c.data[x+i][y+j],pic.getpixel((i,j)))))
        print("Diff count =",len(diffs))
        if diffs:
            maxdiff=max([d for _,_,d in diffs])
            print("maxdiff =",maxdiff)
            pi,pj=random.choice([(i,j) for i,j,d in diffs if d==maxdiff])
            try:
                modify(x+pi,y+pj,color_to_int(pic.getpixel((pi,pj))),c.count)
            except:
                pass
        try:
            c.update()
        except:
            pass
        time.sleep(20)

im=Image.open(sys.argv[1])
im=im.convert('RGB')
modify_to(im,int(sys.argv[2]),int(sys.argv[3]))

