# -*- coding: gb2312 -*-
#:注意requests库
#:
#:
#:
#:
import re
import os
import requests
from urllib import parse

# 樱花搜索api
def GetUrlImomoe(numb,strd):
    url = 'http://www.imomoe.in/search.asp?page='
    url +=  str(numb)
    url += '&searchword='
    url += parse.quote(strd.encode("gb2312"))
    url += '&searchtype=-1'
    return url

# 获取动漫名
def GetimomoeTitle(strd):
    retd = re.search('title=\"(.*?)\">', strd).group()
    retdd = retd.replace('title=\"', '')
    retdd = retdd.replace("\">", '')
    return retdd

#  获取 Url
def GetimomeUrl(strd):
    retd = re.search('<a href=\"(.*?)\" target',strd).group()
    retdd = retd.replace('<a href=\"','')
    retdd = retdd.replace('\" target','')
    retdd = "http://www.imomoe.in" + retdd
    return retdd

# 通过<li>...</li> 获取key:value
def ImomoeVideo(strd):
    if(strd == None):
        print("Video None")
        return None

    AllVide = []
    for i in strd:
        retd = re.search('<h2><a(.*?)</a>',i)

        VideoTitle = GetimomoeTitle(retd.group())
        VideoUrl = GetimomeUrl(retd.group())

        Video ={"title":VideoTitle,"url":VideoUrl}

        AllVide.append(Video)

    return AllVide



header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Connection': 'keep-alive',
            'Cookie':'_uuid=51952425-F593-DE3B-DF2D-BD22A50D9E5103143infoc; buvid3=88413134-0D6F-464D-81C9-43FD9535681353927infoc; sid=56uwx7pi; LIVE_BUVID=AUTO9215915169485113; CURRENT_FNVAL=16; rpdid=|(~umYk|lJJ0J\'ulmulkJlmY; CURRENT_QUALITY=120; _dfcaptcha=11ee7275ff079a97e4c450b0dcd658df; bsource=seo_baidu; bp_video_offset_111255808=403933191631185591; bp_t_offset_111255808=403935236035632003; PVID=25; DedeUserID=111255808; DedeUserID__ckMd5=7c671a99b4d2c8a7; SESSDATA=b8926561%2C1608439279%2C4a087*61; bili_jct=219d28a8804576170c9971dfcda7bb6b',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
            'Referer':'https://t.bilibili.com/?spm_id_from=333.851.b_696e7465726e6174696f6e616c486561646572.31'
          }


search = input("pls type key word\n")
data = {'searchword': search}

number = 1 #页数
post = 0 #重连次数
yinghua = True #樱花搜索是否继续
file = open('fuck.txt','wb+') #文件读写
all_Page = 0 #总页码

while yinghua:

    #获取url
    url = GetUrlImomoe(number, search)

    #输出整个连接 print('樱花\n', url)

    # 判断樱花是否连接
    while 1:
        print("正在进行第",post,"次爬取")
        r = requests.post(url,data=data)
        r.encoding = 'gb2312'
        if(r.status_code != 502):
            break;
        post += 1
        #最多连接重试10次
        if(post >= 10):
            print("No Connect")
            yinghua = False
            break

    #获得返回值 全网页 保存在 html里面
    html =  r.text

    #是否找到动漫数据
    ret = re.search('<b>',html)

    # 没有找到
    if(ret != None):
        print('No Animation')
        yinghua = False#跳出樱花搜索
        break

    # 有动漫数据开始循环获取每一页的数据

    #找动漫栏目 div :有两个pics 只用第一个 第二个是推荐
    ret = re.search("<div class=\"pics\">([\s\S]*)</div>",html)

    # <ui>...</ui>数据
    #获取 全部<li>...</li> 内容 全是动漫连接 保存在 strd 里面
    ret = re.search("<ul>([\s\S]*?)</ul>",ret.group(0))
    strd = ret.group()
    # print(strd)

    #逐个分析在 <ui>里面的<li>
    ret = re.findall('<li>([\s\S]*?)</li>',strd)
    AllDoGa = ImomoeVideo(ret)
    if(AllDoGa != None):
        for i in AllDoGa:
            print(i["title"])
            print(i["url"])
            print("\n")

    #获取总页码
    all_Page = re.search("span>共(.*?)</span>",html)

    #判断是否末页
    ret = re.search("<em class=\'nolink\'>下一页</em>",r.text)
    if(ret != None):
        #末尾
        print("已到末尾")
        yinghua = False
        break

    #不是末页
    print("按下任意键下一页 当前页数是",number)
    print(all_Page.group())
    os.system("pause")
    number += 1
    post = 0
    continue # 继续下一页循环

file.close()
os.system("pause")