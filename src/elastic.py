from elasticsearch import Elasticsearch, helpers
#from pprint import pprint
from time import time
import json
#import pdb
import sys


def set_mapping(es, index_name = "test3", doc_type_name = "description_and_comment"):
    my_mapping = {
        "description_and_comment": {
            "properties": {
                "videoID": {
                    "type": "string"
                 },
                 "description": {
                    "type": "string"
                 }
            }
        }
    }
    create_index = es.indices.create(index = index_name,body = my_mapping)
    mapping_index = es.indices.put_mapping(index = index_name, doc_type = doc_type_name, body = my_mapping)
    if create_index["acknowledged"] != True or mapping_index["acknowledged"] != True:
    	print "Index creation failed..."


es = Elasticsearch()
es.indices.delete(index = "test3")
set_mapping(es)
actions = []

with open("commentdata.json","r") as read_file:

    #for i, line in tqdm(enumerate(open(data_path))):
	info = json.load(read_file)
	i = 0
	#print "combo" + info["videoID"][0]
	for i in range(10):
		print "uploaded video no.=" + str(i), "ID=", info["videoID"][i]
		actions.append({
            "_index": "test3",
            "_type": "description_and_comment",
            "_id": i,
            "_source": {
                "videoID": info["videoID"][i],
                "description": info["combodescription"][i][:100],
            }
        })

        #if len(actions) == 1000:
    #t0 = time()
	helpers.bulk(es, actions)
	print "success"
	actions = []
	#es.get(index = "test3", doc_type = "description_and_comment", id = 1)
	#res= es.search(index='test3',body={'query':{'match':{'videoID':'zQJhQgRH9LU'}}})
	#print res["hits"]["hits"][0]["_source"]["videoID"]
	
	#print 'res='+res
#            print("%d: inserted in %d seconds" % (i, time() - t0))

    	#helpers.bulk(es, actions)
    	#actions = []

