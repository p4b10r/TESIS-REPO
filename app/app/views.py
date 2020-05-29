from flask import Flask, jsonify#, request
import requests
import json
#from app import app
import urllib3
from time import sleep



app=Flask(__name__)


@app.route('/')


def Index():

    return 'este es el index'


@app.route('/centro')

def CentroImpresion():



    api_token = 'FB44A2D826704E18910B445C30520F6B'
    api_url_base = 'http://192.168.1.95:5000/'

    api_url = '{}{}'.format(api_url_base, 'api/connection')

    PARAMS = {'Content-Type': 'application/json','X-Api-Key': api_token} # the name may vary.  I got it from this doc: http://docs.octoprint.org/en/master/api/job.html


    data={'status':'current'}

    response=requests.get(api_url, headers=PARAMS, json=data)
    sleep(1)#


    return json(response)

@app.route('/mtto')
def CentroMtto():
    return 'este es el centro de Mtto'

@app.route('/produccion')
def CentroProd():
    return 'este es el centro de produccion'


if __name__=='__main__':

    app.run(host='192.168.1.95',port=4000, debug=True)
