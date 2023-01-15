# Big-Data-Pipeline-Open-Source-Stack
This project demonstrates a scalebale big data pipeline developed using open source technologies.

## Architecture

## API

### Database setup instructions:

- Run MySQL on terminal using the command "mysql -u <username> -p". When prompted, enter the password.
- Create a database named "eCommerce". 
- In eCommerce database create tables: 
    - user(id, name, address) 
    - products(product_id, category, name)
    - create table orders (
        order_id int(255) not null primary key auto_increment, 
        user_id int(255) not null, 
        product_id int(255) not null, 
        orderedAt timestamp default current_timestamp(), 
        status enum('0','1') default '0', 
        foreign key (user_id) references user(id), 
        foreign key (product_id) references products(product_id)
      );

# Streaming Data

### Kafka topics for producting Streaming data:

- Create topics for click-stream data: productview and orderview
```
    bin/kafka-topics.sh --create --topic productview --bootstrap-server localhost:9092 --replication-factor 1 --partitions 4	
    bin/kafka-topics.sh --create --topic orderview --bootstrap-server localhost:9092 --replication-factor 1 --partitions 4	
```

# Batch Data

### Setup Airbyte



