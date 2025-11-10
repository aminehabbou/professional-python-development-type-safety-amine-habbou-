from mongoengine import connect

MONGO_URL = "mongodb://amineh:secret2@localhost:27017/python-for-de?authSource=admin"

connect(host=MONGO_URL)
