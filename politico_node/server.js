var express=require('express') //Import 
var app=express();
var socket = require('socket.io-client')('http://localhost:5000');
var bodyParser = require('body-parser'); //Hacer get y post desde el front 
var MongoClient = require('mongodb').MongoClient, 
					assert = require('assert'); //May be es errores
var properties = require('./properties.json')

app.use(bodyParser.json()); // support json encoded bodies
app.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies
app.set('views', __dirname + '/views'); //REderizar vistas
app.engine('html', require('ejs').renderFile); // Para procesar todo el HTML 
app.use(express.static('static')); //Donde voy a guardar archivos estaticos (java script y sus librerias)

//app.use(express.bodyParser());


var options = { root: __dirname + '/static/'}

app.get('/', function(request, response){ //Start the main page 
	console.log("Conecting to Node Server...")
	response.render('index.html');
	console.log("Connection completed");
}).listen(properties.node.port) 

function sendMongo(callback){
	var url = 'mongodb://' + properties.mongo.host+':'+properties.mongo.port+'/'+properties.mongo.database;
	MongoClient.connect(url, function(err, db) {
			assert.equal(null, err);
			console.log("Se envío mensaje a mongo");
			callback(db);
			db.close();
		    });
}

app.post('/send_political', function(request, response){
	var political=request.body.search
	context = {}
	socket.emit('search politician', political)
	socket.on('my response', function(msg) {
    	context['nombre']=msg
    	sendMongo(function(database){
    		database.collection("documents").insertMany([msg])
    		console.log([msg])
    		}
    	);
	});
	       response.render('index.html',context)
    });

app.get("/autocomplete/politicos", function (request,response) {
	var nombre=request.query.query
	var arreglo=[]
	 sendMongo(function (db){
	 	db.collection('documents').find({"Nombre": {'$regex' : '.*' + nombre + '.*'}}).toArray(function(err, result) {
    		console.log("Found the following records");
    		for(var i=0;i<result.length;i++){
				arreglo.push({'data':String(result[i]._id),'value':result[i].Nombre})
			}
			console.log(arreglo)
			response.end(
				JSON.stringify({"query": request.query.query,"suggestions": arreglo})
			)
 		});
	})
})
