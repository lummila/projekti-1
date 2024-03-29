import random
import math
import time
import os
import mysql.connector
from geopy import distance

os.system('cls')

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

OHJEET = ("\n\n------------------------------\n"
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
          "\n\nIf you don't find The rat within the ten rounds: you'll lose.\n"
          "------------------------------\n\n")

POS_COINCIDENCES = [
    "Nice! You found a 100€ bill on the airport floor.\n100e will be added to your account",
    "You were helpful to a lost elderly. For the kind act he rewarded you with a 50€ bill!\n50e will be added to your account",
    "Lucky you! The flight company made a mistake with your tickets. You'll be getting 80€ cashback!\n80e will be added to your account",
    "There was a free seat at a more eco-friendly airplane.\n10kg was removed from your emissions!", "The airplane took a shorter route. Emissions were 10kg less than expected.\n10kg of emissions will be removed.",
    "Nothing of note has happened."
]

NEG_COINCIDENCES = [
    "The airport lost your luggage... You'll have to wait one night at the airport.\nOne turn is used",
    "Your flight was canceled, because of a raging storm. Your replacing flight leaves tomorrow morning. \nOne turn is used",
    "You checked-in late to your flight. You'll have to pay a 100€ fee for the manual check-in.\n100e will be removed from your account",
    "Your luggage was over weight. The fee for extra kilos is 50 €.\n50 € will be removed from your account",
    "The aircraft underestimated the flight's emissions. The emissions were 10kg higher than expected.\n10kg of emissions will be added",
    "Nothing of note has happened."
]


def clear():  #  tyhjentää konsolin tarpeettomasta tekstistä joka printattiin aiemmin
    return os.system('cls')


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

    (cursor, result) = sql_execute(sql)

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

            cursor.reset()
            cursor.execute(sql_new_user)

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

        cursor, result = sql_execute(sql_old_PIN)

        if not result:
            print("Invalid username or PIN code.")
            return False

        #####################
        #####################
        # Onnistunut sisäänkirjautuminen!
        if username == result[0][0] and old_user_PIN == result[0][1]:

            pelaaja["name"] = result[0][0]
            print("Successfully logged in!")
            return True
        else:
            print("Something went wrong with login credentials...")
            return False

# Pelaajan arvojen muuttamisfunktiot

# Sattumafunktiot

# Lentokentälle saapuminen -funktio


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


def sql_destination(icao: str):
    sql = "select airport.name, country.name, airport.ident from country, airport "
    sql += f"where country.iso_country = airport.iso_country and airport.ident = '{icao}';"

    # Erotetaan sqlPointerin osoitin ja tulokset käyttöä varten
    cursor, result = sql_execute(sql)

    if cursor.rowcount <= 0:  # Ei tuloksia
        print("Jokin meni vikaan, tarkista syötetty ICAO-koodi.")
        return -1
    else:
        # result on lista, jossa on tuple, jonka ensimmäinen elementti on haettu maan nimi.
        # result = [(Finland,)] / result[0] = (Finland,) / result[0][0] = Finland
        return [result[0][2], result[0][0], result[0][1]]

def sql_select_5_top_players():
    sql = f"select money, screen_name from game order by money desc limit 5;"
    # Erotetaan sqlPointerin osoitin ja tulokset käyttöä varten
    cursor, result = sql_execute(sql)
    print(f"Here are the top 5 player scores")
    for i in range(0, 5):
        print(f"{i+1}. Points: {result[i][0]} Screen name: {result[i][1]}")
    return

def sql_coordinate_query(start: str, dest: str):
    location_list = []

    # Kaksi eri hakua, aloitusmaan ja päämäärän etäisyyden selvittämiseksi.
    for x in range(2):
        sql = "select longitude_deg, latitude_deg from airport "
        # Jos x on 0, kyseessä on ensimmäinen haku, eli käytetään start-muuttujaa, ja toisella kerralla dest-muuttujaa.
        sql += f"where ident = '{start if x == 0 else dest}';"

        # SQL:n käyttö
        cursor, result = sql_execute(sql)

        if cursor.rowcount <= 0:
            print("ERROR calculating coordinates in sql_coordinate_query()")
            return -1
        else:
            # Lisätään locationList-listaan tuple, jossa koordinaatit
            location_list.append(result[0])
    # Palauttaa listan, jossa kahdet koordinaatit tuplemuodossa
    return location_list


# Ottaa parametriksi ICAO-tekstin, ja hakee tietokannasta oikean vihjeen. Palauttaa vihjeen tekstin.
def hint(icao: str):
    sql = "select hint from hints "
    sql += f"where ident = '{icao}';"

    _, result = sql_execute(sql)

    if not result:
        return "ERROR fetching hint from hints!"
    else:
        return result[0][0]


# Ottaa argumentiksi listan, jossa kaksi tuplea koordinaateilla (minkä sqlCoordinateQuery palauttaa) ja booleanin, joka indikoi, palauttaako funktio kilometrit vai päästöt grammoina
def check_for_dist(locs, emissions: bool):
    output = distance.distance(locs[0], locs[1]).km
    # "Ternary operator" eli if else -toteamus yhdellä rivillä. Jos emissions on False, palauta output, jos True, palauta output * 115 (päästöt grammoina)
    return output if not emissions else output * 115


def trip_price(start, dest):
    coords = sql_coordinate_query(start, dest)
    trip = check_for_dist(coords, False)
    price = 100
    price += trip / 10
    return math.floor(price)


def display_hint(current_location: str, can_advance: bool):
    # Säilöö pelaajan sijainnin "index-numeron" DEST_ICAO sanakirjasta
    location = [i for i in DEST_ICAO if DEST_ICAO[i] == current_location][0]
    hint_index = 0

    if location < 10:
        hint_index = 1
    elif location < 20:
        hint_index = 2
    elif location < 30:
        hint_index = 3
    elif location < 40:
        hint_index = 4
    elif location < 50:
        hint_index = 5
    else:
        hint_index = 6

    if not can_advance:
        hint_index -= 1

    return hint(DEST_ICAO[ROTTA["destinations"][hint_index]])


# Hakee SQL:stä listan mahdollisia lentokohteita ja printtaa ne pelaajalle luettavaksi.
def possible_flight_locations(current_location: str, can_advance: bool, prints: bool):
    # Säilöö pelaajan sijainnin "index-numeron" DEST_ICAO sanakirjasta
    location = [i for i in DEST_ICAO if DEST_ICAO[i] == current_location][0]
    # Jos pelaajalla on lupa edetä, näyttää seuraavan tason maat, jos ei, nykyiset.
    possible_loc = location - 10 if can_advance else location - 20

    list_of_locations = []

    if possible_loc < 0:
        for x in range(11, 16):  # Printtaa DEST_ICAOn numeroiden mukaan
            if prints:
                loc = sql_destination(DEST_ICAO[x])
                print(f"({loc[0]}) {loc[1]}, {loc[2]}")
            list_of_locations.append(DEST_ICAO[x])
    elif 0 < possible_loc < 10:
        for x in range(21, 26):
            if prints:
                loc = sql_destination(DEST_ICAO[x])
                print(f"({loc[0]}) {loc[1]}, {loc[2]}")
            list_of_locations.append(DEST_ICAO[x])
    elif 10 < possible_loc < 20:
        for x in range(31, 36):
            if prints:
                loc = sql_destination(DEST_ICAO[x])
                print(f"({loc[0]}) {loc[1]}, {loc[2]}")
            list_of_locations.append(DEST_ICAO[x])
    elif 20 < possible_loc < 30:
        for x in range(41, 46):
            if prints:
                loc = sql_destination(DEST_ICAO[x])
                print(f"({loc[0]}) {loc[1]}, {loc[2]}")
            list_of_locations.append(DEST_ICAO[x])
    else:
        for x in range(51, 56):
            if prints:
                loc = sql_destination(DEST_ICAO[x])
                print(f"({loc[0]}) {loc[1]}, {loc[2]}")
            list_of_locations.append(DEST_ICAO[x])

    return list_of_locations


# Printtaa pelaajalle tilanteen, ei palauta mitään
def status():
    clear()

    # Printtaa pelaajan sijainnin (flygari, maa, ICAO-koodi), rahat ja kierroksen/10
    loc = sql_destination(pelaaja['location'])
    print("------------------------------\n"
          f"Location: ({loc[0]}) {loc[1]}, {loc[2]}\n"
          f"Money: " + "{:,}".format(pelaaja['money']) + " €\n"
          "CO2 Emissions: " + "{:,}".format(pelaaja['emissions']) + " g\n"
          f"Round: {pelaaja['round']}/10\n"
          "------------------------------\n")

    # Mahdollinen edellisen kierroksen sattuma
    print(f"{pelaaja['coincidence']}\n")

    # Printtaa pelaajan tämänhetkisen vihjeen
    print(
        "Rumour for the Rat's next destination:\n" + "\x1B[3m" +
        f'"{display_hint(pelaaja["location"], pelaaja["can_advance"])}"' + "\x1B[0m" + "\n")

    # Listaa pelaajalle mahdolliset
    print("Possible flight locations:")
    possible_flight_locations(
        pelaaja["location"], pelaaja["can_advance"], True)
#############################


# Provides the user a quick guide during the game. The user can continue playing when user inputs "exit".
def help_menu():
    user_input_tips = {
        'Return': 'Continue the game.',
        'Rules': 'Display the rules of the game.',
        'Commands': 'A guide on how to progress in the game.',
        'Exit': 'Exits the game. Always available.',
    }
    print("\n------------------------------\n"
          "Quick commands: \n")
    for i, i2 in user_input_tips.items():  # prints out input tips for the user via iterators
        print(f"{i}: {i2}")
    help_input = input("\nPlease enter a quick command: ").lower()
    while help_input != "exit":
        if help_input == "return":  # exits the "instructions" loop with given user input
            return
        elif help_input == "rules":  #  prints out a shortened version of the game rules
            clear()
            print(OHJEET)
            time.sleep(2.0)
            input("Press Enter to continue...")
            clear()
            status()
            return help_menu()
        elif help_input == "commands":
            print("\nAvailable commands (all case insensitive):\n"
                  "- To travel to available airports, type out their ICAO codes.\n"
                  "For example, typing EFHK (when available) would take you to\n"
                  "Helsinki-Vantaa Airport in Finland.\n"
                  "- If you can't afford to travel, you can type out MONEY\n"
                  "to spend one in-game round doing odd jobs to increase your funds.\n")
            input("Type Enter (or anything) to continue...")
            clear()
            status()
            return help_menu()
        else:
            print("Unknown command.")  #  user enters an invalid input
            help_input = input("\nPlease enter a quick command: ").lower()
    else:
        exit()


def coincidence(positive: bool):
    weights = [80, 20] if positive else [20, 80]
    coincidences_list = random.choices([POS_COINCIDENCES, NEG_COINCIDENCES],
                                       weights=weights)
    choice = random.choice(coincidences_list[0])

    for index, text in enumerate(POS_COINCIDENCES):
        if choice == text:
            if index == 0:
                pelaaja["money"] += 100
            elif index == 1:
                pelaaja["money"] += 50
            elif index == 2:
                pelaaja["money"] += 80
            elif index in [3, 4]:
                if pelaaja["emissions"] >= 10000:
                    pelaaja["emissions"] -= 10000
                else:
                    pelaaja["emissions"] = 0
    for index, text in enumerate(NEG_COINCIDENCES):
        if choice == text:
            if index in [0, 1]:
                pelaaja["round"] += 1
            elif index == 2:
                if pelaaja["money"] >= 100:
                    pelaaja["money"] -= 100
                else:
                    pelaaja["money"] = 0
            elif index == 3:
                if pelaaja["money"] >= 50:
                    pelaaja["money"] -= 50
                else:
                    pelaaja["money"] = 0
            elif index == 4:
                pelaaja["emissions"] += 10000
    return choice


def travel_loop():  # THE main loop
    while True:  #  kysyy käyttäjältä minne hän haluaa lentää
        clear()
        status()
        print("\nType '?' to open Help menu, 'return' to return, 'exit' to exit.")
        icao = input("\nWhere do you wish to fly?: ").strip().upper()
        if icao == "?":
            help_menu()
        elif icao == "EXIT":  #  käyttäjä voi poistua milloin haluaa
            exit()
        elif icao == "RETURN":  #  käyttäjä voi palata edelliseen kohtaan (looppi päättyy)
            return

        icao_index = [i for i in DEST_ICAO if DEST_ICAO[i] == icao][0]

        if icao == pelaaja["location"]:  #  käyttäjä syöttää vahingossa nykyisen sijaintinsa uuden kohteen sijaan --> uudelleen
            print("You're already in this location...")
            time.sleep(4.0)
            continue
        #  pelaaja valitsee oikean lentokentän (rotan aikaisempi olinpaikka)
        if icao in possible_flight_locations(pelaaja["location"], pelaaja["can_advance"], False) and icao_index in ROTTA["destinations"]:

            price = trip_price(pelaaja["location"], icao) # selvittää lennon hinnan hinta-funktion avulla

            if pelaaja["money"] < price:  #  jos pelaajalla ei ole varaa lentoon, joutuu pelaaja jäämään kentälle
                print("\nYou cannot afford this flight...")
                time.sleep(4.0)
                continue
            #  emissionsiin lasketaan lennon päästöt
            emissions = math.floor(check_for_dist(
                sql_coordinate_query(pelaaja["location"], icao), True))

            dest = sql_destination(icao)
            print(
                f"You have travelled to the correct airport: {dest[1]}.")
            #  vähentää pelaajan rahoista matkan, päivittää käytetyt kierrokset ja pelaajan tilastot, pelaaja siirtyy seuravaalle tasolle
            pelaaja["money"] -= price
            pelaaja["round"] += 1
            pelaaja["can_advance"] = True
            pelaaja["coincidence"] = coincidence(True)
            pelaaja["emissions"] += emissions

            if pelaaja["round"] == 10:
                final_round()
            time.sleep(4.0)
            return icao
        #  pelaaja valitsee väärän lentokentän sen hetkisen tason vaihtoehdoista
        elif icao in possible_flight_locations(pelaaja["location"], pelaaja["can_advance"], False) and icao_index not in ROTTA["destinations"]:

            price = trip_price(pelaaja["location"], icao)

            if pelaaja["money"] < price:
                print("\nYou cannot afford this flight...")
                time.sleep(4.0)
                continue

            emissions = math.floor(check_for_dist(
                sql_coordinate_query(pelaaja["location"], icao), True))

            print(
                f"You travelled to the wrong airport: {sql_destination(icao)[1]}...")
            #  pelaaja ei voi vielä edetä seuraavalle tasolle + pelaajan tilastot päivitetään
            pelaaja["money"] -= price
            pelaaja["round"] += 1
            pelaaja["can_advance"] = False
            pelaaja["coincidence"] = coincidence(False)
            pelaaja["emissions"] += emissions


            time.sleep(4.0)
            return icao
        else: # käyttäjä kirjoittaa virheellisen syötteen, ohjelma pyytää kirjoittamaan uudestaan
            print("\nInvalid input, please try again.")
            time.sleep(2.0)

#Final Round päättää pelin
def final_round():
    if (pelaaja["round"]) == 10 and (pelaaja["location"] == DEST_ICAO[ROTTA["destinations"][5]]):
        print(f"You win! Your emissions were {pelaaja['emissions']} grams and you have money left {pelaaja['money']} euros.")
        sql_select_5_top_players()
    else:
        print(f"You lost! Your emissions were {pelaaja['emissions']} grams and you have money left {pelaaja['money']} euros.")
        sql_select_5_top_players()
        exit()

# Suvi:Pelin alkutilannefunktio. Sijainti sama kuin Rotalla aluksi. Massi 1000 e, emissiot 0, Kierros 0.
# Tämän funktion täytyy myös pyöräyttää rotan tiedot, jotta alkupaikka on tiedossa. Niinpä funktio pyöräyttelee myös rottafunktion.
def game_start():
    # Destinations = [], emissions = int, trip_price = int
    (destinations, emissions, trip_price) = generate_rotta()

    # Esim: [11, 22, 33, 44, 51], vastaavat ICAO-koodeja flygarilistalla
    rotta_create = {
        "destinations": destinations,  # Lista
        "price": trip_price,
        "emissions": emissions,
        "rounds": 5,
    }
    player_create = {
        "name": "",
        "location": "EFHK",
        "money": 1000,
        "emissions": 0,
        "round": 1,
        "can_advance": True,
        "coincidence": "Nothing of note has happened."
    }

    return rotta_create, player_create


# --------------------------------------



# pelaaja = [sijainti 0, massit 1, emissiot 2, kierros 3]
# pelaaja = ["EFHK", 0, 0, 0]

'''
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
'''

# SQL-yhteys
connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    database="velkajahti",
    user="root",
    password="",
    autocommit=True
)
#############################
# Ohjeet
esittele_ohjeet = input(
    "Do you wish to read the instructions? (Y / N): ").lower()
if esittele_ohjeet == "exit":
    exit()
# Ohjeiden selitys
elif esittele_ohjeet == "y":
    print(OHJEET)
    input("Press Enter to continue...")
#############################

# Pelaajan (tätä tarvitaan siihen, että kirjautuneen pelaajan nimi talletetaan ["name"]-osioon) ja rotan init:
ROTTA, pelaaja = game_start()
pelaaja["round"] = 10


#############################
# LOGIN
kirjautunut = login(input("Please enter your username to log in: "))
# Jos kirjautumisfunktio palauttaa Falsen (ei onnistunut) ja yritetään uudestaan
while not kirjautunut:
    kirjautunut = login(input("Please enter your username to log in: "))
time.sleep(1.0)
#############################

# print("\n\nYour first tip for your next destination is:")
# print(f'"{hint(DEST_ICAO[ROTTA["destinations"][1]])}"\n')

# main looppi
pelaajan_input = ""
while pelaajan_input != "exit":
    status()
    if pelaaja["round"] == 10:
        final_round()
        sql_select_5_top_players()
    pelaajan_input = input(
        "\n'fly' to travel, '?' to open menu, 'exit' to quit game: ").lower().strip()
    # - pelaajan input
    if pelaajan_input == "?":  # Avaa jelppivalikko
        help_menu()
    elif pelaajan_input == "fly":  #  pelaajan syöte käynnistää lento-funktion
        travel = travel_loop()
        if travel:
            pelaaja["location"] = travel
  # - ehtolausekkeet sille mitä pelaaja on kirjoittanut
    # - oikean funktion käynnistäminen
else:
    exit()


