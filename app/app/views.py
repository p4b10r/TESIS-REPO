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
api_token = 'FB44A2D826704E18910B445C30520F6B'
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
    data_bt=json.dumps({'status':'history'})
    data_conn=json.dumps({'status':'current'})
    data_job=json.dumps({'status':'job'})
    data_progress=json.dumps({'status':'progress'})
    data_state=json.dumps({'status':'state'})
    #Método GET request para data de bed y tool, con los parámetros de URL, headers y json de consulta
    r_bed=requests.get(url=api_url_bed, headers=PARAMS, json=data_bt).json()
    r_tool=requests.get(url=api_url_tool, headers=PARAMS, json=data_bt).json()
    r_conn=requests.get(url=api_url_connection, headers=PARAMS, json=data_conn).json()
    r_job=requests.get(url=api_url_job, headers=PARAMS, json=data_job).json()
    r_progress=requests.get(url=api_url_job, headers=PARAMS, json=data_progress).json()
    r_state=requests.get(url=api_url_job, headers=PARAMS, json=data_state).json()
    #json data de bed y tool
    bed_data=json.dumps(r_bed)
    tool_data=json.dumps(r_tool)
    conn_data=json.dumps(r_conn)
    job_data=json.dumps(r_job)
    progress_data=json.dumps(r_progress)
    state_data=json.dumps(form_data)

    return render_template('interfaz.html', bed_data=bed_data, tool_data=tool_data, conn_data=conn_data, job_data=job_data, progress_data=progress_data, state_data=state_data)

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
