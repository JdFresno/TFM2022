create table races
(YEAR int, 
FIXTUREID int, 
RACEID int,
DIVISIONSEQUENCE int, 
COURSEID int, 
FIXTURETYPE varchar(255), 
COURSEKEY int, 
RACEDATE date, 
RACETIME time, 
DISTANCEVALUE int, 
SEXLIMIT varchar(255), 
ANIMALTYPE varchar(255), 
PRIZEAMOUNT int, 
AGELIMIT varchar(255), 
RACECRITERIARACETYPE varchar(255), 
RACECRITERIAMINIMUMWEIGHT int, 
RACECRITERIAWEIGHTSRAISED int);

create table raceresults 
(RACEID int, 
YEAR int, 
DIVISIONSEQUENCE int,
HORSEID int,
RESULTFINISHPOS varchar(2), 
STATUS varchar(255), 
AGEYEAR int, 
CLOTHNUMBER int, 
WEIGHTVALUE int, 
SEXTYPE varchar(255), 
JOCKEYID int, 
TRAINERID int, 
OWNERID int, 
POSITIONFINISHTIME float, 
BETTINGRATIO varchar(255), 
RACECRITERIARACETYPE varchar(255));

create table jockeys
(
    ENTRYID int,
    ENTRYTYPE varchar(255),
    ENTRYNAME varchar(255),
    TOTALRUN int,
    TOTALWINS int,
    PRE95ENTRYID int
);

create table racecourses
(
NAME VARCHAR(255),
COURSEID INT,
TYPE VARCHAR(255),
TRACKHANDEDNESS VARCHAR(255),
REGION VARCHAR(255),
POSTCODE VARCHAR(255),
LATITUDE VARCHAR(255),
LONGITUDE VARCHAR(255),
FIRSTRACE VARCHAR(255),
NEXTFIXTUREDATE VARCHAR(255)
);

create table owners
(
RANKING int,
OWNERNAME varchar(255),
OWNERID int,
CHAMPIONSHIPTYPE varchar(255),
LEADINGEARNERHORSE varchar(255),
TOTALOWNERCHAMPIONSHIPWINS int,
TOTALOWNERCHAMPIONSHIPSRUNS int,
TOTALOWNERPRIZEMONEYWON varchar(255)
);

select races.* from races, 
(select year, raceid, divisionsequence, count(*) as total from races group by year, raceid, divisionsequence) as consulta
where 
races.year = consulta.year
and races.raceid = consulta.raceid
order by races.year, races.fixtureid, races.raceid;