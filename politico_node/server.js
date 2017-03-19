

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




