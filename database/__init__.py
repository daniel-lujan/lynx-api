import pymongo

from config import DATABASE_NAME, MONGO_URI

client = pymongo.MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

forms = db["forms"]
motels = db["motels"]