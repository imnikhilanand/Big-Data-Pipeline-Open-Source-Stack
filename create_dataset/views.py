import mysql.connector
import time

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="delhi_110062"
)
mycursor = mydb.cursor(buffered=True)
mycursor.execute("use eCommerce;")


def order_view():
    sql="SELECT order_id, user_id, product_id FROM orders WHERE status='0';"
    mycursor.execute(sql)
    result=mycursor.fetchall()
    for res in result:
        print(res)

def product_view():
    sql="SELECT * FROM products;"
    mycursor.execute(sql)
    result=mycursor.fetchall()
    for res in result:
        print(res)

while(True):
    order_view()
    time.sleep(5)
    product_view()
    time.sleep(5)