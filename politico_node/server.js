

/*var http = require('http');
var fs= require('fs');



http.createServer(function(rquest,response){


	var html=fs.readFile('./index.html',function(err,html){

		var nombre="Romario"
		response.write(html);
		response.end();
	})

}).listen(8080)*/





/*module.exports.parse=parse;
parser=require("./nombre_archivo.js")

var p=parser.parse

p(par);*/



var express=require('express')
var app=express();
var socket = require('socket.io-client')('http://localhost:5000');
var bodyParser = require('body-parser');
var MongoClient = require('mongodb').MongoClient
  , assert = require('assert');



var url = 'mongodb://localhost:27017/politicos';


app.use(bodyParser.json()); // support json encoded bodies
app.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies


//app.set('view engine', 'jade')
app.set('views', __dirname + '/views');
app.engine('html', require('ejs').renderFile);
app.use(express.static('static'));

//app.use(express.bodyParser());


var options = {
    	root: __dirname + '/static/'
	}





var insertDocuments = function(db, data,callback) {
  // Get the documents collection 
  var collection = db.collection('documents');
  // Insert some documents 
  collection.insertMany(
    [data]   , function(err, result) {
    assert.equal(err, null);
    /*assert.equal(3, result.result.n);
    assert.equal(3, result.ops.length);
    console.log("Inserted 3 documents into the document collection");*/
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



app.get('/', function(request, response){

	context={}

	context['nombre']=''

	
	//var socket = io.connect('http://localhost:5000/test', { 'forceNew': true });

	response.render('index.html',context);


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
		console.log("Connected correctly to server");
	 
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





