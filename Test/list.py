import json
import pymongo

conn1 = pymongo.MongoClient(host='mongodb://localhost:27019/')
db1 = conn1["SearchEngineDB"]
col1 = db1["htmlResults"]


for i in col1.find({"_id": "tgveukawqd"}):
    data = i['data']
    data = data[0]

    for i in data:
        print('\n' + i)
