# CSE40437/CSE60437 - A2

This is the second assignment for my Social Sensing/Cyber-Physical Systems Class.

## Getting Started

Download everything from either (1) my dropbox (folder A2) or (2) clone this repository on GitHub.

### Prerequisites

I developed this in Python 3.6.4, and used the json, sys, and numpy libraries.

### Exercises

Implement the tweet clustering function using the Jaccard Distance metric and K-means clustering algorithm introduced above to cluster redundant/repeated tweets into the same cluster. You are expected to do the K-means implementation by yourself, so please do not use any external library that has K-means implementation in your code.

Note that while the K-means algorithm is proven to converge, the algorithm is sensitive to the k initial selected cluster centroids (i.e., seeds) and the clustering result is not necessarily optimal on a random selection of seeds. In this assignment, we provide you with a list of K initial centroids that has been tested to generate good results.

Inputs to your K-means Algorithm:

(1) The number of clusters K=25.

(2) A real world dataset sampled from Twitter during the Boston Marathon Bombing event in April 2013 that contains 251 tweets. Tweet Dataset Download .

(3) The list of initial centroids is here: Initial Seeds . Note that each element in this list is the tweet ID (i.e., the id field in JSON format) of the tweet in the dataset.

Jaccard Distance Function
```
def jacc_dist(tweet1, tweet2):
    a = set(tweet1.split(' '))
    b = set(tweet2.split(' '))
    a_and_b = a.intersection(b)
    a_union_b = a.union(b)
    return 1-len(a_and_b)/len(a_union_b)
```

K-means Algorithm
```
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
```

## Running the Script

To run this script in Jupyter, cd into the A1 project folder, and open the notebook (A2.ipynb) with the following command.

```
jupyter notebook A2.ipynb
```

You can then run cells individually.

The K parameter is originally set to 25, but can be changed in cell 5.
**Make sure cell 5 is commented correctly.**

```
# if(len(sys.argv) == 3):
#     tweets_file = sys.argv[1]
#     seeds_file = sys.argv[2]
#     k = 25
# if(len(sys.argv) == 4):
#     tweets_file = sys.argv[1]
#     seeds_file = sys.argv[2]
#     k = int(sys.argv[3])
tweets_file = './tweets.json'
seeds_file = './seeds.txt'
k = 25
```

To run this script from the command line, use the following commands.
**Make sure cell 5 is commented correctly.**

```
if(len(sys.argv) == 3):
    tweets_file = sys.argv[1]
    seeds_file = sys.argv[2]
    k = 25
if(len(sys.argv) == 4):
    tweets_file = sys.argv[1]
    seeds_file = sys.argv[2]
    k = int(sys.argv[3])
# tweets_file = './tweets.json'
# seeds_file = './seeds.txt'
# k = 25
```

Running the following command (only 3 arguments) will execute the script with 25-means clustering.

```
python3 A2_script.py tweets.txt seeds.txt
```

Running the following command (with the 4th argument) will execute the script with 10-means clustering.

```
python3 A2_script.py tweets.txt seeds.txt 10
```
