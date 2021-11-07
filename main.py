import requests
import lxml
import sqlite3
import twstock
import Packages.localDb
from bs4 import BeautifulSoup
from datetime import date
from Packages.stockCrawler import pttCrawler


def get_comment_content(url,date):
    stock_page = requests.get(url)
    stock_soup = BeautifulSoup(stock_page.content,"html.parser")
    article = stock_soup.find_all(lambda tag: tag.name == "a" and date in tag.text)

    if(len(article) == 0):
        raise Exception("The crawler cannot find the article based on the date {0}".format(date))

    art_URL = "https://www.ptt.cc/" + article[0]['href']
    art_page = requests.get(art_URL)
    art_soup = BeautifulSoup(art_page.content,"html.parser")
    result = art_soup.findAll("span", {"class": "f3 push-content"})
    return result

def get_matching_comments(comments_list):
    result = dict()
    if(len(comments_list) ==0):
        raise Exception("The input of the function is null or empty.")

    stocks_list =[ v.name for k,v in twstock.twse.items()]
    for stock in stocks_list:
        matching = [comment.text.replace(": ","") for comment in comments_list if stock in comment.text]
        if len(matching) != 0:
            result[stock] = matching
    return result



def main():
    try:
        db = localDb.sqliteDb("C:\\db\\stockdb.db")
        url = "https://www.ptt.cc/bbs/Stock/index.html"
        today = date.today().strftime("%Y-%m-%d")
        crawler = pttCrawler()
        stock_comments = crawler.get_chichatting_context(today.replace('-','/'))        

        for stock,comments in stock_comments.items():
            url = "http://127.0.0.1:5000//StockData/{0}/{1}"
            data  = {"comments":comments}
            result = requests.post(url.format(stock,today),json=data)
    except Exception as ex:
        print("There is error in the code. Error msg={0}".format(ex))



if __name__=='__main__':
    main()



