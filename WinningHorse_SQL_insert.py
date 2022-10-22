# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 13:59:16 2022

@author: jdelfres
"""

import json
from datetime import datetime

#DEFINICION DE VARIABLES DE CONFIGURACIÓN
PATH_BASE ="./pruebas"
#PATH_BASE ="./data"
PATH_EXTENDIDO = PATH_BASE + "/detailed"
PATH_CLEAN = PATH_BASE + "/clean"
PATH_SQL = PATH_BASE + "/SQL"

def formatField(field):
    if type(field) == int:
        return str(field) 
    elif type(field) == str:
        return "\"" + field + "\""
    else: 
        return "NULL"

def caballostoSQL(nombreFichero, nombreTabla, commitLines):
    
    numInserts = 0
    lastHorse = 0
    
    with open(PATH_CLEAN + '/' + nombreFichero + '_Merged.json', 'r') as caballosFile:
        caballos = json.loads(caballosFile.read())
    
    lastHorse = caballos["to"] - caballos["from"] + 1
    cabecera = "INSERT INTO " + nombreTabla.upper() + "(ID, NAME, DATEOFBIRTH, DEATHDATE, DEATHNOTE, AGE, MONIKER, DAM, SIRE, SEX, TRAINERNAME, TRAINERID, OWNERNAME, OWNERID, RATINGAWT, RATINGCHASE, RATINGFLAT, RATINGHURDLE, NAMEWITHNOCOUNTRY, PERFORMANCEHISTORY, DAMSIRE) VALUES "
    salidaSQL = cabecera
    for caballo in caballos["data"]:   
        salidaSQL += "(" +     formatField(caballo["id"]) + ","               
        salidaSQL +=           formatField(caballo["name"])   + ","             
        salidaSQL +=           formatField(caballo["dateOfBirth"])   + ","      
        salidaSQL +=           formatField(caballo["deathDate"])  + ","         
        salidaSQL +=           formatField(caballo["deathNote"])  + ","         
        salidaSQL +=           formatField(caballo["age"])    + ","              
        salidaSQL +=           formatField(caballo["moniker"])   + ","          
        salidaSQL +=           formatField(caballo["dam"])    + ","             
        salidaSQL +=           formatField(caballo["sire"])   + ","             
        salidaSQL +=           formatField(caballo["sex"])   + "," 
        salidaSQL +=           formatField(caballo["trainerName"])    + ","     
        salidaSQL +=           formatField(caballo["trainerId"])   + ","        
        salidaSQL +=           formatField(caballo["ownerName"]) + ","          
        salidaSQL +=           formatField(caballo["ownerId"])    + ","         
        salidaSQL +=           formatField(caballo["ratingAWT"])   + ","        
        salidaSQL +=           formatField(caballo["ratingChase"])  + ","       
        salidaSQL +=           formatField(caballo["ratingFlat"])    + ","      
        salidaSQL +=           formatField(caballo["ratingHurdle"])   + ","     
        salidaSQL +=           formatField(caballo["nameWithNoCountry"]) + ","  
        salidaSQL +=           formatField(caballo["performanceHistory"]) + ","  
        salidaSQL +=           formatField(caballo["damsire"])          
        salidaSQL +=           ")"

        numInserts += 1
        
        if (numInserts % commitLines != 0) and (numInserts != lastHorse):
            salidaSQL += ",\n"
        
        else:
            salidaSQL += ";\nCOMMIT;\n"
            if (numInserts != lastHorse):
                salidaSQL += cabecera
            
    with open(PATH_SQL + '/' + "INSERTS_" + nombreFichero + '.sql', 'w') as caballosSQLFile:
        caballosSQLFile.write(salidaSQL)
        
    return "OK"


def RacesGeneraltoSQL(nombreFichero, nombreTabla, commitLines, numeracion):
    
    numInserts = 0
    lastRace = 0
    
    with open(PATH_CLEAN + '/' + nombreFichero + '.json', 'r') as RaceGeneralFile:
        races = json.loads(RaceGeneralFile.read())
    
    lastRace = len(races["data"])
    cabecera = "INSERT INTO " + nombreTabla.upper() + "(YEAR, FIXTUREID, RACEID, DIVISIONSEQUENCE, COURSEID, FIXTURETYPE, COURSEKEY, RACEDATE, RACETIME, DISTANCEVALUE, SEXLIMIT, ANIMALTYPE, PRIZEAMOUNT, AGELIMIT, RACECRITERIARACETYPE, RACECRITERIAMINIMUMWEIGHT, RACECRITERIAWEIGHTSRAISED)\n VALUES "
    salidaSQL = cabecera
    for race in races["data"]:   
        salidaSQL += "(" +     formatField(race["year"]) + ","
        salidaSQL +=           formatField(race["fixtureId"]) + ","
        salidaSQL +=           formatField(race["raceId"]) + ","
        salidaSQL +=           formatField(race["divisionSequence"]) + ","
        salidaSQL +=           formatField(race["courseId"]) + ","
        salidaSQL +=           formatField(race["fixtureType"]) + ","
        salidaSQL +=           formatField(race["courseKey"]) + ","
        salidaSQL +=           formatField(race["raceDate"]) + ","
        salidaSQL +=           formatField(race["raceTime"]) + ","
        salidaSQL +=           formatField(race["distanceValue"]) + ","
        salidaSQL +=           formatField(race["sexLimit"]) + ","
        salidaSQL +=           formatField(race["animalType"]) + ","
        salidaSQL +=           formatField(race["prizeAmount"]) + ","
        salidaSQL +=           formatField(race["ageLimit"]) + ","
        salidaSQL +=           formatField(race["raceCriteriaRaceType"]) + ","
        salidaSQL +=           formatField(race["raceCriteriaMinimumWeight"]) + ","
        salidaSQL +=           formatField(race["raceCriteriaWeightsRaised"])       
        salidaSQL +=           ")"

        numInserts += 1
        
        if (numInserts % commitLines != 0) and (numInserts != lastRace):
            salidaSQL += ",\n"
        
        else:
            salidaSQL += ";\nCOMMIT;\n"
            if (numInserts != lastRace):
                salidaSQL += cabecera
            
    with open(PATH_SQL + '/' + "INSERTS_" + 'raceGeneral' + str(numeracion) + '.sql', 'w') as RacesGeneralSQLFile:
        RacesGeneralSQLFile.write(salidaSQL)
        
    return "OK"


def RacePositionstoSQL(nombreFichero, nombreTabla, commitLines, numeracion):
    
    numInserts = 0
    lastRace = 0
    
    with open(PATH_CLEAN + '/' + nombreFichero + '.json', 'r') as RaceGeneralFile:
        races = json.loads(RaceGeneralFile.read())
    
    lastRace = len(races["data"])
    cabecera = "INSERT INTO " + nombreTabla.upper() + "(RACEID, YEAR, DIVISIONSEQUENCE, HORSEID, RESULTFINISHPOS, STATUS, AGEYEAR, CLOTHNUMBER, WEIGHTVALUE, SEXTYPE, JOCKEYID, TRAINERID, OWNERID, POSITIONFINISHTIME, BETTINGRATIO, RACECRITERIARACETYPE)\n VALUES "
    salidaSQL = cabecera
    for race in races["data"]: 
        salidaSQL += "(" +     formatField(race["raceId"]) + ","
        salidaSQL +=           formatField(race["yearOfRace"]) + ","
        salidaSQL +=           formatField(race["divisionSequence"])+ ","	
        salidaSQL +=           formatField(race["horseId"]) + ","
        salidaSQL +=           formatField(race["resultFinishPos"]) + ","
        salidaSQL +=           formatField(race["status"]) + ","
        salidaSQL +=           formatField(race["ageYear"]) + ","
        salidaSQL +=           formatField(race["clothNumber"]) + ","
        salidaSQL +=           formatField(race["weightValue"]) + ","
        salidaSQL +=           formatField(race["sexType"]) + ","
        salidaSQL +=           formatField(race["jockeyId"]) + ","
        salidaSQL +=           formatField(race["trainerId"]) + ","
        salidaSQL +=           formatField(race["ownerId"]) + ","
        salidaSQL +=           formatField(race["positionFinishTime"]) + ","
        salidaSQL +=           formatField(race["bettingRatio"]) + ","
        salidaSQL +=           formatField(race["raceCriteriaRaceType"])
        salidaSQL +=           ")"

        numInserts += 1
        
        if (numInserts % commitLines != 0) and (numInserts != lastRace):
            salidaSQL += ",\n"
        
        else:
            salidaSQL += ";\nCOMMIT;\n"
            if (numInserts != lastRace):
                salidaSQL += cabecera
            
    with open(PATH_SQL + '/' + "INSERTS_" + 'racePosition' + str(numeracion) + '.sql', 'w') as RacesGeneralSQLFile:
        RacesGeneralSQLFile.write(salidaSQL)
        
    return "OK"

def JockeystoSQL(nombreFichero, nombreTabla, commitLines):
    
    numInserts = 0
    lastJockey = 0
    
    with open(PATH_CLEAN + '/' + nombreFichero + '.json', 'r') as JockeyFile:
        jockeys = json.loads(JockeyFile.read())
    
    lastJockey = len(jockeys["data"])
    cabecera = "INSERT INTO " + nombreTabla.upper() + "(ENTRYID, ENTRYTYPE, ENTRYNAME, TOTALRUN, TOTALWINS, PRE95ENTRYID) \n VALUES "
    salidaSQL = cabecera
    for jockey in jockeys["data"]: 
        salidaSQL += "(" +     formatField(jockey["entryId"]) + ","
        salidaSQL +=           formatField(jockey["entryType"]) + ","
        salidaSQL +=           formatField(jockey["entryName"])+ ","	
        salidaSQL +=           formatField(jockey["totalRun"]) + ","
        salidaSQL +=           formatField(jockey["totalWins"]) + ","
        salidaSQL +=           formatField(jockey["pre95EntryId"])
        salidaSQL +=           ")"

        numInserts += 1
        
        if (numInserts % commitLines != 0) and (numInserts != lastJockey):
            salidaSQL += ",\n"
        
        else:
            salidaSQL += ";\nCOMMIT;\n"
            if (numInserts != lastJockey):
                salidaSQL += cabecera
            
    with open(PATH_SQL + '/' + "INSERTS_jockeys.sql", 'w') as JockeysSQLFile:
        JockeysSQLFile.write(salidaSQL)
        
    return "OK"

def RacecoursestoSQL(nombreFichero, nombreTabla, commitLines):
    
    numInserts = 0
    lastRaceCourse = 0
    
    with open(PATH_CLEAN + '/' + nombreFichero + '.json', 'r') as RaceCoursesFile:
        raceCourses = json.loads(RaceCoursesFile.read())
    
    lastRaceCourse = len(raceCourses["data"])
    cabecera = "INSERT INTO " + nombreTabla.upper() + "(NAME,COURSEID,TYPE,TRACKHANDEDNESS,REGION,POSTCODE,LATITUDE,LONGITUDE,FIRSTRACE,NEXTFIXTUREDATE) \n VALUES "
    salidaSQL = cabecera
    for raceCourse in raceCourses["data"]: 
        salidaSQL += "(" +     	formatField(raceCourse["name"]) + ","
        salidaSQL +=			formatField(raceCourse["courseId"]) + ","
        salidaSQL +=			formatField(raceCourse["type"]) + ","
        salidaSQL +=			formatField(raceCourse["trackHandedness"]) + ","
        salidaSQL +=			formatField(raceCourse["region"]) + ","
        salidaSQL +=			formatField(raceCourse["postcode"]) + ","
        salidaSQL +=			formatField(raceCourse["latitude"]) + ","
        salidaSQL +=			formatField(raceCourse["longitude"]) + ","
        salidaSQL +=			formatField(raceCourse[ "firstRace"]) + ","
        salidaSQL +=			formatField(raceCourse["nextFixtureDate"])
        salidaSQL +=           ")"			

        numInserts += 1
        
        if (numInserts % commitLines != 0) and (numInserts != lastRaceCourse):
            salidaSQL += ",\n"
        
        else:
            salidaSQL += ";\nCOMMIT;\n"
            if (numInserts != lastRaceCourse):
                salidaSQL += cabecera
            
    with open(PATH_SQL + '/' + "INSERTS_racecourses.sql", 'w') as RaceCoursesSQLFile:
        RaceCoursesSQLFile.write(salidaSQL)
        
    return "OK"

def OwnerstoSQL(nombreFichero, nombreTabla, commitLines, numeracion):
    
    numInserts = 0
    lastOwner = 0
    
    with open(PATH_CLEAN + '/' + nombreFichero + '.json', 'r') as OwnersFile:
        owners = json.loads(OwnersFile.read())
    
    lastOwner = len(owners["data"])
    cabecera = "INSERT INTO " + nombreTabla.upper() + "(RANKING, OWNERNAME, OWNERID, CHAMPIONSHIPTYPE, LEADINGEARNERHORSE, TOTALOWNERCHAMPIONSHIPWINS, TOTALOWNERCHAMPIONSHIPSRUNS, TOTALOWNERPRIZEMONEYWON) \n VALUES "
    salidaSQL = cabecera
    for owner in owners["data"]: 
        salidaSQL += "(" +     	formatField(owner["rank"]) + ","
        salidaSQL +=			formatField(owner["ownerName"]) + ","
        salidaSQL +=			formatField(owner["ownerId"]) + ","
        salidaSQL +=			formatField(owner["championshipType"]) + ","
        salidaSQL +=			formatField(owner["leadingEarnerHorse"]) + ","
        salidaSQL +=			formatField(owner["totalOwnerChampionshipWins"]) + ","
        salidaSQL +=			formatField(owner["totalOwnerChampionshipsRuns"]) + ","
        salidaSQL +=			formatField(owner["totalOwnerPrizeMoneyWon"])
        salidaSQL +=           ")"		
        numInserts += 1
        
        if (numInserts % commitLines != 0) and (numInserts != lastOwner):
            salidaSQL += ",\n"
        
        else:
            salidaSQL += ";\nCOMMIT;\n"
            if (numInserts != lastOwner):
                salidaSQL += cabecera
            
    with open(PATH_SQL + '/' + "INSERTS_owners" + str(numeracion) + ".sql", 'w') as OwnersSQLFile:
        OwnersSQLFile.write(salidaSQL)
        
    return "OK"


def TrainerstoSQL(nombreFichero, nombreTabla, commitLines, numeracion):
    
    numInserts = 0
    lastTrainer = 0
    
    with open(PATH_CLEAN + '/' + nombreFichero + '.json', 'r') as TrainersFile:
        trainers = json.loads(TrainersFile.read())
    
    lastTrainer = len(trainers["data"])
    cabecera = "INSERT INTO " + nombreTabla.upper() + "(TRAINERID, TRAINERSTYLE, FULLNAME, LICENCETYPE, NUMBEROFDAYSSINCELASTWIN , COUNTY) \n VALUES "
    salidaSQL = cabecera
    for trainer in trainers["data"]: 
        salidaSQL += "(" +     	formatField(trainer["trainerId"]) + ","
        salidaSQL +=			formatField(trainer["trainerStyle"]) + ","
        salidaSQL +=			formatField(trainer["fullName"]) + ","
        salidaSQL +=			formatField(trainer["licenceType"]) + ","
        salidaSQL +=			formatField(trainer["numberOfDaysSinceLastWin"]) + ","
        salidaSQL +=			formatField(trainer["county"])
        salidaSQL +=           ")"				
        numInserts += 1
        
        if (numInserts % commitLines != 0) and (numInserts != lastTrainer):
            salidaSQL += ",\n"
        
        else:
            salidaSQL += ";\nCOMMIT;\n"
            if (numInserts != lastTrainer):
                salidaSQL += cabecera
            
    with open(PATH_SQL + '/' + "INSERTS_trainers" + str(numeracion) + ".sql", 'w') as TrainersSQLFile:
        TrainersSQLFile.write(salidaSQL)
        
    return "OK"

#AMPLIACIÓN DE INFORMACIÓN PARA AQUELLOS CABALLOS QUE TENEMOS INFORMACIÓN EXTRA <- Los updates son muy costosos, intentar evitar
def caballosRatedDetailedtoSQL(nombreFichero, nombreTabla, commitLines):
    
    numUpdates = 0
    lastHorse = 0
    salidaSQL = ""
    
    with open(PATH_EXTENDIDO + '/' + nombreFichero + '.json', 'r') as caballosRatedDetailedFile:
        caballosRatedDetail = json.loads(caballosRatedDetailedFile.read())
    
    lastHorse = caballosRatedDetail["to"] - caballosRatedDetail["from"] + 1

    for caballoRatedDetail in caballosRatedDetail["data"]:   
        salidaSQL += "UPDATE " + nombreTabla.upper() + " SET "
        salidaSQL += "name = " +          formatField(caballoRatedDetail["name"])   + ","             
        salidaSQL += "dateOfBirth = " +          formatField(caballoRatedDetail["dateOfBirth"])   + ","      
        salidaSQL += "deathDate = " +          formatField(caballoRatedDetail["deathDate"])  + ","         
        salidaSQL += "deathNote = " +          formatField(caballoRatedDetail["deathNote"])  + ","         
        salidaSQL += "age = " +          formatField(caballoRatedDetail["age"])    + ","              
        salidaSQL += "moniker = " +          formatField(caballoRatedDetail["moniker"])   + ","          
        salidaSQL += "dam = " +          formatField(caballoRatedDetail["lineage"]["dam"]["animalId"])    + ","             
        salidaSQL += "sire = " +          formatField(caballoRatedDetail["lineage"]["sire"]["animalId"])   + ","             
        salidaSQL += "sex = " +          formatField(caballoRatedDetail["sex"])   + "," 
        salidaSQL += "trainerName = " +          formatField(caballoRatedDetail["trainerName"])    + ","     
        salidaSQL += "trainerId = " +          formatField(caballoRatedDetail["trainerId"])   + ","        
        salidaSQL += "ownerName = " +          formatField(caballoRatedDetail["ownerName"]) + ","          
        salidaSQL += "ownerId = " +          formatField(caballoRatedDetail["ownerId"])    + ","         
        salidaSQL += "ratingAWT = " +          formatField(caballoRatedDetail["ratingAWT"])   + ","        
        salidaSQL += "ratingChase = " +          formatField(caballoRatedDetail["ratingChase"])  + ","       
        salidaSQL += "ratingFlat = " +          formatField(caballoRatedDetail["ratingFlat"])    + ","      
        salidaSQL += "ratingHurdle = " +          formatField(caballoRatedDetail["ratingHurdle"])   + ","     
        salidaSQL += "nameWithNoCountry = " +          formatField(caballoRatedDetail["nameWithNoCountry"]) + ","  
        salidaSQL += "performanceHistory = " +          formatField(caballoRatedDetail["performanceHistory"]) + ","  
        salidaSQL += "damsire = " +          formatField(caballoRatedDetail["lineage"]["damsire"]["animalId"]) + " "
        salidaSQL += "WHERE " + "ID = " + formatField(caballoRatedDetail["id"]) + ";\n"

        numUpdates += 1
        
        if (numUpdates % commitLines == 0) or (numUpdates == lastHorse):
            salidaSQL += "\nCOMMIT;\n"

            
    with open(PATH_SQL + '/' + "UPDATES_" + nombreFichero + '.sql', 'w') as caballosRatedDetailedFile:
        caballosRatedDetailedFile.write(salidaSQL)
        
    return "OK"

def caballostoSQLAll(nombreFichero, inicio, final):
    for numFich in range(inicio, final + 1):
        caballostoSQL(nombreFichero + str(numFich), "horses", 500)
        
def caballosRatedDetailedtoSQLAll(nombreFichero, inicio, final):
    for numFich in range(inicio, final + 1):
        #print(nombreFichero + str(numFich))
        caballosRatedDetailedtoSQL(nombreFichero + str(numFich), "horses", 500)


#UNIFICADOR DE FICHEROS SQL        
def uneFicherosInsert(nombreFichero, inicio, final):   
    with open(PATH_SQL + '/' + nombreFichero + '_' + str(inicio) + '_' + str(final) + '_Global.sql', 'a') as ficheroGlobal:
        for numFich in range(inicio, final + 1):
            comentario = "\n\n\n############### INICIO DE FICHERO " + nombreFichero + str(numFich) + " ###############\n\n"
            ficheroGlobal.write(comentario)
            with open(PATH_SQL + '/' + nombreFichero + str(numFich) + '.sql', 'r') as ficheroPart:
                ficheroGlobal.write(ficheroPart.read())
                

# RacesGeneraltoSQL("raceResults20211_detailed_1_5_general", "races",500, 1)
# RacesGeneraltoSQL("raceResults20211_detailed_6_10_general", "races",500, 2)
# RacesGeneraltoSQL("raceResults20211_detailed_11_15_general", "races",500, 3)
# RacesGeneraltoSQL("raceResults20221_detailed_1_2_general", "races",500, 4)
# RacesGeneraltoSQL("raceResults20221_detailed_3_5_general", "races",500, 5)
# RacesGeneraltoSQL("raceResults20221_detailed_6_10_general", "races",500, 6)
# RacesGeneraltoSQL("raceResults20221_detailed_11_15_general", "races",500, 7)

# RacePositionstoSQL("raceResults20211_detailed_1_5_positions_B", "raceresults",500, 1)
# RacePositionstoSQL("raceResults20211_detailed_6_10_positions_B", "raceresults",500, 2)
# RacePositionstoSQL("raceResults20211_detailed_11_15_positions_B", "raceresults",500, 3)
# RacePositionstoSQL("raceResults20221_detailed_1_2_positions_B", "raceresults",500, 4)
# RacePositionstoSQL("raceResults20221_detailed_3_5_positions_B", "raceresults",500, 5)
# RacePositionstoSQL("raceResults20221_detailed_6_10_positions_B", "raceresults",500, 6)
# RacePositionstoSQL("raceResults20221_detailed_11_15_positions_B", "raceresults",500, 7)
# uneFicherosInsert("INSERTS_racePosition",1,7)

# TrainerstoSQL("trainers1", "trainers", 100, 1)
# TrainerstoSQL("trainers2", "trainers", 100, 2)
# TrainerstoSQL("trainers3", "trainers", 100, 3)
# uneFicherosInsert("INSERTS_trainers",1,3)      