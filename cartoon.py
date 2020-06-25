# -*- coding: gb2312 -*-
#:ע��requests��
#:
#:
#:
#:
import re
import os
import requests
from urllib import parse

# ӣ������api
def GetUrlImomoe(numb,strd):
    url = 'http://www.imomoe.in/search.asp?page='
    url +=  str(numb)
    url += '&searchword='
    url += parse.quote(strd.encode("gb2312"))
    url += '&searchtype=-1'
    return url

# ��ȡ������
def GetimomoeTitle(strd):
    retd = re.search('title=\"(.*?)\">', strd).group()
    retdd = retd.replace('title=\"', '')
    retdd = retdd.replace("\">", '')
    return retdd

#  ��ȡ Url
def GetimomeUrl(strd):
    retd = re.search('<a href=\"(.*?)\" target',strd).group()
    retdd = retd.replace('<a href=\"','')
    retdd = retdd.replace('\" target','')
    retdd = "http://www.imomoe.in" + retdd
    return retdd

# ͨ��<li>...</li> ��ȡkey:value
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

number = 1 #ҳ��
post = 0 #��������
yinghua = True #ӣ�������Ƿ����
file = open('fuck.txt','wb+') #�ļ���д
all_Page = 0 #��ҳ��

while yinghua:

    #��ȡurl
    url = GetUrlImomoe(number, search)

    #����������� print('ӣ��\n', url)

    # �ж�ӣ���Ƿ�����
    while 1:
        print("���ڽ��е�",post,"����ȡ")
        r = requests.post(url,data=data)
        r.encoding = 'gb2312'
        if(r.status_code != 502):
            break;
        post += 1
        #�����������10��
        if(post >= 10):
            print("No Connect")
            yinghua = False
            break

    #��÷���ֵ ȫ��ҳ ������ html����
    html =  r.text

    #�Ƿ��ҵ���������
    ret = re.search('<b>',html)

    # û���ҵ�
    if(ret != None):
        print('No Animation')
        yinghua = False#����ӣ������
        break

    # �ж������ݿ�ʼѭ����ȡÿһҳ������

    #�Ҷ�����Ŀ div :������pics ֻ�õ�һ�� �ڶ������Ƽ�
    ret = re.search("<div class=\"pics\">([\s\S]*)</div>",html)

    # <ui>...</ui>����
    #��ȡ ȫ��<li>...</li> ���� ȫ�Ƕ������� ������ strd ����
    ret = re.search("<ul>([\s\S]*?)</ul>",ret.group(0))
    strd = ret.group()
    # print(strd)

    #��������� <ui>�����<li>
    ret = re.findall('<li>([\s\S]*?)</li>',strd)
    AllDoGa = ImomoeVideo(ret)
    if(AllDoGa != None):
        for i in AllDoGa:
            print(i["title"])
            print(i["url"])
            print("\n")

    #��ȡ��ҳ��
    all_Page = re.search("span>��(.*?)</span>",html)

    #�ж��Ƿ�ĩҳ
    ret = re.search("<em class=\'nolink\'>��һҳ</em>",r.text)
    if(ret != None):
        #ĩβ
        print("�ѵ�ĩβ")
        yinghua = False
        break

    #����ĩҳ
    print("�����������һҳ ��ǰҳ����",number)
    print(all_Page.group())
    os.system("pause")
    number += 1
    post = 0
    continue # ������һҳѭ��

file.close()
os.system("pause")