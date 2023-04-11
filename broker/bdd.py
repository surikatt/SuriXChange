from pymongo import MongoClient
from dotenv import load_dotenv
import os


load_dotenv()

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = os.getenv('IDBDD')
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
   return client

client = get_database()

db = client.get_database("surikatt")
appareils = db.get_collection("appareils")


# item_1 = {
#   "id_appareil" : "2",
#   "nom" : "contacteur porte",
#   "category" : "appareils"
# }

#appareils.insert_one(item_1)

def check_apppareil(id):
   return appareils.find_one({'id_appareil': id})