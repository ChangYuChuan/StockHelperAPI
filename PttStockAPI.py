from typing import ByteString
from flask import Flask, request, Response
from Packages.mysqlDb import mysqlDb


app = Flask(__name__)

@app.route('/StockData/<stock_name>', methods=['GET'])
def get(stock_name):
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
        return Response("Fail to retrive the data",status=404,mimetype='application/json')

@app.route('/StockData/<source>/<stock_name>/<date>', methods=['POST'])
def InsertStockComments(source,stock_name,date):
    try:
        db = mysqlDb()
        # hwo to get the data from body when post.
        data = request.get_json()
        comments = data['comments']
        db.add_stock_comment(stock_name,source,date,comments)
        db.close()
        return "Insert the data completed"
    except Exception as ex:
        return Response("Fail to insert the data",status=404,mimetype='application/json')
    


if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True)
    