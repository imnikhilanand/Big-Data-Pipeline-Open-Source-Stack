# Big-Data-Pipeline-Open-Source-Stack
This project demonstrates a scalebale big data pipeline developed using open source technologies. We tried to imitate an Ecommerce website where the APIs will be producing data in Batches and as a Stream. We will be using open sources tools to build the data pipelines and ETL layers. 

## Architecture

The data source for the project is an API(imitatte Ecommerce website) that repeatedly produce orders and click-stream data. The real-time orders are stored in MySQL databases (OLTP) and extracted in batches to ingest in the Hadoop HDFS (OLAP), which is used as a Data Lake. Periodically raw data from the Data-Lake is extracted and transformed and laoded in Hive distributed Data Warehouse system to analyze large scale data. The streaming APIs produce distirbuted click-stream using Kafka which is processed in real-time using Apache Spark and stored in Cassandra Distributed Databases. Both batch and streaming data is visualized using open sources visualization tool Metabase.  

<p align="center">
	<img src="img/data_pipeline.jpg" width='100%'>
</p>

## API

The API for this project consists of both REST APIs and Streaming APIs. The rest APIs produces random orders data and store them in the eCommerce database. ```orders``` table in the database has the orders data and ```completed_orders``` table has those orders that were completed. The Streaming APIs produces random data of those user who have viewed random products on the Ecommmerce website and those users who have checked the status of their orders which are not delivered.

### Database setup instructions:

1. Run MySQL on terminal using the command "mysql -u ```<your-username>``` -p". When prompted, enter the password.
2. Create a database named ```eCommerce```. 
3. In eCommerce database create tables: 
    
    ```
    CREATE TABLE user(
        id INT(255) NOT NULL PRIMARY KEY AUTO_INCREMENT, 
        name VARCHAR(255) NOT NULL,  
        address VARCHAR(255)
    ); 
    
    CREATE TABLE products(
        product_id INT(255) NOT NULL PRIMARY KEY AUTO_INCREMENT, 
        category VARCHAR(255) NOT NULL, 
        name VARCHAR(255)
    );
    
    CREATE TABLE orders(
        order_id int(255) NOT NULL PRIMARY KEY AUTO_INCREMENT, 
        user_id int(255) NOT NULL, 
        product_id int(255) NOT NULL, 
        orderedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP(), 
        status ENUM('0','1') DEFAULT '0', 
        FOREIGN KEY (user_id) REFERENCES user(id), 
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );

    CREATE TABLE completed_orders(
        order_id int(255) NOT NULL PRIMARY KEY, 
        completedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP(), 
        status ENUM('0','1') DEFAULT '1', 
        FOREIGN KEY (order_id) REFERENCES orders(order_id) 
    );
    ```

### Running the APIs:

1. To produce orders data we have run the following files:

    ```
    python3 src/api/rest_api.py
    python3 src/api/create_orders.py
    python3 src/api/updated_orders.py
    ```

2. To produce streaming data we have run the following file:

    ```
    python3 src/stream/stream_producer.py
    ```

## Streaming Data

### Kafka and Cassandra Setup Instructions:

1. Create topics for click-stream data: productview and orderview

    ```
    bin/kafka-topics.sh --create --topic productview --bootstrap-server localhost:9092 --replication-factor 1 --partitions 4	
    bin/kafka-topics.sh --create --topic orderview --bootstrap-server localhost:9092 --replication-factor 1 --partitions 4	
    ```

2. Create Keyspace ecommerce and Column families product_view and order_view

    ```
    CREATE KEYSPACE eCommerce WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
    CREATE TABLE product_view(product_id TEXT, view_count INT, create_at TIMESTAMP);
    CREATE TABLE order_view(order_id TEXT, create_at TIMESTAMP);
    ```

### Processing Streaming Data:

To process the product views data, open a separate terminal and follow the below instructions:

1. Open a spark shell with following jar files:

    ```
    bin/spark-shell --packages "com.datastax.spark:spark-cassandra-connector_2.12:3.0.0","org.apache.spark:spark-streaming-kafka-0-10_2.12:3.2.1"
    ```

2. Once the spark shell opens up run the following commands:

    ```
    import org.apache.spark.streaming._
    import org.apache.spark.SparkContext
    import com.datastax.spark.connector.SomeColumns
    import com.datastax.spark.connector.cql.CassandraConnector
    import com.datastax.spark.connector.streaming._
    import org.apache.spark.streaming.kafka010._
    import org.apache.kafka.common.serialization.StringDeserializer
    import org.apache.kafka.common.TopicPartition
    import java.time

    val sc = SparkContext.getOrCreate

    val ssc = new StreamingContext(sc, Seconds(10))

    val preferredHosts = LocationStrategies.PreferConsistent

    val topics = List("productview")

    val kafkaParams = Map(
    "bootstrap.servers" -> "localhost:9092",
    "key.deserializer" -> classOf[StringDeserializer],
    "value.deserializer" -> classOf[StringDeserializer],
    "group.id" -> "spark-streaming-notes",
    "auto.offset.reset" -> "earliest"
    )

    val offsets = Map(new TopicPartition("productview", 0) -> 2L)

    val dstream = KafkaUtils.createDirectStream[String, String](
    ssc,
    preferredHosts,
    ConsumerStrategies.Subscribe[String, String](topics, kafkaParams, offsets))

    dstream.map(record=>(record.value().toString.split(",")(1).toString.substring(0,record.value().toString.split(",")(1).toString.length()-1),1)).reduceByKey( _ + _ ).map{case (k,v) => (k,v); (k,v,time.LocalDateTime.now().toString)}.saveToCassandra("ecommerce", "product_view", SomeColumns("product_id","view_count","created_at"))

    ssc.start
    ```

To process the order views data, open a separate terminal and follow the below instructions:

1. Open a spark shell with following jar files:

    ```
    bin/spark-shell --packages "com.datastax.spark:spark-cassandra-connector_2.12:3.0.0","org.apache.spark:spark-streaming-kafka-0-10_2.12:3.2.1"
    ```

2. Once the spark shell opens up run the following commands:

    ```
    import org.apache.spark.streaming._
    import org.apache.spark.SparkContext
    import com.datastax.spark.connector.SomeColumns
    import com.datastax.spark.connector.cql.CassandraConnector
    import com.datastax.spark.connector.streaming._
    import org.apache.spark.streaming.kafka010._
    import org.apache.kafka.common.serialization.StringDeserializer
    import org.apache.kafka.common.TopicPartition
    import java.time

    val sc = SparkContext.getOrCreate

    val ssc = new StreamingContext(sc, Seconds(10))

    val preferredHosts = LocationStrategies.PreferConsistent

    val topics = List("orderview")

    val kafkaParams = Map(
    "bootstrap.servers" -> "localhost:9092",
    "key.deserializer" -> classOf[StringDeserializer],
    "value.deserializer" -> classOf[StringDeserializer],
    "group.id" -> "spark-streaming-notes",
    "auto.offset.reset" -> "earliest"
    )

    val offsets = Map(new TopicPartition("orderview", 0) -> 2L)

    val dstream = KafkaUtils.createDirectStream[String, String](
    ssc,
    preferredHosts,
    ConsumerStrategies.Subscribe[String, String](topics, kafkaParams, offsets))

    dstream.map(record=>(record.value().toString.split(",")(1).toString.substring(0,record.value().toString.split(",")(1).toString.length()-1))).map(line => {val order_id = line.toString; (order_id, time.LocalDateTime.now().toString)}).saveToCassandra("ecommerce", "order_view", SomeColumns("order_id","created_at"))

    ssc.start
    ```

## Batch Data

### Airbyte Setup Instructions:

1. Download and Run Airbyte on the machine. Use the official documentation for the refernce - https://docs.airbyte.com/deploying-airbyte/local-deployment/

2. Create a new connection with MySQL source and Local File (.csv format) as the destination.

3. For both ```orders``` and ```completed_orders``` table <b>Sync mode</b> should be <b>Incremental | Append</b>.

### Processing Batch Data:

<p align="center">
	<img src="img/batch_pipeline.jpg" width='100%'>
</p>


## Data Lake and Warehouse

### Setup Data Lake and Warehouse


### Load data from Daata Lake to Warehouse


## Dashboard

