from logging import exception
import mysql.connector
import json

class mysqlDb:
    def __read_local_config(self,config_path):
        f = open(config_path, "r")
        config = json.load(f)
        f.close()
        return config['localhost']

    def __init__(self) -> None:
        config = self.__read_local_config("C:\\Config\\mysql_config.json")
        self.__db = mysql.connector.connect(**config)
       
    def add_stock_comment(self,stock_name, source ,log_date, comments):
        cursor = self.__db.cursor()
        try:
            # if comment in string type
            if isinstance(comments,str):
                cursor.callproc('collect_Comments_of_stock_name',[stock_name,source,log_date,comments])
            # if comment in list type, iterate the comments.
            elif isinstance(comments,list):
                for comment in comments:
                    cursor.callproc('collect_Comments_of_stock_name',[stock_name,source,log_date,comment])
            else:
                raise Exception('invalid comments')
        except Exception as ex:
            print('Error! fail to add stock comment msg: {0}'.format(ex))
        finally:
            cursor.close()
            self.__db.commit()
    def get_stock_commments(self,stock_name,start_date,end_date):
        output_list = []
        cursor = self.__db.cursor()
        try:
            cursor.callproc('get_Comments_of_stock_name',[stock_name,start_date,end_date])
            for result in cursor.stored_results():
                output_list.extend(result.fetchall())
            output_list = map(lambda x:x[0],output_list)
            return list(output_list)
        except Exception as ex:
            print('Error! fail to get stock comment msg: {0}'.format(ex))
        finally:
            cursor.close()

    def close(self):
        self.__db.close()




if __name__ == '__main__':
    db = mysqlDb()
    comments = db.get_stock_commments('台積電','2021-08-30','2021-09-30')
    print(comments)
    db.close()
