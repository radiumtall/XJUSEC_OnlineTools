import requests
from bs4 import BeautifulSoup
from application.data import *
import datetime
from application.BlogDb import Blog,db
import sys
sys.path.append('../')
from app import app
app.app_context().push()
today = datetime.date.today().strftime('%Y-%m-%d')
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36",
    # "":""

}

def inDb(data,src):
    url = data['url']
    title = data['title']
    time = data['time']
    src = src
    # print(Blog.query.filter_by(url=url).all())
    if Blog.query.filter_by(url=url,title=title,time=time).first() != None:
    # if url =="":
        return "[ * ]url: {} is existed".format(url)
    else:
        if  Blog.query.filter_by(src=src).first() == None:
            num = 1
        else:
            num = Blog.query.filter_by(src=src).order_by(Blog.num.desc()).first().num + 1
        db_blog = Blog(url=url,title=title,time=time,src=src,num=num)
        db.session.add(db_blog)
        db.session.commit()
        return "[ * ]url: {} in db success!!".format(url)
def getHtml(url):
    req = requests.get(url,headers=headers)

    html = req.text
    return html

def getTime(time):
    if '年' in time and '月' in time:
        time = time.replace('年', '-').replace('月', '-').replace('日', '')
    else:
        time = today
    return time

def spiderFreebuf():
    html = getHtml(BLOG_WEB_URL['Freebuf'])
    soup = BeautifulSoup(html, "lxml")
    datas = soup.select('#timeline > div > div.news-info')
    times = soup.select('#timeline > div > div > dl > dd > span.time')
    # print(datas)
    num = 0
    result = {}
    for data in datas:
        tmp = {}
        num = num + 1
        url = data.dl.dt.a['href']
        title = data.dl.dt.a.text
        time = times[datas.index(data)].text
        # print(title + "   -   "+url + "   -   "+time)
        tmp['url'] = url
        tmp['title'] = title
        tmp['time'] = time
        result[str(num)] = tmp
    return result

def spider4hou():
    html = getHtml(BLOG_WEB_URL['4hou'])
    soup = BeautifulSoup(html,"lxml")
    datas = soup.select('#container > div > div > li > div')
    # container > div.innerCeil > div:nth-child(1) > li > div > a > h1
    times = soup.select('#container > div > div > li > div > div > p')

    num = 0
    result = {}
    for data in datas:
        tmp = {}
        num = num + 1
        url = data.a['href']
        title = data.a.h1.text
        time = times[datas.index(data)].text
        time = getTime(time)
        # print(title+url+time)
        tmp['url'] = url
        tmp['title'] = title
        tmp['time'] = time
        result[str(num)] = tmp
    return result

def spiderGlijin():
    html = getHtml(BLOG_WEB_URL['Glzjin'])
    soup = BeautifulSoup(html,"lxml")
    datas = soup.select('#wrap > div > div > main > article > header')
    # print(datas)
    # times = soup.select('div > div > div.posted-by.vcard.author > a > time.entry-date.published')
    # print(times)
    result = {}
    num = 0
    for data in datas:
        num = num + 1
        tmp = {}
        url = data.h2.a['href']
        title = data.h2.text
        time = data.p.time.a.text.replace('年','-').replace('月','-').replace('日','')

        tmp['url'] = url
        tmp['title'] = title
        tmp['time'] = time
        result[str(num)] = tmp
        # print(title + "   -   "+url + "   -   "+time)
    return result

def spiderSeebug():
    html = getHtml(BLOG_WEB_URL['Seebug'])
    soup = BeautifulSoup(html,"lxml")
    datas = soup.select('#wrapper > main > div > article')
    num = 0
    result = {}
    for data in datas:
        tmp = {}
        num = num + 1
        url = 'https://paper.seebug.org'+data.h5.a['href']
        title = data.h5.a.text
        time = data.section.span.time['datetime']
        # print(title+url+time)
        tmp['url'] = url
        tmp['title'] = title
        tmp['time'] = time
        result[str(num)] = tmp
    return result

def spiderYlg():

    html = getHtml(BLOG_WEB_URL['Ylg'])
    soup = BeautifulSoup(html,"lxml")
    datas = soup.select('div > div > h2')
    times = soup.select('div > div > div.posted-by.vcard.author > a > time.entry-date.published')
    # print(times)
    result = {}
    num = 0
    for data in datas:
        num = num + 1
        tmp = {}
        url = data.a['href']
        title = data.a['title']
        time = times[datas.index(data)]['content']

        tmp['url'] = url
        tmp['title'] = title
        tmp['time'] = time
        result[str(num)] = tmp
        # print(title + "   -   "+url + "   -   "+time)
    return result

def getAllData():
    data_4hou = spider4hou()
    data_Freebuf = spiderFreebuf()
    data_Glzjin = spiderGlijin()
    data_Seebug = spiderSeebug()
    data_Ylg = spiderYlg()
    # print(data_4hou)
    # print(data_Freebuf)
    # print(data_Glzjin)
    # print(data_Seebug)
    # print(data_Ylg)
    for i in  range(int(len(data_4hou))):
        datas = data_4hou[str(int(len(data_4hou))-i)]
        result = inDb(datas,"4hou")
        print(result)
        # print(datas)
    for i in  range(int(len(data_Freebuf))):
        datas = data_Freebuf[str(int(len(data_Freebuf))-i)]
        result = inDb(datas, "Freebuf")
        print(result)
        # print(datas)
    for i in  range(int(len(data_Glzjin))):
        datas = data_Glzjin[str(int(len(data_Glzjin))-i)]
        result = inDb(datas, "Glzjin")
        print(result)
        # print(datas)
    for i in  range(int(len(data_Seebug))):
        datas = data_Seebug[str(int(len(data_Seebug))-i)]
        result = inDb(datas, "Seebug")
        print(result)
        # print(datas)
    for i in  range(int(len(data_Ylg))):
        datas = data_Ylg[str(int(len(data_Ylg))-i)]
        result = inDb(datas, "Ylg")
        print(result)
        # print(datas)
    print("All Data In Db")

def get4hou():
    data_4hou = spider4hou()
    for i in  range(int(len(data_4hou))):
        datas = data_4hou[str(i+1)]
        # print(data_4hou[str(i+1)])
        result = inDb(datas,"4hou")
        print(result)
    return "ok"
def getFreebuf():
    data_Freebuf = spiderFreebuf()
    for i in  range(int(len(data_Freebuf))):
        datas = data_Freebuf[str(i+1)]
        result = inDb(datas, "Freebuf")
        print(result)
        # print(datas)
    return "ok"
def getGlzjin():
    data_Glzjin = spiderGlijin()
    for i in  range(int(len(data_Glzjin))):
        datas = data_Glzjin[str(i+1)]
        result = inDb(datas, "Glzjin")
        print(result)
        # print(datas)
    return "ok"
def getSeebug():
    data_Seebug = spiderSeebug()
    for i in range(int(len(data_Seebug))):
        datas = data_Seebug[str(i + 1)]
        result = inDb(datas, "Seebug")
        print(result)
        # print(datas)
    return "ok"
def getYlg():
    data_Ylg = spiderYlg()
    for i in  range(int(len(data_Ylg))):
        datas = data_Ylg[str(i+1)]
        result = inDb(datas, "Ylg")
        print(result)
    return "ok"
        # print(datas)


def show_data_limit(num):
    data_4hou = Blog.query.filter_by(src="4hou").order_by(Blog.num.desc()).limit(num).all()
    data_Freebuf = Blog.query.filter_by(src="Freebuf").order_by(Blog.num.desc()).limit(num).all()
    data_Glzjin = Blog.query.filter_by(src="Glzjin").order_by(Blog.num.desc()).limit(num).all()
    data_Seebug = Blog.query.filter_by(src="Seebug").order_by(Blog.num.desc()).limit(num).all()
    data_Ylg = Blog.query.filter_by(src="Ylg").order_by(Blog.num.desc()).limit(num).all()
    show_4hou = {}
    show_Freebuf = {}
    show_Glzjin = {}
    show_Seebug = {}
    show_Ylg = {}

    for i in data_4hou:
        tmp = {}
        tmp['url'] = i.url
        tmp['title'] = i.title
        show_4hou[str(len(show_4hou)+1)] = tmp
    for i in data_Freebuf:
        tmp = {}
        tmp['url'] = i.url
        tmp['title'] = i.title
        show_Freebuf[str(len(show_Freebuf) + 1)] = tmp
    for i in data_Glzjin:
        tmp = {}
        tmp['url'] = i.url
        tmp['title'] = i.title
        show_Glzjin[str(len(show_Glzjin) + 1)] = tmp
    for i in data_Seebug:
        tmp = {}
        tmp['url'] = i.url
        tmp['title'] = i.title
        show_Seebug[str(len(show_Seebug) + 1)] = tmp
    for i in data_Ylg:
        tmp = {}
        tmp['url'] = i.url
        tmp['title'] = i.title
        show_Ylg[str(len(show_Ylg) + 1)] = tmp
    # print(show_4hou,show_Freebuf,show_Glzjin,show_Seebug,show_Ylg)
    return  show_4hou,show_Freebuf,show_Glzjin,show_Seebug,show_Ylg

def show_data_all():
    data_4hou = Blog.query.filter_by(src="4hou").order_by(Blog.num.desc()).all()
    data_Freebuf = Blog.query.filter_by(src="Freebuf").order_by(Blog.num.desc()).all()
    data_Glzjin = Blog.query.filter_by(src="Glzjin").order_by(Blog.num.desc()).all()
    data_Seebug = Blog.query.filter_by(src="Seebug").order_by(Blog.num.desc()).all()
    data_Ylg = Blog.query.filter_by(src="Ylg").order_by(Blog.num.desc()).all()
    show_4hou = {}
    show_Freebuf = {}
    show_Glzjin = {}
    show_Seebug = {}
    show_Ylg = {}
    # tmp = {}
    for i in data_4hou:
        tmp = {}
        tmp['url'] = i.url
        tmp['title'] = i.title
        show_4hou[str(len(show_4hou)+1)] = tmp
    for i in data_Freebuf:
        tmp = {}
        tmp['url'] = i.url
        tmp['title'] = i.title
        show_Freebuf[str(len(show_Freebuf) + 1)] = tmp
    for i in data_Glzjin:
        tmp = {}
        tmp['url'] = i.url
        tmp['title'] = i.title
        show_Glzjin[str(len(show_Glzjin) + 1)] = tmp
    for i in data_Seebug:
        tmp = {}
        tmp['url'] = i.url
        tmp['title'] = i.title
        show_Seebug[str(len(show_Seebug) + 1)] = tmp
    for i in data_Ylg:
        tmp = {}
        tmp['url'] = i.url
        tmp['title'] = i.title
        show_Ylg[str(len(show_Ylg) + 1)] = tmp

    return  show_4hou,show_Freebuf,show_Glzjin,show_Seebug,show_Ylg

# getAllData()