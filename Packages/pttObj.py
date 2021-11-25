from bs4 import BeautifulSoup
import requests
from datetime import datetime
from collections import namedtuple
class PttPage():
    # def __init__(self,topic,num) -> None:
    #     # get url of first page
    #     url = self.__getPageUrlByNumb(topic,num)
    #     page = requests.get(url)
    #     # Make the soup global and able to be called across the functions.
    #     self.__soup = BeautifulSoup(page.content,"html.parser")
    #     btn_urls = self.__get_btn()
    #     self.last_page_url = btn_urls[1]
    #     self.next_page_url = btn_urls[2]
    #     self.articles_list = self.__get_list_articles(url)

    def __init__(self,url) -> None:
        page = requests.get(url)
        # Make the soup global and able to be called across the functions.
        self.__soup = BeautifulSoup(page.content,"html.parser")
        btn_urls = self.__get_btn()
        self.last_page_url = btn_urls[1]
        self.next_page_url = btn_urls[2]
        r_ent_nodes = self.__soup.find_all('div',class_='r-ent')
        self.title_url = list(map(self.__get_article_attrs, r_ent_nodes))

    def __get_btn(self):
        btn_nodes = self.__soup.find_all('a', class_='btn wide')
        btn_urls = list(map(self.__get_href, btn_nodes))
        return btn_urls

    def __get_href(self,node):
        try:
            return "https://www.ptt.cc" + node.get('href')
        except Exception as ex:
            return None

    def get_list_articles(self):
        urls = list(map(lambda x:x['url'], self.title_url))
        return list(map(self.__to_pttArticles, urls))

    def get_article(self, url):
        return self.__to_pttArticles(url)

    def __get_article_attrs(self,node):
        try:
            href = node.find("a",href=True).get('href')
            date = node.find("div",class_='date').text.strip()
            title = node.find("a",href=True).text.strip()
            title = namedtuple("Crime", ['title','date','url'])
            return  {'title':title,'date':date, 'url':"https://www.ptt.cc" + href}
        except Exception as ex:
            return None
    def searchByDate(self,start_date,end_date):
            search_result = []
            for obj in self.title_url:
                obj['title']
                pass
    def searchByTitle(self,title):
            pass

    # def __getPageUrlByNumb(self,topic,num):
    #     base_url = "https://www.ptt.cc/bbs/{0}/index{1}.html"
    #     return base_url.format(topic,num)

    def __to_pttArticles(self,url):
        try:
            return PttArticle(url)
        except Exception as ex:
            return None

    def __filter_article_node(self,tag):
        if(len(tag.find_parents("div", class_="title"))>0):
            return True
        else:
            return False

class PttPush():
    def __init__(self,user,comment) -> None:
        self.user = user
        self.comment = comment
        pass

class PttArticle():
    author = ''
    title = ''
    date = None
    pushs = None
    def __init__(self,url) -> None:
        try:
            if url is None:
                raise Exception('url is None')
            page = requests.get(url)
            self.__soup = BeautifulSoup(page.content,"html.parser")
            push_nodes = self.__soup.find_all("div", class_="push")
            metaline_nodes = self.__soup.find_all("span", class_="article-meta-value")
            metalines = list(map(lambda x:x.text,metaline_nodes))
            # The result of metalines should be like ['androider (androider)','Stock','[新聞] MSCI最新季調\u3000台灣成分股增3剔3檔','Fri Nov 12 07:56:25 2021']
            if(len(metaline_nodes) != 4):
                return
            self.author = metalines[0]
            self.title = metalines[2]
            # Example of the datetime format: Fri Nov 12 15:32:45 2021
            self.date = datetime.strptime(metalines[3], '%a %b %d %H:%M:%S %Y')
            self.url = url
            if (len(push_nodes) > 0):
                self.pushs = list(map(self.__to_push_array,push_nodes))
        except Exception as ex:
            raise Exception('Fail to parse the url {0}. error msg= {1}'.format(url,ex))

    def __to_push_array(self,node):
        user = node.find("span",class_="f3 hl push-userid").text.strip()
        comment = node.find("span",class_="f3 push-content").text.replace(': ','')
        return PttPush(user,comment)

        
def main():
    pttPage = PttPage("https://www.ptt.cc/bbs/Stock/index30.html")
    print(pttPage.last_page_url)
    print(pttPage.next_page_url)
    print(pttPage.title_date_urls)
    result = pttPage.get_list_articles()
    print(result[0].title)
    print(result[0].author)
    print(result[0].url)

if __name__=='__main__':
    main()