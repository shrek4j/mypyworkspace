import tushare as ts
import MySQLdb

api = ts.pro_api('318937ff6bf3c29a921d03cf609ac255a4896ed2f03c47ea91a07bc0')
data = api.stock_basic(exchange_id='', list_status='D', fields='ts_code,symbol,name,area,industry,market,exchange_id,list_status,list_date,delist_date')
db = MySQLdb.connect('localhost', 'root', 'Password123', 'stock', charset="utf8")
cursor = db.cursor()
sql =   "INSERT INTO ts_stock_list (ts_code, symbol, `name`, area, industry, market, exchange_id, list_status, list_date, delist_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
for i in data.index:
    row = data.loc[i]
    params = (row['ts_code'],row['symbol'],row['name'],row['area'],row['industry'],row['market'],row['exchange_id'],row['list_status'],row['list_date'],row['delist_date'])
    cursor.execute(sql, params)
db.commit()

if cursor:
    cursor.close()
if db:
    db.close()

