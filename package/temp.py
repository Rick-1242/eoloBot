import sqlite3

db = sqlite3.connect("../db/wether.db")


def convert(lat, lon):
    latDEG = int(lat[0:2])
    latFST = int(lat[3:5])
    latSEC = int(lat[6:8])
    latDECIMAL = latDEG + (latFST/60) + (latSEC/3600)
    
    lonDEG = int(lon[0:2])
    lonFST = int(lon[3:5])
    lonSEC = int(lon[6:8])
    lonDECIMAL = lonDEG + (lonFST/60) + (lonSEC/3600)
    return latDECIMAL,lonDECIMAL

try:
    cursor = db.cursor()
    querry = """SELECT CoordinateStazioni.Latitude, CoordinateStazioni.Longitude 
                FROM CoordinateStazioni
            """
    cursor.execute(querry)
    record = cursor.fetchall()
    for i in record:
        convert(str(i[0]).replace('"', ''), str(i[1]).replace('"', ''))

except sqlite3.Error as sqlerror:
    print("Error while connecting to sqlite", sqlerror)
db.close()
