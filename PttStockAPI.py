from typing import ByteString
from flask import Flask, request, Response
from Packages.mysqlDb import mysqlDb


app = Flask(__name__)

@app.route('/StockData/<stock_name>/<date>', methods=['GET'])
def get(stock_name,date):
    try:
        db = mysqlDb()
        result =  {"stock":stock_name,
            "date":date,
        "comments" : db.get_stock_commments(date,stock_name)
        }
        db.close()
        return  result
    except Exception as ex:
        return Response("Fail to retrive the data",status=404,mimetype='application/json')

@app.route('/StockData/<source>/<stock_name>/<date>', methods=['POST'])
def InsertStockComments(source,stock_name,date):
    try:
        db = mysqlDb()
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
    