from flask import Flask
from flask_restful import Api, Resource
from localDb import sqliteDb



class PttStockDataApi(Resource):
    def get(self,stockId,date):
        db = sqliteDb("C:\\db\\stockdb.db")
        result =  {"stock":stockId,
            "date":date,
        "comments" : db.get_commments(date,stockId)
        }
        db.close()
        return result
        


def main():
    
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(PttStockDataApi,"/PttStockComment/<string:stockId>/<string:date>")
    app.run(debug=True)


if __name__ == "__main__":
    main()