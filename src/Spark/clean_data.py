import sys
import os
import itertools
import boto3
import json

from pyspark.context import SparkContext
from pyspark.sql import SparkSession, SQLContext, Row
from pyspark.sql.functions import to_timestamp, regexp_replace, udf, explode
from pyspark.sql.types import *
from pyspark.sql.functions import udf

#create spark object
sc = SparkContext.getOrCreate()
sqlContext = SQLContext(sc)

#read file from S3
#video_df stores the videoID, title, description, view count, likes/dislikes, author username, duration and category for a video
video_df = spark.read.format("csv") \
        .option("delimiter", ",")\
        .load('s3a://youtubedatainsight/video_info.csv')

# add headers
video_df = video_df.toDF("keyword","videoID","title","description","author","published","viewcount",\
"duration","likes","dislikes","rating","category","comments")

#video_channel_df stores the videoID and channelID for a video
video_channel_df = sqlContext.read.option("mode", "DROPMALFORMED").option('charset', 'UTF-8').json("s3a://youtubedatainsight/video_channel.json")

#join two tables to map video information to channel_ID
video_df = video_df.join(video_channel_df, video_df.videoID == video_channel_df.youID)

#drop duplicated rows of video information if videoID is the same
video_df = video_df.dropDuplicates(['videoID'])

#join description column with title 
df = df.withColumn('joincol', sf.concat(sf.col('description'),sf.lit('_'), sf.col('title')))

#combine title,description,all user comments together                    
df = df.withColumn('combo_description', sf.concat(sf.col('joincol'),sf.lit('_'), sf.col('comments')))

#drop some columns
columns_to_drop = ["duration","published","likes","dislikes","rating","category","youID", "description","title","joincol","comments"]
video_df.drop(*columns_to_drop)

#save to json file
pandas_df = df.toPandas()
pandas_df.to_json("video_processed.json")





