import mysql.connector

class mysqlDb:
    def __init__(self) -> None:
       self.__db = mysql.connector.connect( host="localhost",user="root",password="19920827",database="stockdb")
       
    def add_stock_comment(self,stock_name, source ,log_date, comments):
        try:
            cursor = self.__db.cursor()
            # if comment in string type
            if isinstance(comments,str):
                cursor.callproc('collect_Comments_of_stock_name',[stock_name,source,log_date,comments])
            # if comment in list type, iterate the comments.
            elif isinstance(comments,list):
                for comment in comments:
                    cursor.callproc('collect_Comments_of_stock_name',[stock_name,source,log_date,comment])
            else:
                raise('invalid comments')
        except Exception as ex:
            print('Error! fail to add stock comment msg:{0}'.format(ex))
        finally:
            self.__db.commit()
    def close(self):
        self.__db.close()




if __name__ == '__main__':
    db = mysqlDb()
    db.add_stock_comment('聯電-KY','PTT','2021-10-30',['慘','沒救','請問有人買嗎?'])
    db.close()
