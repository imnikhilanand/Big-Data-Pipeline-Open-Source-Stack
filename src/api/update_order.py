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
  sql='''SELECT *
         FROM orders 
         WHERE status='0' AND  
         TIMESTAMPDIFF(SECOND, orderedAt, CURRENT_TIMESTAMP)>1800 AND 
         TIMESTAMPDIFF(SECOND, orderedAt, CURRENT_TIMESTAMP)<3600  ;
      ''' 

      
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  i=len(myresult)
  print(i)
  print(myresult[i-1])

  while i>0:
    myresult=[list(ele) for ele in myresult]
    myresult[i-1][4]='1'
    myresult=[tuple(ele) for ele in myresult]
    print(myresult[i-1])
    update_sql="INSERT into completed_orders values(%s,%s,%s,%s,%s) ;"
    mycursor.execute(update_sql,myresult[i-1])
    mydb.commit()
    i-=1
    time.sleep(5)
  time.sleep(300)
  
mycursor.close()


