import configparser
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession

config = configparser.ConfigParser()

# Load the configuration file
config.read("/config.ini")

sc = SparkContext('local')

scala_version = '2.12'
spark_version = '3.5.3'

packages = [
    f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
    'org.apache.kafka:kafka-clients:3.2.3'
]
spark = SparkSession.builder\
   .appName("kafka-example")\
   .config("spark.jars.packages", ",".join(packages))\
   .getOrCreate()

df = spark \
    .read \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("startingOffsets", "earliest") \
    .option("subscribe", config['kafka']['TopicInName']) \
    .load()

df1 = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

df1.show()