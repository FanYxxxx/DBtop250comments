# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 23:33:29 2016

@author: FanYxxx
"""

import urllib.request
from bs4 import BeautifulSoup
import time
import os

start = time.clock() # recording time
rooturl='https://movie.douban.com/top250'
indexlist=['https://movie.douban.com/top250']
global count
count=0


def commentsmining(url,url2):
    global count
    url1=urllib.request.Request(url,headers={
      'User-Agent':'xxxxxx',
      'Cookie':'xxxxxxx'
       })
    html = urllib.request.urlopen(url1)
    miningPage = html.read()    
    html.close()
    miningText = BeautifulSoup(miningPage,'lxml')
    name2=miningText.find('meta',{'name':'description'}).get('content')
    
    ##count2=count2+100
    ## print(miningText)  ##正确
    for li in miningText.findAll('div',{'class':'comment'}):
        comment = li.find('p',{'class':''}).get_text()
        time.sleep(0.05)
        fpath= os.path.abspath('/Users/FanYxxx/百度云同步盘/爬虫/movie/'+name2+'.txt')   
        f = open(fpath,'a+',encoding='utf-8')
        f.write(comment+'\r\n')
        ##print(comment)
        count=count+1
        if count%300==0:
            print(count)
        
        ##count1=count1+1
    f.close
    if (miningText.find('a',{'class':'next'}).get('href')==None or count>1500):
        print('没有了,下一个movieurl')
        count=0
        # count1=0
        #count2=0
    else:
        nextPageurl=url2+miningText.find('a',{'class':'next'}).get('href')
        commentsmining(nextPageurl,url2)
        
        
def pagemining(url):
    url1=urllib.request.Request(url,headers={
      'User-Agent':'xxxxxx',
      'Cookie':'xxxxxxx'})
    html = urllib.request.urlopen(url1)
    ##currentPage = html.read().decode("utf-8")
    currentPage = html.read()    
    html.close()
    currentText = BeautifulSoup(currentPage,'lxml')
    for tag in currentText.findAll('div',{'class':'item'}):
        order = tag.find('em').get_text()
        name = tag.find('span',{'class':'title'}).get_text()
        classtitle = order + ' ' + name
        time.sleep(0.1)
##数据加入txt文件
        fpath= os.path.abspath('/Users/FanYxxx/百度云同步盘/爬虫/movie/'+name+'短评.txt')   
        f = open(fpath,'a+',encoding='utf-8')
        ##f.write(classtitle+'\r\n')
        print(classtitle+' '+'start')
        f.close
        ##find comment url
        moviePage = tag.find('a').get('href')
        commentPage = moviePage +'comments'
        print('评论链接'+commentPage)
        commentsmining(commentPage,commentPage)


        
   
## get rooturl analytics
print('目录解析链接:'+rooturl)
rooturl1=urllib.request.Request(rooturl,headers={
        'User-Agent':'xxxxxx',
        'Cookie':'xxxxxxx' })
html = urllib.request.urlopen(rooturl1)

Text = html.read().decode("utf-8")         
html.close()
soup = BeautifulSoup(Text,'lxml')
targetDiv = soup.find('div',{'class':'paginator'})
cataloglinks = targetDiv.findAll('a')
for l in cataloglinks:
    indexlist.append('https://movie.douban.com/top250'+l.get('href'))
indexlist.pop()
del indexlist[0]
del indexlist[0]
del indexlist[0]
del indexlist[0]
del indexlist[0]
print(indexlist)
print('目录链接解析完成')

## circulation 
for index in indexlist:
    page = index
    count=0
    pagemining(page)

    
end=time.clock()
print(end-start)