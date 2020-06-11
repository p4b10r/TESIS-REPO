from flask import jsonify, request
import requests
import json

api_token='7AFEEA24F9F2465D8F6F58E2E4CF7898'
api_url_base='http://octopi.local/'
form_data='UTF-8'

headers={'Content-Type': 'application/json','X-Api-Key': api_token, 'form-data': form_data}

def DataBed():
    api_url_bed='{}{}'.format(api_url_base, '/api/printer/bed?history=true&limit=2')
    dr_b={'status':'history'}

    dbed=requests.get(url=api_url_bed, headers=headers, json=dr_b)
    data_bed=json.loads(dbed.content)

    return data_bed

def DataTool():
    api_url_tool='{}{}'.format(api_url_base, 'api/printer/tool?history=true&limit=2')
    dr_t={'status':'history'}

    dtool=requests.get(url=api_url_tool, headers=headers, json=dr_t)
    data_tool=json.loads(dtool.content)

    return data_tool

def DataConnection():
    api_url_conn='{}{}'.format(api_url_base, 'api/connection')
    dr_conn={'status':'current'}

    dconn=requests.get(url=api_url_conn, headers=headers, data=dr_conn)
    data_conn=json.loads(dconn.content)

    return data_conn

def DataJob():
    api_url_job='{}{}'.format(api_url_base, 'api/job')
    dr_job={'status':'job'}

    djob=requests.get(url=api_url_job, headers=headers, data=dr_job)
    data_job=json.loads(djob.content)

    return data_job

def DataState():
    api_url_state='{}{}'.format(api_url_base, 'api/job')
    dr_state={'status':'state'}

    dstate=requests.get(url=api_url_state, headers=headers, data=dr_state)
    data_state=json.loads(dstate.content)

    return data_state
