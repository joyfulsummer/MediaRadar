# MediaRadar
# Project Idea
This data product empowers context market by matching Youtube bloggers with product advertisement through Elasticsearch.
# Use Case
There are too much advertisement now, no matter people are walking on the street or surfing the internet. One good question is how much your advertising is trusted? One efficient way to build trust between product advertisement and audience is to collaborate with Youtube bloggers, and ask them to create videos and present the product in their channel. Then the question is which bloggers to choose? Instead of spending days searching on Youtube, companies can just use my product, Media Radar!

With Media Radar, the brand, type, and keyword of a product is entered, and Media Radar will return a list of channels according to the total views of related videos (popularity) or the average similarity scores of the related videos (similarity). With the list of recommended channels, the company can go ahead and contact the bloggers!
# Algorithm
I first built my own database by collecting one million Youtube video information using 3000 keywords. The keywords come from multiple sources like the Wiki page, Amazon, Macy’s, and Youtube 8M dataset (https://research.google.com/youtube8m/). The keywords are used to search for videos by calling Youtube API. The video information that I collected includes video title, description, comments, number of views, likes/dislikes, duration, author name, channel ID, etc. 

The front end receives keywords of a product like the product brand, type, and keyword. The database returns a list of 1000 videos which matches the description of the product. Each video will map to a channel ID. I sort the channel ID according to two metrics: popularity (total number of views of related videos) and similarity (average similarity score returned by database). 
# Data Pipeline

# Data Challenge
