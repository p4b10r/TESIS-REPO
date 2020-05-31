from flask import jsonify, request
import requests
import json
from app import app
import urllib3
from time import sleep
from flask import render_template



#app=Flask(__name__)
#app.config['DEBUG'] = True

api_token = 'FB44A2D826704E18910B445C30520F6B'
api_url_base = 'http://octopi.local/'
form_data='UTF-8'

@app.route('/')

def Index():
    return render_template("index.html")


@app.route('/interfaz',methods=['GET','POST'])
def CentroImpresion():

    api_url_bed = '{}{}'.format(api_url_base, 'api/printer/bed?history=true&limit=2')
    #api_url_tool = '{}{}'.format(api_url_base, 'api/printer/tool?history=true&limit=2')

    PARAMS = {'Content-Type': 'application/json','X-Api-Key': api_token, 'form-data': form_data}
    data={'status':'history'}

    r_bed=requests.get(url=api_url_bed, headers=PARAMS, json=data)
    #r_tool=requests.get(url=api_url_tool, headers=PARAMS, json=data)


    return render_template("interfaz.html")


@app.route('/mtto')
def CentroMtto():
    return 'este es el centro de Mtto'

@app.route('/produccion')
def CentroProd():
    return 'este es el centro de produccion'


#if __name__=='__main__':

#    app.run(host='127.0.0.1',port=4000, debug=True)
