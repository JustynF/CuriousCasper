from flask import Flask,jsonify,request,url_for, json,Response
from flask_cors import CORS
from src import *
from src.server.service import Service
from os.path import dirname

app = Flask(__name__)

CORS(app)

service = Service()

with open(dirname(dirname(__file__))+"/output/topics.json") as outfile:
    topics = json.load(outfile)


@app.route('/api/tasks')
def hello_world():
    return 'Hello, World'

@app.route('/',methods=['POST'])
def getQuery():
    data = request.json
    if request.headers['Content-Type'] == 'application/json':
        print (json.dumps(data))
    search_type = data["search"]
    query = data["query"]
    mode = data["mode"]
    corpus = data["corpus"]
    topics = data["topic"]

    if data["search"] == "bool":
         doc_ids = service.perfom_boolean_query(query,mode,corpus)
         topic_list = []
         for key, value in topics.iteritems():
             if value:
                 topic_list.append(key)

         returned_docs = service.corpus_access(doc_ids,corpus,topic_list)

    elif data["search"] == "vsm":
        doc_ids = service.perfom_vsm_query(query,mode,corpus)
        topic_list = []
        for key, value in topics.iteritems():
            if value:
                topic_list.append(key)
        only_ids = []
        docs_score = {}
        for pair in doc_ids:
            docs_score[pair[0]] = pair[1]


        retreived_docs = service.corpus_access(docs_score.keys(),corpus, topic_list)

        returned_docs = []

        for doc in retreived_docs:
            doc["score"] = docs_score[doc["docId"]]
            returned_docs.append(doc)




    elif data["search"] == "bm25":
        doc_ids = service.perfom_bm25_query(query,mode,corpus)
        topic_list = []
        for key, value in topics.iteritems():
            if value:
                topic_list.append(key)

        retreived_docs = service.corpus_access(doc_ids.keys(),corpus, topic_list)

        returned_docs = []
        for doc in retreived_docs:
            doc_id = str(doc["docId"]).decode("utf-8") if corpus == "uo" else doc["docId"]
            doc["score"] = doc_ids[doc_id]
            returned_docs.append(doc)




    print (returned_docs)
    resp = jsonify(returned_docs)
    resp.status_code = 200
    resp.headers['Link'] = "http://localhost:3000/"
    return resp

@app.route('/autocomplete',methods = ["POST"])
def api_root():
    data = request.json
    if request.headers['Content-Type'] == 'application/json':
        print (json.dumps(data))
    autocomplete = data["autocomplete"]

    res_data = service.autocomplete(autocomplete)
    print res_data
    resp = jsonify(res_data)
    resp.status_code = 200
    resp.headers['Link'] = "http://localhost:3000/"
    return resp

@app.route('/doc',methods = ["POST"])
def api_doc():
    data = request.json
    if request.headers['Content-Type'] == 'application/json':
        print (json.dumps(data))
    doc = data["selected_doc"]
    query = data["query"]
    corpus = data["corpus"]

    res_data = service.get_doc(doc, corpus)

    service.add_relevant_doc(doc,query,corpus)

    resp = jsonify(res_data)
    resp.status_code = 200
    resp.headers['Link'] = "http://localhost:3000/"
    return resp






@app.route('/hello')
def api_hello():
    if 'name' in request.args:
        return 'Hello ' + request.args['name']
    else:
        return 'Hello John Doe'


@app.route('/json', methods = ['GET'])
def api_json():
    print(topics)
    resp = jsonify(topics)
    resp.status_code = 200
    resp.headers['Link'] = 'http://localhost:3000/'

    return resp

if __name__ == '__main__':
    app.run(threaded=True)
# @app.route('/articles/<int:articleid>')
# @app.route('/articles/<float:articleid>')
# @app.route('/articles/<path:articleid>')
