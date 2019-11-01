import json
from pprint import pprint
from heapq import nlargest
import math

with open('wordcount.json') as f:
    data = json.load(f)

largest = nlargest(10, data, key=data.get)

pprint(largest)


# 10 Most common words:
# can
# learning
# model
# function
# set
# data
# algorithm
# using
# number
# also