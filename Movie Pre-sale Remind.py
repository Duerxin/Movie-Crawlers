import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz, process
import time

if __name__ == '__main__':
    target = 'https://maoyan.com/cinema/1676?poi=1448425'
    # search_movie = '复仇者联盟4：终局之战'
    search_movie = '比悲伤更悲伤的故事'
    req = requests.get(url=target)
    html = req.text
    bf = BeautifulSoup(html, 'html.parser')
    onsale_movies_html = bf.find_all('h3', class_ = 'movie-name')
    onsale_movies = []
    for movie in onsale_movies_html:
        onsale_movies.append(movie.get_text())

    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    print("目前检查时间：",otherStyleTime)

    print("精准匹配结果：\n===============")
    if search_movie in onsale_movies:
        print(search_movie, "，已经开售啦！")
    else:
        print(search_movie, "，尚未查询到结果！")

    print("\n模糊匹配结果：\n===============")
    fuzz_result = process.extractOne(search_movie, onsale_movies, score_cutoff=50)
    print("匹配结果：")
    if fuzz_result == None:
        print(search_movie, "，模糊匹配尚未查询到结果！")
    else:
        print(fuzz_result[0], "，模糊查询最匹配结果！相似度：", fuzz.partial_ratio(search_movie,fuzz_result[0]))

