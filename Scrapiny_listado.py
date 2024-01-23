import requests
from bs4 import BeautifulSoup
from lxml import etree
import math

def listado_Productos(data_Body):
    lista_Titulos = []
    lista_Urls = []
    lista_Precios = []
    url_Request = "https://tienda.mercadolibre.com.ve/"+data_Body["vendedor"]
    print(url_Request)

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
        
        print(pagina_Actual,total_Paginacion )

        if pagina_Actual == total_Paginacion:
            break
        
        #Encontrar la Url para paginar
        url_Request = dom.xpath("//div[@class='ui-search-pagination']/nav/ul/li[contains(@class,'--next')]/a")[0].get('href')

    return lista_Titulos, lista_Urls, lista_Precios