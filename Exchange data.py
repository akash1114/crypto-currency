from pycoingecko import CoinGeckoAPI

import mysql.connector

con = mysql.connector.connect(user='root',password='', host='127.0.0.1',database='demo')

cursor = con.cursor()

query = "insert into demo1(name) VALUES ('%s')" % ('Akash')

cursor.execute(query)

con.commit()

con.close()
