import requests
from bs4 import BeautifulSoup
from lxml import etree
import math

def listado_Productos(data_Body):
    #Declaracion de las lista donde de guardara la informacion obtenida
    lista_Titulos = []
    lista_Urls = []
    lista_Precios = []

    #Validacion y transformacion de la informacion enviada desde el formulario
    palabra_Clave = data_Body["palabra_Clave"].lower().replace(" ","-")
    limitador_Producto = int(data_Body["limitador_Producto"])
    cantidad_Productos_Mostrados = int(data_Body["cantidad_Productos_Mostrados"])
    condicion_Envio = int(data_Body["condicion_Envio"])

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
            pagina_Actual = soup.find("span", attrs={"class":"andes-pagination__link"}).text
            pagina_Actual = int(pagina_Actual)

            #Total de la paginacion
            total_Paginacion = soup.find("li", attrs={"class":"andes-pagination__page-count"})
            total_Paginacion = int(total_Paginacion.text.split(' ')[1])
    
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
        url_Request = dom.xpath("//div[@class='ui-search-pagination']/nav/ul/li[contains(@class,'--next')]/a")[0].get('href')
    
    return lista_Titulos, lista_Urls, lista_Precios