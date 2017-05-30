import Libraries.pyRedis as redis
import Libraries.FileManager as fm

# -*- coding: utf-8 -*-
def loadCategorias():
	try:     
		with fm.readFile("categorias.txt") as file:
			for line in file:
				print "sadd categoria " + line.strip("\n")
				def function(redisClient):					
					return "Registros insertados: " + str(redisClient.sadd("categoria",line.strip("\n")))
				print(redis.sendRedis(function))
	except IOError as ierror:
		fm.registerError("No se puede leer el archivo: \n" + str(ierror))
	except Exception as ex:
		fm.registerError("Se presento el error en la carga de las categorias: \n" + str(ex))
def cleanOnotology():
	def function(redisClient):
		redisClient.flushall()
	redis.sendRedis(function)
cleanOnotology()	
loadCategorias()