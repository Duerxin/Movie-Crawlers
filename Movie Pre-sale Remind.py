import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz, process
from fake_useragent import UserAgent
import time
import random
import os
from twilio.rest import Client

class PreSaleQuery():
    def __init__(self, cinemaId, movieName):
        self.cinemaId = cinemaId
        self.movieName = movieName
        self.onsale_movies = []
        self.checkTimes = 2
        self.message = ""

    def getPage(self):
        target = 'https://maoyan.com/cinema/'+str(self.cinemaId)

        # Fake User Agent
        ua = UserAgent(verify_ssl=False)
        header = {"User-Agent": ua.random}
        req = requests.get(url=target, headers=header, proxies=self.getProxy(),timeout=10)
        html = req.text
        bf = BeautifulSoup(html, 'html.parser')
        cinema_title_html = bf.find_all('h3', class_='name text-ellipsis')
        onsale_movies_html = bf.find_all('h3', class_='movie-name')
        self.onsale_movies = []
        for movie in onsale_movies_html:
            self.onsale_movies.append(movie.get_text())
        formatTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("> 检查时间：", formatTime)
        print("> 电影：", self.movieName)
        print("> 影院：", cinema_title_html[0].get_text())
        self.message = cinema_title_html[0].get_text() + " 《" + self.movieName + "》 开售啦！"

    def getProxy(self):
        api = requests.get("http://ip.jiangxianli.com/api/proxy_ip")
        proxyData = api.json()
        proxy = 'http:\\' + proxyData['data']['ip'] + ':' + proxyData['data']['port']
        proxies = {'proxy': proxy}
        return proxies

    def accurateCheck(self):
        print("> 精准匹配结果：", end="")
        if self.movieName in self.onsale_movies:
            print("已经开售啦！")
            return True
        else:
            print("尚未查询到结果！")
            return False

    def fuzzCheck(self):
        print("> 模糊匹配结果：", end="")
        fuzz_result = process.extractOne(self.movieName, self.onsale_movies, score_cutoff=50)
        if fuzz_result == None:
            print("模糊匹配尚未查询到结果！")
            return False
        else:
            print(fuzz_result[0], "模糊查询最匹配结果！相似度：", fuzz.partial_ratio(self.movieName, fuzz_result[0]))
            return True

    def messaging(self):

        # Your Account SID from twilio.com/console
        account_sid = "x"
        # Your Auth Token from twilio.com/console
        auth_token = "x"
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            to="+xxx",
            from_="+xxx",
            body=self.message)

    def loopCheck(self):
        ps.getPage()
        while not ps.accurateCheck() and not ps.fuzzCheck():
            time.sleep(random.randint(5,30))
            os.system("cls")

            print("= 第{}次查询".format(self.checkTimes))
            ps.getPage()
        self.messaging()
        return
#


if __name__ == '__main__':
    cinemaID = 14409
    search_movie = '复仇者联盟4：终局之战'
    # search_movie = '小飞象'
    ps = PreSaleQuery(cinemaID, search_movie)
    ps.loopCheck()


