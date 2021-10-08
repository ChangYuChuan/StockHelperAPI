from typing import ByteString
from flask import Flask, request, Response
from localDb import sqliteDb


app = Flask(__name__)

@app.route('/StockData/<stock_name>/<date>', methods=['GET'])
def get(stock_name,date):
    try:
        db = sqliteDb("C:\\db\\stockdb.db")
        result =  {"stock":stock_name,
            "date":date,
        "comments" : db.get_commments(date,stock_name)
        }
        db.close()
        return  result
    except Exception as ex:
        return Response("Fail to retrive the data",status=404,mimetype='application/json')

@app.route('/StockData/<stock_name>/<date>', methods=['POST'])
def InsertStockComments(stock_name,date):
    try:
        db = sqliteDb("C:\\db\\stockdb.db")
        data = request.get_json()
        comments = data['comments']
        table_name = '{0}-{1}'.format(date,stock_name)
        db.insert_main_data("TW_Stock","stock","log_date",stock_name,date)
        db.create_stock_table(table_name)
        db.insert(comments,table_name,"comment")
        db.commit()
        db.close()
        return "Insert the data completed"
    except Exception as ex:
        return Response("Fail to insert the data",status=404,mimetype='application/json')
    


if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True)
    