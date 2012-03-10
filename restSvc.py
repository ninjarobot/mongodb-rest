from twisted.web import server, resource, http
from twisted.internet import reactor, threads
from pymongo import Connection
import json
from json import JSONEncoder
from pymongo.objectid import ObjectId
import string
import datetime

class MongoEncoder(JSONEncoder):
    def default(self, obj, **kwargs):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date) or isinstance(obj, datetime.time):
			return unicode(obj)
        else:            
            return JSONEncoder.default(obj, **kwargs)
            
def getConnection():
	return Connection('mongodb://localhost:27017/?slaveOk=true')

def getItemsAsJson(items):
    return json.dumps(items, cls=MongoEncoder)

def getItemsAsJsonDeferred(items):
	d = threads.deferToThread(getItemsAsJson,items)
	d.addCallback(getItemsAsJsonCallback)

def getItemsAsJsonCallback(result):
	return result

def parseParam(p):
	if string.find(p,'"') > -1:
		return p.replace('\"','')
	elif string.find(p,'.') > -1:
		return float(p)
	else:
		return long(p)

def parseQuery(query):
	ne = string.split(query,'!=')
	gte = string.split(query,'>=')
	lte = string.split(query,'<=')
	gt = string.split(query,'>')
	lt = string.split(query,'<')
	eq = string.split(query,'=')
	if len(ne) > 1:
		ne[1] = parseParam(ne[1])
		return {ne[0]:{"$ne":ne[1]}}
	if len(gte) > 1:
		gte[1] = parseParam(gte[1])
		return {gte[0]:{"$gte": gte[1]}}
	if len(lte) > 1:
		lte[1] = parseParam(lte[1])
		return {lte[0]:{"$lte": lte[1]}}
	if len(eq) > 1:
		eq[1] = parseParam(eq[1])
		return {eq[0]:eq[1]}
	if len(gt) > 1:
		gt[1] = parseParam(gt[1])
		return {gt[0]:{"$gt": gt[1]}}
	if len(lt) > 1:
		lt[1] = parseParam(lt[1])
		return {lt[0]:{"$lt": lt[1]}}
	
def getItems(dbName, collName, id=None, query=None, find=None):
	conn = getConnection()
	db = conn[dbName]
	coll = db[collName]
	if id != None:
		res = coll.find({"_id":int(id)});
	else:
		if find != None:
			res = coll.find(json.loads(find[0]))
		elif query != None:
			res = coll.find(parseQuery(query[0]))
		else:
			res = coll.find()
	items = list()
	for item in res:
		items.append(item)
	return items

class RootResource(resource.Resource):
	isLeaf = True
	def render_GET(self, request):
		if len(request.postpath) == 2 and request.args.has_key("find"):
			return getItemsAsJson(getItems(request.postpath[0],request.postpath[1],find=request.args["find"]))
		elif len(request.postpath) == 2 and request.args.has_key("query"):
			return getItemsAsJson(getItems(request.postpath[0],request.postpath[1],query=request.args["query"]))
		elif len(request.postpath) == 2:
			return getItemsAsJson(getItems(request.postpath[0],request.postpath[1]))
		elif len(request.postpath) == 3:
			return getItemsAsJson(getItems(request.postpath[0],request.postpath[1], request.postpath[2]))
		else:
			return "<html>%s</html>" % (request.__dict__);
		
site = server.Site(RootResource())
reactor.listenTCP(8090, site)
reactor.run()