import sqlite3

f = open('crime.db','a')
f.close()
conn = sqlite3.connect('crime.db')
cursor = conn.cursor()
crime = """CREATE TABLE "Crimes" (\
	"Id"	TEXT NOT NULL UNIQUE,\
	"Type"	TEXT NOT NULL,\
	"Dates"	TEXT NOT NULL,\
	"Year"  TEXT NOT NULL,
	"Month" TEXT NOT NULL,
	"Day"   TEXT NOT NULL, 
	"Hour"	TEXT NOT NULL,\
	"Address"	TEXT NOT NULL,\
	"Link"	TEXT NOT NULL,\
	PRIMARY KEY("Id")\
);"""
daily = """CREATE TABLE "DailyStats" (
	"Dates"	TEXT NOT NULL UNIQUE,
	"Vandalism"	INTEGER NOT NULL,
	"Assault"	INTEGER NOT NULL,
	"Burglary"	INTEGER NOT NULL,
	"Robbery"	INTEGER NOT NULL,
	"Theft"	INTEGER NOT NULL,
	"Other"	INTEGER NOT NULL,
	"Arrest"	INTEGER NOT NULL,
	"Shooting"	INTEGER NOT NULL,
	PRIMARY KEY("Dates"),
	FOREIGN KEY("Dates") REFERENCES "Crimes"("Dates")
);"""
cursor.execute(crime)
cursor.execute(daily)

