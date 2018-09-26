import json
import sys
#import pandas as pd
#import numpy as np
import csv

csv.field_size_limit(sys.maxsize)

data = {'videoID': [],"title": [],"description":[],"author":[],"published":[],"viewcount":[], "duration":[], "likes":[], "dislikes":[],"rating":[],"category":[],"comments":[]}
video_comment = {'videoID':[], 'audience_comment':[[]], 'audience_name':[[]]}
video_combo_description = {'videoID': [], 'combodescription': []}
commentlist = []
channel_video = []
video_view = []

filename = "Health_new_scrapebyvideo.csv"
filename2 = "Health_new.json"
# store in sql: channel-video pair, video-view pair, channel-totalview pair
filename3 = "Health_channel_video.csv"
filename4 = "Health_video_view.csv"
filename5 = "Health_channel_view.csv"

with open(filename2, 'r') as input_file: 
	info = json.load(input_file)

with open(filename3, 'a') as out_file:
	wr = csv.writer(out_file, dialect='excel')
	for i in range(len(info['youID'])):
		channel_data = [info['channelID'][i], info['youID'][i]]
		wr.writerow(channel_data)
	
		
out_file2 = open(filename4, 'a')

with open(filename,'r') as input_file2:
    csv_reader = csv.reader(input_file2,delimiter=',')
    wr2 = csv.writer(out_file2, dialect='excel')
    row_count = 0
    for row in csv_reader:
        #commentlist = []
        #if row_count == 0: 
        #    commentlist = row[11].split('],')
        #    print commentlist[0].split(",")[1].strip("]")
        if row_count == 3:
        	test = row[12].strip("[").split('],')[0]
        	listoftest = test.split(",")
        	print listoftest[1]
        video_view = []
        data['videoID'].append(row[1])
        video_view.append(row[1])
        video_comment['videoID'].append(row[1])
        video_combo_description['videoID'].append(row[1])
        data['title'].append(row[2])
        video_combo_description['combodescription'].append(row[2])
        data['description'].append(row[3])
        video_combo_description['combodescription'][row_count] += row[3]
        data['author'].append(row[4])
        data['published'].append(row[5])
        data['viewcount'].append(row[6])
        video_view.append(row[6])
        wr2.writerow(video_view)
        data['duration'].append(row[7])
        data['likes'].append(row[8])
        data['dislikes'].append(row[9])
        data['rating'].append(row[10])
        data['category'].append(row[11])
        data['comments'].append(row[12])
        video_comment['audience_comment'].append([])
        video_comment['audience_name'].append([])
        commentlist = []
        commentlist = row[12].strip("[").split('],')
        for item in commentlist:
        	breaklist = item.split(",")
        	#username = breaklist[0][3:]
        	#content = breaklist[1][2:]
        	try:
        		username = breaklist[0]
        		content = breaklist[1]
        	
       		 	video_comment['audience_name'][row_count].append(username)
        		video_comment['audience_comment'][row_count].append(content)
        		video_combo_description['combodescription'][row_count] += content
        	except: pass
        row_count += 1
    
    #print 'row count=' + str(row_count)

#file to be loaded in Elasticsearch
with open('commentdata.json','w') as output_file2:
    json.dump(video_combo_description, output_file2)
    



    
    