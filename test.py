
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus

username = 'webmasterthreeedubild'
password = 'Oi9ads8TFEkPn4Yy'
encoded_username = quote_plus(username)
encoded_password = quote_plus(password)
print(encoded_username, "---", encoded_password)

uri = f"mongodb+srv://{encoded_username}:{encoded_password}@cluster0.ysm4ibh.mongodb.net/?appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)