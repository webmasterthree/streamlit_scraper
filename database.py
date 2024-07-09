import pymongo
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus


load_dotenv(".env")


encoded_username = quote_plus(os.getenv('MONGO_USERNAME'))
encoded_password = quote_plus(os.getenv('MONGO_PASSWORD'))


mongo_uri = f"mongodb+srv://{encoded_username}:{encoded_password}@cluster0.ysm4ibh.mongodb.net/?appName=Cluster0"

# client = pymongo.MongoClient("mongodb://root:Edubild_123@mongodb:27017")
client = pymongo.MongoClient(mongo_uri)

# client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.get_database("scraped")