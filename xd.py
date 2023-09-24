import pymongo

def update_s3_uri(mongo_connection_uri, database_name, coll_name):
    client = pymongo.MongoClient(mongo_connection_uri)
    db = client[database_name]
    collection = db[coll_name]

    for doc in collection.find():
        original_uri = doc['s3_uri']
        updated_uri = original_uri.replace('/mw2022/', '/').replace('/mw2019/', '/')
        if updated_uri != original_uri:
            collection.update_one({'_id': doc['_id']}, {'$set': {'s3_uri': updated_uri}})

if __name__ == "__main__":
    mongo_connection_uri = 'mongodb+srv://kikogoncalves:XlYJBZmCAYe2qfSE@finishershub.fkag1ww.mongodb.net/finishers-club?retryWrites=true&w=majority'
    database_name = 'finishers-club'
    coll_name = 'Videos'

    update_s3_uri(mongo_connection_uri, database_name, coll_name)
