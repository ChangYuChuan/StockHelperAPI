
from bs4 import BeautifulSoup
import requests
from datetime import datetime


class PttObj():
    """Objectfy the ptt page based on topic and number."""
    def __init__(self, topic:str = 'stock',number:int=0) -> None:
        if(topic == '' or number < 0):
            raise Exception('Input parameters passed to constructor are not correct')
        self.topic = topic
        self.number = number
        ptt_url = "https://www.ptt.cc/bbs/{0}/index{1}.html".format(topic,number)
        self.__page_html = requests.get(ptt_url)
        
        if str(self.__page_html).find("404") != -1:
            raise Exception("cannot request the url: {0}".format(ptt_url))
        
        self.__soup = BeautifulSoup(self.__page_html.content,"html.parser")
        btn_urls = self.__get_btn()
        self.__last_page_url = btn_urls[1]
        self.__next_page_url = btn_urls[2]
    @property
    def last_page_url(self):
        return self.__last_page_url
    @property
    def next_page_url(self):
        return self.__next_page_url

    def next_page(self):
        try:
            return PttObj(self.topic,self.number+1)
        except Exception as ex:
            return None 
    
    def last_page(self):
        try:
            return PttObj(self.topic,self.number-1)
        except Exception as ex:
            return None 
   
    def __get_btn(self):
        try:
            """get the button user click to move to next page or last page."""
            btn_urls = None
            btn_nodes = self.__soup.find_all('a', class_='btn wide')
            btn_urls = list(map(lambda node: "https://www.ptt.cc" + node.get('href'), btn_nodes))
            if(btn_urls is None or len(btn_urls) == 0):
                raise Exception('url of button is None or empty')
            return btn_urls
        except Exception as ex:
            raise Exception('Fail to get the url of button error msg= {0}'.format(ex))

    def __get_article_info(self,node):
        try:
            href = node.find("a",href=True).get('href')
            date = node.find("div",class_='date').text.strip()
            title = node.find("a",href=True).text.strip()
            return  PttArticleInfo(title,date,"https://www.ptt.cc" + href)
        except Exception as ex:
            return None

    def get_articles_list(self, filter_keyword:str =None ):
        """get the list of the article info including title, date, url"""
        r_ent_nodes = self.__soup.find_all('div',class_='r-ent')
        info_list = []
        info_list = list(map(self.__get_article_info,r_ent_nodes))
        if filter_keyword != None and (info_list != None and len(info_list)>0):
            filtered_info_list = list(filter(lambda info: info != None and (filter_keyword not in info.title) , info_list))
            return filtered_info_list
        
        return info_list
    def move_to(self,number:int):
        try:
            return PttObj(self.topic,int(number))
        except Exception as ex:
            print('Cannot move to the topic:{0},number:{1}. error message={2}'.format(self.topic,number,ex))
            return None
    def get_first_article(self):
        articleList = self.get_articles_list()
        for i in range(len(articleList)):
            articleInfo = articleList[i]
            if articleInfo is None:
                continue
            return articleInfo


class PttArticleInfo():
    def __init__(self,title,date,url) -> None:
        self.title = title
        self.url = url
        self.date = date
    def read(self):
        try:
            return PttArticleContent(self.url)
        except Exception as ex:
            print('Unable to create PttArticleContent object')
            return None
        
        

class PttPushInfo():
    def __init__(self,user,comment) -> None:
        self.user = user
        self.comment = comment

class PttArticleContent():
    def __init__(self,url) -> None:
        try:
            if url is None or url == '':
                raise Exception('url is empty or None')
            page = requests.get(url)
            self.__soup = BeautifulSoup(page.content,"html.parser")
            push_nodes = self.__soup.find_all("div", class_="push")
            metaline_nodes = self.__soup.find_all("span", class_="article-meta-value")
            metalines = list(map(lambda x:x.text,metaline_nodes))
            # The result of metalines should be like ['androider (androider)','Stock','[新聞] MSCI最新季調\u3000台灣成分股增3剔3檔','Fri Nov 12 07:56:25 2021']
            if(len(metaline_nodes) != 4):
                raise Exception('cannot get at least 4 metaline nodes')
            self.author = metalines[0]
            self.title = metalines[2]
            # Example of the datetime format: Fri Nov 12 15:32:45 2021
            self.date = datetime.strptime(metalines[3], '%a %b %d %H:%M:%S %Y')
            self.url = url
            self.pushs_list = []
            if (len(push_nodes) > 0):
                self.pushs_list = list(map(self.__to_push_array,push_nodes))
        except Exception as ex:
            raise Exception('Fail to parse the url {0}. error msg= {1}'.format(url,ex))

    def __to_push_array(self,node):
        try:
            user = node.find("span",class_="f3 hl push-userid").text.strip()
            comment = node.find("span",class_="f3 push-content").text.replace(': ','')
            return PttPushInfo(user,comment)
        except Exception as ex:
            return PttPushInfo(None,None)
       

        
def main():
    # pttPage = PttPage("https://www.ptt.cc/bbs/Stock/index30.html")
    # print(pttPage.last_page_url)
    # print(pttPage.next_page_url)
    # print(pttPage.title_date_urls)
    # result = pttPage.get_list_articles()
    # print(result[0].title)
    # print(result[0].author)
    # print(result[0].url)
    # pttPage = PttObj("https://www.ptt.cc/bbs/Stock/index0.html")
    # articleInfo = pttPage.get_articles_list('[公告]')
    # for article in articleInfo:
    #     print(article.title)
    article = PttArticleContent('https://www.ptt.cc/bbs/Stock/M.1645489820.A.97B.html')
    for push in article.pushs_list:
        print(push.comment)



if __name__=='__main__':
    main()