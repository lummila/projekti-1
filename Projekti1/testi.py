import mysql.connector
import random
import math
from geopy import distance

'''
#############################
LÄTINÄÄ

Ensimmäisen kierroksen mahdolliset lentokentät (maiden nimet ja ICAO-koodit):
Ruotsi(ESSA), Norja(ENGM), Latvia(EVRA), Tanska(EKCH), Liettua(EYVI)

Toisen kierroksen mahdolliset lentokentät:
Puola(EPWA), Saksa(EDDB), Alankomaat(EHAM), Slovakia(LZIB), Tsekki(LKPR)

Kolmannen kierroksen mahdolliset lentokentät:
Itävalta(LOWW), Unkari(HU), Belgia(EBBR), Serbia(LYBE), Kroatia(LDZA)

Neljännen kierroksen mahdolliset lentokentät:
Sveitsi(CH), Italia(LIRN), Ranska(LFPO), UK(EGLL), Irlanti(EIDW)

Viides kierros eli maalimaat:
Espanja(LEBL), Portugali(LPPT), Tenerife(GCTS), Fuerteventura(GCFV), Gran Canaria(GCLP)

'''


# SQL-haku kahdella ICAO-tunnuksella, palauttaa listan, jossa kaksi tuplea, joissa koordinaatit
def sqlDistanceQuery(start, dest):
    locationList = []

    for x in range(2):
        sql = "select longitude_deg, latitude_deg from airport "
        if x == 0:
            sql += f"where ident = '{start}';"
        else:
            sql += f"where ident = '{dest}';"

        pointer = connection.cursor()
        pointer.execute(sql)
        result = pointer.fetchall()

        if pointer.rowcount <= 0:
            print("Jokin meni vikaan, tarkista lähtökenttäsi ja kohteesi.")
            return -1
        else:
            locationList.append(result[0])

    return locationList


# Ottaa argumentiksi listan, jossa kaksi tuplea koordinaateilla (minkä sqlDistanceQuery palauttaa)
def checkForDist(locs):
    return distance.distance(locs[0], locs[1]).km


# SQL-yhteyden luominen tietokannan käyttöä varten
connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    database="flight_game",
    user="root",
    password="metropolia",
    autocommit=True
)

testi = sqlDistanceQuery("EFHK", "EGLL")
# print(testi)
matka = checkForDist(testi)
print(f"Etäisyys: {matka:0.3f} kilometriä.")
