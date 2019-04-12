# coding=utf-8
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz, process
from fake_useragent import UserAgent
import time
import random
import os
from twilio.rest import Client
import threading

class PreSaleQuery():
    def __init__(self, cinemaID, movieID, dateID):
        self.cinemaID = cinemaID
        self.movieID = movieID
        self.dateID = dateID
        self.onsale_movies = []
        self.checkTimes = 2
        self.message = ""
        self.movieName = None
        self.movieName_eng = None
        self.cinemaName = None

    def getMovieName(self):
        target = 'https://maoyan.com/films/' + str(self.movieID)
        header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"}
        req = requests.get(url=target, headers=header)
        html = req.text
        bf = BeautifulSoup(html, 'html.parser')
        movie_html = bf.find_all('h3', class_='name')
        self.movieName = movie_html[0].get_text()
        movie_html = bf.find_all('div', class_='ename ellipsis')
        self.movieName_eng = movie_html[0].get_text()

    def checkSell(self):
        target = 'https://maoyan.com/cinema/'+str(self.cinemaID)
        # html = req.text
        # bf = BeautifulSoup(html, 'html.parser')
        # Fake User Agent
        # ua = UserAgent(verify_ssl=False)
        # header = {"User-Agent": ua.random}
        header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"}
        # try:
        #     req = requests.get(url=target, headers=header, proxies=self.getProxy(),timeout=10)
        # except:
        req = requests.get(url=target, headers=header)
        html = req.text
        bf = BeautifulSoup(html, 'html.parser')
        cinema_title_html = bf.find_all('h3', class_='name text-ellipsis')
        self.cinemaName = cinema_title_html[0].get_text()
        onsale_movies_html = bf.find_all('a', class_='buy-btn normal')
        for movie in onsale_movies_html:
            sell_link = movie.get('href').strip('/xseats/')
            if 'cinemaId='+str(self.cinemaID) in sell_link and 'movieId='+str(self.movieID) in sell_link and str(self.dateID) == sell_link[:8]:
                print("Found!")
                return True
        print(self.movieName,self.movieName_eng,self.cinemaName, self.dateID,"Not Found!")
        return False

    def getProxy(self):
        api = requests.get("http://ip.jiangxianli.com/api/proxy_ip")
        proxyData = api.json()
        proxy = 'http:\\' + proxyData['data']['ip'] + ':' + proxyData['data']['port']
        proxies = {'proxy': proxy}
        return proxies

    def messaging(self):

        self.message = self.cinemaName + " 《" + self.movieName + "》" + self.movieName_eng + " "+ str(self.dateID) + " 开售啦！"
        # Your Account SID from twilio.com/console
        account_sid = "AC117049c0a5b24dd11f72f9a433866468"
        # Your Auth Token from twilio.com/console
        auth_token = "c86273c4c2e53052d0dde129fbe6c48f"
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            to="+8615626281204",
            from_="+12039417796",
            body=self.message)

    def loopCheck(self):
        while not self.checkSell():
            time.sleep(random.randint(30,300))
            formatTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print("> 检查时间：", formatTime)
            print("> 电影：", self.movieName, self.movieName_eng)
            print("> 影院：", self.cinemaName)
            print("= 第{}次查询".format(self.checkTimes))
            # os.system("cls")
            self.checkTimes += 1
        try:
            self.messaging()
        except Exception as e:
            self.messaging()


def gogo():
    cinemaID = 14409
    movieID = 248172
    dateID = 20190424
    ps = PreSaleQuery(cinemaID, movieID, dateID)
    ps.getMovieName()
    ps.loopCheck()

def gogo_sat():
    cinemaID = 14409
    movieID = 248172
    dateID = 20190427
    ps = PreSaleQuery(cinemaID, movieID, dateID)
    ps.getMovieName()
    ps.loopCheck()

def wanda():
    cinemaID = 16769
    movieID = 248172
    dateID = 20190424
    ps = PreSaleQuery(cinemaID, movieID, dateID)
    ps.getMovieName()
    ps.loopCheck()


def wanda_sat():
    cinemaID = 16769
    movieID = 248172
    dateID = 20190427
    ps = PreSaleQuery(cinemaID, movieID, dateID)
    ps.getMovieName()
    ps.loopCheck()

def cgv():
    cinemaID = 26470
    movieID = 248172
    dateID = 20190424
    ps = PreSaleQuery(cinemaID, movieID, dateID)
    ps.getMovieName()
    ps.loopCheck()

def cgv_sat():
    cinemaID = 26470
    movieID = 248172
    dateID = 20190427
    ps = PreSaleQuery(cinemaID, movieID, dateID)
    ps.getMovieName()
    ps.loopCheck()

if __name__ == '__main__':
    t = threading.Thread(target=gogo,args = [])
    t.start()  #线程启动
    t = threading.Thread(target=gogo_sat,args = [])
    t.start()  #线程启动
    t = threading.Thread(target=wanda,args = [])
    t.start()  #线程启动
    t = threading.Thread(target=wanda_sat,args = [])
    t.start()  #线程启动
    t = threading.Thread(target=cgv,args = [])
    t.start()  #线程启动
    t = threading.Thread(target=cgv_sat,args = [])
    t.start()  #线程启动



