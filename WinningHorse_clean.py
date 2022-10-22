# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 16:52:50 2022

@author: jdelfres
"""

import json
import requests
from datetime import datetime

#DEFINICION DE VARIABLES DE CONFIGURACIÓN
PATH_BASE ="./pruebas"
#PATH_BASE ="./data"
PATH_EXTENDIDO = PATH_BASE + "/detailed"
PATH_LIMPIO = PATH_BASE + "/clean"

#############################################
### FUNCIONES DE LIMPIEZA DE DATOS (JSON) ###
#############################################

### FUNCIONES DE LIMPIEZA DE HORSES RATED ###
def limpiaHorsesRated(nombreFicheros, indice1, indice2):
        salida = {}
        horsesClean = []
        horseTemp = {}
        
        nombreFicheroEntrada = PATH_EXTENDIDO + '/' + nombreFicheros + str(indice1) + '_detailed' + str(indice2) + '.json'
        nombreFicheroSalida = PATH_LIMPIO + '/' + nombreFicheros + str(indice1) + '_detailed' + str(indice2) + '.json'
        
        with open(nombreFicheroEntrada, 'r') as f:        
            contenido = json.loads(f.read())
        
        salida["total"] = contenido["total"]
        salida["per_page"] = contenido["per_page"]
        salida["current_page"] = contenido["current_page"]
        salida["last_page"] = contenido["last_page"]
        salida["from"] = contenido["from"]
        salida["to"] = contenido["to"]
        
        #Copiamos los datos que queremos mantener por cada caballo
        for horse in contenido["data"]:
            horseTemp["id"] = horse["id"] if ("id" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["name"] = horse["name"] if ("name" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["dateOfBirth"] = horse["dateOfBirth"] if ("dateOfBirth" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["deathDate"] = horse["deathDate"] if ("deathDate" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["deathNote"] = horse["deathNote"]  if ("deathNote" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["age"] = horse["age"] if ("age" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["moniker"] = horse["moniker"] if ("moniker" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["dam"] = horse["dam"] if ("dam" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["sire"] = horse["sire"] if ("sire" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["sex"] = horse["sex"] if ("sex" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["trainerName"] = horse["trainerName"] if ("trainerName" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["trainerId"] = horse["trainerId"] if ("trainerId" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["ownerName"] = horse["ownerName"] if ("ownerName" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["ownerId"] = horse["ownerId"] if ("ownerId" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["ratingAWT"] = horse["ratingAWT"] if ("ratingAWT" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["ratingChase"] = horse["ratingChase"] if ("ratingChase" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["ratingFlat"] = horse["ratingFlat"] if ("ratingFlat" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["ratingHurdle"] = horse["ratingHurdle"] if ("ratingHurdle" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["nameWithNoCountry"] = horse["nameWithNoCountry"] if ("nameWithNoCountry" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["performanceHistory"] = horse["performanceHistory"] if ("performanceHistory" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["dam"] = horse["lineage"]["dam"]["animalId"] if ("lineage" in horse and "dam" in horse["lineage"]) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["sire"] = horse["lineage"]["sire"]["animalId"] if ("lineage" in horse and "sire" in horse["lineage"]) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["damsire"] = horse["lineage"]["damsire"]["animalId"] if ("lineage" in horse and "damsire" in horse["lineage"]) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horsesClean.append(horseTemp.copy())
        
        #Una vez terminado incorporamos a la salida
        salida["data"] = horsesClean
        
        with open(nombreFicheroSalida, 'w') as f:   
            f.write(json.dumps(salida))
            
        return "fichero limpio volcado en: " + nombreFicheroSalida


def limpiaAllHorsesRated(nombreFicheros, indice1, indice2):
    
    for i in range(1,indice2 + 1):
            resultado = limpiaHorsesRated(nombreFicheros, indice1, i)
            print(resultado)
            
### FUNCIONES DE LIMPIEZA DE HORSES RATED AND NON RATED###           
def limpiaHorsesFull(nombreFicheros, indice1):
        salida = {}
        horsesClean = []
        horseTemp = {}
        
        nombreFicheroEntrada = PATH_BASE + '/' + nombreFicheros + str(indice1) + '.json'
        nombreFicheroSalida = PATH_LIMPIO + '/' + nombreFicheros + str(indice1) + '.json'
        
        with open(nombreFicheroEntrada, 'r') as f:        
            contenido = json.loads(f.read())
        
        salida["total"] = contenido["total"]
        salida["per_page"] = contenido["per_page"]
        salida["current_page"] = contenido["current_page"]
        salida["last_page"] = contenido["last_page"]
        salida["from"] = contenido["from"]
        salida["to"] = contenido["to"]
        
        #Copiamos los datos que queremos mantener por cada caballo
        for horse in contenido["data"]:
            horseTemp["id"] = horse["id"] if ("id" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["name"] = horse["name"] if ("name" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["dateOfBirth"] = horse["dateOfBirth"] if ("dateOfBirth" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["deathDate"] = horse["deathDate"] if ("deathDate" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["deathNote"] = horse["deathNote"]  if ("deathNote" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["age"] = horse["age"] if ("age" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["moniker"] = horse["moniker"] if ("moniker" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["dam"] = horse["dam"] if ("dam" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["sire"] = horse["sire"] if ("sire" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["sex"] = horse["sex"] if ("sex" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["trainerName"] = horse["trainerName"] if ("trainerName" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["trainerId"] = horse["trainerId"] if ("trainerId" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["ownerName"] = horse["ownerName"] if ("ownerName" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["ownerId"] = horse["ownerId"] if ("ownerId" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["ratingAWT"] = horse["ratingAWT"] if ("ratingAWT" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["ratingChase"] = horse["ratingChase"] if ("ratingChase" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["ratingFlat"] = horse["ratingFlat"] if ("ratingFlat" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["ratingHurdle"] = horse["ratingHurdle"] if ("ratingHurdle" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["nameWithNoCountry"] = horse["nameWithNoCountry"] if ("nameWithNoCountry" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["performanceHistory"] = horse["performanceHistory"] if ("performanceHistory" in horse) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["dam"] = horse["lineage"]["dam"]["animalId"] if ("lineage" in horse and "dam" in horse["lineage"]) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["sire"] = horse["lineage"]["sire"]["animalId"] if ("lineage" in horse and "sire" in horse["lineage"]) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horseTemp["damsire"] = horse["lineage"]["damsire"]["animalId"] if ("lineage" in horse and "damsire" in horse["lineage"]) else None #COMPROBAR CON "LINEAGE" IN HORSE   
            horsesClean.append(horseTemp.copy())
        
        #Una vez terminado incorporamos a la salida
        salida["data"] = horsesClean
        
        with open(nombreFicheroSalida, 'w') as f:   
            f.write(json.dumps(salida))
            
        return "fichero limpio volcado en: " + nombreFicheroSalida


def limpiaAllHorsesFull(nombreFicheros, indice1):
    
    for i in range(1,indice1 + 1):
            resultado = limpiaHorsesFull(nombreFicheros, i)
            print(resultado)            
            
### FUNCIONES DE LIMPIEZA DE JOCKEYS ###            
def limpiaJockeys(nombreFichero):
        salida = {}
        jockeysClean = []
        jockeyTemp = {}
        
        nombreFicheroEntrada = PATH_BASE + '/' + nombreFichero + '.json'
        nombreFicheroSalida = PATH_LIMPIO + '/' + nombreFichero + '.json'
        
        with open(nombreFicheroEntrada, 'r') as f:        
            contenido = json.loads(f.read())
        
        salida["total"] = contenido["total"]
        salida["success"] = contenido["success"]

        
        #Copiamos los datos que queremos mantener por cada caballo
        for jockey in contenido["data"]:
            jockeyTemp["entryId"] = jockey["entryId"] if "entryId" in jockey else None
            jockeyTemp["entryType"] = jockey["entryType"] if "entryType" in jockey else None
            jockeyTemp["entryName"] = jockey["entryName"] if "entryName" in jockey else None
            jockeyTemp["totalRun"] = jockey["totalRun"] if "totalRun" in jockey else None
            jockeyTemp["totalWins"] = jockey["totalWins"] if "totalWins" in jockey else None
            jockeyTemp["pre95EntryId"] = jockey["pre95EntryId"] if "pre95EntryId" in jockey else None
          
            jockeysClean.append(jockeyTemp.copy())
        
        #Una vez terminado incorporamos a la salida
        salida["data"] = jockeysClean
        
        with open(nombreFicheroSalida, 'w') as f:   
            f.write(json.dumps(salida))
            
        return "fichero limpio volcado en: " + nombreFicheroSalida


def limpiaAllJockey(nombreFicheros):

            resultado = limpiaJockeys(nombreFicheros)
            print(resultado)            
            
            
            
### FUNCIONES DE LIMPIEZA DE JOCKEYS ###    
def limpiaResultados(nombreFichero, year, indice):
        salida = {}
        resultadosClean = []
        resultTemp = {}
        
        nombreFicheroEntrada = PATH_EXTENDIDO + '/' + nombreFichero + str(year) + '1_detailed' + str(indice) + '.json'
        nombreFicheroSalida = PATH_LIMPIO + '/' + nombreFichero + str(year) + '1_detailed' + str(indice) + '.json'
        
        with open(nombreFicheroEntrada, 'r') as f:        
            contenido = json.loads(f.read())
        
        salida["total"] = contenido["total"]
        salida["per_page"] = contenido["per_page"]
        salida["current_page"] = contenido["current_page"]
        salida["last_page"] = contenido["last_page"]
        salida["from"] = contenido["from"]
        salida["to"] = contenido["to"]
        
        #Copiamos los datos que queremos mantener por cada caballo
        for result in contenido["data"]:
            resultTemp["fixtureId"] = result["fixtureId"] if ("fixtureId" in result) else None
            resultTemp["fixtureYear"] = result["fixtureYear"] if ("fixtureYear" in result) else None
            resultTemp["fixtureDate"] = result["fixtureDate"] if ("fixtureDate" in result) else None
            resultTemp["BSTime"] = result["BSTime"] if ("BSTime" in result) else None
            resultTemp["distance"] = result["distance"] if ("distance" in result) else None
            resultTemp["courseName"] = result["courseName"] if ("courseName" in result) else None
            resultTemp["alertLevel"] = result["alertLevel"] if ("alertLevel" in result) else None
            resultTemp["region"] = result["region"] if ("region" in result) else None
            resultTemp["tier"] = result["tier"] if ("tier" in result) else None
            resultTemp["firstRace"] = result["firstRace"] if ("firstRace" in result) else None
            resultTemp["racecardAvailable"] = result["racecardAvailable"] if ("racecardAvailable" in result) else None
            resultTemp["entriesAvailable"] = result["entriesAvailable"] if ("entriesAvailable" in result) else None
            resultTemp["transparentAvailable"] = result["transparentAvailable"] if ("transparentAvailable" in result) else None
            resultTemp["blackTypeRaces"] = result["blackTypeRaces"] if ("blackTypeRaces" in result) else None
            resultTemp["bcsEvent"] = result["bcsEvent"] if ("bcsEvent" in result) else None
            resultTemp["numberOfRaces"] = result["numberOfRaces"] if ("numberOfRaces" in result) else None
            resultTemp["fixtureName"] = result["fixtureName"] if ("fixtureName" in result) else None
            resultTemp["fixtureType"] = result["fixtureType"] if ("fixtureType" in result) else None
            resultTemp["meetingId"] = result["meetingId"] if ("meetingId" in result) else None
            resultTemp["racingTrackType"] = result["racingTrackType"] if ("racingTrackType" in result) else None
            resultTemp["racePlanningCode"] = result["racePlanningCode"] if ("racePlanningCode" in result) else None
            resultTemp["courseId"] = result["courseId"] if ("courseId" in result) else None
            resultTemp["ticketsLink"] = result["ticketsLink"] if ("ticketsLink" in result) else None
            resultTemp["majorEvent"] = result["majorEvent"] if ("majorEvent" in result) else None
            resultTemp["stalls"] = result["stalls"] if ("stalls" in result) else None
            resultTemp["abandonedReasonCode"] = result["abandonedReasonCode"] if ("abandonedReasonCode" in result) else None
            resultTemp["fixtureSession"] = result["fixtureSession"] if ("fixtureSession" in result) else None
            resultTemp["goingUpdatedDate"] = result["goingUpdatedDate"] if ("goingUpdatedDate" in result) else None
            resultTemp["goingUpdatedTime"] = result["goingUpdatedTime"] if ("goingUpdatedTime" in result) else None
            resultTemp["resultsAvailable"] = result["resultsAvailable"] if ("resultsAvailable" in result) else None
            resultTemp["courseKey"] = result["courseKey"] if ("courseKey" in result) else None
            resultTemp["criteriaType"] = result["criteriaType"] if ("criteriaType" in result) else None
            resultTemp["prizeMoney"] = result["prizeMoney"] if ("prizeMoney" in result) else None
            resultTemp["transitionDate"] = result["transitionDate"] if ("transitionDate" in result) else None
            resultTemp["stewardsReport"] = result["stewardsReport"] if ("stewardsReport" in result) else None
            resultTemp["cotcInspectionStatus"] = result["cotcInspectionStatus"]  if ("cotcInspectionStatus" in result) else None
            resultTemp["cotcInspectionText"] = result["cotcInspectionText"] if ("cotcInspectionText" in result) else None
            resultTemp["cotcInspectionPreCautionary"] = result["cotcInspectionPreCautionary"] if ("cotcInspectionPreCautionary" in result) else None
            resultTemp["cotcInspectionUpdatedAt"] = result["cotcInspectionUpdatedAt"] if ("cotcInspectionUpdatedAt" in result) else None
            resultTemp["weatherUpdatedAt"] = result["weatherUpdatedAt"] if ("weatherUpdatedAt" in result) else None
            resultTemp["stallsText"] = result["stallsText"] if ("stallsText" in result) else None
            resultTemp["stallsUpdatedAt"] = result["stallsUpdatedAt"] if ("stallsUpdatedAt" in result) else None
            resultTemp["goingUpdatedAt"] = result["goingUpdatedAt"] if ("goingUpdatedAt" in result) else None
            resultTemp["inspectionsText"] = result["inspectionsText"] if ("inspectionsText" in result) else None
            resultTemp["inspectionsUpdatedAt"] = result["inspectionsUpdatedAt"] if ("inspectionsUpdatedAt" in result) else None
            resultTemp["railUpdatedAt"] = result["railUpdatedAt"] if ("railUpdatedAt" in result) else None
            resultTemp["otherUpdatedAt"] = result["otherUpdatedAt"] if ("otherUpdatedAt" in result) else None
            resultTemp["wateringText"] = result["wateringText"] if ("wateringText" in result) else None
            resultTemp["wateringUpdatedAt"] = result["wateringUpdatedAt"] if ("wateringUpdatedAt" in result) else None
            resultTemp["lastUpdated"] = result["lastUpdated"] if ("lastUpdated" in result) else None
          
            resultadosClean.append(resultTemp.copy())
        
        #Una vez terminado incorporamos a la salida
        salida["data"] = resultadosClean
        
        with open(nombreFicheroSalida, 'w') as f:   
            f.write(json.dumps(salida))
            
        return "fichero limpio volcado en: " + nombreFicheroSalida

def limpiaAllResultados(nombreFicheros, year, numFicheros):

            for fichero in range(1,numFicheros + 1):
                resultado = limpiaResultados(nombreFicheros, year, fichero)
                print(resultado)
                

def mergeHorsesDetailedHorses(ficheroHorses, ficheroDetailed, inicioHorses, finHorses, inicioDetailed, finDetailed):
    #Para cada fichero de horses:
    for contHorses in range(inicioHorses,finHorses + 1):    
        buscador = 0
        #Volcar fichero en variable json horseAll
        with open(PATH_LIMPIO + "/" + ficheroHorses + str(contHorses) + '.json', 'r' ) as ficheroHorseAll:
            horseAll = json.loads(ficheroHorseAll.read())
            print(horseAll["to"])
            maxHorseIndex = horseAll["to"] - horseAll["from"] + 1
        #Para cada fichero de detailed:
            for contHorsesDetailed in range(inicioDetailed,finDetailed + 1):
            #Volcar fichero en variable json ficheroDetailed
                with open(PATH_LIMPIO + "/" + ficheroDetailed + str(contHorsesDetailed) + '.json', 'r' ) as ficheroHorseDetailed:
                    horseDetailed = json.loads(ficheroHorseDetailed.read())
            #Para cada horseDetailed de horseDetailed["data"]:
                for horseDetailed in horseDetailed["data"]:
                #Buscar horseDetailed["id"] == horseAll["data"][buscador]["id"]:
                    while (buscador < maxHorseIndex) and (horseDetailed["id"] != horseAll["data"][buscador]["id"]):
                        buscador += 1
                    #Si lo encuentra horseAll["data"][buscador]["id"] =  horseDetailed.copy()
                    if (buscador < maxHorseIndex) and (horseDetailed["id"] == horseAll["data"][buscador]["id"]):
                        horseAll["data"][buscador] =  horseDetailed.copy()
                    buscador = 0
                
            with open(PATH_LIMPIO + "/" + ficheroHorses + str(contHorses) + '_Merged.json', 'w' ) as ficheroHorseMerged:
                ficheroHorseMerged.write(json.dumps(horseAll))

def limpiaRaceResultsDetailed(ficheroRaceResultsDetailed):
    raceTemp = {}
    raceResultPositionTemp = {}
    
    arrayGeneral = []
    arrayPositions = []

    salidaGeneral = {}
    salidaPositions = {}
    
    #Abrimos el fichero y nos quedamos con el campo data
    with open(PATH_EXTENDIDO + '/' + ficheroRaceResultsDetailed + '.json','r') as fichero:
        races = json.loads(fichero.read())["data"]
    #Para cada fixture dentro de data:
    for race in races:
        raceTemp["year"] = race["year"]
        raceTemp["fixtureId"] = race["fixtureId"]
        raceTemp["raceId"] = race["raceId"]
        raceTemp["divisionSequence"] = race["divisionSequence"]
        raceTemp["courseId"] = race["courseId"]
        raceTemp["fixtureType"] = race["fixtureType"]
        raceTemp["courseKey"] = race["courseKey"]        
        raceTemp["raceDate"] = race["general"][0]["raceDate"]
        raceTemp["raceTime"] = race["general"][0]["raceTime"]
        raceTemp["distanceValue"] = race["general"][0]["distanceValue"]
        raceTemp["sexLimit"] = race["general"][0]["sexLimit"]
        raceTemp["animalType"] = race["general"][0]["animalType"]
        raceTemp["prizeAmount"] = race["general"][0]["prizeAmount"]
        raceTemp["ageLimit"] = race["general"][0]["ageLimit"]
        raceTemp["raceCriteriaRaceType"] = race["general"][0]["raceCriteriaRaceType"]
        raceTemp["raceCriteriaMinimumWeight"] = race["general"][0]["raceCriteriaMinimumWeight"]
        raceTemp["raceCriteriaWeightsRaised"] = race["general"][0]["raceCriteriaWeightsRaised"]

        for raceResultPosition in race["results"]:
            raceResultPositionTemp["year"] = race["year"]
            raceResultPositionTemp["fixtureId"] = race["fixtureId"]
            raceResultPositionTemp["raceId"] = race["raceId"]
            raceResultPositionTemp["divisionSequence"] = race["divisionSequence"]            
            raceResultPositionTemp["horseId"] = raceResultPosition["horseId"]
            raceResultPositionTemp["resultFinishPos"] = raceResultPosition["resultFinishPos"]
            raceResultPositionTemp["status"] = raceResultPosition["status"]
            raceResultPositionTemp["ageYear"] = raceResultPosition["ageYear"]
            raceResultPositionTemp["clothNumber"] = raceResultPosition["clothNumber"]
            raceResultPositionTemp["weightValue"] = raceResultPosition["weightValue"]
            raceResultPositionTemp["sexType"] = raceResultPosition["sexType"]
            raceResultPositionTemp["jockeyId"] = raceResultPosition["jockeyId"]
            raceResultPositionTemp["trainerId"] = raceResultPosition["trainerId"]
            raceResultPositionTemp["ownerId"] = raceResultPosition["ownerId"]
            raceResultPositionTemp["positionFinishTime"] = raceResultPosition["positionFinishTime"]
            raceResultPositionTemp["bettingRatio"] = raceResultPosition["bettingRatio"]
            raceResultPositionTemp["raceCriteriaRaceType"] = raceResultPosition["raceCriteriaRaceType"]
            
            arrayPositions.append(raceResultPositionTemp.copy())
        arrayGeneral.append(raceTemp.copy())
    
    salidaGeneral["data"] = arrayGeneral
    salidaPositions["data"] = arrayPositions
     #Escribimos los dos resultados en limpio   
    with open(PATH_LIMPIO + '/' + ficheroRaceResultsDetailed + '_general.json', 'w') as ficheroGeneral:
        ficheroGeneral.write(json.dumps(salidaGeneral))
    
    with open(PATH_LIMPIO + '/' + ficheroRaceResultsDetailed + '_positions.json', 'w') as ficheroPositions:
        ficheroPositions.write(json.dumps(salidaPositions))   
    
    return "OK"

#FUNCIONES EXTRA PARA REPARACIÓN DE ARCHIVOS INCOMPLETOS
def mergeRaces(ficheroDetailed, ficheroClean, inicioDetailed, finDetailed):
    detailed = []
    clean = []
    
    tempValues = {}
    salida = {}
    
    indiceRaceClean = 0
    
    with open(PATH_LIMPIO + '/' + ficheroClean + '_general.json', 'r') as contenidoClean:
        clean = json.loads(contenidoClean.read())["data"]
    
    for indiceFichero in range(inicioDetailed, finDetailed + 1):
        with open(PATH_EXTENDIDO + '/' + ficheroDetailed + str(indiceFichero) +  '.json', 'r') as contenidoDetailed:
            detailed = json.loads(contenidoDetailed.read())["data"]
        
        for indiceFixtureDetailed in range(0, len(detailed)):
            print(detailed[indiceFixtureDetailed]["fixtureId"])
            if ("races" in detailed[indiceFixtureDetailed]):
                for indiceRaceDetailed in range(0, len(detailed[indiceFixtureDetailed]["races"])):
                    print("id clean" + str(clean[indiceRaceClean]["fixtureId"]))
                    if detailed[indiceFixtureDetailed]["races"][indiceRaceDetailed]["raceId"] == clean[indiceRaceClean]["raceId"]:
                        # tempValues["courseId"] = detailed[indiceFixtureDetailed]["courseId"]
                        # tempValues["fixtureType"] = detailed[indiceFixtureDetailed]["fixtureType"]
                        # tempValues["courseKey"] = detailed[indiceFixtureDetailed]["courseKey"]
                        
                        tempValues["divisionSequence"] = detailed[indiceFixtureDetailed]["races"][indiceRaceDetailed]["divisionSequence"]
                        
                        clean[indiceRaceClean].update(tempValues)
                    indiceRaceClean += 1

    salida["data"] = clean
    with open(PATH_LIMPIO + '/' + ficheroClean + '_general_cleanB.json', 'w') as contenidoCleanMerged:
        contenidoCleanMerged.write(json.dumps(salida))      
        
    return "OK"
    
def mergeRaces2(ficheroDetailed, ficheroClean,inicioDetailed, finDetailed):
    detailed = []
    clean = []
    
    tempValues = {}
    salida = {}
    
    indiceRaceClean = 0
    
    with open(PATH_LIMPIO + '/' + ficheroClean + '_general.json', 'r') as contenidoClean:
        clean = json.loads(contenidoClean.read())["data"]
    
    for indiceFichero in range(inicioDetailed, finDetailed + 1):
        with open(PATH_EXTENDIDO + '/' + ficheroDetailed + str(indiceFichero) +  '.json', 'r') as contenidoDetailed:
            detailed = json.loads(contenidoDetailed.read())["data"]
        
        for indiceFixtureDetailed in range(0, len(detailed)):
            print("Fixture " + str(detailed[indiceFixtureDetailed]["fixtureId"]))
            
            if ("races" in detailed[indiceFixtureDetailed]):
                for indiceRaceDetailed in range(0, len(detailed[indiceFixtureDetailed]["races"])):                 
                     if detailed[indiceFixtureDetailed]["races"][indiceRaceDetailed]["raceId"] == clean[indiceRaceClean]["raceId"]:
                         print("saluda")
    #                     # tempValues["courseId"] = detailed[indiceFixtureDetailed]["courseId"]
    #                     # tempValues["fixtureType"] = detailed[indiceFixtureDetailed]["fixtureType"]
    #                     # tempValues["courseKey"] = detailed[indiceFixtureDetailed]["courseKey"]
                        
                         tempValues["divisionSequence"] = detailed[indiceFixtureDetailed]["races"][indiceRaceDetailed]["divisionSequence"]
                         print(tempValues)
                         clean[indiceRaceClean].update(tempValues)
                         print(clean[indiceRaceClean])
                     indiceRaceClean += 1

    salida["data"] = clean
    with open(PATH_LIMPIO + '/' + ficheroClean + '_general_cleanB.json', 'w') as contenidoCleanMerged:
        contenidoCleanMerged.write(json.dumps(salida))      
        
    return "OK"

def mergeRaces3(ficheroCleanGeneral, ficheroCleanPositions):
    payloads={}
    headers = {
        'Cookie': 'incap_ses_1485_2476407=8sO0e1FR7Uuo8I1u18ebFBh61WIAAAAANI0+Z6FZ597Fin/LQtIiNw==; visid_incap_2476407=0PkrmaWeTVaiWkiWfalg1Dt8xGIAAAAAQUIPAAAAAACvrjs1/Yo4ajgxNvjwMFbv'
    }
    tempResultClean = {}
    salida = {}

    with open(PATH_LIMPIO + '/' + ficheroCleanGeneral + '.json', 'r') as contenidoClean:
        general = json.loads(contenidoClean.read())["data"]

    with open(PATH_LIMPIO + '/' + ficheroCleanPositions + '.json', 'r') as contenidoClean:
        positions = json.loads(contenidoClean.read())["data"]
    
    print("Tratando fichero: ", ficheroCleanPositions)    
    
    #Incluimos el campo que falta en todos los registros:
    for position in positions:
        position["divisionSequence"] = 0
    
    nonDuplicatedPositions  = []
    for position in positions:
        if position not in nonDuplicatedPositions:
            nonDuplicatedPositions.append(position)
            
    positions = nonDuplicatedPositions
        
    for race in general:
       if(race["divisionSequence"] != 0 ):
           print("Toca incorporarlo")
           url = "https://www.britishhorseracing.com/feeds/v3/races/" +  str(race["year"]) + "/" +  str(race["raceId"]) + "/" + str(race["divisionSequence"]) + '/results' 

           response = requests.request("GET", url, headers=headers, data=payloads)
           detalle = json.loads(response.text)
           
           for responseResult in detalle["data"]:
               tempResultClean["year"] = responseResult["yearOfRace"]
               tempResultClean["fixtureId"] = race["fixtureId"]
               tempResultClean["raceId"] = responseResult["raceId"]
               tempResultClean["divisionSequence"] = race["divisionSequence"]            
               tempResultClean["horseId"] = responseResult["horseId"]
               tempResultClean["resultFinishPos"] = responseResult["resultFinishPos"]
               tempResultClean["status"] = responseResult["status"]
               tempResultClean["ageYear"] = responseResult["ageYear"]
               tempResultClean["clothNumber"] = responseResult["clothNumber"]
               tempResultClean["weightValue"] = responseResult["weightValue"]
               tempResultClean["sexType"] = responseResult["sexType"]
               tempResultClean["jockeyId"] = responseResult["jockeyId"]
               tempResultClean["trainerId"] = responseResult["trainerId"]
               tempResultClean["ownerId"] = responseResult["ownerId"]
               tempResultClean["positionFinishTime"] = responseResult["positionFinishTime"]
               tempResultClean["bettingRatio"] = responseResult["bettingRatio"]
               tempResultClean["raceCriteriaRaceType"] = responseResult["raceCriteriaRaceType"]
                
           positions.append(tempResultClean.copy())
           
    salida["data"] = positions
    with open(PATH_LIMPIO + '/' + ficheroCleanPositions + '_B.json', 'w') as contenidoCleanMerged:
        contenidoCleanMerged.write(json.dumps(salida))
    
    return "OK"

#EJECUCIONES MASIVAS
# limpiaRaceResultsDetailed("raceResults20221_detailed_1_2")
# limpiaRaceResultsDetailed("raceResults20221_detailed_3_5")
# limpiaRaceResultsDetailed("raceResults20221_detailed_5_10")
# limpiaRaceResultsDetailed("raceResults20221_detailed_11_15")
# limpiaRaceResultsDetailed("raceResults20221_detailed_11_15")
# limpiaRaceResultsDetailed("raceResults20211_detailed_1_5")
# limpiaRaceResultsDetailed("raceResults20211_detailed_6_10")
# limpiaRaceResultsDetailed("raceResults20211_detailed_11_15")
#limpiaAllResultados("results",2013,14)
# limpiaAllResultados("results",2014,15)
# limpiaAllResultados("results",2015,14)
# limpiaAllResultados("results",2016,15)
# limpiaAllResultados("results",2017,15)
# limpiaAllResultados("results",2018,15)
# limpiaAllResultados("results",2019,15)
# limpiaAllResultados("results",2020,11)
# limpiaAllResultados("results",2021,14)
# limpiaAllResultados("results",2022,14)
#limpiaAllResultados("results",2023,14)

# mergeRaces2("results20221_detailed","raceResults20221_detailed_1_2", 1, 2)
# mergeRaces2("results20221_detailed","raceResults20221_detailed_3_5", 3, 5)
# mergeRaces2("results20221_detailed","raceResults20221_detailed_6_10", 6, 10)
# mergeRaces2("results20221_detailed","raceResults20221_detailed_11_15", 11, 15)
# mergeRaces2("results20211_detailed","raceResults20211_detailed_1_5", 1, 5)
# mergeRaces2("results20211_detailed","raceResults20211_detailed_6_10", 6, 10)
# mergeRaces2("results20211_detailed","raceResults20211_detailed_11_15", 11, 15)

#mergeRaces3("raceResults20221_detailed_1_2_general", "raceResults20221_detailed_1_2_positions")
#mergeRaces3("raceResults20221_detailed_3_5_general", "raceResults20221_detailed_3_5_positions")
#mergeRaces3("raceResults20221_detailed_6_10_general", "raceResults20221_detailed_6_10_positions")
#mergeRaces3("raceResults20221_detailed_11_15_general", "raceResults20221_detailed_11_15_positions")
#mergeRaces3("raceResults20211_detailed_1_5_general", "raceResults20211_detailed_1_5_positions")
#mergeRaces3("raceResults20211_detailed_6_10_general", "raceResults20211_detailed_6_10_positions")
#mergeRaces3("raceResults20211_detailed_11_15_general", "raceResults20211_detailed_11_15_positions")



#limpiaAllHorsesRated("RatedCaballos", 1, 50)
#limpiaAllHorsesFull("horses", 45)

#mergeHorsesDetailedHorses("horses","ratedCaballos1_detailed", 1, 45, 1, 50)