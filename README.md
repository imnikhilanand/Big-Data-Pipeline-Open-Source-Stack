# Big-Data-Pipeline-Open-Source-Stack
This project demonstrates a scalebale big data pipeline developed using open source technologies.
Database setup instructions:
- Run MySQL on terminal using the command "mysql -u <username> -p". When prompted, enter the password.
- Create a database named "eCommerce". 
- In eCommerce database create tables named user(id, name, address), products(product_id, category, name), orders(order_id, user_id, product_id, orderedAt(CURRENT_TIMESTAMP), status(enum[0,1]))

