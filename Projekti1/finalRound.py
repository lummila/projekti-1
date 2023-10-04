import random
import math
import copy
from geopy import distance
import mysql.connector

DEST_ICAO = {
    1: "EFHK",  # Helsinki
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


def generate_rotta():
    # ROTAN KOHTEET
    output = [1]
    for level in range(1, 6):  # 1-5
        rand = random.randint(1, 5)
        # Esim. 2 + 20 = 22, eli EDDB, Saksa
        output.append(rand + (level * 10))

        # ROTAN PÄÄSTÖT
        totalGrams = 0
        for entry in range(len(output) - 1):
            # Tehdään funktiossa etäisyyden mittaus jokaisen rotan matkan perusteella. -1 sen takia, että [entry + 1]
            # tuottaisi virheen, koska mennään listan ulkopuolelle.
            coords = sqlCoordinateQuery(
                DEST_ICAO[output[entry]], DEST_ICAO[output[entry + 1]]
            )
            # Käytetään checkForDistia, ja syötetään true argumentiksi, jotta tulos saadaan emissiomääränä
            totalGrams += checkForDist(coords, True)

        # ROTAN MATKOJEN HINTA
        totaldistance = 0
        # print("Rottalist: {}".format(output))
        # print("Rottalist[0]: {}".format(output[0]))
        for i in range(len(output) - 1):
            # Tehdään funktiossa etäisyyden mittaus jokaisen rotan matkan perusteella. -1 sen takia, että [entry + 1] tuottaisi virheen, koska mennään listan ulkopuolelle.
            coords = sqlCoordinateQuery(
                DEST_ICAO[output[i]], DEST_ICAO[output[i + 1]]
            )
            # print(DEST_ICAO[output[i]], DEST_ICAO[output[i + 1]])
            distance_for_one_trip = float(
                distance.distance(coords[0], coords[1]).km)
            totaldistance += distance_for_one_trip
            # print(totaldistance)
        totalPrice = (len(output) - 1) * 100
        totalPrice += totaldistance / 10

    # Lista, jossa yksi koodi joka tason maalle, viimeinen on maali
    return (output, math.floor(totalGrams), math.floor(totalPrice))

# Suvi:Pelin alkutilannefunktio. Sijainti sama kuin Rotalla aluksi. Massi 1000 e, emissiot 0, Kierros.
# Tämän funktion täytyy myös pyöräyttää rotan tiedot, jotta alkupaikka on tiedossa. Niinpä funktio pyöräyttelee myös rottafunktiot.
def game_start():
    # Destinations = [], emissions = int, trip_price = int
    (destinations, emissions, trip_price) = generate_rotta()

    # Esim: [11, 22, 33, 44, 51], vastaavat ICAO-koodeja flygarilistalla
    rottagame = {
        "destinations": destinations,  # Lista
        "price": trip_price,
        "emissions": emissions,
        "rounds": 5,
    }
    player_create = {
        "location": "EFHK",
        "money": 1000,
        "emissions": 0,
        "round": 0
    }

    return (rottagame, player_create)

def sqlCountryQuery(icao):
    sql = "select country.name from country "
    sql += "where country.iso_country in ("  # Fancy sulkuhaku
    sql += "select airport.iso_country from airport "
    sql += f"where ident = '{icao}');"

    # Erotetaan sqlPointerin osoitin ja tulokset käyttöä varten
    pointer = connection.cursor()
    pointer.execute(sql)
    result = pointer.fetchall()

    if pointer.rowcount <= 0:  # Ei tuloksia
        print("Jokin meni vikaan, tarkista syötetty ICAO-koodi.")
        return -1
    else:
        # result on lista, jossa on tuple, jonka ensimmäinen elementti on haettu maan nimi.
        # result = [(Finland,)] / result[0] = (Finland,) / result[0][0] = Finland
        return result[0][0]


def sqlCoordinateQuery(start, dest):
    locationList = []
    pointer = connection.cursor()

    # Kaksi eri hakua, aloitusmaan ja päämäärän etäisyyden selvittämiseksi.
    for x in range(2):
        sql = "select longitude_deg, latitude_deg from airport "
        # Jos x on 0, kyseessä on ensimmäinen haku, eli käytetään start-muuttujaa, ja toisella kerralla dest-muuttujaa.
        sql += f"where ident = '{start if x == 0 else dest}';"

        # SQL:n käyttö
        pointer.reset()
        pointer.execute(sql)
        result = pointer.fetchall()

        if pointer.rowcount <= 0:
            print("Jokin meni vikaan, tarkista lähtökenttäsi ja kohteesi.")
            return -1
        else:
            # Lisätään locationList-listaan tuple, jossa koordinaatit
            locationList.append(result[0])
    # Palauttaa listan, jossa kahdet koordinaatit tuplemuodossa
    return locationList


# Ottaa argumentiksi listan, jossa kaksi tuplea koordinaateilla (minkä sqlCoordinateQuery palauttaa) ja booleanin, joka indikoi, palauttaako funktio kilometrit vai päästöt grammoina
def checkForDist(locs, emissions: bool):
    output = distance.distance(locs[0], locs[1]).km
    # "Ternary operator" eli if else -toteamus yhdellä rivillä. Jos emissions on False, palauta output, jos True, palauta output * 115 (päästöt grammoina)
    return output if not emissions else output * 115

def status():
    return print(
        f"Current location: {sqlCountryQuery(pelaaja['location'])}\t"
        f"Current money: {pelaaja['money']}\t"
        f"Current round (out of 10): {pelaaja['round']}")

# Suvi: viimeisen pelin funktiot.
# After reaching the goal the game will calculate your final points by summing up
# how many rounds you used and your emissions
# Will print out how much money is left and how much are the emissions
def finalRound(gamestats, rottagame):
    if (gamestats[0][len(gamestats[0])-1] == rottagame[0][5]) and len(gamestats[0]) <9:
        print(f"You win! Your emissions were {gamestats[1]} grams and you have money left {gamestats[2]} euros.")

    else:
        print(f"You lost! Your emissions were {gamestats[1]} grams and you have money left {gamestats[2]} euros.")


# SQL-yhteyden luominen tietokannan käyttöä varten
connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    database="flight_game",
    user="suvi",
    password="HarmaaPoyta123",
    autocommit=True,
)


generoiturotta= generate_rotta()
generoiturotta2=([1, 11, 25, 35, 45, 38, 50, 39, 80, 40, 52], 764554, 1164)
generoiturotta[0][5] = generoiturotta2[0][len(generoiturotta2[0])-1]
muuttuja = [generoiturotta[0][5]]

print(f"generoiturotta: {generoiturotta}")
print(f"generoiturotta2 {generoiturotta2}")
print(generoiturotta[0][5])
print(generoiturotta2[0][len(generoiturotta2[0])-1])
finalRound(generoiturotta2, generoiturotta)
print("hello")
