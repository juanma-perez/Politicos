var express=require('express') //Import 
var app=express();
var socket = require('socket.io-client')('http://localhost:5000');
var bodyParser = require('body-parser'); //Hacer get y post desde el front 
var MongoClient = require('mongodb').MongoClient, 
					assert = require('assert'); //May be es errores
var properties = require('./properties.json')
var redis = require('redis')



app.use(bodyParser.json()); // support json encoded bodies
app.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies
app.set('views', __dirname + '/views'); //REderizar vistas
app.engine('html', require('ejs').renderFile); // Para procesar todo el HTML 
app.use(express.static('static')); //Donde voy a guardar archivos estaticos (java script y sus librerias)

function testRedis(redisClient){
	//redisClient.set('test','It's working,redis.print)
	redisClient.get('test',function(error,value){
			if(error){
				throw error
			}
			console.log("Testing a query in redis")
			console.log("-->" + value)
		})
}

var options = { root: __dirname + '/static/'}

app.get('/', function(request, response){ //Start the main page 
	console.log("Conecting to Node Server...")
	response.render('index.html');
	console.log("Connection completed");
	//sendRedis(testRedis);
}).listen(properties.node.port) 

function sendMongo(callback){
	var url = 'mongodb://' + properties.mongo.host+':'+properties.mongo.port+'/'+properties.mongo.database;
	MongoClient.connect(url, function(err, db) {
		if (err){
			console.log("Se presentó error" + err)
		}
		assert.equal(null, err);
		console.log("Se envío mensaje a mongo");
		callback(db);
		console.log(err)
		db.close();
	});

}
function sendRedis(callback){	
	var redisClient = redis.createClient(properties.redis.port, properties.redis.host)
	console.log("Conectandose a redis")
	redisClient.on('error',function(error){
		console.log("Se presentó un error con redis")
	})
	console.log("Se envío mensaje a redis")
	callback(redisClient)
	redisClient.quit();
}

app.use(express.static('static')); 

app.get('/send_political', function(request, response){

	var political="Ernesto Samper"

	
	context = {}
	socket.emit('search politician', political)
	socket.on('my response', function(msg) {
    	context['nombre']=msg
    	sendMongo(function(database){
    		database.collection(properties.mongo.collections).insertMany([msg])
    		console.log([msg])
    		}
    	);
	});
	       response.render('index.html',context)
    });

app.get('/search/person:*', function(request, response){

	var political=request.query.search
	console.log(request.query.search)
	
	context = {}
	list_political=[]

	sendMongo(function (db){
	 	db.collection(properties.mongo.collections).find({"Nombre": {"$in": [new RegExp(political, "i") ]} }).toArray(function(err, result) {
	 		console.log({"Nombre": {"$in": [/nombre/i] } })

    		for(var i=0;i<result.length;i++){

    			dict_personaje={}

    			dict_personaje['id']=result[i]._id

    			if(result[i].Nombre){

    				dict_personaje['nombre']=result[i].Nombre
    			}else{
    				dict_personaje['nombre']=''
    			}

    			if(result[i].Foto != 'No_Disponible' ){
    				dict_personaje['foto']=result[i].Foto

    			}else{
    				dict_personaje['foto']='/images/hombre.png'
    			}

    			if (result[i]['Información personal']){
	    			if(result[i]['Información personal']['Nacionalidad']){
	    				dict_personaje['nacionalidad']=result[i]['Información personal']['Nacionalidad']

	    			}else{
	    				dict_personaje['nacionalidad']=''
	    			}
	    			if(result[i]['Información personal']['Nacimiento']){
	    				dict_personaje['nacimiento']=result[i]['Información personal']['Nacimiento'][0]

	    			}else{
	    				dict_personaje['nacimiento']=''
	    			}

	    			if(result[i]['Información personal']['Residencia']){
	    				dict_personaje['residencia']=result[i]['Información personal']['Residencia']

	    			}else{
	    				dict_personaje['residencia']=''
	    			}
    			}else{
    				dict_personaje['nacionalidad']=''
    				dict_personaje['nacimiento']=''
    				dict_personaje['residencia']=''
    			}
   	
    			
				if(result[i]['Información profesional']){
					if(result[i]['Información profesional']['Ocupación']){
	    				dict_personaje['ocupacion']=result[i]['Información profesional']['Ocupación']
	    			}else{
	    				dict_personaje['ocupacion']=''
	    			}
				}else{
					dict_personaje['ocupacion']=''
				}	

    			

				list_political.push(dict_personaje)
			}

			context['political_list']=list_political
			context['search']=request.query.search

			response.render('search_political.html',context)
 		});
	})

    });


app.get("/autocomplete/politicos", function (request,response) {
	var nombre=request.query.query
	var arreglo=[]

	sendMongo(function (db){
	 	db.collection(properties.mongo.collections).find({"Nombre": {"$in": [new RegExp(nombre, "i") ]} }).toArray(function(err, result) {
	 		console.log({"Nombre": {"$in": [/nombre/i] } })
    		for(var i=0;i<result.length;i++){
				arreglo.push({'data':String(result[i]._id),'value':result[i].Nombre})
			}
			response.end(
				JSON.stringify({"query": request.query.query,"suggestions": arreglo})
			)
 		});
	})
})