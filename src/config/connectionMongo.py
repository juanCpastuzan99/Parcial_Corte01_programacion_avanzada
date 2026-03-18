from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["acortador_enlaces"]
imagenUrl = db["imagenUrl"]

