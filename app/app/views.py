from flask import jsonify, request, redirect, url_for, flash
import requests
import json
from app import app
import urllib3
from time import sleep
from flask import render_template
import time
from flask_mysqldb import MySQL

#Configuracion conexion MYSQL
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']="password"
app.config['MYSQL_DB']='produccion'
mysql=MySQL(app)

#configuración sesion del servidor
app.secret_key='mysecretkey'

#Headers para solicitud API
api_token = '7AFEEA24F9F2465D8F6F58E2E4CF7898'
api_url_base = 'http://octopi.local/'
form_data='UTF-8'

@app.route('/')
def Index():
    return 'este es el index'

#Ruta que muestra el estado actual de la impresora, y los métodos usados
@app.route('/estadoactual',methods=['GET','POST'])
def EstadoActual(): #se define la función estado actual que no recibe parámetros, y retorna la data de cama, herramienta y conexión con el método render_template en interfaz.html
    #se definen los arreglos api_url_bed y api_url_tool, api_url_connectionutilizando la url base de la impresora y los query asociados a cada dato.
    api_url_bed = '{}{}'.format(api_url_base, 'api/printer/bed?history=true&limit=2')
    api_url_tool = '{}{}'.format(api_url_base, 'api/printer/tool?history=true&limit=2')
    api_url_connection='{}{}'.format(api_url_base,'api/connection')
    api_url_job='{}{}'.format(api_url_base,'api/job')
    #se definen los parámetros header para el método GET
    PARAMS = {'Content-Type': 'application/json','X-Api-Key': api_token, 'form-data': form_data}

    #Data de bed y tool para solicitud GET
    data_bt={'status':'history'}
    data_conn=json.dumps({'status':'current'})
    #data_job=json.dumps({'status':'job'})
    #data_progress=json.dumps({'status':'progress'})
    #data_state=json.dumps({'status':'state'})
    #Método GET request para data de bed y tool, con los parámetros de URL, headers y json de consulta
    r_bed=requests.get(url=api_url_bed, headers=PARAMS, json=data_bt)
    r_tool=requests.get(url=api_url_tool, headers=PARAMS, json=data_bt)
    r_conn=requests.get(url=api_url_connection, headers=PARAMS, json=data_conn)
    #r_job=requests.get(url=api_url_job, headers=PARAMS, json=data_job).json()
    #r_progress=requests.get(url=api_url_job, headers=PARAMS, json=data_progress).json()
    #r_state=requests.get(url=api_url_job, headers=PARAMS, json=data_state).json()
    #json data de bed y tool

    r_bed=json.loads(r_bed.content)
    r_tool=json.loads(r_tool.content)
    r_conn=json.loads(r_conn.content)

    bed_data=str(r_bed["bed"]["actual"])
    tool_data=str(r_tool["tool0"]["actual"])
    conn_dataport=r_conn["current"]["port"]
    conn_datastate=r_conn["current"]["state"]


    return render_template('interfaz.html', bed_data=bed_data, tool_data=tool_data, conn_dataport=conn_dataport, conn_datastate=conn_datastate)
    #, job_data=job_data, progress_data=progress_data, state_data=state_data)

@app.route('/produccion')
def CentroProd():
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM produccion_en_proceso')
    data=cur.fetchall()
    return render_template('produccion.html',procesos=data)

@app.route('/agregar_op', methods=['POST'])
def Agregar_op():
    if request.method=='POST':
        OP=request.form['OP']
        Producto=request.form['Producto']
        Pieza=request.form['Pieza']
        cur=mysql.connection.cursor()
        cur.execute('INSERT INTO produccion_en_proceso (OP, Producto, Pieza) VALUES (%s, %s, %s)',(OP,Producto,Pieza))
        mysql.connection.commit()
        flash('Orden Agregada Satisfactoriamente')
    return redirect(url_for('CentroProd'))

@app.route('/terminar_op/<string:id>')
def Terminar_op(id):
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM produccion_en_proceso WHERE id={0}'.format(id))
    mysql.connection.commit()
    flash('Producción finalizada')
    return redirect(url_for('CentroProd'))



#if __name__=='__main__':

#    app.run(host='127.0.0.1',port=4000, debug=True)
