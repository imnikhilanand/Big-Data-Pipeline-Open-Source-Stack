from flask import Flask
app = Flask(__name__)

# generate some integers
in_memory_datastore=[]
for i in range(1,10001):
    in_memory_datastore.append(i)

    
@app.get('/')
def list_programming_languages():
   return in_memory_datastore
   
# @app.route('/order')
# def get_order(oid, uid, pid, timestamp, status):
#  return in_memory_datastore[programming_language_name]
   



