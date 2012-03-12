## MongoDB REST API

mongodb-rest provides a RESTful API for accessing a MongoDB database.  It is built on python and the twisted web framework.

You can run any query that you would with the command line or pymongo driver and get JSON back.  There are a few ways to query:

http://localhost:8090/dbName/collectionName - this will return all documents in the collection.
http://localhost:8090/dbName/collectionName/id - this will return a single document by its ID
http://localhost:8090/dbName/collectionName?find={"someField":{"$gte":90}} - this will execute the MongoDB query document specified in the find parameter.  
http://localhost:8090/dbName/collectionName?query=someField>=90 - this will do simple queries on a particular field.  Operators supported include =, !=, >, >=, <, <=.

### Prerequisites
- Twisted
- Pymongo

### Getting started
1. Download restSvc.py
2. Change the connection string (line 21) to match your DB if not connecting to localhost.
3. Change the port (line 110) if you don't want to run on port 8090
4. At a command line, run "twistd -y restSvc.py" to start twistd running the application.

### A few limitations:
- Query only at this time.
- Working on insert and update.
- There is no way to select partial documents.
