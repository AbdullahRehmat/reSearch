import json
import pymongo
import datetime

if __name__ == "__main__":

    mongo_port = 27020
    mongo_host = "localhost"
    mongo_db_1 = "ContentScraperDB"
    mongo_col_1 = "scrapedData"

    # Database Connection: MongoDB
    conn = pymongo.MongoClient(
        host=f"mongodb://{mongo_host}:{str(mongo_port)}/")

    db1 = conn[mongo_db_1]      # ContentScraperDB
    col1 = db1[mongo_col_1]     # scrapedData


    documents = []
    cursor = col1.find({})
    for document in cursor:

        # Format Document ID As String
        document["_id"] = str(document["_id"])

        documents.append(document)

    json_output = {
        "version": "1.0.0",
        "last_updated": str(datetime.datetime.today().strftime('%d-%m-%Y')),
        "document_count": len(documents),
        "documents": documents
    }

    with open("database_dump.json", "w") as outfile:
        outfile.write(json.dumps(json_output))
