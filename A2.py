
# coding: utf-8

# In[1]:


import json, sys
import numpy as np


# In[2]:


def jacc_dist(tweet1, tweet2):
    a = set(tweet1.split(' '))
    b = set(tweet2.split(' '))
    a_and_b = a.intersection(b)
    a_union_b = a.union(b)
    return 1-len(a_and_b)/len(a_union_b)


# In[3]:


def cluster_tweets(tweet_dict, centroid_ids):

    # initialize centroid_dict
    centroid_dict = {}
    for centroid_id in centroid_ids:
        centroid_dict[centroid_id] = []
    
    # get centroid texts for comparison/distance measure
    centroid_text_list = [tweet_dict[tweet_id] for tweet_id in list(centroid_dict.keys())]

    # loop through every tweet in tweet_dict
    for tweet_id, tweet_text in tweet_dict.items():
    
        # get distances to each centroid
        dist_to_centroid = [jacc_dist(tweet_text, centroid_text) for centroid_text in centroid_text_list]

        # get index of closest centroid
        index = np.argmin(dist_to_centroid)

        # append tweet_id to closest centroid_id 
        centroid_dict[centroid_ids[index]].append(tweet_id)
    
    # return centroid_dict
    return(centroid_dict)


# In[4]:


def update_centers(tweet_dict, centroid_dict):
    
    # to store updated/new means
    new_centroid_ids = []

    # find updated mean for each centroid
    for centroid_id, tweet_ids in centroid_dict.items():

        centroid_min_dist = 1
        centroid_min_dist_id = ''

        # compute distance from 'this' tweet to 'other' tweets
        for tweet_id in tweet_ids:

            this_tweet   = tweet_dict[tweet_id]
            other_tweets = [tweet_dict[other_id] for other_id in tweet_ids]

            # calculate dist to other tweets
            dist_to_other_tweets     = [jacc_dist(this_tweet, other_tweet) for other_tweet in other_tweets]
            ave_dist_to_other_tweets = np.mean(dist_to_other_tweets)

            # if 'this' tweet closer to other tweets, make it new center
            if ave_dist_to_other_tweets < centroid_min_dist:
                centroid_min_dist = ave_dist_to_other_tweets
                centroid_min_dist_id = tweet_id

        # append new centroid id to new list
        new_centroid_ids.append(centroid_min_dist_id)

    # return new means
    return(new_centroid_ids)


# In[5]:


if(len(sys.argv) == 3):
    tweets_file = sys.argv[1]
    seeds_file = sys.argv[2]
    k = 25
if(len(sys.argv) == 4):
    tweets_file = sys.argv[1]
    seeds_file = sys.argv[2]
    k = int(sys.argv[3])
#tweets_file = './tweets.json'
#seeds_file = './seeds.txt'
#k = 25


# In[6]:


tweet_dict = {}
for tweet in open(tweets_file):
    tweet_json = json.loads(tweet)
    tweet_dict[tweet_json['id']] = tweet_json['text']

with open(seeds_file) as f:
    centroid_ids = f.readlines()
centroid_ids = [int(x.strip().replace(',','')) for x in centroid_ids]

# implement k parameter
centroid_ids = list(np.random.choice(centroid_ids, size=k, replace=False))


# In[7]:


# tracking
iter_no = 1

print('using {}-means algorithm'.format(k))

while(True):
    
    # cluster phase
    cd = cluster_tweets(tweet_dict, centroid_ids)
    
    # save old centroids for checking convergence
    centroid_ids_old = centroid_ids
    
    # update phase - new centroid_ids
    centroid_ids = update_centers(tweet_dict, cd)

    if centroid_ids == centroid_ids_old: # convergence reached
        
        print('iteration #{}: converged'.format(iter_no))
        
        # write to file
        with open('results.txt', 'w') as file:
             file.write(json.dumps(cd))
        
        # break out of loop
        break
        
    else: # has not converged
    
        print('iteration #{}: converging...'.format(iter_no))
        iter_no += 1

