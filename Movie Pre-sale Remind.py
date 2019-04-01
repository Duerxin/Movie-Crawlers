import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz, process
import time

class PreSaleQuery():
    def __init__(self, cinemaId, movieName):
        self.cinemaId = cinemaId
        self.movieName = movieName
        self.onsale_movies = []

    def getPage(self):
        target = 'https://maoyan.com/cinema/'+str(self.cinemaId)
        req = requests.get(url=target)
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

if __name__ == '__main__':
    cinemaID = 14409
    search_movie = '比悲伤更悲伤的故事'
    ps = PreSaleQuery(cinemaID, search_movie)
    ps.getPage()
    if not ps.accurateCheck():
        ps.fuzzCheck()


