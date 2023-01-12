import time
import requests
from kafka import KafkaProducer
import json

def order_view():
    response = requests.get('http://127.0.0.1:5000/vieworders')
    # Parse the JSON response
    data = response.json()
    # Access the data in the response
    def json_serializer(data):
            return json.dumps(data).encode('utf-8')
    # Access the data in the response
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=json_serializer)
    try:
        producer.send("orderview",data)
    except Exception as e:
        print("Producer not working: ",e)


def product_view():
    response = requests.get('http://127.0.0.1:5000/viewproducts')
    # Parse the JSON response
    data = response.json()
    def json_serializer(data):
            return json.dumps(data).encode('utf-8')
    # Access the data in the response
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=json_serializer)
    try:
        producer.send("productview",data)
    except Exception as e:
        print("Producer not working: ",e)

while(True):
    product_view()
    order_view()
    time.sleep(5)