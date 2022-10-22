SELECT fixturetype, count(*) FROM winninghorse.races group by fixturetype;
SELECT animaltype, count(*) FROM winninghorse.races group by animaltype;
SELECT agelimit, count(*) FROM winninghorse.races group by agelimit;
SELECT RACECRITERIAMINIMUMWEIGHT, count(*) FROM winninghorse.races group by RACECRITERIAMINIMUMWEIGHT;
SELECT RACECRITERIAWEIGHTSRAISED, count(*) FROM winninghorse.races group by RACECRITERIAWEIGHTSRAISED;

select * from races;

select year, raceid, divisionsequence, count(*) as total from races group by year, raceid, divisionsequence order by total desc;

select rr.year, h.NAMEWITHNOCOUNTRY, r.fixtureType, rr.ageyear, j.ENTRYNAME, rr.bettingratio, count(*) as total
from raceresults rr, horses h, jockeys j, races r
where resultfinishpos = 1
and rr.horseid = h.id
and rr.JOCKEYID = j.ENTRYID
and r.RACEID = rr.RACEID
and r.DIVISIONSEQUENCE = rr.DIVISIONSEQUENCE
group by rr.year, h.NAMEWITHNOCOUNTRY, r.fixtureType, rr.ageyear, j.ENTRYNAME, rr.bettingratio
order by year desc, total desc;

select id from horses;

select * from owners;

select rc.name , sum(r.prizeamount) premio from races r, racecourses rc
where r.COURSEID = rc.COURSEID
group by rc.name
order by premio desc;

select * from racecourses order by courseid;

