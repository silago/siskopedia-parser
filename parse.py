from bs4 import BeautifulSoup
import requests
import re
from time import sleep
import os
import urllib2, urllib
import pickle
import thread


URLS = []
ITEMS = []
BASE = "boobpedia.com"
PROCESS_COUNT = 0
MAX_PROCESS_COUNT = 30

def getImage(url,header):
    #print "getting image on url: "+BASE+url
    try:
        r = requests.get("http://" +BASE+url)
    except:
        print "error: cannot get url "+url
        return False
    soup = BeautifulSoup(''.join(r.text))
    for i in soup.findAll('img'):
        if i.has_attr('src'):
            try:
                urllib.urlretrieve('http://'+BASE+i['src'],header+'/'+i['src'].split('/')[-1])
            except: print "error: cannot save file"

def parsePage(url):
    global PROCESS_COUNT, BASE, MAX_PROCESS_COUNT
    #while PROCESS_COUNT>=MAX_PROCESS_COUNT:
    #    pass   #return "f"
    #PROCESS_COUNT+=1
    
    #url = "boobpedia.com/boobs/CreamySweet" 
    try:
        r = requests.get("http://"+BASE+url)
    except:
        print "error: cannot get page "+url
        PROCESS_COUNT-=1
        return False
    
    data = r.text
    main_data = r.text
    
    
    data = data.replace("\n","")
    data = data.encode("ascii","ignore")
    
    soup = BeautifulSoup(''.join(r.text))
    if soup.findAll('h1'):
        header = soup.findAll('h1')[0].text
    else: return 0;
    try:
        os.mkdir(header)
    except:
        pass

    for i in soup.findAll('a'):
        if i.has_attr('class') and i['class'][0] == 'image':
            if i.has_attr('href'):
                createProccess(getImage,(i['href'],header))
                #thread.start_new_thread(getImage,(i['href'],header))

        
    
    #for i in images:
    #    if i.has_key('src'):
    #        urllib.urlretrieve('http://'+BASE+i['src'],header+'/'+i['src'].split('/')[-1])
    
    
    #table = re.findall('.+table class="infobox".+?>(.+)</table>',data,re.MULTILINE)
    info = {}
    for table in soup.findAll('table'):
        if table.has_attr('class') and table['class'][0]=='infobox':
            for tr in table.findAll('tr'):
                td = tr.findAll('td')
                if len(td)==2: info[td[0].text]=td[1].text
                if len(td)==1: info[td[0].text]=td[0].text 
    
    text=[]
    p = soup.findAll('p')
    if p:
        try:
            text.append(p[0].text)
            text.append(p[1].text)
        except: pass
    links = []
    for i in soup.findAll('a'):
        if i.has_attr('class') and i['class'][0]=='external' and i.has_attr('href'):
            links.append({'href':i['href'],'text':i.text})
    result = {'text':text,'info':info,'links':links}
    #for dt in soup.findAll('p')

    


    #for i in re.findall(r"tr>(.+?)<tr",data,re.MULTILINE):
    #    z = re.findall(r"td>(.+?)</td",i)
    #    if len(z)>1:
    #        info[re.sub(r"<[^>]*?>","",z[0])]=re.sub(r"<[^>]*?>"," ",z[1])
    
    pickle.dump(result,open(header+"/info.p","wb"))
    PROCESS_COUNT-=1

def createProccess(f,p)
    global PROCESS_COUNT, BASE, MAX_PROCESS_COUNT
    sleep(0.5)
    while PROCESS_COUNT>=MAX_PROCESS_COUNT:
        sleep(0.5)
    PROCESS_COUNT+=1
    thread.start_new_thread(f,p)
    
def collectUrls(url = False, items = False):
    global PROCESS_COUNT, BASE, MAX_PROCESS_COUNT
    #sleep(0.5)
    #while PROCESS_COUNT>=MAX_PROCESS_COUNT:
    #    sleep(0.5)
    #PROCESS_COUNT+=1

    urls = {}
    URLS.append(url)
    items = {}
    if not url: url = "/boobs/Category:Categories" 
    url = BASE+url
    print url
    try:
        r = requests.get("http://" +url)
    except:
        print "cannot get page "+url
        PROCESS_COUNT-=1
        return False 
    #if not r: return False
    data = BeautifulSoup(''.join(r.text))
    #return data
    for i in data.findAll('a'):
        if i.has_attr("href"):
            url_from_page = i['href']
            if re.findall("/boobs/.*",url_from_page) and not re.findall("boobpedia.com",url_from_page):
                if url_from_page not in URLS:
                    URLS.append(url_from_page)
                    if not re.findall("/boobs/.*:.*",url_from_page):
                        createProccess(parsePage,(url_from_page,))
                        #print "going to parse page: "+url_from_page
                        #thread.start_new_thread(parsePage,(url_from_page,))
                        #ITEMS.append(parsePage(url_from_page)) 
                    else:
                        #print "going to collect page: "+url_from_page
                        createProccess(collectUrls,(url_from_page,))
                        #thread.start_new_thread(collectUrls,(url_from_page,))
    PROCESS_COUNT-=1
    #return 1








