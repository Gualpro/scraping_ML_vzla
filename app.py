from flask import Flask, jsonify, request, render_template
from Scrapiny_listado import listado_Productos
import json

app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    titulo = "Scraping Mercadolire Venezuela"
    return render_template('index.html', titulo=titulo)


@app.route("/mercadolibre", methods=['GET'])
    
def mercadoLibre():
    #Recibe la data del Body

    data_Body = json.loads(request.data)
    print(data_Body)
    #Llama a la funcion para obtener el listado de productos
    titulos, urls, precios = listado_Productos(data_Body)
    return jsonify({'data':{'Titulo':titulos, 'Url':urls, 'Precio':precios}} )

if (__name__)=='__main__':
    app.run(host="0.0.0.0", debug=True)