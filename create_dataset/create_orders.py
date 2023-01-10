import mysql.connector
from faker import Faker
import random
import time



mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="delhi_110062"
)
mycursor = mydb.cursor(buffered=True)
mycursor.execute("use eCommerce;")

fake=Faker()

while(True):
  uid = random.randint(1, 10000)
  pid = random.randint(1, 304)
  val=(uid,pid)
  sql="INSERT INTO orders(user_id,product_id, orderedAt) VALUES(%s,%s, CURRENT_TIMESTAMP);"
  mycursor.execute(sql,val)
  mydb.commit()
  time.sleep(5)
