from datetime import datetime
import yfinance
import functools


class YahooFinance:
    def __init__(self) -> None:
        pass
    def get_stock_history(self,stockName, startDate, end_date=datetime.today().strftime('%Y-%m-%d')):
        try:
            if(isinstance(stockName,str) != True):
                raise Exception("The input is not string")
            data = yfinance.download(stockName, start=startDate,end=end_date,interval="1mo")
            time_price = list(map(lambda x: [x[0].strftime('%Y-%m-%d'),x[1][3]], data.iterrows()))
            result = list(filter(lambda data: data[1] == data[1] , time_price))
            return result
        except Exception as ex:
            return []
    def buying_plan(self, stockName, startDate, pay_per_month):
        try:
            price_history = self.get_stock_history(stockName,startDate)
            if(len(price_history) == 0):
                return [{'date':0, 'shares': 0, 'cost': 0}]
            buying_history = list(map(lambda element: self.__buying_history_calculator(element[0],element[1],pay_per_month) , price_history))
            return buying_history
        except Exception as ex:
            return [{'date':0, 'shares': 0, 'cost': 0}]


    def __buying_history_calculator(self,date,stock_price,pay_per_month):
        try:
            shares = int(int(pay_per_month)/stock_price)
            return {'date':date, 'price':stock_price ,'shares': shares, 'cost': shares*stock_price}
        except Exception as ex:
            print(ex)
            return {'date':date, 'price':stock_price ,'shares': 0, 'cost': 0*stock_price}

    def calculate_profit(self, stockName, startDate, pay_per_month):
        try:
            buying_history = self.buying_plan(stockName,startDate,pay_per_month)
            # combine the cost and share by using reduce
            total = functools.reduce(lambda x,y : {'shares': (x['shares']+y['shares']), 'cost':(x['cost']+y['cost'])}, buying_history, {'date':0, 'shares': 0, 'cost': 0})
            # last of the element is the latest price.
            netLiq = total['shares'] * buying_history[buying_history.__len__()-1]['price']
            profit = netLiq -total['cost']
            return {'stockName': stockName,'profit':profit, 'netLiq':netLiq, 'cost':total['cost'], 'startDate':startDate}
        except Exception as ex:
            return {'stockName': '','profit':'', 'netLiq':'', 'cost':'', 'startDate':'' }

def main():
    yf = YahooFinance()
    buying_history = yf.buying_plan('MSFT','2021-01-01',300)
    print(buying_history)
    total = functools.reduce(lambda x,y : {'shares': (x['shares']+y['shares']), 'cost':(x['cost']+y['cost'])}, buying_history, {'date':0, 'shares': 0, 'cost': 0})
    asset = total['shares'] * buying_history[buying_history.__len__()-1]['price']
    profit = asset -total['cost']
    print('profit: {0} total asset: {1} toal cost: {2}'.format(profit,asset,total['cost']))

if(__name__ == '__main__'):
	main()