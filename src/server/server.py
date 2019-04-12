from flask import Flask,jsonify,request
from flask_cors import CORS
from service import Service
app = Flask(__name__)

CORS(app)

@app.route('/api/tasks')
def hello_world():
    return 'Hello, World'

@app.route('/',methods=['POST'])
def getQuery():
    data = request.json

    query = data['query']
    mode = data['mode']
    service = Service(mode)
    list = service.bool_model.process_query(str(query))
    print(list)
    return str(list)

if __name__ == '__main__':
    app.run(threaded=True)

