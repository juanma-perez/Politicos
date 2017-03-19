from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
from pySearcher import Searcher
from pyJSONManager import JSONManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

#@app.route('/')
#def index():
#    return render_template('index.html')

@socketio.on('search politician', namespace='/')
def test_message(message):
	#busqueda = "Donald trump"
	jsonFile = JSONManager(message)
	print jsonFile
	print message
	emit('my response', jsonFile.scrapeTable())

#@socketio.on('my broadcast event', namespace='/')
#def test_message(message):
#    emit('my response', {'data': message['data']}, broadcast=True)

#@socketio.on('connect', namespace='/')
#def test_connect():
#    emit('my response', {'data': 'Connected'})

#@socketio.on('disconnect', namespace='/')
#def test_disconnect():
#    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)