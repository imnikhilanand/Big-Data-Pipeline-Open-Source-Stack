
# importing the libraries
import pandas as pd 
import numpy as np

# loading the datasets
product = pd.read_csv("create_dataset/Products/things.csv", names=["product"])
pro_clothes = pd.read_csv("create_dataset/Products/clothes.csv", names=["product"])
pro_flowers = pd.read_csv("create_dataset/Products/flowers.csv", names=["product"])
pro_instru = pd.read_csv("create_dataset/Products/instruments.csv", names=['product'])

# preprocess the clothes data 
pro_clothes["product"] = pro_clothes["product"].apply(lambda x: str(x).strip())
pro_flowers["product"] = pro_flowers["product"].apply(lambda x: str(x).strip())
pro_instru["product"] = pro_instru["product"].apply(lambda x: str(x).strip())

# create categories
things = np.repeat("things",100)
clothes = np.repeat('clothes',61)
flowers = np.repeat('flowers',91)
instru = np.repeat('instru',52)

# adding the category
product["category"] = things
pro_clothes["category"] = clothes
pro_flowers["category"] = flowers
pro_instru['category'] = instru

# appending different types of products
product = product.append(pro_clothes)
product = product.append(pro_flowers)
product = product.append(pro_instru)

# resetting the index
product = product.reset_index(drop=True)

# create random numbers 
rand_ids = np.random.randint(1001,9999, (1,304))  
rand_ids = rand_ids.reshape(304,1)

# creating primary key 
product['product_id'] = rand_ids

# reordering and rearraning the columns
product = product.sort_values(['product_id'])
product = product[['product_id', 'category', 'product']]

# save the data
product.to_csv('data/product_list.csv', index=False)