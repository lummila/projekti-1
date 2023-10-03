import random
import math
import mysql.connector
from geopy import distance

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

OHJEET = ("Welcome to Chase The Rat!\n\nYou'll need to enter an existing username "
          "and a PIN-code to play with your user\n"
          "OR if you are a new player you can create your own username and a four-digit PIN-code.\n\n"
          "In this game you'll travel between different airports, trying to find 'the rat' who owes "
          "you money.\nThe rat has done some airport-hopping and he has travelled somewhere in Europe.\n"
          "The game will give you clues of the rat's route and his final location.\n\n"
          "Each game will draw a new route of five airports, the fifth being the current location of "
          "the rat,\nbefore he leaves Europe and is beyond your reach.\n\n"
          "Your goal is to follow the given clues to try and find him before this.\n\nThere "
          "are a total of ten rounds in each game for you to try to find the rat.\nYou'll "
          "need to unravel the clues and follow the route that the rat took.\n\n"
          "You have a limited amount of money to spend on your trip and your emissions will alter your final score in the game.\n\n"
          "The game will start by telling you your first clue and after unravelling it you can "
          "start\ntravelling to the first airport."
          "\nIf you get the given clue correct, and travel to the right airport, the game "
          "will give you a clue to reach the next airport.")
print("-------------------------")
print(OHJEET)
print("-------------------------")

exit()

# TÄMÄ PELITTÄÄ

# SQL-funktiot


# Palauttaa pyydetyn kolummnin arvon nykyiseltä pelaajalta. Käytä pienellä kirjoitettuja "nimiä", vaikka funktiossa onkin .lower() varmistajana
def getColumn(column: str):
    pointer = connection.cursor()
    sql = f"select {column.lower()} from game where screen_name = '{pelaaja_nimi}';"

    pointer.execute(sql)
    result = pointer.fetchall()

    return result[0][0]


# Käytetään arvojen päivittämiseen valitussa kolumnissa, VAROVASTI NIIDEN ARGUMENTTIEN KANSSA!
# Column EI SAA olla: id, screen_name, passcode, location
# SAA OLLA: co2_consumed, co2_budget, money
def updateValue(column: str, action: str, amount: int):
    # Ainoat käytettävät toiminnot funktiossa: Lisää, poista, aseta
    if action not in ["add", "remove", "set"] or amount < 0:
        print("ERROR in updateValue() function arguments.")
        return False

    currentValue = getColumn(column)
    pointer = connection.cursor()
    sql = f"update game set {column} = "

    if action == "set":
        # Asetetaan määrä pyydetyksi
        sql += f"{amount} "
    elif action == "add":
        # Lisätään pyydetty määrä
        sql += f"({column} + {amount}) "
    elif action == "remove":
        # Jos rahaa on vähemmän kuin pitäisi poistaa, laitetaan nollille. Muuten vain vähennetään.
        sql += f"0 " if amount >= currentValue else f"({column} - {amount}) "

    sql += f"where screen_name = '{pelaaja_nimi}';"
    pointer.execute(sql)

    return True


def login(username: str):
    if username.lower() == "exit":
        exit()

    pointer = connection.cursor()
    username = username.upper()

    sql = "select screen_name from game "
    sql += f"where screen_name = '{username}';"

    pointer.execute(sql)
    result = pointer.fetchall()

    #########################
    #########################
    # Jos käyttäjänimeä ei löydy tietokannasta game -> screen_name
    if not result:
        print("User not found, create a new user? You can also type 'exit' to exit game. (Y = yes / N = no)")
        loginInput = input("Y / N ").lower()

        while loginInput not in ["y", "n", "exit"]:
            loginInput = input(
                "Invalid command, enter Y, N or exit: ").lower()

        if loginInput == "exit":
            exit()  # Ohjelma sulkeutuu
        elif loginInput == "n":
            return False  # EI LUODA UUTTA KÄYTTÄJÄÄ, PELI EI ETENE
        # LUODAAN UUSI KÄYTTÄJÄ
        elif loginInput == "y":
            newPIN = input(
                "Enter your new 4-digit PIN code: ")

            # Jos PIN-koodi ei ole validi
            while len(newPIN) != 4 or not newPIN.isdigit():
                # Pitää muistaa aina päästää käyttäjä pois
                if newPIN == "exit":
                    exit()
                else:
                    newPIN = input(
                        "Entered PIN code is invalid. Please enter a 4-number PIN code: ")

            # Jos PIN-koodi on oikea, syötetään uusi käyttäjä tietokantaan.
            sql_new_user = "insert into game (co2_consumed, co2_budget, screen_name, location, money, passcode) "
            sql_new_user += f"values (0, 0, '{username}', 'EFHK', 0, {int(newPIN)});"

            pointer.reset()
            pointer.execute(sql_new_user)

            newUser = input(
                "User created! You can now log in: ").upper()

            if newUser == "EXIT":
                exit()

            return login(newUser)
    # UUDEN KÄYTTÄJÄN LUONTI LOPPUU
    #########################
    #########################
    else:
        oldUserPIN = input("Input your 4-digit PIN code: ")

        # Käyttäjän pitää aina päästä ulos
        if oldUserPIN.upper() == "EXIT":
            exit()

        oldUserPIN = int(oldUserPIN)

        sqlOldPIN = "select screen_name, passcode from game "
        sqlOldPIN += f"where screen_name = '{username}' and passcode = {oldUserPIN};"

        pointer.execute(sqlOldPIN)
        result = pointer.fetchall()

        if not result:
            print("Invalid username or PIN code.")
            return False

        #####################
        #####################
        # Onnistunut sisäänkirjautuminen!
        if username == result[0][0] and oldUserPIN == result[0][1]:
            pelaaja_nimi = result[0][0]
            return True
        else:
            print("Something went wrong with login credentials...")
            return False

# Pelaajan arvojen muuttamisfunktiot

# Sattumafunktiot

# Lentokentälle saapuminen -funktio

# Ohjeet-funktio


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
        "money": 1000.00,
        "emissions": 0,
        "round": 0
    }

    return (rottagame, player_create)


# --------------------------------------

# pelaaja = [sijainti 0, massit 1, emissiot 2, kierros 3]
# pelaaja = ["EFHK", 0, 0, 0]


#############################
# SQL-yhteys
connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    database="velkajahti",
    user="vj_admin",
    password="velkajahti",
    autocommit=True
)
#############################

# LOGIN
pelaaja_nimi = ""
kirjautunut = login(input("Please enter your username to log in: "))
while not kirjautunut:
    kirjautunut = login(input("Please enter your username to log in: "))

# Pelaajan ja rotan init:
(ROTTA, pelaaja) = game_start()

# Ohjeet
# Alun selitys

# main looppi
while True:

    # - pelaajan input
    # - ehtolausekkeet sille mitä pelaaja on kirjoittanut
    # - oikean funktion käynnistäminen

    exit()
