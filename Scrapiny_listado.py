import requests
from bs4 import BeautifulSoup
from lxml import etree
import math

def listado_Productos(html_Producto, html_Envio, html_Limitador, html_Limite):
    #Declaracion de las lista donde de guardara la informacion obtenida
    lista_Titulos = []
    lista_Urls = []
    lista_Precios = []

    #Validacion y transformacion de la informacion enviada desde el formulario
    palabra_Clave = html_Producto.lower().replace(" ","-")
    condicion_Envio = int(html_Envio)
    limitador_Producto = int(html_Limitador)
    cantidad_Productos_Mostrados = int(html_Limite)

    #Construccion de la URL para hacer el request 
    if condicion_Envio == 1:
        #Solo producto con envio Gratis
        url_Request = ("https://listado.mercadolibre.com.ve/" + palabra_Clave + "_CostoEnvio_Gratis_NoIndex_True")
    else:
        #Todo los producto
        url_Request = ("https://listado.mercadolibre.com.ve/" + palabra_Clave)

    print(f"URL Visitada: {url_Request}")
    while True:
        #realiza el primer request de la url semilla
        re = requests.get(url_Request)

        #Evalua si la url es valida
        if re.status_code == 200:
            soup = BeautifulSoup(re.content, 'html.parser')
            dom = etree.HTML(str(soup))
        
            #Obtiene los Titulos
            titulos = soup.find_all("h2", attrs={"class":"ui-search-item__title"})
            titulos = [i.text for i in titulos]
            lista_Titulos.extend(titulos)

            #Obtiene las Urls
            urls = soup.find_all("a", attrs={"class":"ui-search-item__group__element ui-search-link__title-card ui-search-link"})
            urls = [i.get("href") for i in urls]
            lista_Urls.extend(urls)

            #Obtiene Precio de los Productos
            precio_todos_productos = dom.xpath('//span[@class="andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript"]')
            precios = []
            n = 0
            d = 0 
            for i in precio_todos_productos:
                if len(i)==4:
                    precios_entero = dom.xpath('//span[@class="andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript"]/span[2]')
                    precios_decimal = dom.xpath('//span[@class="andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript"]/span[4]')
                    precios.append(precios_entero[n].text + "." + precios_decimal[d].text)
                    d = d + 1
                else:
                    precios_entero = dom.xpath('//span[@class="andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript"]/span[2]')
                    precios.append(precios_entero[n].text)
                n = n + 1
            lista_Precios.extend(precios)

            #Pagina actual
            
            pagina_Actual = dom.xpath("//li[@class='andes-pagination__button andes-pagination__button--current']/button")[0].text
            pagina_Actual = int(pagina_Actual)

            #Total de la paginacion
            total_Paginacion = soup.find("span", attrs={"class":"ui-search-search-result__quantity-results"})
            total_Paginacion = int(total_Paginacion.text.split(' ')[0].replace(".",""))
            if total_Paginacion <= 450:
                total_Paginacion = math.ceil(total_Paginacion/50)
            else:
                total_Paginacion = 9

        else:
            break
        
        #Limitador de cantidad de Producto a buscar y mostrar
        if limitador_Producto == 0:
            #Busqueda sin limitador de cantidad de productos 
            print(f"Pagina {pagina_Actual} de {total_Paginacion}")
            if pagina_Actual == total_Paginacion:
                break
        else:
            #Limitado activado muestra solo la cantidad de productos elegida por el usuario

            #Se valida la cantidad de pagina a visitar
            numero_paginas = math.ceil(cantidad_Productos_Mostrados/50)
            #Se valida si la cantidad de paginas a visita esta donde del rango obtenido
            if numero_paginas >= total_Paginacion:
                print(f"Pagina {pagina_Actual} de {total_Paginacion}")
                if pagina_Actual == total_Paginacion:
                    #Se Valida  la cantidad de producto a retornar
                    if len(lista_Titulos) >= cantidad_Productos_Mostrados:
                        return lista_Titulos[0:cantidad_Productos_Mostrados], lista_Urls[0:cantidad_Productos_Mostrados], lista_Precios[0:cantidad_Productos_Mostrados]
                    else:
                        return lista_Titulos, lista_Urls, lista_Precios
            
            else:
                #Retorna los productos dentro del rango del productos encontrado menos 1
                print(f"Pagina {pagina_Actual} de {numero_paginas}")
                if pagina_Actual == numero_paginas:
                        return lista_Titulos[0:cantidad_Productos_Mostrados], lista_Urls[0:cantidad_Productos_Mostrados], lista_Precios[0:cantidad_Productos_Mostrados]

        #Encontrar la Url para paginar
        url_Request = dom.xpath("//li[@class='andes-pagination__button andes-pagination__button--next']/a")[0].get('href')
    
    return lista_Titulos, lista_Urls, lista_Precios