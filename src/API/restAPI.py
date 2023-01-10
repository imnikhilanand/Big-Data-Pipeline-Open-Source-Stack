from flask import Flask, request
import subprocess
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="delhi_110062"
)
mycursor = mydb.cursor(buffered=True)
mycursor.execute("use eCommerce;")

app = Flask(__name__)

# generate some integers
in_memory_datastore=[]
for i in range(1,10001):
    in_memory_datastore.append(i)

    
@app.get('/')
def home():
   return in_memory_datastore
   
@app.route('/createorders', methods=['GET','POST'])
def run_script():
  script_path = r'/home/sourabhlodhisrb/Downloads/Big-Data-Pipeline-Open-Source-Stack/create_dataset/create_orders.py'
  subprocess.call(['python3', script_path])
  return 'Orders Created'

@app.route('/updateorders', methods=['GET','POST'])
def updateorders():
  script_path = r'/home/sourabhlodhisrb/Downloads/Big-Data-Pipeline-Open-Source-Stack/create_dataset/update_status.py'
  subprocess.call(['python3', script_path])
  return 'Orders Updated'

@app.get('/vieworders')
def vieworders():
    sql="SELECT order_id, user_id, product_id FROM orders WHERE status='0';"
    mycursor.execute(sql)
    result=mycursor.fetchall()
    return result

@app.get('/viewproducts')
def viewproducts():
    sql="SELECT * FROM products ;"
    mycursor.execute(sql)
    result=mycursor.fetchall()
    return result

if __name__ == '__main__':
  app.run()
   



