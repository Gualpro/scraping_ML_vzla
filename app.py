from flask import Flask, jsonify, request, render_template
from Scrapiny_listado import listado_Productos
import json

app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    titulo = "Scraping Mercadolire Venezuela"
    return render_template('index.html', titulo=titulo)


@app.route("/mercadolibre", methods=['GET', 'POST'])
    
def mercadoLibre():
    #Recibe la data del Formulario HTML
    html_Producto = request.form["Producto"]
    html_Envio = request.form["Envio"]
    html_Limite = request.form["Limite"]
    html_Limitador = request.form["Limitador"]
    
    #Llama a la funcion para obtener el listado de productos
    titulos, urls, precios = listado_Productos(html_Producto, html_Envio, html_Limitador, html_Limite)

    #Retorna un Json
    return jsonify({'data':{'Titulo':titulos, 'Url':urls, 'Precio':precios}})


if (__name__)=='__main__':
    app.run(host="0.0.0.0", debug=True)