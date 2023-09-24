'''
#############################
LÄTINÄÄ

-MAAT-
Ensimmäisen kierroksen mahdolliset lentokentät (maiden nimet ja ICAO-koodit):
Ruotsi(ESSA), Norja(ENGM), Latvia(EVRA), Tanska(EKCH), Liettua(EYVI)

Toisen kierroksen mahdolliset lentokentät:
Puola(EPWA), Saksa(EDDB), Alankomaat(EHAM), Slovakia(LZIB), Tsekki(LKPR)

Kolmannen kierroksen mahdolliset lentokentät:
Itävalta(LOWW), Unkari(LHBP), Belgia(EBBR), Serbia(LYBE), Kroatia(LDZA)

Neljännen kierroksen mahdolliset lentokentät:
Sveitsi(LSZH), Italia(LIRN), Ranska(LFPO), UK(EGLL), Irlanti(EIDW)

Viides kierros eli maalimaat:
Espanja(LEBL), Portugali(LPPT), Tenerife(GCTS), Fuerteventura(GCFV), Gran Canaria(GCLP)

-MEKANIIKAT-



'''

from geopy import distance
import math
import random
import mysql.connector

DESTINATION_ICAO = {
    11: "ESSA",  # Ruotsi (HUOM Eka kiekka)
    12: "ENGM",  # Norja
    13: "EVRA",  # Latvia
    14: "EKCH",  # Tanska
    15: "EYVI",  # Liettua
    21: "EPWA",  # Puola (HUOM Toka kierros)
    22: "EDDB",  # Saksa
    23: "EHAM",  # Alankomaat
    24: "LZIB",  # Slovakia
    25: "LKPR",  # Tsekki
    31: "LOWW",  # Itävalta (HUOM Kolmas kierros)
    32: "LHBP",  # Unkari
    33: "EBBR",  # Belgia
    34: "LYBE",  # Serbia
    35: "LDZA",  # Kroatia
    41: "LSZH",  # Sveitsi (HUOM Neljäs kierros)
    42: "LIRN",  # Italia
    43: "LFPO",  # Ranska
    44: "EGLL",  # UK
    45: "EIDW",  # Irlanti
    51: "LEBL",  # Espanja (HUOM Viides kierros)
    52: "LPPT",  # Portugali
    53: "GCTS",  # Tenerife
    54: "GCFV",  # Fuerteventure
    55: "GCLP",  # Gran Canaria
}

DESTINATION_TIPS = {
    # Ruotsi (HUOM Eka kiekka)
    11: "Rakas vihollismaamme, varsinkin jääkiekossa.",
    12: "Siellä on kuulemma todella paljon vuoristoja ja öljyä.",  # Norja
    13: "Se etelänaapurimme etelänaapuri.",  # Latvia
    14: "Sieltä tulee ainakin Legoja, ja kaikki ajavat pyörällä.",  # Tanska
    15: "Siellä ainakin kolmasosa koko maasta on metsää, ja sillä on virallinen tuoksu.",  # Liettua
    21: "Se on vodkan kotimaa.",  # Puola (HUOM Toka kierros)
    22: "Kaljan ja makkaran luvattu maa.",  # Saksa
    23: "Jos hyvä tuuri käy, ehdin käydä kahvilassa tai punaisten lyhtyjen kadulla.",  # Alankomaat
    24: "Nuoret opiskelijat voivat matkustaa ilmaiseksi junalla siellä.",  # Slovakia
    25: "Olen kuullut, että se on todella hyvä jääkiekossa, "
    "ja siellä on eniten linnoja Euroopassa!",  # Tsekki
    31: "lorem",  # Itävalta (HUOM Kolmas kierros)
    32: "lorem",  # Unkari
    33: "lorem",  # Belgia
    34: "lorem",  # Serbia
    35: "lorem",  # Kroatia
    41: "lorem",  # Sveitsi (HUOM Neljäs kierros)
    42: "lorem",  # Italia
    43: "lorem",  # Ranska
    44: "lorem",  # UK
    45: "lorem",  # Irlanti
    51: "lorem",  # Espanja (HUOM Viides kierros)
    52: "lorem",  # Portugali
    53: "lorem",  # Tenerife
    54: "lorem",  # Fuerteventure
    55: "lorem",  # Gran Canaria
}


# Rotan reitti tasojen läpi
def rottaDestinations():
    output = []
    for level in range(1, 6):
        rand = random.randint(1, 5)
        # Esim. 2 + 20 = 22, eli EDDB, Saksa
        output.append(rand + (level * 10))
    return output


# Palauttaa CO^2 kiloina rotan matkan päästöt = optimaalinen määrä mihin pelaajaa verrataan
def rottaEmissions(rottaList):
    total = 0
    for entry in range(len(rottaList) - 1):
        coords = sqlDistanceQuery(
            DESTINATION_ICAO[rottaList[entry]], DESTINATION_ICAO[rottaList[entry + 1]])
        grams = checkForDist(coords, True)
        total += grams
    return total / 1000


# Tekee SQL-haun ja palauttaa tuplen, jossa osoitin ja haun tulokset. Parametrinä sql-koodi.
def sqlPointer(code):
    pointer = connection.cursor()
    pointer.execute(code)
    result = pointer.fetchall()

    return (pointer, result)


# SQL-haku kahdella ICAO-tunnuksella, palauttaa listan, jossa kaksi tuplea, joissa koordinaatit
def sqlDistanceQuery(start, dest):
    locationList = []

    for x in range(2):
        sql = "select longitude_deg, latitude_deg from airport "
        if x == 0:
            sql += f"where ident = '{start}';"
        else:
            sql += f"where ident = '{dest}';"

        # Erotetaan sqlPointerin osoitin ja tulokset käyttöä varten
        (pointer, result) = sqlPointer(sql)

        if pointer.rowcount <= 0:
            print("Jokin meni vikaan, tarkista lähtökenttäsi ja kohteesi.")
            return -1
        else:
            locationList.append(result[0])

    return locationList


def sqlCountryQuery(icao):
    sql = "select country.name from country "
    sql += "where country.iso_country in ("
    sql += "select airport.iso_country from airport "
    sql += f"where ident = '{icao}');"

    (pointer, result) = sqlPointer(sql)

    if pointer.rowcount <= 0:
        print("Jokin meni vikaan, tarkista syötetty ICAO-koodi.")
        return -1
    else:
        # result on lista, jossa on tuple, jonka ensimmäinen elementti on haettu maan nimi.
        # result = [(Suomi,)] / result[0] = (Suomi,) / result[0][0] = Suomi
        return result[0][0]


# Ottaa argumentiksi listan, jossa kaksi tuplea koordinaateilla (minkä sqlDistanceQuery palauttaa) ja booleanin, joka indikoi, palauttaako funktio kilometrit vai päästöt grammoina
def checkForDist(locs, emissions: bool):
    output = distance.distance(locs[0], locs[1]).km
    # "Ternary operator" eli if else -toteamus yhdellä rivillä. Jos emissions on False, palauta output, jos True, palauta output * 115 (päästöt grammoina)
    return output if not emissions else output * 115


# Palauttaa CO^2 g / km integraalina
def emissions(locs):
    return checkForDist(locs) * 115


# SQL-yhteyden luominen tietokannan käyttöä varten
connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    database="flight_game",
    user="root",
    password="metropolia",
    autocommit=True
)

testi = rottaDestinations()
print(testi)
print(f"{rottaEmissions(testi):.2f} kiloa päästöjä.")
print(sqlCountryQuery(DESTINATION_ICAO[11]))
