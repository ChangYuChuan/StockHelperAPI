import requests
from datetime import date
from Packages.stockCrawler import pttCrawler



def main():
    try:
        url = "https://www.ptt.cc/bbs/Stock/index.html"
        today = date.today().strftime("%Y-%m-%d")
        crawler = pttCrawler()
        stock_comments = crawler.get_today_chichatting_context(today.replace('-','/'))
        if(stock_comments == None):
            raise Exception('The return from pttCrawler is empty')   

        for stock,comments in stock_comments.items():
            url = "http://127.0.0.1:5000//StockData/{0}/{1}"
            data  = {"comments":comments}
            result = requests.post(url.format(stock,today),json=data)
    except Exception as ex:
        print("There is error in the code. Error msg={0}".format(ex))
    finally:
        print('Complete the transition')


if __name__=='__main__':
    main()



