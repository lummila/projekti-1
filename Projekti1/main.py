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

OHJEET = ("------------------------------\n"
          "Welcome to Chase The Rat!\n\nYou'll need to enter an existing username "
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
          "You have a limited amount of money to spend on your trip \n"
          "and your emissions will alter your final score in the game.\n\n"
          "The game will start by telling you your first clue "
          "\nand after unravelling it you can start travelling to the first airport."
          "\n\nIf you get the given clue correct, and travel to the right airport, \nthe game "
          "will give you a clue to reach the next airport.\nIf you travel to the wrong airport you'll miss one round."
          "\n\nWith the clues, you also have chance to be given a coincidence. "
          "\nThe coincidences can either have a positive OR negative impact on you.\n"
          "But remember: if you solve the clue the possibility to get a positive coincidence is much higher "
          "\nAND if you travel to the wrong airport you are more likely to be drawn a negative coincidence."
          "\n\nEach time you travel you'll use one round "
          "and \nif you travel to a wrong location, you'll have to wait one extra round."
          "\n\nIf you reach the final destination where the rat is within the given rounds: You'll win."
          "\n\nAfter reaching the goal the game will calculate your final points by summing up "
          "\nhow many rounds you used, your emissions and the money that's left."
          "\n\nIf you don't find The rat within the ten rounds: you'll lose."
          "------------------------------")

# exit()

# TÄMÄ PELITTÄÄ

# SQL-funktiot

# HINT-funktio, joka ottaa DEST_ICAO-koodin parametriksi ja palauttaa tekstinä vinkin tietokannasta


# -------------------------------------
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
# -------------------------------------


# Lyhennys sql:n kanssa kommunikoinnissa
def sql_execute(code: str):
    cursor = connection.cursor()
    cursor.execute(code)
    result = cursor.fetchall()

    return (cursor, result)


def login(username: str):
    if username.lower() == "exit":
        exit()

    username = username.upper()

    sql = "select screen_name from game "
    sql += f"where screen_name = '{username}';"

    (pointer, result) = sql_execute(sql)

    #########################
    #########################
    # Jos käyttäjänimeä ei löydy tietokannasta game -> screen_name
    if not result:
        print("User not found, create a new user? You can also type 'exit' to exit game. (Y = yes / N = no)")
        login_input = input("Y / N ").lower()

        while login_input not in ["y", "n", "exit"]:
            login_input = input(
                "Invalid command, enter Y, N or exit: ").lower()

        if login_input == "exit":
            exit()  # Ohjelma sulkeutuu
        elif login_input == "n":
            return False  # EI LUODA UUTTA KÄYTTÄJÄÄ, PELI EI ETENE
        # LUODAAN UUSI KÄYTTÄJÄ
        elif login_input == "y":
            new_PIN = input(
                "Enter your new 4-digit PIN code: ")

            # Jos PIN-koodi ei ole validi
            while len(new_PIN) != 4 or not new_PIN.isdigit():
                # Pitää muistaa aina päästää käyttäjä pois
                if new_PIN == "exit":
                    exit()
                else:
                    new_PIN = input(
                        "Entered PIN code is invalid. Please enter a 4-number PIN code: ")

            # Jos PIN-koodi on oikea, syötetään uusi käyttäjä tietokantaan.
            sql_new_user = "insert into game (co2_consumed, co2_budget, screen_name, location, money, passcode) "
            sql_new_user += f"values (0, 0, '{username}', 'EFHK', 0, {int(new_PIN)});"

            pointer.reset()
            pointer.execute(sql_new_user)

            new_user = input(
                "User created! You can now log in: ").upper()

            if new_user == "EXIT":
                exit()

            return login(new_user)
    # UUDEN KÄYTTÄJÄN LUONTI LOPPUU
    #########################
    #########################
    else:
        old_user_PIN = input("Input your 4-digit PIN code: ")

        # Käyttäjän pitää aina päästä ulos
        if old_user_PIN.upper() == "EXIT":
            exit()

        old_user_PIN = int(old_user_PIN)

        sql_old_PIN = "select screen_name, passcode from game "
        sql_old_PIN += f"where screen_name = '{username}' and passcode = {old_user_PIN};"

        pointer.execute(sql_old_PIN)
        result = pointer.fetchall()

        if not result:
            print("Invalid username or PIN code.")
            return False

        #####################
        #####################
        # Onnistunut sisäänkirjautuminen!
        if username == result[0][0] and old_user_PIN == result[0][1]:
            pelaaja_nimi = result[0][0]
            print("Successfully logged in!")
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
    total_grams = 0
    for entry in range(len(output) - 1):
        # Tehdään funktiossa etäisyyden mittaus jokaisen rotan matkan perusteella. -1 sen takia, että [entry + 1]
        # tuottaisi virheen, koska mennään listan ulkopuolelle.
        coords = sql_coordinate_query(
            DEST_ICAO[output[entry]], DEST_ICAO[output[entry + 1]]
        )
        # Käytetään checkForDistia, ja syötetään true argumentiksi, jotta tulos saadaan emissiomääränä
        total_grams += check_for_dist(coords, True)

    # ROTAN MATKOJEN HINTA
    total_distance = 0
    # print("Rottalist: {}".format(output))
    # print("Rottalist[0]: {}".format(output[0]))
    for i in range(len(output) - 1):
        # Tehdään funktiossa etäisyyden mittaus jokaisen rotan matkan perusteella. -1 sen takia, että [entry + 1] tuottaisi virheen, koska mennään listan ulkopuolelle.
        coords = sql_coordinate_query(
            DEST_ICAO[output[i]], DEST_ICAO[output[i + 1]]
        )
        # print(DEST_ICAO[output[i]], DEST_ICAO[output[i + 1]])
        distance_for_one_trip = float(
            distance.distance(coords[0], coords[1]).km)
        total_distance += distance_for_one_trip
        # print(totaldistance)
    total_price = (len(output) - 1) * 100
    total_price += total_distance / 10

    # Tuple, jossa lista Rotan sijainneista, Rotan emissiot ja Rotan matkojen hinta
    return (output, math.floor(total_grams), math.floor(total_price))


def sql_destination(icao):
    sql = "select airport.name, country.name, airport.ident from country, airport "
    sql += f"where country.iso_country = airport.iso_country and airport.ident = '{icao}';"

    # Erotetaan sqlPointerin osoitin ja tulokset käyttöä varten
    pointer, result = sql_execute(sql)

    if pointer.rowcount <= 0:  # Ei tuloksia
        print("Jokin meni vikaan, tarkista syötetty ICAO-koodi.")
        return -1
    else:
        # result on lista, jossa on tuple, jonka ensimmäinen elementti on haettu maan nimi.
        # result = [(Finland,)] / result[0] = (Finland,) / result[0][0] = Finland
        return f"{result[0][0]}, {result[0][1]}\t({result[0][2]})"


def sql_coordinate_query(start, dest):
    location_list = []
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
            location_list.append(result[0])
    # Palauttaa listan, jossa kahdet koordinaatit tuplemuodossa
    return location_list


# Ottaa parametriksi ICAO-tekstin, ja hakee tietokannasta oikean vihjeen. Palauttaa vihjeen tekstin.
def hint(icao: str):
    pointer = connection.cursor()

    sql = "select hint from hints "
    sql += f"where ident = '{icao}';"

    pointer.execute(sql)
    result = pointer.fetchall()

    if not result:
        return "ERROR fetching hint from hints!"
    else:
        return result[0][0]

    return


# Ottaa argumentiksi listan, jossa kaksi tuplea koordinaateilla (minkä sqlCoordinateQuery palauttaa) ja booleanin, joka indikoi, palauttaako funktio kilometrit vai päästöt grammoina
def check_for_dist(locs, emissions: bool):
    output = distance.distance(locs[0], locs[1]).km
    # "Ternary operator" eli if else -toteamus yhdellä rivillä. Jos emissions on False, palauta output, jos True, palauta output * 115 (päästöt grammoina)
    return output if not emissions else output * 115


def possible_flight_locations(current_location):
    location = [i for i in DEST_ICAO if DEST_ICAO[i] == current_location][0]

    print("Possible flight locations (type the 4-letter code to travel to said airport):")
    if (location - 10) < 0:
        for x in range(11, 16):
            print(sql_destination(DEST_ICAO[x]))
    elif 0 < (location - 10) < 10:
        for x in range(21, 26):
            print(sql_destination(DEST_ICAO[x]))

    return


# Printtaa pelaajalle tilanteen


def status():
    print(
        f"Current location: {sql_destination(pelaaja['location'])}\t"
        f"Current money: {pelaaja['money']}\t"
        f"Current round (out of 10): {pelaaja['round']}")

    possible_flight_locations(pelaaja["location"])
    return


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

    return rottagame, player_create


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

#############################
# Ohjeet
esittele_ohjeet = input(
    "Do you wish to read the instructions? (Y / N): ").lower()
if esittele_ohjeet == "exit":
    exit()
# Ohjeiden selitys
elif esittele_ohjeet == "y":
    print(OHJEET)
#############################

#############################
# LOGIN
pelaaja_nimi = ""
kirjautunut = login(input("Please enter your username to log in: "))
while not kirjautunut:
    kirjautunut = login(input("Please enter your username to log in: "))
#############################

# Pelaajan ja rotan init:
ROTTA, pelaaja = game_start()

print("Your first tip for your next destination is:")
print(hint(DEST_ICAO[ROTTA["destinations"][1]]))
# main looppi
while True:
    status()
    pelaajan_input = input("")
    # - pelaajan input

    # - ehtolausekkeet sille mitä pelaaja on kirjoittanut
    # - oikean funktion käynnistäminen

    exit()


#
