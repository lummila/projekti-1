'''
#############################
LÄTINÄÄ

-MAAT-
Ensimmäisen kierroksen lentokentät (maiden nimet ja ICAO-koodit):
Ruotsi(ESSA), Norja(ENGM), Latvia(EVRA), Tanska(EKCH), Liettua(EYVI)

Toisen kierroksen lentokentät:
Puola(EPWA), Saksa(EDDB), Alankomaat(EHAM), Slovakia(LZIB), Tsekki(LKPR)

Kolmannen kierroksen lentokentät:
Itävalta(LOWW), Unkari(LHBP), Belgia(EBBR), Serbia(LYBE), Kroatia(LDZA)

Neljännen kierroksen lentokentät:
Sveitsi(LSZH), Italia(LIRN), Ranska(LFPO), UK(EGLL), Irlanti(EIDW)

Viides kierros eli maalimaat:
Espanja(LEBL), Portugali(LPPT), Tenerife(GCTS), Fuerteventura(GCFV), Gran Canaria(GCLP)

-MEKANIIKAT-

- Pelaajalla on n kierrosta aikaa päästä viidennen tason maahan, jossa rotta on
- Pelaajalla on x määrä valuuttaa pelin alussa

'''

# JIIIIHAAAA

from geopy import distance
import math
import random
import mysql.connector

# Jokaisen pelin maan ICAO-koodit. Numeropari on se, millä näitä kutsutaan, ja teksti on se, mikä palautuu.
DEST_ICAO = {
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

DEST_TIPS = {
    # Ruotsi (HUOM Eka kiekka)
    11: "Finland's beloved enemy, especially in hockey.",
    12: "I've heard they have a lot of crude oil and beautiful mountain lines!",  # Norja
    13: "The southern neighbor of Finland's southern neighbor...",  # Latvia
    14: "They're the source of lego's and everyone rides a bicycle!",  # Tanska
    15: "At least a third of the country is covered with forest and it has an official scent.",  # Liettua
    21: "The birthplace of vodka!",  # Puola (HUOM Toka kierros)
    22: "The promised land of beer and sausage!",  # Saksa
    23: "If I get lucky, I might find time to visit a coffee shop or the red light district.",  # Alankomaat
    24: "Young students are able to travel there by train with no extra cost.",  # Slovakia
    25: "I've heard they're very good in hockey and they have the most castles in all of Europe.",  # Tsekki
    # Itävalta (HUOM Kolmas kierros)
    31: "The home country of a famous action star.",
    32: "The beloved language related to Finnish! The president is not too interested in democracy.",  # Unkari
    33: "Is there anything better than a serving of waffles and some delicious chocolate!",  # Belgia
    34: "The home country of the famous Tesla, not the car...",  # Serbia
    35: "Unfortunately this country doesn't let Bosnian people have a swim.",  # Kroatia
    # Sveitsi (HUOM Neljäs kierros)
    41: "I might buy a watch made by a famous brand! This could be a setback to my budget.",
    42: "Ordering pineapple on your food in a restaurant might get you banished.",  # Italia
    43: "Weird food and romantic sights! The president has something in common with a known pastry.",  # Ranska
    44: "Does this island have anything besides football?",  # UK
    45: "Catch the small green creature and acquire unfathomable riches! Don't forget Guinness!",  # Irlanti
    # Espanja (HUOM Viides kierros)
    51: "The promised land of bullfights and delicious food!",
    52: "The country of amazing wine. The people might sound like drunk Spaniards.",  # Portugali
    53: "The largest one of the Spanish islands on the coast of Western Africa.",  # Tenerife
    54: "Easternmost one of the Spanish islands on the coast of western Africa.",  # Fuerteventure
    55: "The dream island location of elderly Finnish pensioners on the coast of Western Africa.",  # Gran Canaria
}


# Rotan satunnaisesti päätetty reitti tasojen läpi
def rottaDestinations():
    output = []
    for level in range(1, 6):  # 1-5
        rand = random.randint(1, 5)
        # Esim. 2 + 20 = 22, eli EDDB, Saksa
        output.append(rand + (level * 10))
    return output  # Lista, jossa yksi koodi joka tason maalle, viimeinen on maali


# Palauttaa CO^2 kiloina rotan matkan päästöt = optimaalinen määrä mihin pelaajaa verrataan
def rottaEmissions(rottaList):
    total = 0
    for entry in range(len(rottaList) - 1):
        # Tehdään funktiossa etäisyyden mittaus jokaisen rotan matkan perusteella. -1 sen takia, että [entry + 1] tuottaisi virheen, koska mennään listan ulkopuolelle.
        coords = sqlCoordinateQuery(
            DEST_ICAO[rottaList[entry]], DEST_ICAO[rottaList[entry + 1]])
        # Käytetään checkForDistia, ja syötetään true argumentiksi, jotta tulos saadaan emissiomääränä
        grams = checkForDist(coords, True)
        total += grams
    return total / 1000  # Total on grammoina, jaetaan tonnilla, ja saadaan kiloina ulos


# Tekee SQL-haun ja palauttaa tuplen, jossa osoitin ja haun tulokset. Parametrinä sql-koodi. Lyhentää koodeja, joissa tehdään SQL-hakuja
def sql_execute(code):
    pointer = connection.cursor()
    pointer.execute(code)
    result = pointer.fetchall()

    return (pointer, result)


# SQL-haku kahdella ICAO-tunnuksella, palauttaa listan, jossa kaksi tuplea, joissa koordinaatit.
def sqlCoordinateQuery(start, dest):
    locationList = []

    # Kaksi eri hakua, aloitusmaan ja päämäärän etäisyyden selvittämiseksi.
    for x in range(2):
        sql = "select longitude_deg, latitude_deg from airport "
        # Jos x on 0, kyseessä on ensimmäinen haku, eli käytetään start-muuttujaa, ja toisella kerralla dest-muuttujaa.
        sql += f"where ident = '{start if x == 0 else dest}';"

        # Erotetaan sqlPointerin osoitin ja tulokset käyttöä varten
        (pointer, result) = sql_execute(sql)

        if pointer.rowcount <= 0:
            print("Jokin meni vikaan, tarkista lähtökenttäsi ja kohteesi.")
            return -1
        else:
            # Lisätään locationList-listaan tuple, jossa koordinaatit
            locationList.append(result[0])
    # Palauttaa listan, jossa kahdet koordinaatit tuplemuodossa
    return locationList


# Ottaa parametriksi ICAO-koodin, jonka avulla etsii tietokannasta oikean maan nimen.
def sqlCountryQuery(icao):
    sql = "select country.name from country "
    sql += "where country.iso_country in ("  # Fancy sulkuhaku
    sql += "select airport.iso_country from airport "
    sql += f"where ident = '{icao}');"

    # Erotetaan sqlPointerin osoitin ja tulokset käyttöä varten
    (pointer, result) = sql_execute(sql)

    if pointer.rowcount <= 0:  # Ei tuloksia
        print("Jokin meni vikaan, tarkista syötetty ICAO-koodi.")
        return -1
    else:
        # result on lista, jossa on tuple, jonka ensimmäinen elementti on haettu maan nimi.
        # result = [(Finland,)] / result[0] = (Finland,) / result[0][0] = Finland
        return result[0][0]


# Ottaa argumentiksi listan, jossa kaksi tuplea koordinaateilla (minkä sqlCoordinateQuery palauttaa) ja booleanin, joka indikoi, palauttaako funktio kilometrit vai päästöt grammoina
def checkForDist(locs, emissions: bool):
    output = distance.distance(locs[0], locs[1]).km
    # "Ternary operator" eli if else -toteamus yhdellä rivillä. Jos emissions on False, palauta output, jos True, palauta output * 115 (päästöt grammoina)
    return output if not emissions else output * 115


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
print(rottaEmissions(testi))
print(sqlCountryQuery(DEST_ICAO[12]))
