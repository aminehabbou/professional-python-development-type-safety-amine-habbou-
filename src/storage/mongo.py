from mongoengine import connect

MONGO_URL = "mongodb://amineh:secret2@localhost:27017/"

connect("pythonde", host=MONGO_URL)
