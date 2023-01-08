from faker import Faker
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
mydb.commit()