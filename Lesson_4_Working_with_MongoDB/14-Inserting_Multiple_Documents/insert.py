from autos import process_file


def insert_autos(infile, db):
    data = process_file(infile)
    # Add your code here. Insert the data in one command.
    db.autos.insert(data)


from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.examples

insert_autos('autos.csv', db)
