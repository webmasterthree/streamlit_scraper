import pymongo
client = pymongo.MongoClient("mongodb://root:Edubild_123@mongodb:27017")
# client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.get_database("scraped")