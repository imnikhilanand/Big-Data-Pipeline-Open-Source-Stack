# importing the library to run the commands in the python file
import os
import time

# variable to rename the files
i=1

while(True):
    home = os.environ['HOME']
    os.chdir(home)
    os.chdir("test_airbyte/product_names")
    os.getcwd()
    os.listdir()

    # moving order from local to data lake
    first_command = "echo 'delhi_110062' | sudo -S mv _airbyte_raw_ordersorders.csv "+str(i)+"_orders.csv"
    os.system(first_command)
    second_command = "hdfs dfs -copyFromLocal /home/hdoop/test_airbyte/product_names/"+str(i)+"_orders.csv /ecomm_data/data_lake/orders"
    os.system(second_command)
    third_command = "echo 'delhi_110062' | sudo rm "+str(i)+"_orders.csv"
    os.system(third_command)

    # moving order from local to data lake
    fourth_command = "echo 'delhi_110062' | sudo -S mv _airbyte_raw_orderscompleted_orders.csv "+str(i)+"_completed_orders.csv"
    os.system(fourth_command)
    fifth_command = "hdfs dfs -copyFromLocal /home/hdoop/test_airbyte/product_names/"+str(i)+"_completed_orders.csv /ecomm_data/data_lake/completed_orders"
    os.system(fifth_command)
    sixth_command = "echo 'delhi_110062' | sudo rm "+str(i)+"_completed_orders.csv"
    os.system(sixth_command)

    i = i+1

    time.sleep(240)