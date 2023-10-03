"""
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

"""

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
    11: "Our beloved enemy, especially in hockey.",
    12: "I've heard they have a lot of crude oil and beautiful mountain lines!",  # Norja
    13: "The southern neighbor of our southern neighbor...",  # Latvia
    14: "They're the source of lego's and everyone rides a bicycle!",  # Tanska
    15: "At least a third of the country is covered with forest and it has an official scent.",  # Liettua
    21: "The birthplace of vodka!",  # Puola (HUOM Toka kierros)
    22: "The promised land of beer and sausage!",  # Saksa
    23: "If I get lucky, I might find time to visit a coffee shop or the red light district.",  # Alankomaat
    24: "Young students are able to travel there by train with no extra cost.",  # Slovakia
    25: "I've heard they're very good in hockey and they have the most castles in all of Europe.",  # Tsekki
    # Itävalta (HUOM Kolmas kierros)
    31: "The home country of a famous action star and a not so beloved dictator.",
    32: "The beloved language related to Finnish! The president is not too interested in democracy",  # Unkari
    33: "Is there anything better than a serving of waffles and some delicious chocolate!",  # Belgia
    34: "The home country of the famous Tesla, not the car...",  # Serbia
    35: "Unfortunately this country doesn't let Bosnian people have a swim.",  # Kroatia
    # Sveitsi (HUOM Neljäs kierros)
    41: "I might buy a watch made by a famous brand! This could be a setback to my budget.",
    42: "Ordering pineapple on your food in a restaurant... people have been killed for less.",  # Italia
    43: "Weird food and romantic sights! The president has something in common with a known pastry",  # Ranska
    44: "Does this island have anything besides football?",  # UK
    45: "Catch the small green creature and acquire unfathomable riches! Don't forget Guinness!'",  # Irlanti
    # Espanja (HUOM Viides kierros)
    51: "The promised land of bullfights and delicious food!",
    52: "The country of amazing wine. The people might sound like drunk Spaniards.",  # Portugali
    53: "The largest one of the Spanish islands on the coast of Western Africa",  # Tenerife
    54: "Easternmost one of the Spanish islands on the coast of western Africa.",  # Fuerteventure
    55: "The dream island location of elderly Finnish pensioners on the coast of Western Africa.",  # Gran Canaria
}


# Suvi:Pelin alkutilannefunktio. Sijainti sama kuin Rotalla aluksi. Massi 1000 e, emissiot 0, Kierros.
# Tämän funktion täytyy myös pyöräyttää rotan tiedot, jotta alkupaikka on tiedossa. Niinpä funktio pyöräyttelee myös rottafunktiot.
def gameStart():
    # Esim: [11, 22, 33, 44, 51], vastaavat ICAO-koodeja flygarilistalla
    rottadestinations = generate_rottaDestinations()
    rottagame = {
        "rotta_destinationslist": rottadestinations,  # Lista
        "rotta_price": rottaPrice(rottadestinations),
        "rotta_emissions": rottaEmissions(rottadestinations),
        "rotta_rounds": 5,
    }
    gamestart_state = {
        "first_destination": rottadestinations[0],
        "money": 1000,
        "emissions": 0,
    }
    start_country = sqlCountryQuery(
        DEST_ICAO[gamestart_state["first_destination"]])
    start_money = gamestart_state["money"]
    start_emissions = gamestart_state["emissions"]
    print(
        f"Welcome to the game. You will start from {start_country}. You have {start_money} euros to start with. Your emissions are {start_emissions}."
    )
    return rottagame, gamestart_state


# feikkistatsit pelin finalRoundin testausta varten
def fakeFinalGame(rottagame):
    fakedestinations = generate_rottaDestinations()
    print(fakedestinations)
    fakedestinations[0] = rottagame["rotta_destinationslist"][0]
    print(fakedestinations)
    fakegame = {
        "fake_destinationslist": fakedestinations,
        "fake_price": rottaPrice(fakedestinations),
        "fake_emissions": rottaEmissions(fakedestinations),
        "fake_rounds": 5,
    }
    print(fakegame)
    return fakegame


# Suvi: viimeisen pelin funktiot.
# After reaching the goal the game will calculate your final points by summing up
# how many rounds you used and your emissions
# Will print out how much money is left, but it is not a good way to calculate score, because the base
# fare of 100 e for a flight represents rounds and the distance km is already represented in emissions
def finalRound(gamestats, rottagame):
    rowofdestinations = gamestats["fake_destinationslist"]
    print(f"this is row of destinations {rowofdestinations}")
    atdestinations = rottagame["rotta_destinationsList"][3]
    roundscore = (rottagame['rotta_rounds'])/(gamestats['fake_rounds'])
    emissionscore = (rottagame["rotta-emissions"]) / \
        (gamestats["fake_emissions"])
    scoreprocentage = ((roundscore + emissionscore)/2)*100


# Rotan satunnaisesti päätetty reitti tasojen läpi
def generate_rottaDestinations():
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
        # Tehdään funktiossa etäisyyden mittaus jokaisen rotan matkan perusteella. -1 sen takia, että [entry + 1]
        # tuottaisi virheen, koska mennään listan ulkopuolelle.
        coords = sqlCoordinateQuery(
            DEST_ICAO[rottaList[entry]], DEST_ICAO[rottaList[entry + 1]]
        )
        # Käytetään checkForDistia, ja syötetään true argumentiksi, jotta tulos saadaan emissiomääränä
        grams = checkForDist(coords, True)
        total += grams
    return total / 1000  # Total on grammoina, jaetaan tonnilla, ja saadaan kiloina ulos


# Suvi: Ottaa parametriksi koordinaatit. Laskee etäisyyden. Lisää perushinnaksi 100 e + kilometrit/10 e.
# Suvi: Laskee saman 4 kertaa.
def rottaPrice(rottaList):
    totaldistance = 0
    print("Rottalist: {}".format(rottaList))
    print("Rottalist[0]: {}".format(rottaList[0]))
    for i in range(len(rottaList) - 1):
        # Tehdään funktiossa etäisyyden mittaus jokaisen rotan matkan perusteella. -1 sen takia, että [entry + 1] tuottaisi virheen, koska mennään listan ulkopuolelle.
        coords = sqlCoordinateQuery(
            DEST_ICAO[rottaList[i]], DEST_ICAO[rottaList[i + 1]]
        )
        # print(DEST_ICAO[rottaList[i]], DEST_ICAO[rottaList[i + 1]])
        distanceforonetrip = float(distance.distance(coords[0], coords[1]).km)
        totaldistance += distanceforonetrip
        # print(totaldistance)
    totalprice = (len(rottaList) - 1) * 100
    totalprice += totaldistance / 10
    return round(totalprice, 2)  # Palauttaa floatin


# Tekee SQL-haun ja palauttaa tuplen, jossa osoitin ja haun tulokset. Parametrinä sql-koodi. Lyhentää koodeja, joissa tehdään SQL-hakuja
def sqlPointer(code):
    pointer = connection.cursor()
    pointer.execute(code)
    result = pointer.fetchall()

    return (pointer, result)


# SQL-haku kahdella ICAO-tunnuksella, palauttaa listan, jossa kaksi tuplea, joissa koordinaatit.
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


# Ottaa parametriksi ICAO-koodin, jonka avulla etsii tietokannasta oikean maan nimen.
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


# Ottaa argumentiksi listan, jossa kaksi tuplea koordinaateilla (minkä sqlCoordinateQuery palauttaa) ja booleanin, joka indikoi, palauttaako funktio kilometrit vai päästöt grammoina
def checkForDist(locs, emissions: bool):
    output = distance.distance(locs[0], locs[1]).km
    # "Ternary operator" eli if else -toteamus yhdellä rivillä. Jos emissions on False, palauta output, jos True, palauta output * 115 (päästöt grammoina)
    return output if not emissions else output * 115


# Suvi: Ottaa argumenteiksi koordinaatit (minkä sqlCoordinateQuery palauttaa). Laskee etäisyyden. Lisää perushinnaksi 100 e + kilometrit/10 e
# voiko haitata pyöristys?
def checkForPrice(coords):
    trip = float(distance.distance(coords[0], coords[1]).km)
    price = 100
    price += trip / 10
    return round(price, 2)


# SQL-yhteyden luominen tietokannan käyttöä varten
connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    database="flight_game",
    user="suvi",
    password="HarmaaPoyta123",
    autocommit=True,
)

"""connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    database="flight_game",
    user="root",
    password="metropolia",
    autocommit=True
)"""

"""testi = rottaDestinations()
print(testi)
print(len(testi))
#destinations1 = print(testi[1])
print(sqlCountryQuery(DEST_ICAO[11]))
print(sqlCountryQuery(DEST_ICAO[12]))
print(sqlCoordinateQuery(DEST_ICAO[testi[0]], DEST_ICAO[testi[1]]))
testemissions =rottaEmissions(testi)
print(testemissions)
print(checkForDist(sqlCoordinateQuery(DEST_ICAO[testi[0]], DEST_ICAO[testi[1]]), True))
print(checkForDist(sqlCoordinateQuery(DEST_ICAO[testi[0]], DEST_ICAO[testi[1]]), False))
print(f" This is price: {checkForPrice(sqlCoordinateQuery(DEST_ICAO[testi[0]], DEST_ICAO[testi[1]]))}")
print(f"This is rat emissions {rottaEmissions(testi)}")
print(f"This is rat price {rottaPrice(testi)}")
geimi = gameStart()
list(geimi)
rottapeli = geimi
print(geimi[1])
print(geimi[0])
print(f"tämä on rottapeli : {gameStart()}")
print(f" tämä on feikkipeli: {fakeFinalGame(geimi[0])}")"""

"""geimi = list(gameStart())
print("geimi lähtö: {}".format(geimi))
print(type(geimi))
print(f"geimi 0 : {geimi[0]}")
lista = geimi[0][0]
print(f"lista 0 elemen: {lista[0]}")
geimi0 = fakeFinalGame(lista[0])
print(f"printing final : {finalRound(geimi0, geimi, geimi[1])}")
# round, gamestats, rottagame
"""

fakestats = fakeFinalGame(gameStart()[0])
print(f"fakestats: {fakestats}")
rottastats = gameStart()[0]
print(f"rottastats: {rottastats}")
print(finalRound(fakestats, rottastats))
