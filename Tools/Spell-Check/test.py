import pymongo
from app import SpellChecker

mongo_host = "localhost"
mongo_port = 27019
mongo_db = "ContentScraperDB"
mongo_col = "ScrapedData-C1"


conn = pymongo.MongoClient(
    host=f"mongodb://{mongo_host}:{str(mongo_port)}/")
db = conn[mongo_db]
col = db[mongo_col]


for data in col.find():
    id = data["_id"]
    title = data["title"]
    url = data["url"]

    s = SpellChecker()

    print(type(title))

    new_title = s.spell_checker(title)
    new_title = new_title

    filter = {"title": title}
    replacement = {"title": new_title}

    print(title)
    print(new_title)
    print("")

    col.find_one_and_replace(filter, replacement)

corpus = []
for data in col.find():
    corpus += data["title"]
    
print(len(corpus))
