from flask import Flask
from faker import Faker
fake = Faker()
app = Flask(__name__)

# generate some integers
in_memory_datastore=[]
for i in range(10000):
    in_memory_datastore.append(i)
# for i in range(20):
#     print(in_memory_datastore[i])
    
@app.get('/')
def list_programming_languages():
   return {in_memory_datastore:[fake.name(),fake.address()]}
   
#@app.route('/programming_languages/<programming_language_name>')
#def get_programming_language(programming_language_name):
#  return in_memory_datastore[programming_language_name]
   



