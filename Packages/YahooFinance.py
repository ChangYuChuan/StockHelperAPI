from datetime import datetime
import yfinance
import functools


class YahooFinance:
    def __init__(self) -> None:
        pass
    def get_stock_history(self,stock, start_date, end_date=datetime.today().strftime('%Y-%m-%d')):
        try:
            if(isinstance(stock,str) != True):
                raise Exception("The input is not string")
            data = yfinance.download(stock, start=start_date,end=end_date,interval="1mo")
            time_price = list(map(lambda x: [x[0].strftime('%Y-%m-%d'),x[1][3]],data.iterrows()))
            result = list(filter(lambda data: data[1] == data[1] , time_price))
            return result
        except Exception as ex:
            return []
    def buying_plan(self, stock, start_date, pay_per_month):
        price_history = self.get_stock_history(stock,start_date)
        buying_history = list(map(lambda element: self.__buying_history_calculator(element[0],element[1],pay_per_month) , price_history))
        return buying_history

    def __buying_history_calculator(self,date,stock_price,pay_per_month):
        shares = int(pay_per_month/stock_price)
        return {'date':date, 'price':stock_price ,'shares': shares, 'cost': shares*stock_price}
        


def main():
    yf = YahooFinance()
    buying_history = yf.buying_plan('AAPL','2021-01-01',300)
    print(buying_history)
    total = functools.reduce(lambda x,y : {'shares': (x['shares']+y['shares']), 'cost':(x['cost']+y['cost'])}, buying_history, {'date':0, 'shares': 0, 'cost': 0})
    asset = total['shares'] * buying_history[buying_history.__len__()-1]['price']
    gain = asset -total['cost']
    print('gain: {0} total asset: {1} toal cost: {2}'.format(gain,asset,total['cost']))

if(__name__ == '__main__'):
	main()