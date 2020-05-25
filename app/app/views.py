from app import app

@app.route('/')
def Index():
    return 'Index'

@app.route('/centro')
def CentroImpresion():
    return 'este es el centro de impresion'

@app.route('/mtto')
def CentroMtto():
    return 'este es el centro de Mtto'

@app.route('/produccion')
def CentroProd():
    return 'este es el centro de produccion'
