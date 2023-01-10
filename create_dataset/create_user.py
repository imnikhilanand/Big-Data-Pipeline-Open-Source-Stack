from faker import Faker
import pandas as pd
fake = Faker()
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="delhi_110062"
)
mycursor = mydb.cursor(buffered=True)
mycursor.execute("use eCommerce;")
sql = "INSERT INTO user (name, address) VALUES ( %s, %s);"

for i in range(10000):
    val = (fake.name(),fake.address())
    mycursor.execute(sql, val)


product = pd.read_csv("data/product_list.csv")

for index, values in product.iterrows():
    sql = "INSERT INTO products (product_id, category, name ) VALUES (%s, %s, %s)"
    val = (values["product_id"], values["category"], values["name"])
    mycursor.execute(sql, val)



mydb.commit()