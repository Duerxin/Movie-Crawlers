import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz, process
from fake_useragent import UserAgent
import time
import random
import os

class PreSaleQuery():
    def __init__(self, cinemaId, movieName):
        self.cinemaId = cinemaId
        self.movieName = movieName
        self.onsale_movies = []
        self.checkTimes = 2

    def getPage(self):
        target = 'https://maoyan.com/cinema/'+str(self.cinemaId)

        # Fake User Agent
        ua = UserAgent(verify_ssl=False)
        header = {"User-Agent": ua.random}
        req = requests.get(url=target, headers=header)
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

    def loopCheck(self):
        ps.getPage()
        while not ps.accurateCheck() and not ps.fuzzCheck():
            time.sleep(random.randint(5,30))
            os.system("cls")

            print("= 第{}次查询".format(self.checkTimes))
            ps.getPage()


if __name__ == '__main__':
    cinemaID = 14409
    search_movie = '雷霆沙赞'
    ps = PreSaleQuery(cinemaID, search_movie)
    ps.loopCheck()


