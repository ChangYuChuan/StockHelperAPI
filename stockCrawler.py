from bs4 import BeautifulSoup
from datetime import date
from abc import ABC, abstractmethod
import requests
import twstock


class crawler(ABC):

    @abstractmethod
    def get_comments(self,stocks,start,end):
        """
        stocks: list of stocks
        start: string of "%Y-%m-%d"
        end: string of "%Y-%m-%d"
        output: stock:[comment1,comment2...]
        """
        pass


class pttCrawler(crawler):
    def __init__(self) -> None:
        self.base_url = "https://www.ptt.cc/bbs/Stock/"
        self.twStocksList = [ v.name for k,v in twstock.twse.items()] 

    def __getPageUrlByNumb(self,num):
        return self.base_url + "index{0}.html".format(num)
    
    def __get_matching_comments(self,comments_list,stocks='none'):
        """
        return the comments in which user mentioned the name of specified stocks.
        If the input, stocks, is none, default of the stocks will be the all stocks listed in Taiwan stock market.
        """
        result = dict()
        stocks_list = list()

        if stocks == 'none':
            stocks_list = self.twStocksList
        else:
            stocks_list = stocks

        if(len(comments_list) ==0):
            raise Exception("The input of the function is null or empty.")

        for stock in stocks_list:
            matching = [comment.text.replace(": ","") for comment in comments_list if stock in comment.text]
            if len(matching) != 0:
                result[stock] = matching
        return result

    def get_chichatting_context(self,date,stocks='none'):
        # get url of first page
        url = self.__getPageUrlByNumb(0)
        page = requests.get(url)
        stock_soup = BeautifulSoup(page.content,"html.parser")
        article_node = stock_soup.find_all(lambda tag: tag.name == "a" and date in tag.text)
        if(len(article_node) == 0):
            raise Exception("The crawler cannot find the article based on the date {0}".format(date))
        cchat_URL = "https://www.ptt.cc/" + article_node[0]['href']
        cchat_page = requests.get(cchat_URL)
        cchat_soup = BeautifulSoup(cchat_page.content,"html.parser")
        comments_list = cchat_soup.findAll("span", {"class": "f3 push-content"})
        return self.__get_matching_comments(comments_list,stocks)

    def get_comments(self, stocks, start, end):
        pass




class telgramCrawler(crawler):
    def get_comments(self, stocks, start, end):
        pass


def main():
    crawler = pttCrawler()
    result = crawler.get_chichatting_context("2021/09/28",['長榮','陽明'])
    print(result)

if __name__=='__main__':
    main()
