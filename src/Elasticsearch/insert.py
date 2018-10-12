import json
import sys
import boto3
from elasticsearch import Elasticsearch, helpers

# create mapping and create index
def set_mapping(es, index_name = "youtubedata", doc_type_name = "video_info"):

# format mapping for indexing 
    my_mapping = {
        "video_info": {
            "properties": {
                "videoID": {
                    "type": "string"
                 },
                 "description": {
                    "type": "string"
                 },
                "views": {
                    "type": "string"
                 },
                "combodescription": {
                    "type": "string"
                 }
            }
        }
    }

# create index and put mapping
    create_index = es.indices.create(index = index_name,body = my_mapping)
    mapping_index = es.indices.put_mapping(index = index_name, doc_type = doc_type_name, body = my_mapping)

# inform if creating index fail
    if create_index["acknowledged"] != True or mapping_index["acknowledged"] != True:
    	print "Index creation failed..."

# establish connection with Elasticsearch cluster 
es = Elasticsearch(["your Elasticsearch IP"])

# create index and put mapping for the index of "youtubedata"
set_mapping(es)

# file contains all video information scraped and cleaned previously
filename = "video_processed.json"

with open(filename,'r') as input_file:
# variable to count how many items are processed, how many items are inserted into ES
    row_count = 0
    actual_row = 0
# create a list to store data for bulk request
    actions = []

# bulk request size is 200 documents each time
    size=200
    for line in input_file:

# load each line
          v_info = json.loads(line)

# store video information in the "actions" list
        	row_count += 1
        	actions.append({
            "_index": "youtubedata",
            "_type": "video_info",
            "_source": {
                "videoID": v_info["videoID"],
                "description": v_info["combodescription"],
                "channelID": v_info["channelID"],
                "views": v_info["views"],
            }
        })

# bulk insert to ES every 200 documents
        	if row_count%size ==0:
        			helpers.bulk(es, actions,request_timeout=20)

# "actions" list is emptied after bulk insert is finished
        		  actions = []
        actual_row += 1

# inform how many lines are processed and how many lines are inserted
print "total =" + str(actual_row)+"actual="+str(row_count)



    
    
