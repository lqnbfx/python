#-*- coding=utf-8 -*-



from bs4 import BeautifulSoup
import re
import urllib.request, urllib.error
import xlwt
import sqlite3
import os

def main():
    baseurl = 'https://movie.douban.com/top250?start='
    #1.爬取网页
    datalist = getData(baseurl)
    savepath = "豆瓣电影Top250.xls"

    #保存数据 excl
    saveData(datalist, savepath)
    # 保存数据sqlite3
    save2db(datalist)
    #askURL(baseurl)

#详情连接
findLink = re.compile(r'<a href="(.*?)">')
#缩略图链接
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)  #re.S 让换行符包含在字符中
#片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
#评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
#评价人数
findJudge = re.compile(r'<span>(\d*人评价)</span>')
#找到概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
#找到影片相关内容
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)

#爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0, 10):    #调用获取页面信息函数10次
        url = baseurl + str(i*25)
        html = askURL(url)   #保存获取的网页

        #2.逐一解析数据
        soup = BeautifulSoup(html,"html.parser")
        for item in  soup.find_all('div', class_="item"):  #查找符合要求字符串形成列表
            #print(item)  #测试查看获取的item信息
            data = []
            item = str(item)
            link = re.findall(findLink, item)[0]
            data.append(link)
            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)
            Titles = re.findall(findTitle, item)   #可能有一个中文名字和其它名字
            if len(Titles)==2:
                ctitle = Titles[0]
                data.append(ctitle)
                otitle = Titles[1].replace("/", "")   #去掉无关的符合
                data.append(otitle)
            else:
                data.append(Titles[0])
                data.append(" ")       # 外国名留空
            Rating = re.findall(findRating, item)[0]
            data.append(Rating)
            Judge = re.findall(findJudge, item)[0]
            data.append(Judge)
            Inq = re.findall(findInq, item)
            if len(Inq) != 0:
                Inq = Inq[0].replace("。", ",")  # 去掉句号
                data.append(Inq)
            else:
                data.append(" ")
            Bd = re.findall(findBd, item)[0]
            Bd = re.sub('<br(\s+)?/>(\s+)?', "", Bd)
            Bd = re.sub('/', '', Bd)
            data.append(Bd.strip())

            datalist.append(data)  # 将处理好的一部电影放入datalist


    return datalist

#得到指定url内容
def askURL(url):
    head = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36"
    }
    request = urllib.request.Request(url, headers=head)
    #html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
       # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html

#3.保存数据
def saveData(datalist, savepath):

    work = xlwt.Workbook(encoding="utf-8")
    sheet = work.add_sheet("TOP250", cell_overwrite_ok=True)
    col = ("电影详情链接","图片链接","影片中文名","影片外国名","评分","评分人数","概况","相关信息")
    for i in range(0, 8):
        sheet.write(0, i, col[i]) # 列名
    for i in range(0, 250):
        print("EXCL中插入第%d条" % (i+1))
        data = datalist[i]
        for j in range(0, 8):
            sheet.write(i+1, j, data[j])

    work.save(savepath)

def  save2db(datalist):
    conn = sqlite3.connect("douban.db")
    cur = conn.cursor()
    try:
        createtable = """
           create table if not exists top250
             ( id INTEGER primary key autoincrement,
               link text,
               imgsrc text,
               title text not null,
               otitle text,
               rating real,
               judge text,
               inq text,
               bd text);
           """
        cur.execute(createtable)
    except:
        print("create talbe failed ,table has exists")
    for i in range(0, 250):
        print("数据库中插入第%d条" % (i + 1))
        data = datalist[i]
        for j in range(0, 8):
            data[j] = '"'+data[j]+'"'

        insert_top = """
            insert into  top250
           (link,imgsrc,title,otitle,rating,judge,inq,bd) 
           values (%s);"""%",".join(data)

        cur.execute(insert_top)
        conn.commit()
    cur.close()
    conn.close()

def downimg():
    head = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36"
    }
    picpath = os.path.abspath('..')+"\\doudemon\\static\\assets\\img\\portfolio\\"
    conn = sqlite3.connect("douban.db")
    cur = conn.cursor()
    imgsrc = cur.execute("select imgsrc from top250 where id < 4;")
    for img in imgsrc:
        if not os.path.isfile(picpath+img.split('/')[7]):
            urllib.request.urlretrieve(img, filename=img.split('/')[7])






if __name__ == '__main__':
    #main()
    downimg()
    print("抓取完成")