import os
import ast
import yaml
import logging
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import lit
from datetime import datetime, timedelta, time

def getSQLData(kwargs):
    #Getting AWS access keys
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

    #Getting column types
    columnTypes = kwargs['columnTypes']
    #logging.info('Column types:' + str(columnTypes))

    # Creating spark session and session configuration
    spark = SparkSession.builder \
        .master("local") \
        .appName("pyspark-etl-perseo") \
        .config("spark.sql.shuffle.partitions", "4") \
        .getOrCreate()

    spark._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    spark._jsc.hadoopConfiguration().set("fs.s3a.access.key", AWS_ACCESS_KEY_ID)
    spark._jsc.hadoopConfiguration().set("fs.s3a.secret.key", AWS_SECRET_ACCESS_KEY)
    spark._jsc.hadoopConfiguration().set("fs.s3a.multiobjectdelete.enable", 'false')

    #Connecting to DB & executing query
    data= spark \
          .read \
          .format("jdbc") \
          .option("url", kwargs['url']) \
          .option("driver", "com.mysql.jdbc.Driver") \
          .option("user", kwargs['user']) \
          .option("password", kwargs['password']) \
          .option("query", kwargs['query']) \
          .load()

    #Parsing column data types
    for col in columnTypes:
        data = data.withColumn(col, F.col(col).cast(columnTypes[col]))

    return data

def uploadDataToS3(kwargs, df):
    #Bucket info
    protocol ='s3a:'
    bucket_name = kwargs['bucket_name']
    prefix = kwargs['prefix']

    #Time variables
    dateToWork = kwargs['date_to_work']
    uploadedAt = kwargs['exec_date']

    #Putting together S3 path
    path = '{}//{}/{}/{}'.format(protocol, bucket_name, prefix, dateToWork)
    logging.info('Path info: ' + path)


    #Writing data to S3 - Adding control column
    df = df.withColumn("uploaded_at", lit(uploadedAt))
    df.write.parquet(path, mode = 'overwrite')
    return('Success')

def main():
    os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages mysql:mysql-connector-java:8.0.18,org.apache.hadoop:hadoop-aws:2.7.0 pyspark-shell'

    exec_date = os.environ['exec_date']
    date_to_work = os.environ['date_to_work']
    logging.info('Execution date is: {}. Date to work is: {}.'.format(exec_date, date_to_work))

    host = os.environ['dbhost']
    user = os.environ['dbuser']
    port = os.environ['dbport']
    password = os.environ['dbpassword']

    #Variables
    dbname = os.environ['dbname']
    bucket_name = os.environ['bucket_name']
    prefix = os.environ['prefix']
    table = os.environ['table']
    query = os.environ['query']
    columnTypes = os.environ['columnTypes']
    url = 'jdbc:mysql://{}:{}/{}'.format(host, port, dbname)

    df = getSQLData({'host': host, 'user': user, 'port': port,
                     'password': password, 'dbname': dbname,
                     'url' : url, 'query': query, 'columnTypes' : ast.literal_eval(columnTypes)})

    if df.count != 0:
        uploadDataToS3({"exec_date" : exec_date, "date_to_work" : date_to_work,
                        'bucket_name' : bucket_name,
                        'prefix': '{}/{}/{}/'.format(prefix, dbname, table)}, df)
        return('Data succesfully extracted')
    else:
        return('No rows have been extracted')


if __name__== "__main__":
    main()
