from flask import jsonify, request, redirect, url_for, flash
import json
from app import app
import urllib3
from time import sleep
from flask import render_template
import time
from flask_mysqldb import MySQL

from app import data

#Configuracion conexion MYSQL
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']="password"
app.config['MYSQL_DB']='produccion'
mysql=MySQL(app)

#configuración sesion del servidor
app.secret_key='mysecretkey'

@app.route('/estadoactual',methods=['GET','POST'])
def EstadoActual():

    bed_data=data.DataBed()["bed"]["actual"]
    tool_data=data.DataTool()["tool0"]["actual"]
    conn_data=data.DataConnection()["current"]
    job_data=data.DataJob()["job"]
    state_data=data.DataState()["state"]

    return render_template('interfaz.html', bed_data=bed_data, tool_data=tool_data, conn_data=conn_data, job_data=job_data, state_data=state_data)

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
