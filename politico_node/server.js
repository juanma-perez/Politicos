var express=require('express') //Import 
var app=express();
var socket = require('socket.io-client')('http://localhost:5000');
var bodyParser = require('body-parser'); //Hacer get y post desde el front 
var MongoClient = require('mongodb').MongoClient, 
					assert = require('assert'); //May be es errores


var url = 'mongodb://localhost:27017/politicos'; //con puerto por defecto 


app.use(bodyParser.json()); // support json encoded bodies
app.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies
app.set('views', __dirname + '/views'); //REderizar vistas
app.engine('html', require('ejs').renderFile); // Para procesar todo el HTML 
app.use(express.static('static')); //Donde voy a guardar archivos estaticos (java script y sus librerias)

//app.use(express.bodyParser());


var options = { root: __dirname + '/static/'}

var insertDocuments = function(db, data,callback) {
  // Get the documents collection 
  var collection = db.collection('documents');
  // Insert some documents 
  collection.insertMany(
    [data]   , function(err, result) {
    assert.equal(err, null);
    callback(result);
  });
}

var findPoliticosAutocomplete = function(db, value,callback) {
  // Get the documents collection 
  var collection = db.collection('documents');
  // Find some documents 
  //console.log(value)
  collection.find({"Nombre": {'$regex' : '.*' + value + '.*'}}).toArray(function(err, docs) {
    assert.equal(err, null);
    //assert.equal(2, docs.length);
    console.log("Found the following records");
    //console.dir(docs);
    callback(docs);
  });
}



app.get('/', function(request, response){ //Start the main page 
	console.log("Conecting to Node Server...")
	response.render('index.html');
	console.log("Connection completed")
}).listen(8080) 



app.post('/send_political', function(request, response){
	var political=request.body.search
	socket.emit('search politician', political)
	socket.on('my response', function(msg) {
		context={}
    	context['nombre']=msg
    	console.log(msg)
    	MongoClient.connect(url, function(err, db) {
			assert.equal(null, err);
			console.log("Connected correctly to server");		 
			insertDocuments(db, msg, function() {
		    db.close();
	  	});


	});
	       response.render('index.html',context)
    });


});


app.get("/autocomplete/politicos", function (request,response) {
	//console.log(request.query.query)

	var nombre=request.query.query

	var arreglo=[]

	MongoClient.connect(url, function(err, db) {
		assert.equal(null, err);
		console.log("Connected correctly to MongoDB Server");
	 
		findPoliticosAutocomplete(db, nombre, function(result) {

			console.log(result)

			for(var i=0;i<result.length;i++){

				console.log(result[i].Nombre)
				console.log(String(result[i]._id))
				obj={}

				obj['data']=String(result[i]._id)
				obj['value']=result[i].Nombre
				arreglo.push(obj)

			}
			console.log(arreglo)
			var countries=
			{
			    // Query is not required as of version 1.2.5
			    "query": request.query.query,
			    "suggestions": arreglo
			}			
			response.end(JSON.stringify(countries))

		})


	    db.close();
	});


	
	
})





