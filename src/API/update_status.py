# importing the libraries
import mysql.connector
import time
import random

# setting up the mysql
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="delhi_110062"
)

# completing the orders (once they were ordered 30 mins ago. The reason being, we will get time to randomly view some order and generate order-view stream data)
while(True):
  mycursor = mydb.cursor(buffered=True)
  mycursor.execute("use eCommerce;")
  sql='''SELECT order_id 
         FROM orders 
         WHERE status='0' AND  
         TIMESTAMPDIFF(SECOND, orderedAt, CURRENT_TIMESTAMP)>18 AND 
         TIMESTAMPDIFF(SECOND, orderedAt, CURRENT_TIMESTAMP)<3600 ;
      ''' 
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  print(myresult)
  oid=[]
  for x in myresult:
    oid.append(x[0])
  while len(oid)>0:
    update_val=(random.choice(oid),)
    # Find the index of the element with the specified value
    index_arr = oid.index(update_val[0])
    # Delete the element at the specified index
    del oid[index_arr]
    update_sql="UPDATE orders SET status='1' WHERE order_id='%s';"
    mycursor.execute(update_sql,update_val)
    mydb.commit()
    time.sleep(5)
  
mycursor.close()
      
  #time.sleep(36)


