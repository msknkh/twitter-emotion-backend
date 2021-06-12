from flask import Flask, render_template, request
from my_package.model import predict_on_twitter_data 
import requests
from flask_cors import CORS
import tracemalloc

tracemalloc.start(25)

# ... run your application ...

json = predict_on_twitter_data("happu", 100)

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('traceback')

# pick the biggest memory block
stat = top_stats[0]
print("%s memory blocks: %.1f KiB" % (stat.count, stat.size / 1024))
for line in stat.traceback.format():
    print(line)