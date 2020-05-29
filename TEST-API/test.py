from flask import Flask, jsonify, request
from flask_restful import Api
import requests
import json

app=Flask(__name__)

api_token = 'FB44A2D826704E18910B445C30520F6B'
api_url_base = 'http://192.168.1.95:5000/'

api_url = '{}{}'.format(api_url_base, '/api/connection')

headers = {
         'Content-Type': 'application/json',
         'X-Api-Key': api_token # the name may vary.  I got it from this doc: http://docs.octoprint.org/en/master/api/job.html
          }
data1={'status': 'port','status': 'baudrate'}



data = {
         'command': 'pause', # notice i also removed the " inside the strings
         'action': 'pause'

          }


print(api_url)
#response = requests.get(api_url, headers=headers, json=data)
response2=request.get(api_url, headers= headers, json=data1)

print(response2.json())


if __name__=='__main__':
    app.run(debug=True, port=4000)
