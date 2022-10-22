# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 19:57:02 2022

@author: jdelfres
"""

import requests
import json
from datetime import datetime

#DEFINICION DE VARIABLES DE CONFIGURACIÓN
PATH_BASE ="./pruebas"
#PATH_BASE ="./data"
PATH_EXTENDIDO = PATH_BASE + "/detailed"


###############################################
### FUNCIONES DE EXTRACCIÓN DE DATOS (JSON) ###
###############################################

#####################################################################################################
## Función de extracción JSON de páginas web de forma general para British Horse Racing Authority ###
## Argumentos:
##      direccion: dirección del web de donde se extraen los datos
##      nombre: nombre del fichero a generar    
##      limitePaginas: máximo de páginas a descargar si es que hay paginación 
##      porPagina: máximo de páginas de resultados. Si se fija a 0 no se usa en la petición
##      rated: Filtrado extra para caballos que han sido puntuados.
##      extras: Modificadores de petición, como filtros o orden de salida.
##
#####################################################################################################

def extraeWeb(direccion, nombre, limitePaginas = 10000, porPagina = 0, rated = False, extras = ""):
    
    
    maximo = 0
    contenido = {}
    per_page = ""
    
    if porPagina != 0:
        per_page = "?per_page=" + str(porPagina)
        
    if (porPagina == 0) and (extras != ""):
        extras = '?' + extras
    
    if (porPagina != 0) and (extras != ""):
        extras = '&' + extras

    #primera pasada cogiendo los datos de cabecera
    url = direccion + per_page + extras

    print(url)
    
    if rated == True:
        url = url + '&rated=true'
    payload={}
    headers = {
      'Cookie': 'incap_ses_1485_2476407=8sO0e1FR7Uuo8I1u18ebFBh61WIAAAAANI0+Z6FZ597Fin/LQtIiNw==; visid_incap_2476407=0PkrmaWeTVaiWkiWfalg1Dt8xGIAAAAAQUIPAAAAAACvrjs1/Yo4ajgxNvjwMFbv'
    }
    
    response = requests.request("GET", url, headers=headers, data=payload)
    contenido = json.loads(response.text)
    
    #recogemos el número total de páginas siempre que haya
    if porPagina != 0:
        maximo = contenido["last_page"] + 1 if contenido["last_page"] < limitePaginas else limitePaginas
    

    #aprovechamos para guardar el contenido en el primer fichero
    with open(PATH_BASE + '/' + nombre + "1" + '.json', 'w') as f:
        f.write(response.text)
        f.close()
    
    #a partir de la segunda página, guardamos los datos en bucle hasta el número total de páginas
    if maximo != 0:    
        for contador in range(2,maximo):
            url = direccion + "?page=" + str(contador) + per_page + extras
            if rated == True:
                url = url + '&rated=true'
            
            payload={}
            headers = {
              'Cookie': 'incap_ses_1485_2476407=8sO0e1FR7Uuo8I1u18ebFBh61WIAAAAANI0+Z6FZ597Fin/LQtIiNw==; visid_incap_2476407=0PkrmaWeTVaiWkiWfalg1Dt8xGIAAAAAQUIPAAAAAACvrjs1/Yo4ajgxNvjwMFbv'
            }
            
            response = requests.request("GET", url, headers=headers, data=payload)
            
            with open(PATH_BASE + '/' + nombre + str(contador) + '.json', 'w') as f:
                f.write(response.text)
                f.close()
                
    #eliminar tras las pruebas
    return json.loads(response.text)


#####################################################################################################
## Función específica de extracción JSON detalles de caballos                                     ###
## Argumentos:
##      idCaballo: identificador del caballo para extraer sus detalles        
##      direccion: dirección del web de donde se extraen los datos
##
#####################################################################################################

def extraeDetalleCaballo(idCaballo, direccion):
        url = direccion + '/' + str(idCaballo)
        payloads={}
        headers = {
            'Cookie': 'incap_ses_1485_2476407=8sO0e1FR7Uuo8I1u18ebFBh61WIAAAAANI0+Z6FZ597Fin/LQtIiNw==; visid_incap_2476407=0PkrmaWeTVaiWkiWfalg1Dt8xGIAAAAAQUIPAAAAAACvrjs1/Yo4ajgxNvjwMFbv'
        }
        
        response = requests.request("GET", url, headers=headers, data=payloads)
        salida = json.loads(response.text)
        return salida["data"]

#####################################################################################################
## Función específica de extracción JSON histórico de entrenamiento de caballos                   ###
## Argumentos:
##      idCaballo: identificador del caballo para extraer su histórico        
##      direccion: dirección del web de donde se extraen los datos
##
#####################################################################################################
    
def extraeTrainingHistoryCaballo(idCaballo, direccion):
        url = direccion + '/' + str(idCaballo) + '/training-history'
        payloads={}
        headers = {
            'Cookie': 'incap_ses_1485_2476407=8sO0e1FR7Uuo8I1u18ebFBh61WIAAAAANI0+Z6FZ597Fin/LQtIiNw==; visid_incap_2476407=0PkrmaWeTVaiWkiWfalg1Dt8xGIAAAAAQUIPAAAAAACvrjs1/Yo4ajgxNvjwMFbv'
        }
        
        response = requests.request("GET", url, headers=headers, data=payloads)
        salida = json.loads(response.text)
        return salida["data"]

#####################################################################################################
## Función específica de extracción JSON rendimiento(performance) de caballos                     ###
## Argumentos:
##      idCaballo: identificador del caballo para extraer su rendimiento        
##      direccion: dirección del web de donde se extraen los datos
##
#####################################################################################################

def extraePerformanceCaballo(idCaballo, direccion):
        performance = []
        last_page = 0
        
        url = direccion + '/' + str(idCaballo) + '/performances'
        payloads={}
        headers = {
            'Cookie': 'incap_ses_1485_2476407=8sO0e1FR7Uuo8I1u18ebFBh61WIAAAAANI0+Z6FZ597Fin/LQtIiNw==; visid_incap_2476407=0PkrmaWeTVaiWkiWfalg1Dt8xGIAAAAAQUIPAAAAAACvrjs1/Yo4ajgxNvjwMFbv'
        }
        
        #primera pasada cogiendo los datos de cabecera
        response = requests.request("GET", url, headers=headers, data=payloads)
        contenido = json.loads(response.text)
        
        #comprobamos el número de registros total
        last_page = contenido["last_page"]
        if contenido["data"] != []:
            performance.append(contenido["data"].copy()) 
        
        #Si hay varias páginas las recorremos todas añadiendo al array los registros de cada página
        if last_page != 1:
            for contador in (2, last_page):
                url2 = url + '?page=' + str(contador)
                response = requests.request("GET", url2, headers=headers, data=payloads)
                contenido = json.loads(response.text)
                performance.append(contenido["data"].copy())
        
        return performance

#######################################################################################################################
## Función específica de extracción JSON detalles de caballos                                                       ###
## Argumentos:  
##      direccion: dirección del web de donde se extraen los datos
##      JsonCaballos: Json de caballos original que se completa con los detalles, histórico y performance 
##      nombreFicheroDetalle: nombre y ruta del fichero de detalle
##      perJson: número de registros por fichero Json
##
#######################################################################################################################

def completaJsonCaballosRated(direccion, JsonCaballos, nombreFicheroDetalle, perJson = 1000):
    listaExtendida = []
    caballoTemp = {}
    contador = 0
    resultadoTemp = {}
    totalPaginas = JsonCaballos["total"] // perJson + 1
    
    print("Tratando el fichero ", nombreFicheroDetalle)
    
    for caballo in JsonCaballos["data"]:
        contador+= 1

        #Sacamos los detalles principales del caballo
        caballoTemp = extraeDetalleCaballo(caballo["id"], direccion)
        
        listaExtendida.append(caballoTemp.copy())
        
        if (contador % perJson == 0):
            resultadoTemp["total"] = JsonCaballos["total"]
            resultadoTemp["per_page"] = perJson
            resultadoTemp["current_page"] = contador // perJson
            resultadoTemp["last_page"] = totalPaginas
            resultadoTemp["from"] = contador - perJson + 1
            resultadoTemp["to"] = contador
            resultadoTemp["data"] = listaExtendida
            
            with open(nombreFicheroDetalle + str(contador // perJson) + ".json", 'w') as f:
               f.write(json.dumps(resultadoTemp))
               f.close()
               
            listaExtendida = []
            resultadoTemp = {}
            print(contador)
            
    if (contador % perJson != 0):
        resultadoTemp["total"] = JsonCaballos["total"]
        resultadoTemp["per_page"] = perJson
        resultadoTemp["current_page"] = contador // perJson
        resultadoTemp["last_page"] = totalPaginas
        resultadoTemp["from"] = contador - perJson + 1
        resultadoTemp["to"] = contador
        resultadoTemp["data"] = listaExtendida
        
        with open(nombreFicheroDetalle + str(contador // perJson) + 1 + ".json", 'w') as f:
           f.write(json.dumps(resultadoTemp))
           f.close()
    
        print(contador)
    
    return "Ficheros volcados en " + PATH_EXTENDIDO


#######################################################################################################################
## Función específica de extracción JSON detalles de caballos                                                       ###
## Argumentos:  
##      direccion: dirección del web de donde se extraen los datos
##      JsonCaballos: Json de caballos original que se completa con los detalles, histórico y performance 
##      nombreFicheroDetalle: nombre y ruta del fichero de detalle
##      perJson: número de registros por fichero Json
##
#######################################################################################################################

def completaJsonCaballosNonRated(direccion, JsonCaballos, nombreFicheroDetalle, perJson = 1000):
    listaExtendida = []
    caballoTemp = {}
    contador = 0
    resultadoTemp = {}
    totalPaginas = JsonCaballos["total"] // perJson + 1
    
    print("Tratando el fichero ", nombreFicheroDetalle)
    
    for caballo in JsonCaballos["data"]:
        contador+= 1

        #Sacamos los detalles principales del caballo
        caballoTemp = extraeDetalleCaballo(caballo["id"], direccion)
        
        #Para aquellos que identificamos el entrenador, sacamos el historial de entrenamientos
        if caballoTemp["trainerId"] is not None:
            caballoTemp["trainingHistory"] = extraeTrainingHistoryCaballo(caballo["id"], direccion) 
        
        performance = extraePerformanceCaballo(caballo["id"], direccion)
        if performance != []:
            caballoTemp["performance"] = performance 
        
        listaExtendida.append(caballoTemp.copy())
        
        if (contador % perJson == 0):
            resultadoTemp["total"] = JsonCaballos["total"]
            resultadoTemp["per_page"] = perJson
            resultadoTemp["current_page"] = contador // perJson
            resultadoTemp["last_page"] = totalPaginas
            resultadoTemp["from"] = contador - perJson + 1
            resultadoTemp["to"] = contador
            resultadoTemp["data"] = listaExtendida
            
            with open(nombreFicheroDetalle + str(contador // perJson) + ".json", 'w') as f:
               f.write(json.dumps(resultadoTemp))
               f.close()
               
            listaExtendida = []
            resultadoTemp = {}
            print(contador)
            
    if (contador % perJson != 0):
        resultadoTemp["total"] = JsonCaballos["total"]
        resultadoTemp["per_page"] = perJson
        resultadoTemp["current_page"] = contador // perJson
        resultadoTemp["last_page"] = totalPaginas
        resultadoTemp["from"] = contador - perJson + 1
        resultadoTemp["to"] = contador
        resultadoTemp["data"] = listaExtendida
        
        with open(nombreFicheroDetalle + str(contador // perJson) + 1 + ".json", 'w') as f:
           f.write(json.dumps(resultadoTemp))
           f.close()
    
        print(contador)
    
    return "Ficheros volcados en " + PATH_EXTENDIDO

#####################################################################################################
## Función específica de extracción JSON detalles de Fixture                                      ###
## Argumentos:
##      idFixture: identificador del fixture para extraer sus detalles        
##      year: año de la carrera        
##      direccion: dirección del web de donde se extraen los datos
##
#####################################################################################################

def extraeDetalleFixture(idFixture, year, direccion):

        payloads={}
        headers = {
            'Cookie': 'incap_ses_1485_2476407=8sO0e1FR7Uuo8I1u18ebFBh61WIAAAAANI0+Z6FZ597Fin/LQtIiNw==; visid_incap_2476407=0PkrmaWeTVaiWkiWfalg1Dt8xGIAAAAAQUIPAAAAAACvrjs1/Yo4ajgxNvjwMFbv'
        }
        
        urlFixture = direccion + '/' + str(year) + '/' + str(idFixture)
        urlRaces = direccion + '/' + str(year) + '/' + str(idFixture) + '/races'
        urlGoing = direccion + '/' + str(year) + '/' + str(idFixture) + '/going'

        response = requests.request("GET", urlFixture, headers=headers, data=payloads)
        salida = json.loads(response.text)
        
        response = requests.request("GET", urlRaces, headers=headers, data=payloads)
        salida["data"][0]["races"] = json.loads(response.text)["data"]
        
        response = requests.request("GET", urlGoing, headers=headers, data=payloads)
        salida["data"][0]["going"] = json.loads(response.text)["data"]
        
        return salida["data"][0]
    
#####################################################################################################
## Función específica de extracción JSON detalles de Fixture                                      ###
## Argumentos:
##      idFixture: identificador del fixture para extraer sus detalles        
##      year: año de la carrera        
##      direccion: dirección del web de donde se extraen los datos
##
#####################################################################################################

def completaJsonFixture(direccion, jsonFixtures, jsonPlanning, nombreFicheroDetalle, perJson, inicio = 0):
    contadorResultado = inicio
    idPlanning = 0
    resultadoTemp = {}
    totalPaginas = jsonFixtures["total"] // perJson + 1 
    arrayFixtures = jsonFixtures["data"][inicio:]
    arrayFixturesTemp = []
    indiceUltimoFichero = 0
    
    print("Tratando el fichero ", nombreFicheroDetalle)
    #Combinamos la información de planificados y ya disputados para tener una lista completa de datos
    for fixture in arrayFixtures:
        while (len(jsonPlanning["data"]) > 0) and (idPlanning < len(jsonPlanning["data"])) and (fixture["fixtureId"] != jsonPlanning["data"][idPlanning]["fixtureId"]):
            idPlanning += 1
        
        #Al encontrarlo recogemos el json y lo añadimos
        contadorResultado += 1
        if (len(jsonPlanning["data"]) > idPlanning) and (fixture["fixtureId"] == jsonPlanning["data"][idPlanning]["fixtureId"]):
            planning = jsonPlanning["data"][idPlanning]
            fixture.update(planning)
            jsonPlanning["data"].remove(planning) #Eliminamos el planning una vez que se ha encontrado para que las búsquedas futuras se reduzcan
            fixtureDetails = extraeDetalleFixture(str(fixture["fixtureId"]), str(fixture["fixtureYear"]), direccion)
            fixture.update(fixtureDetails)
            
        #Volcamos la información al array de resultados temporales
        arrayFixturesTemp.append(fixture.copy())    
        
        #Si hemos llegado al límite por JSON, escribimos el fichero y reiniciamos el array de resultados
        if(contadorResultado % perJson == 0):
            now = datetime.now()
            print("Fixture #" + str(contadorResultado) +" Id: " + str(fixture["fixtureId"]) + " Timestamp: " + "{:02}".format(now.hour) + ":" + "{:02}".format(now.minute) + ":" + "{:02}".format(now.second))
                    
            indiceUltimoFichero = contadorResultado - perJson + 1
            resultadoTemp["total"] = jsonFixtures["total"]
            resultadoTemp["per_page"] = perJson
            resultadoTemp["current_page"] = contadorResultado // perJson
            resultadoTemp["last_page"] = totalPaginas
            resultadoTemp["from"] = contadorResultado - perJson + 1
            resultadoTemp["to"] = contadorResultado
            resultadoTemp["data"] = arrayFixturesTemp
            arrayFixturesTemp = []
                
            with open(nombreFicheroDetalle + str(contadorResultado // perJson) + ".json", 'w') as f:
                f.write(json.dumps(resultadoTemp))
                f.close()
                
        idPlanning = 0
                
    if(contadorResultado % perJson != 0): 
        now = datetime.now()
        print("Fixture #" + str(contadorResultado) +" Id: " + str(fixture["fixtureId"]) + " Timestamp: " + "{:02}".format(now.hour) + ":" + "{:02}".format(now.minute) + ":" + "{:02}".format(now.second))

        
        resultadoTemp["total"] = jsonFixtures["total"]
        resultadoTemp["per_page"] = perJson
        resultadoTemp["current_page"] = contadorResultado // perJson
        resultadoTemp["last_page"] = totalPaginas
        resultadoTemp["from"] = indiceUltimoFichero + 1
        resultadoTemp["to"] = contadorResultado
        resultadoTemp["data"] = arrayFixturesTemp
        
        with open(nombreFicheroDetalle + str((contadorResultado // perJson) + 1) + "_last.json", 'w') as f:
            f.write(json.dumps(resultadoTemp))
            f.close()
        
    #Por cada id que consultamos año/fixture /races /going                                       /officials no es necesario
    
    return "Ficheros volcados en " + PATH_EXTENDIDO

#####################################################################################################
## Función específica de extracción JSON detalles de Trainer                                      ###
## Argumentos:
##      jsonEntrenador: Variable JSON con los datos del entrenador a completar        
##      direccion: dirección del web de donde se extraen los datos
##
#####################################################################################################

def extraeDetalleTrainer(jsonEntrenador, direccion):
    respuestaTemp = {}
    payloads={}
    headers = {
        'Cookie': 'incap_ses_1485_2476407=8sO0e1FR7Uuo8I1u18ebFBh61WIAAAAANI0+Z6FZ597Fin/LQtIiNw==; visid_incap_2476407=0PkrmaWeTVaiWkiWfalg1Dt8xGIAAAAAQUIPAAAAAACvrjs1/Yo4ajgxNvjwMFbv'
    }
    
    urlDetail = direccion + '/' + str(jsonEntrenador["trainerId"]) 
    urlPerformances = urlDetail + '/performances'
    urlNonrunners = urlDetail + '/nonrunners'
    
    
    #Repasar y poner bucle para todas las páginas
    response = requests.request("GET", urlPerformances, headers=headers, data=payloads)
    respuestaTemp = json.loads(response.text)
    jsonEntrenador["performances"] = respuestaTemp["data"]    
    
    if (respuestaTemp["last_page"] != 1):
        for contador in range(2, respuestaTemp["last_page"] + 1):
            response = requests.request("GET", urlPerformances + '?page=' + str(contador), headers=headers, data=payloads)
            jsonEntrenador["performances"] += json.loads(response.text)["data"]
            print(contador) if contador > respuestaTemp["last_page"] - 10 else None
            
    response = requests.request("GET", urlNonrunners, headers=headers, data=payloads)
    jsonEntrenador["nonrunners"] = json.loads(response.text)["data"]
    
    return jsonEntrenador

#####################################################################################################
## Función específica para completar JSON de Trainers                                             ###
## Argumentos:
##      direccion: dirección del web de donde se extraen los datos
##      jsonTrainers: Diccionario JSON de entrenadores
##      nombreFicheroDetalle: nombre del fichero final de detalles de entrenadores
##      perJson: número de entrenadores por fichero JSON de detalle de entrenadores
##
#####################################################################################################

def completaJsonTrainers(direccion, jsonTrainers, nombreFicheroDetalle, perJson = 100):
    listaExtendida = []
    contador = 0
    resultadoTemp = {}
    totalPaginas = jsonTrainers["total"] // perJson + 1    
    trainerTemp = {}
    
    print("Tratando el fichero ", nombreFicheroDetalle)
    for trainer in jsonTrainers["data"]:
        contador+= 1
        now = datetime.now()
        print("Entrenador #" + str(contador) +" Id: " + str(trainer["trainerId"]) + " Timestamp: " + "{:02}".format(now.hour) + ":" + "{:02}".format(now.minute) + ":" + "{:02}".format(now.second))
        trainerTemp = trainer
        #Por cada iteración se añaden los datos de performance y nonrunners al Json
        detalles = extraeDetalleTrainer(trainer, direccion)
        trainerTemp["performances"] = detalles["performances"]
        trainerTemp["nonrunners"] = detalles["nonrunners"]
        listaExtendida.append(trainerTemp.copy())
    
        #Comprobamos si hemos llegado al límite de paginación y si es así completamos y volcamos a fichero
        if(contador % perJson == 0):
            resultadoTemp["total"] = jsonTrainers["total"]
            resultadoTemp["per_page"] = perJson
            resultadoTemp["current_page"] = contador // perJson
            resultadoTemp["last_page"] = totalPaginas
            resultadoTemp["from"] = contador - perJson + 1
            resultadoTemp["to"] = contador
            resultadoTemp["data"] = listaExtendida
    
            with open(nombreFicheroDetalle + str(contador // perJson) + ".json", 'w') as f:
                f.write(json.dumps(resultadoTemp))
                f.close()
   
            listaExtendida = []
            resultadoTemp = {}
    
    #Al llegar al final, si quedan datos por volcar completamos y volcamos a fichero    
    if (contador % perJson != 0):
        resultadoTemp["total"] = jsonTrainers["total"]
        resultadoTemp["per_page"] = perJson
        resultadoTemp["current_page"] = contador // perJson
        resultadoTemp["last_page"] = totalPaginas
        resultadoTemp["from"] = contador - perJson + 1
        resultadoTemp["to"] = contador
        resultadoTemp["data"] = listaExtendida
        
        with open(nombreFicheroDetalle + str(contador // perJson) + 1 + ".json", 'w') as f:
            f.write(json.dumps(resultadoTemp))
            f.close()
    
    return "Ficheros volcados en " + PATH_EXTENDIDO




#################################################
### FUNCIONES DE TRATAMIENTO DE FICHEROS JSON ###
#################################################

#######################################################################################################################
## Función específica de lectura de fichero JSON que añade detalles de caballos                                     ###
## Argumentos:  
##      nombre: nombre del fichero JSON de origen con los datos de los caballos
##      direccion: url del servicio web donde se ubican los detalles de los caballos 
##
#######################################################################################################################

def completaFicheroJsonCaballosRated(nombre, direccion, perJson):
    
    with open(PATH_BASE + '/' + nombre + '.json', 'r') as f:
        contenido = f.read()
        f.close()

    jsonCaballos = json.loads(contenido)
    
    nombreFicheroDetalle = PATH_EXTENDIDO + '/' + nombre + "_detailed"
    
    resultado = completaJsonCaballosRated(direccion, jsonCaballos, nombreFicheroDetalle, perJson)
            
    return resultado

#######################################################################################################################
## Función específica de lectura de fichero JSON que añade detalles de caballos                                     ###
## Argumentos:  
##      nombre: nombre del fichero JSON de origen con los datos de los caballos
##      direccion: url del servicio web donde se ubican los detalles de los caballos 
##
#######################################################################################################################

def completaFicheroJsonCaballosNonRated(nombre, numFicheros, direccion, perJson):
    
    for indice in range(1, numFicheros + 1): 
        with open(PATH_BASE + '/' + nombre + str(indice) + '.json', 'r') as f:
            contenido = f.read()
            f.close()

        jsonCaballos = json.loads(contenido)

        nombreFicheroDetalle = PATH_EXTENDIDO + '/' + nombre + str(indice) + "_detailed"
        resultado = completaJsonCaballosNonRated(direccion, jsonCaballos, nombreFicheroDetalle, perJson)
        print(resultado)
            
    return resultado

#######################################################################################################################
## Función específica de lectura de fichero JSON que añade detalles de caballos                                     ###
## Argumentos:  
##      nombre: nombre del fichero JSON de origen con los datos de los caballos
##      direccion: url del servicio web donde se ubican los detalles de los caballos 
##
#######################################################################################################################

def completaFicheroJsonTrainers(nombre, direccion, perJson):
    
    with open(PATH_BASE + '/' + nombre + '.json', 'r') as f:
        contenido = f.read()
        f.close()

    jsonTrainers = json.loads(contenido)
    
    nombreFicheroDetalle = PATH_EXTENDIDO + '/' + nombre + "_detailed"
    
    resultado = completaJsonTrainers(direccion, jsonTrainers, nombreFicheroDetalle, perJson)
            
    return resultado

#######################################################################################################################
## Función específica de lectura de fichero JSON que añade detalles de fixtures                                     ###
## Argumentos:  
##      nombre: nombre del fichero JSON de origen con los datos de los caballos
##      direccion: url del servicio web donde se ubican los detalles de los caballos 
##
#######################################################################################################################

def completaFicheroJsonFixtures(nombreFixture, nombreFixturePlanning, temporada, direccion, perJson, inicio = 0):
    
    with open(PATH_BASE + '/' + nombreFixture + str(temporada) + '1.json', 'r') as fixture:
        contenidoFixture = fixture.read()
        fixture.close()

    with open(PATH_BASE + '/' + nombreFixturePlanning + str(temporada) + '1.json', 'r') as planning:
        contenidoPlanning = planning.read()
        planning.close()


    jsonFixture = json.loads(contenidoFixture)
    jsonPlanning = json.loads(contenidoPlanning)
    
    nombreFicheroDetalle = PATH_EXTENDIDO + '/' + nombreFixture + str(temporada) + "1_detailed"
    
    resultado = completaJsonFixture(direccion, jsonFixture, jsonPlanning, nombreFicheroDetalle, perJson, inicio)
            
    return resultado

#######################################################################################################################
## Función específica de extracción de carreras de fixtures para un año dado                                        ###
## Argumentos:  
##      year: año
##
#######################################################################################################################

def extraeRacesFixtures(year, inicio, fin):
    salida = {}
    racesReferences = []
    raceReference = {}
    
    payloads={}
    headers = {
        'Cookie': 'incap_ses_1485_2476407=8sO0e1FR7Uuo8I1u18ebFBh61WIAAAAANI0+Z6FZ597Fin/LQtIiNw==; visid_incap_2476407=0PkrmaWeTVaiWkiWfalg1Dt8xGIAAAAAQUIPAAAAAACvrjs1/Yo4ajgxNvjwMFbv'
    }
    
    for indiceFichero in range(inicio, fin + 1):
        with open(PATH_EXTENDIDO + '/' + "results" + str(year) + '1_detailed' + str(indiceFichero) + '.json', 'r') as jsonResults:
            results = json.loads(jsonResults.read())
        
        for fixture in results["data"]:
            if ("races" in fixture) and (fixture["races"] != ""):
                for race in fixture["races"]:
                    raceReference["year"] = year
                    raceReference["fixtureId"] = fixture["fixtureId"]
                    raceReference["raceId"] = race["raceId"]
                    raceReference["divisionSequence"] = race["divisionSequence"]
                    raceReference["courseId"] = fixture["courseId"]
                    raceReference["fixtureType"] = fixture["fixtureType"]
                    raceReference["courseKey"] = fixture["courseKey"]
                    
                    url = "https://www.britishhorseracing.com/feeds/v3/races/" + str(year) + '/' + str(race["raceId"]) + '/' + str(race["divisionSequence"])
                    response = requests.request("GET", url, headers=headers, data=payloads)
                    raceReference["general"] = json.loads(response.text)["data"]
                    
                    url = "https://www.britishhorseracing.com/feeds/v3/races/" + str(year) + '/' + str(race["raceId"]) + '/' + str(race["divisionSequence"]) + '/results'
                    response = requests.request("GET", url, headers=headers, data=payloads)
                    raceReference["results"] = json.loads(response.text)["data"]
                    racesReferences.append(raceReference.copy())
            
            now = datetime.now()
            print(str(fixture["fixtureId"]) + " Timestamp: " + "{:02}".format(now.hour) + ":" + "{:02}".format(now.minute) + ":" + "{:02}".format(now.second))
            
    salida["data"] = racesReferences
            
    with open(PATH_EXTENDIDO + '/' + "raceResults" + str(year) + '1_detailed_' + str(inicio) + '_' + str(fin) + '.json', 'w') as raceResultsFile:
        raceResultsFile.write(json.dumps(salida))
        
    return racesReferences

def extraeRacesFixturesAnual(year, inicio, fin):
    origen = inicio
    final = inicio + 4

    while origen < fin + 1:
        print("Extrayendo año " + str(year) + " desde " + str(origen) + " hasta " + str(final))
        extraeRacesFixtures(year, origen, final)
        origen = final + 1
        final = origen + 4 if (final + 4 < fin) else fin
        
    
#COMIENZO DE CÓDIGO DE PRUEBAS DE PETICIONES
#salida = extraeRacesFixtures(2022,11,15)

#YA EXTRAIDOS:

#web="https://www.britishhorseracing.com/feeds/v3/racehorses"
#resultado = extraeWeb(web,"caballos",1,10)
#449941 Caballos registrados (rated & non rated)

#web="https://www.britishhorseracing.com/feeds/v3/racehorses"
#resultado = extraeWeb(web,"ratedCaballos",3,10000,rated = True)
#Caballos rated contiene además detalles, training-history y performance <--- Solo se extraen para los valorados
#12047 Caballos Rated, máximo por página 10000

#web="https://www.britishhorseracing.com/feeds/v3/jockeys"
#extraeWeb(web,"jockeys",658,250)
#658 Jockeys, máximo por página 250

#web="https://www.britishhorseracing.com/feeds/v3/jockeys/milestones"
#extraeWeb(web,"jockeysMilestones",635)
#635 Jockeys, máximo por página 250

#web="https://www.britishhorseracing.com/feeds/v3/championships/owners"
#extraeWeb(web,"owners",4804,4804, extras="type=jump")
#extraeWeb(web,"owners",4804,4804, extras="type=flat")
#Owners se dividen en flat y jumps
#4804 Owners, máximo por página 10000

#web="https://www.britishhorseracing.com/feeds/v3/racehorses"
#resultado = extraeWeb(web,"ratedCaballos",3,10000,rated = True)
#Caballos rated contiene además detalles, training-history y performance <--- Solo se extraen para los valorados
#12047 Caballos Rated, máximo por página 10000

#web = "https://www.britishhorseracing.com/feeds/v1/racecourses"
#extraeWeb(web,"racecourses",60)
#Racecourses se dividen en flat y jumps
#59 Racecourses

#Planificaciones por año
# web = "https://www.britishhorseracing.com/feeds/v3/fixtures/planning"
# extraeWeb(web,"planning2023",porPagina=2000 ,extras="year=2023")
# extraeWeb(web,"planning2022",porPagina=2000 ,extras="year=2022")
# extraeWeb(web,"planning2021",porPagina=2000 ,extras="year=2021")
# extraeWeb(web,"planning2020",porPagina=2000 ,extras="year=2020")
# extraeWeb(web,"planning2019",porPagina=2000 ,extras="year=2019")
# extraeWeb(web,"planning2018",porPagina=2000 ,extras="year=2018")
# extraeWeb(web,"planning2017",porPagina=2000 ,extras="year=2017")
# extraeWeb(web,"planning2016",porPagina=2000 ,extras="year=2016")
# extraeWeb(web,"planning2015",porPagina=2000 ,extras="year=2015")
# extraeWeb(web,"planning2014",porPagina=2000 ,extras="year=2014")
# extraeWeb(web,"planning2013",porPagina=2000 ,extras="year=2013")

#Resultados por año
#web = "https://www.britishhorseracing.com/feeds/v3/fixtures"
#extraeWeb(web,"results2023",2000,2000, extras="resultsAvailable=false&year=2023")
#extraeWeb(web,"results2022",2000,2000, extras="resultsAvailable=false&year=2022")
#extraeWeb(web,"results2021",2000,2000, extras="resultsAvailable=true&year=2021")
#extraeWeb(web,"results2020",2500,2500, extras="resultsAvailable=true&year=2020")
#extraeWeb(web,"results2019",3000,3000, extras="resultsAvailable=true&year=2019")
#extraeWeb(web,"results2018",3000, 3000, extras="resultsAvailable=true&year=2018")
#extraeWeb(web,"results2017",3000, 3000, extras="resultsAvailable=true&year=2017")
#extraeWeb(web,"results2016",3000, 3000, extras="resultsAvailable=true&year=2016")
#extraeWeb(web,"results2015",3000, 3000, extras="resultsAvailable=true&year=2015")
#extraeWeb(web,"results2014",3000, 3000, extras="resultsAvailable=true&year=2014")
#extraeWeb(web,"results2013",3000, 3000, extras="resultsAvailable=true&year=2013")

#Entrenadores
#web="https://www.britishhorseracing.com/feeds/v3/trainers"
#extraeWeb(web,"trainers",565,250)
#565 Trainers, máximo por página 250

#Extracción de detalles de varios caballos
#web = "https://www.britishhorseracing.com/feeds/v3/racehorses"
#salidaJson = completaFicheroJsonCaballos("ratedCaballos1", web, 200)
#salidaJson = completaFicheroJsonCaballos("ratedCaballos2", web, 200)


#POR EXTRAER:

#Detalles de los resultados (races y going)
#web = "https://www.britishhorseracing.com/feeds/v3/fixtures"
#Results se divide por años

# resultado = completaFicheroJsonFixtures("results", "planning", 2023, web, 100) #COMPLETO
# resultado = completaFicheroJsonFixtures("results", "planning", 2022, web, 100) #COMPLETO
# resultado = completaFicheroJsonFixtures("results", "planning", 2021, web, 100) #COMPLETO
# resultado = completaFicheroJsonFixtures("results", "planning", 2020, web, 100) #COMPLETO
# resultado = completaFicheroJsonFixtures("results", "planning", 2019, web, 100) #COMPLETO
# resultado = completaFicheroJsonFixtures("results", "planning", 2018, web, 100) #--> Repetir los dos últimos
# resultado = completaFicheroJsonFixtures("results", "planning", 2017, web, 100, 1400) #--> Repetir los dos últimos
# resultado = completaFicheroJsonFixtures("results", "planning", 2016, web, 100, 1400) #--> Repetir los dos últimos
# resultado = completaFicheroJsonFixtures("results", "planning", 2015, web, 100) #--> Repetir los dos últimos
# resultado = completaFicheroJsonFixtures("results", "planning", 2014, web, 100, 1400) #--> Repetir los dos últimos
# resultado = completaFicheroJsonFixtures("results", "planning", 2013, web, 100) #--> Repetir los dos últimos

#Extracción de detalles de varios caballos
#web = "https://www.britishhorseracing.com/feeds/v3/racehorses" #<--- Repetir para extraer correctamente todos los detalles
#salidaJson = completaFicheroJsonCaballosRated("ratedCaballos1", web, 200)
#salidaJson = completaFicheroJsonCaballosRated("ratedCaballos2", web, 200)
#completaFicheroJsonCaballosNonRated("horses", 2, web, 10000)

#Detalles de los entrenadores
#Trainers contiene además detalles, performances y nonrunners                    --> Lleva mucho tiempo, hasta 20 minutos por entrenador
#web="https://www.britishhorseracing.com/feeds/v3/trainers"
#completaFicheroJsonTrainers("trainers3", web, 10)

