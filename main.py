import imp
from types import SimpleNamespace
from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
from Packages.mysqlDb import mysqlDb
from Packages.stockCrawler import PttCrawler, TelgramCrawler
import json,time
from Packages.YahooFinance import YahooFinance
from Packages.pttObj import PttObj
from functools import wraps
import asyncio


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/api/StocksHistory', methods=['POST'])
def get_stock_history():
    '''The purpose of the API is used to cacluate how much profit we would gain from certain stock if we follow the concept BUY AND HOLD'''
    try:
        result = []
        print('entering /api/StocksHistory')
        # the methods below is the way how we get the arguments from body.
        req = request.get_json()
        # In comprison with the query, the format of the body is originaly json. Therefore, there is no need of transforming it to json.
        json_orders = req['data']
        print(json_orders)

        # by using SimpleNamespace, we are able to transform dict to a fake object, which makes key of dict become attribute
        orders = list(map(lambda element: SimpleNamespace(**element), json_orders))

        yf = YahooFinance()
        for order in orders:
            order_result = yf.calculate_profit(order.stockName, order.startDate, order.endDate ,order.payPerMonth)
            result.append(order_result)
        print(result)
        return {'result':result}
    except Exception as ex:
        print(ex)
        return Response("Fail to retrive the data: {0}".format(ex), status=404,mimetype='application/json')



@app.route('/api/StockData/<stock_name>', methods=['GET'])
def get(stock_name):
    '''Get the comments stored in SQL DB'''
    try:
        # the methods below is the way how we get the arguments from query.
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        db = mysqlDb()
        print(start_date)
        print(end_date)
        
        result = {
             "stock":stock_name,
             "start_date":start_date,
             "end_date":end_date,
             "comments" : db.get_stock_commments(stock_name,start_date,end_date)
             }
        db.close()
        return result
    except Exception as ex:
        return Response("Fail to retrive the data error message={0}".format(ex),status=404,mimetype='application/json')

@app.route('/api/StockData/<source>/<stock_name>/<date>', methods=['POST'])
def InsertStockComments(source,stock_name,date):
    '''How to insert the comments we get from telegram or ptt to DB'''
    try:
        db = mysqlDb()
        # hwo to get the data from body when post.
        data = request.get_json()
        comments = data['comments']
        db.add_stock_comment(stock_name,source,date,comments)
        db.close()
        return Response(mimetype='application/json',status=200 )
    except Exception as ex:
        return Response("Fail to insert the data",status=404,mimetype='application/json')


@app.route('/api/StockData/PTT', methods=['GET'])
def get_ptt_stock_comments():
    '''craw the ptt to get the comments for certain stock'''
    try:
        print('entering get_ptt_stock_comments()')
        # the methods below is the way how we get the arguments from query.
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        stock_name = request.args.get('stock_name')
        if stock_name is None or stock_name == '':
            stock_name = []
        else:
            stock_name = [stock_name]
        limit = request.args.get('limit')
        pttCrawler = PttCrawler()
        result = pttCrawler.get_comments(stock_name,start_date,end_date,limit)
        return {
            "result":result
        }
    except Exception as ex:
        return Response("Fail to retrive the data error message={0}".format(ex),status=404,mimetype='application/json')

@app.route('/api/StockData/Telegram', methods=['GET'])
async def get_tele_stock_comments():
    '''craw the ptt to get the comments for certain stock'''
    try:
        result = ''
        print('entering get_tele_stock_comments()')
        config_path = "C:\\Config\\telegram_config.json"
        # the methods below is the way how we get the arguments from query.
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        stock_name = request.args.get('stock_name')
        limit = request.args.get('limit')
        teleCrawler = TelgramCrawler(config_path)
        result = await teleCrawler.get_comments(stock_name,start_date,end_date,limit)
        return {
            "result" : result
        }
    except Exception as ex:
        return Response("Fail to retrive the data error message={0}".format(ex),status=404,mimetype='application/json')

if __name__ == "__main__":
    # app.config['JSON_AS_ASCII'] = False
    app.run(debug=True)
    