from abc import ABC, abstractmethod
import traceback
from telethon import TelegramClient
from telethon import functions, types
from datetime import datetime, timedelta
from telethon.tl.types import InputPeerChat
import json
from .pttObj import PttObj
import asyncio
import twstock 
import jieba
import re
from collections import defaultdict


class crawler(ABC):

    @abstractmethod
    async def get_comments(self,stocks:list,start_date,end_date,lim):
        """
        stocks: list of stocks
        start: string of "%Y/%m/%d"
        end: string of "%Y/%m/%d"
        output: stock:[comment1,comment2...]
        """
        pass

class PttCrawler(crawler):
    def __init__(self) -> None:
        #self.base_url = "https://www.ptt.cc/bbs/Stock/index0.html"
        twStockFiltered=list(filter(lambda x:x[1].type == '股票', twstock.twse.items()))
        self.twStocksSet = set(map(lambda x:x[1].name,twStockFiltered))
        jieba.load_userdict('./stock_list.txt')
        
    def get_comments(self, target_stocks, start_date, end_date,limit=None):
        new_date=datetime.strptime(start_date, '%Y/%m/%d')
        old_date=datetime.strptime(end_date, '%Y/%m/%d')
        # prevent the inputs from being swapped.
        if(new_date<old_date):
            return self.get_comments(target_stocks,end_date,start_date,limit)
        # prevent future input.
        if(datetime.now() < new_date):
            new_date = datetime.now()
        if(target_stocks is None):
            target_stocks = []
        pttObj = PttObj()
        collected_comments = self.collect_pushInfo(pttObj,target_stocks,old_date,new_date,limit)
        # group the values by same key
        ddic = defaultdict(list)
        for kvp in collected_comments:
            print(kvp)
            for key,val in kvp.items():
                print('{0} {1}'.format(key,val))
                ddic[key.strftime('%Y-%m-%d')].extend(val)
        return dict(ddic)
    
    def __collect_pushInfo_by_loop(self, pttObj:PttObj, target_stocks:list,old_date:datetime, new_date:datetime,limit:int):
        if(old_date > new_date):
            return self.collect_pushInfo_by_loop(pttObj,target_stocks,new_date,old_date)
        new_date = new_date.replace(hour=23,minute=59,second=59)
        result = []
        count = 0
        loop_each_article = False
        current_article = None
        while(pttObj != None):
            articleInfo_list = pttObj.get_articles_list(filter_keyword='[公告]')
            # if thearticle info is empty, move to last page.
            if(len(articleInfo_list)==0):
                print('Unable to resolve the article list')
                continue
            # to get the avaialbe and usable first article on the page.
            for i in range(len(articleInfo_list)):
                current_article = articleInfo_list[i].read()
                if(current_article is None):
                    print('Unable to resolve the article')
                    continue
                break
            #Determine to loop the each article on the page or move to next|last one.
            # if we decide not to loop the article, we start move the page by page
            if(loop_each_article == False):
                if( old_date < current_article.date and current_article.date < new_date ):
                    pttObj = pttObj.next_page()
                    loop_each_article = True
                    continue
            # if we decide loop the article on the page
            else:
                for i in range(len(articleInfo_list)):
                    current_article = articleInfo_list[i].read()
                    if(current_article is None):
                        print('Unable to resolve the article')
                        continue
                    
                    if(new_date < current_article.date ):
                        continue
                    if(current_article.date < old_date ):
                        return result
                    if(limit != None and count > int(limit)):
                        return result
                    filterd_pushs = self.__find_keyword(target_stocks,current_article.pushs_list)
                    count = count + len(filterd_pushs)
                    result.append({current_article.date.date():filterd_pushs})
                    print('result counts: {0}'.format(count))
                    
            pttObj = pttObj.last_page()
        return []

    def __find_keyword(self,keyword_list:list = [], pushInfoList: list = [])->list:
        if not isinstance(keyword_list,list):
            return []
        result = []
        # No specific key word or keyword_list is empty. Use default tw stock list.
        if keyword_list == None or len(keyword_list) == 0:
            filter_word = self.twStocksSet
        else:
            filter_word = set(keyword_list)
        # loop the input: pushInfoList
        for pushInfo in pushInfoList:
            seq_list=''
            try:
                if(pushInfo.comment == None or pushInfo.comment == ''):
                    continue
                seq_list = jieba.cut(pushInfo.comment)
                if(seq_list is None ):
                    continue
                # if the comment which is cutted by jieba intersect the stock list, collect the comment
                if len(filter_word.intersection(set(seq_list))) > 0:
                    result.append(pushInfo.comment)
            except Exception as ex:
                print('Failed to search the key word in comment {0}  error msg= {1}'.format(pushInfo.comment ,ex))
                continue
        return result

    def collect_pushInfo(self, pttObj:PttObj, target_stocks:list,old_date:datetime, new_date:datetime,limit:int):
        result = []
        try:
            digits = re.findall(r'\d+', pttObj.move_to(0).last_page_url)
            first_page_number = 1
            last_page_number = digits[0]
            target_number = self.__find_page_number_by_BS(int(first_page_number),int(last_page_number),new_date,pttObj)
            target_number = int(target_number)
            print('target_number:{0}'.format(target_number))
            if(target_number == -1):
                raise Exception('Cannot find target number')
            startObj = pttObj.move_to(target_number)
            return self.__collect_pushInfo_by_loop(startObj,target_stocks,old_date,new_date,limit)
        except Exception as ex:
            traceback.print_exc()
            return []


    def __find_page_number_by_BS(self,left_num, right_num, target_date:datetime, pttObj:PttObj):
        mid_number = left_num + ( right_num - left_num)/2
        mid_number = int(mid_number)
        articleInfo = pttObj.move_to(mid_number).get_first_article()
        mid_date = articleInfo.read().date
        target_date_start  = target_date.replace(hour=0,minute=0,second=0) - timedelta(days=7)
        target_date_end = target_date.replace(hour=23,minute=59,second=59)

        print('mid_number:{0} mid_date:{1}'.format(mid_number,mid_date))
        if(left_num <= right_num):
            if( target_date_start <= mid_date and mid_date <= target_date_end):
                return mid_number
            if(mid_date <= target_date_end):
                return self.__find_page_number_by_BS(mid_number+1,right_num,target_date,pttObj)
            if(target_date_end <= mid_date):
                return self.__find_page_number_by_BS(left_num,mid_number-1,target_date,pttObj)
        return -1
            

        

class TelgramCrawler(crawler):
    def __init__(self,config_path) -> None:
        super().__init__()
        with open(config_path, "r") as f:
            self.config = json.load(f)

    async def get_comments(self, stock_name, start_date, end_date, limit):
        if(stock_name is None or stock_name == ''):
            raise Exception('stock_name cannot be None or empty')
        peerChat = InputPeerChat(1301096229)
        async with TelegramClient(self.config['username'], self.config['api_id'],self.config['api_hash']) as client:
            chat = await client.get_input_entity(1301096229)
            result = await client(functions.messages.SearchRequest(
                peer=chat,
                q=stock_name,
                filter=types.InputMessagesFilterEmpty(),
                min_date=datetime.strptime(start_date, '%Y/%m/%d'),
                max_date=datetime.strptime(end_date, '%Y/%m/%d'),
                offset_id=0,
                add_offset=0,
                limit=int(limit),
                max_id=0,
                min_id=0,
                hash=0,
                from_id=None ,
                top_msg_id=None 
            ))
        collected_comments = list( map(lambda x: {x.date.date(): x.message}, result.messages))
        # group the values by same key
        ddic = defaultdict(list)
        for kvp in collected_comments:
            print(kvp)
            for key,val in kvp.items():
                print('{0} {1}'.format(key,val))
                ddic[key.strftime('%Y-%m-%d')].append(val)
        print(ddic)
        return dict(ddic)


async def main():
    crawler = TelgramCrawler("C:\\Config\\telegram_config.json")
    # crawler = PttCrawler()
    result = crawler.get_comments('台積電','2021/12/31','2022/3/1',100)
    # jieba.load_userdict('./stock_list.txt')
    # twStockFiltered=list(filter(lambda x:x[1].type == '股票', twstock.twse.items()))
    # twStocksSet = set(map(lambda x:x[1].name,twStockFiltered))
    # result = []
    # article = PttArticleContent('https://www.ptt.cc/bbs/Stock/M.1645103535.A.C45.html')
    # print(article.date)
    # for push in article.pushs_list:
    #     print(push.comment)
    #     if(push.comment == None):
    #         continue
    #     seq_list = set(jieba.cut(push.comment))
    #     print('origin: {0} jieba: {1}'.format(push.comment,'/'.join(seq_list)))
    #     if(len(twStocksSet.intersection(seq_list)) > 0):
    #         result.append(push.comment)
    #         print('Accepted')
    #     else:
    #         print('Denied')
    print(result)




def createFile():
    twStockFiltered=list(filter(lambda x:x[1].type == '股票', twstock.twse.items()))
    twStocksList = list(map(lambda x: "{0}\n".format(x[1].name),twStockFiltered))
    print(twStocksList)
    file_path = './stock_list.txt'
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(twStocksList)

if __name__=='__main__':
    asyncio.run(main())
