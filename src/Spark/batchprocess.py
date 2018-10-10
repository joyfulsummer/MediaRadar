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
        .option("delimiter", ",").option("quote", "") \
        .option("header", "true") \
        .load('s3a://youtubedatainsight/Beauty_new_scrape.csv')
#video_channel_df stores the videoID and channelID for a video
video_channel_df = sqlContext.read.option("mode", "DROPMALFORMED").option('charset', 'UTF-8').json("s3a://youtubedatainsight/Beauty_1.json")

#join two tables to map video information to channel_ID
video_df = video_df.join(video_channel_df, video_df.videoID == video_channel_df.videoID).drop(video_channel_df.videoID)

#drop duplicated video information according to videoID
df.dropDuplicates(['videoID'])

#drop useless columns
df.drop("keyword","published","duration","category")

#define function to split comments, store all comments in one string
def func(col):
	combo_comment = ""
    comment_list =  col.strip("[").split('],')
    for item in commen_list:
    	breaklist = item.split(",")
    	username = breaklist[0]
    	content = breaklist[1]
    	combo_comment += content
    return combo_comment

func_udf = udf(func, IntegerType())
# put all comments into a combined comments
df = df.withColumn('combo_comment',func_udf(df['comments']))

#drop original comment
df.drops(['comments'])

#join newly generated combo_comment column with title 
df = df.withColumn('joincol', sf.concat(sf.col('combo_comment'),sf.lit('_'), sf.col('title')))

#combine title,description,all user comments together                    
df = df.withColumn('combo_description', sf.concat(sf.col('joincol'),sf.lit('_'), sf.col('description')))

#drop useless columns
df.drops(['joincol','description','title'])

#save to json file
pandas_df = df.toPandas()
pandas_df.to_json("Beauty_video.json")
