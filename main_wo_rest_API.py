from configparser import Interpolation
from bs4 import BeautifulSoup
from datetime import date
from Packages.stockCrawler import pttCrawler
from Packages.mysqlDb import mysqlDb



def main():
    try:
        db = mysqlDb()
        today = date.today().strftime("%Y-%m-%d")
        crawler = pttCrawler()
        stock_comments = crawler.get_today_chichatting_context(today.replace('-','/'))
        
        for stock_name,comments in stock_comments.items():
            db.add_stock_comment(stock_name,'PTT',today,comments)
        db.close()
    except Exception as ex:
        print("There is error in the code. Error msg={0}".format(ex))



if __name__=='__main__':
    main()



