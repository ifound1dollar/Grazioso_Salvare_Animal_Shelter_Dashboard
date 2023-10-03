from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
  def __init__(self, username, password, host, port, database, collection):
    # connection vars, fully parameterized
    USER = username
    PASS = password
    HOST = host
    PORT = port
    DB = database
    COL = collection
    
    # actually open connection
    self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER, PASS, HOST, PORT))
    self.database = self.client['%s' % (DB)]
    self.collection = self.database['%s' % (COL)]
  
  def create(self, data): # data is a single dictionary to add
    # ensure data is not empty
    if data is not None:
      # attempt to insert, then return acknowledgement
      result = self.database.animals.insert_one(data)
      return result.acknowledged
    else:
      raise Exception("Cannot insert empty data into database.")
  
  def read(self, query):
    # if query is null, return entire collection
    if query is not None:
      find_result = self.database.animals.find(query)
    else:
      find_result = self.database.animals.find()
    
    # create empty list and populate with find results via iterator
    result_list = list()
    for document in find_result:
      result_list.append(document)
    
    # after list populated with results (or empty if no results), return it
    return result_list
  
  def update(self, query, data):
    # do not allow query or data to be empty
    if query is not None and data is not None:
      # call update_many function with 'query' dict and update 'data' dict,
      # setting new data (strictly using $set keyword) and returning a cursor
      update_result = self.database.animals.update_many(query, {'$set': data})
      return update_result.modified_count
    else:
      raise Exception("Cannot perform update on null query or update data.")
  
  def delete(self, query):
    # do not allow query to be empty (would delete entire collection contents)
    if query is not None:
      # call delete_many function with 'query' dict, returning a cursor
      delete_result = self.database.animals.delete_many(query)
      return delete_result.deleted_count
    else:
      raise Exception("Cannot perform delete on null query.")
