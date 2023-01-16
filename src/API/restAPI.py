# importing the libraries
from flask import Flask, jsonify
import time
import subprocess
import mysql.connector
import random
import numpy

# connecting to the database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="delhi_110062"
)
mycursor = mydb.cursor(buffered=True)
mycursor.execute("use eCommerce;")

# flask app
app = Flask(__name__)


# Defining route to create random orders
@app.route('/createorders', methods=['GET','POST'])
def run_script():
  script_path = r'src/API/create_orders.py'
  subprocess.call(['python3', script_path])
  return 'Orders Created'

# Defining route to update random orders
@app.route('/updateorders', methods=['GET','POST'])
def updateorders():
  script_path = r'src/API/update_status.py'
  subprocess.call(['python3', script_path])
  return 'Orders Updated'

# Defining route to view random orders which are uncomplete(status=0)
@app.get('/vieworders')
def vieworders():
    sql1="SELECT user_id FROM orders WHERE status='0';"
    mycursor.execute(sql1)
    user_id=mycursor.fetchall()
    uid_arr=[]
    for uid in user_id:
      uid_arr.append(uid[0])
    uid = random.choice(uid_arr)
    sql="SELECT order_id, CURRENT_TIMESTAMP() FROM orders WHERE status='0' and user_id='%s';"
    mycursor.execute(sql, (uid,))
    result=mycursor.fetchall()
    return result

# Defining route to view random products
@app.get('/viewproducts')
def viewproducts():
    sql="SELECT product_id FROM products ORDER BY RAND() LIMIT 1;"
    mycursor.execute(sql)
    result=mycursor.fetchall()
    return [random.randint(1, 10000), result[0][0]]

if __name__ == '__main__':
  app.run()


   



