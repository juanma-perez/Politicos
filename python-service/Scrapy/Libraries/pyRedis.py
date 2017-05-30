# -*- coding: utf-8 -*-
import json 
import redis

def sendRedis(callback):
	redisClient = redis.StrictRedis(host='localhost', port=6379, db=0) 	
	#print("Conectandose a redis")
	#print("Se envío mensaje a redis")
	return callback(redisClient)	

def testRedis(redisClient):
	print(redisClient.get('test'))

def addSet(root, json):
	for subRoot in json:
		clave = root + ':' + subRoot
		for i in range(0,len(json[subRoot])):				
			print("sadd "+clave.encode("utf-8")+" " +json[subRoot][i].encode("utf-8"))
			def function(redisClient):
				return "Registros insertados: " + str(redisClient.sadd(clave,json[subRoot][i]))
			print(self.sendRedis(function))

def getSet(self, query):
	def function(redisClient):
				return redisClient.smembers(query)
	return self.sendRedis(function)
