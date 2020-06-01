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



api_token = 'FB44A2D826704E18910B445C30520F6B'
api_url_base = 'http://octopi.local/'
form_data='UTF-8'

@app.route('/')

def Index():
    return 'este es el index'


@app.route('/interfaz',methods=['GET','POST'])
def CentroImpresion():
    while True:

        time.sleep(2)
        api_url_bed = '{}{}'.format(api_url_base, 'api/printer/bed?history=true&limit=2')
    #api_url_tool = '{}{}'.format(api_url_base, 'api/printer/tool?history=true&limit=2')

        PARAMS = {'Content-Type': 'application/json','X-Api-Key': api_token, 'form-data': form_data}
        data={'status':'history'}

    r_bed=requests.get(url=api_url_bed, headers=PARAMS, json=data)
    #r_tool=requests.get(url=api_url_tool, headers=PARAMS, json=data)


    return r_bed.json()

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
