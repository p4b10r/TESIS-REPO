from flask import Flask, jsonify, request
from flask_restful import Api



app=Flask(__name__)
api=Api(app)



#from impresoras import impresoras

#@app.route('/ping')
#def ping():
#    return jsonify({"mensaje":"Pong"})

#@app.route('/impresoras', methods=['GET'])
#def getImpresoras():
#    return jsonify(impresoras)



if __name__=='__main__':
    app.run(debug=True, port=4000)
