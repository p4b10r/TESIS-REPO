from flask import Flask
from flaskext.mysql import MySQL
from app import app
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']="password"
app.config['MYSQL_DB']='registro_mantenimiento'
mysql=MySQL(app)
