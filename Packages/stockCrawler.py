from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import requests
import twstock
from telethon import TelegramClient
from telethon import functions, types
from datetime import datetime
from telethon.tl.types import InputPeerChat
import json


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
        twStockFiltered=list(filter(lambda x:x[1].type == '股票',twstock.twse.items()))
        self.twStocksList = list(map(lambda x:x[1].name,twStockFiltered))


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

    def get_today_chichatting_context(self,date,stocks='none'):
        try:
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
        except Exception as ex:
            print(ex)

    def get_comments(self, stocks, start, end):
        pass




class telgramCrawler(crawler):
    def __init__(self,config_path) -> None:
        super().__init__()
        with open(config_path, "r") as f:
            self.config = json.load(f)

    async def get_comments(self, stock_name, start_date, end_date):
        try:
            peerChat = InputPeerChat(1301096229)
            async with TelegramClient(self.config['username'], self.config['api_id'],self.config['api_hash']) as client:
                chat = await client.get_input_entity(1301096229)
                result = await client(functions.messages.SearchRequest(
                    peer=chat,
                    q=stock_name,
                    filter=types.InputMessagesFilterEmpty(),
                    min_date=datetime.strptime(start_date, '%Y-%m-%d'),
                    max_date=datetime.strptime(end_date, '%Y-%m-%d'),
                    offset_id=0,
                    add_offset=0,
                    limit=100,
                    max_id=0,
                    min_id=0,
                    hash=0,
                    from_id=None ,
                    top_msg_id=None 
                ))
            comments = list(map(lambda x:(x.date.strftime("%Y-%m-%d")),result.messages))
            return True, comments
        except Exception as ex:
            return False, ex


def main():
    pass

if __name__=='__main__':
    main()
