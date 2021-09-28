import sqlite3

class sqliteDb:
    def __init__(self,db_path):
        self.con = sqlite3.connect(db_path)
        self.cur = self.con.cursor()
        
    def create_stock_table(self,table_name):
        self.cur.execute("CREATE TABLE IF NOT EXISTS \"{0}\" (id INTEGER NOT NULL UNIQUE,comment VARCHAR,PRIMARY KEY(id AUTOINCREMENT));".format(table_name))
    
    def insert(self,data,table_name,colum):
        if(isinstance(data,str)):
            self.cur.execute("INSERT INTO \"{0}\" ({1}) VALUES (\"{2}\");".format(table_name,colum,data))
            return
        for element in data:
            self.cur.execute("INSERT INTO \"{0}\" ({1}) VALUES (\"{2}\");".format(table_name,colum,element))

    def insert_main_data(self,table_name,colum_stockId,colum_date,stockId,date):
        self.cur.execute("INSERT INTO \"{0}\" ({1},{2}) VALUES (\"{3}\",\"{4}\");".format(table_name,colum_stockId,colum_date,stockId,date))

    def get_table_name(self,stockId,span):
        if(isinstance(span,list) != True):
            return
        cursor = self.cur.execute("SELECT log_date,stock FROM \"TW_Stock\" WHERE log_date BETWEEN date(\'{0}\') AND date(\'{1}\') AND stock=\'{2}\'".format(span[0],span[1],stockId))
        return cursor.fetchall()

    def get_commments(self,date,stockId):
        table_name = "{0}-{1}".format(date,stockId)
        cursor = self.cur.execute("SELECT comment FROM \"{0}\" ".format(table_name))
        return cursor.fetchall()


    def commit(self):
        self.con.commit()

    def close(self):
        self.con.close()



def main():
    db = sqliteDb("C:\\db\\stockdb.db")
    result = db.get_table_name("長榮",["2021-09-05","2021-09-30"])
    for row in result:
        comments = db.get_commments(row[0],row[1])
        print(comments)


    db.commit()
    db.close()

if __name__=='__main__':
    main()
