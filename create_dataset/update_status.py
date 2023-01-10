import mysql.connector
import time
import random



mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="delhi_110062"
)
mycursor = mydb.cursor(buffered=True)
mycursor.execute("use eCommerce;")

while(True):
  sql="SELECT order_id FROM orders WHERE status='0' AND  TIMESTAMPDIFF(SECOND, orderedAt, CURRENT_TIMESTAMP)> 1800 AND TIMESTAMPDIFF(SECOND, orderedAt, CURRENT_TIMESTAMP) <3600 ;" 
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  oid=[]
  for x in myresult:
    oid.append(x[0])
    print("oid:",oid[0])
  for id in oid:
    update_val=(random.choice(oid),)
     # Find the index of the element with the specified value
    index = oid.index(update_val)
    # Delete the element at the specified index
    del oid[index]
    print("update val: ",update_val)
    update_sql="UPDATE orders SET status='1' WHERE order_id='%s';"
    mycursor.execute(update_sql,update_val)
    mydb.commit()
  time.sleep(5)


