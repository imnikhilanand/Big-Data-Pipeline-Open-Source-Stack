import requests
import time

# this function will generate the batch data
def create_order():
    response = requests.get('http://127.0.0.1:5000/createorders')

def update_order():
    response = requests.get('http://127.0.0.1:5000/updateorders')

if __name__== '__main__':
    create_order()
    time.sleep(3600)
    update_order()
    