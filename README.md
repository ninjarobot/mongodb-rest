## MongoDB REST API

mongodb-rest provides a RESTful API for accessing a MongoDB database.  It is built on python and the twisted web framework.

You can run any query that you would with the command line or pymongo driver and get JSON back.  There are a few ways to query:

http://localhost:8090/dbName/collectionName - this will return all documents in the collection.
http://localhost:8090/dbName/collectionName/id - this will return a single document by its ID
http://localhost:8090/dbName/collectionName?find={"someField":{"$gte":90}} - this will execute the MongoDB query document specified in the find parameter.  
http://localhost:8090/dbName/collectionName?query=someField>=90 - this will do simple queries on a particular field.  Operators supported include =, !=, >, >=, <, <=.

### A few limitations:
- Query only at this time.
- Working on insert and update.
- There is no way to select partial documents.
