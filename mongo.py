import pymongo


def update_s3_uri(mongo_connection_uri, database_name, coll_name):
    client = pymongo.MongoClient(mongo_connection_uri)
    db = client[database_name]
    collection = db[coll_name]

    for doc in collection.find():
        original_uri = doc["s3_uri"]
        updated_uri = original_uri.replace("/mw2022/", "/").replace("/mw2019/", "/")
        if updated_uri != original_uri:
            collection.update_one(
                {"_id": doc["_id"]}, {"$set": {"s3_uri": updated_uri}}
            )


def update_bucket_entries(mongo_connection_uri, database_name, coll_name):
    client = pymongo.MongoClient(mongo_connection_uri)
    db = client[database_name]
    collection = db[coll_name]

    for doc in collection.find():
        if "bucket" in doc and doc["bucket"] != "finishershub":
            collection.update_one(
                {"_id": doc["_id"]}, {"$set": {"bucket": "finishershub"}}
            )

        if "s3_uri" in doc:
            original_uri = doc["s3_uri"]
            updated_uri = original_uri.replace(
                "finishershub.mw2019", "finishershub"
            ).replace("finishershub.mw2022", "finishershub")
            if updated_uri != original_uri:
                collection.update_one(
                    {"_id": doc["_id"]}, {"$set": {"s3_uri": updated_uri}}
                )


def update_s3_uris_with_new_format(mongo_connection_uri, database_name, coll_name):
    client = pymongo.MongoClient(mongo_connection_uri)
    db = client[database_name]
    collection = db[coll_name]

    for doc in collection.find():
        original_uri = doc.get("s3_uri", "")
        bucket = doc.get("bucket", "")
        filename = doc.get("filename", "")
        new_s3_uri = f"s3://{bucket}/{filename}"

        if new_s3_uri != original_uri:
            collection.update_one({"_id": doc["_id"]}, {"$set": {"s3_uri": new_s3_uri}})


if __name__ == "__main__":
    mongo_connection_uri = "mongodb+srv://kikogoncalves:XlYJBZmCAYe2qfSE@finishershub.fkag1ww.mongodb.net/finishers-club?retryWrites=true&w=majority"
    database_name = "finishers-club"
    coll_name = "Videos"

    update_s3_uris_with_new_format(mongo_connection_uri, database_name, coll_name)
