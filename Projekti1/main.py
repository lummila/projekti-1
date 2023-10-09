'''
Asioiden järjestys koodissa:
1.  Importit
2.  HUOM: Jos tietokantahallintajärjestelmässäsi on salasana, KIRJAA SE admin_root_name -muuttujaan!
3.  Muuttumattomat DEST_ICAO, OHJEET ja sattumat
4.  clear() ja kaikki SQL-hakuja tekevät funktiot
5.  tutorial()
6.  generate_rotta()
7.  Matkojen etäisyys- ja hintafunktiot
8.  Funktiot mahdollisille lentokohteille ja vinkeille
9.  status() pelaajan tilanteen tulostamiselle
10. help_menu() apuvalikolle
11. coincidence() sattumien arpomiselle
12. Matkustamisessa käytettävät funktiot
13. stay() pelaajan rahankeruuta varten
14. final_round() pelin päättämistä varten
15. Pelin aloitusfunktio, joka määrittää rotan ja pelaajan tiedot
16. SQL-yhteys
17. Pelaajan ja rotan init
18. Ohjeiden kysyminen, LOGIN, tutorial
19. Pelin päälooppi, pyörii niin kauan kunnes pelaaja kirjoittaa päävalikossa "exit"

(Aleksi Lummila, Suvi Liimatainen, Karri Partanen, Elli Riskala 2023)
'''

import random
import math
import os
import mysql.connector
from geopy import distance
from colorama import Fore as CF, Back as CB

os.system('cls')

#########################################################################################
# VAIHDA TÄMÄ SIIHEN, MIKÄ SALASANA PELAAJALLA ON TIETOKANTAHALLINTOJÄRJESTELMÄSSÄÄN!
admin_root_name = "metropolia"
#########################################################################################

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
    53: "GMMX",  # Marokko
    54: "HECA",  # Egypti
    55: "GCLP",  # Gran Canaria
}

OHJEET = (f"------------------------------------------------------------------------------------------\n"
          f"Welcome to {CF.YELLOW}Chase The Rat{CF.RESET}! {CF.RED}This guide is not required, but may help you understand the game.{CF.RESET}\n\nYou'll need to enter an existing {CF.YELLOW}username{CF.RESET} "
          f"and a {CF.YELLOW}PIN-code{CF.RESET} to play with your user\n"
          f"OR you can create new {CF.YELLOW}username{CF.RESET} and a {CF.YELLOW}PIN-code{CF.RESET}.\n\n"
          f"In this game you'll travel between different {CF.YELLOW}airports{CF.RESET}, trying to find '{CF.RED}the Rat{CF.RESET}' who owes "
          f"you money.\nThe rat has done some airport-hopping "
          f"and the game will give you {CF.YELLOW}clues{CF.RESET} of his route and {CF.YELLOW}final location{CF.RESET}.\n"
          f"Each game will draw a new route of {CF.YELLOW}five airports{CF.RESET}, the fifth being the current location of "
          f"{CF.RED}the Rat{CF.RESET}.\n\nYou'll need to unravel the {CF.YELLOW}clues{CF.RESET} and follow the route that the rat took.\n"
          f"There are a total of {CF.YELLOW}ten rounds{CF.RESET} in each game for you to try to find {CF.RED}the Rat{CF.RESET} "
          f"and each time you travel you'll use one round.\n"
          f"You have a limited amount of {CF.YELLOW}money{CF.RESET} to spend on your trip"
          f"and your {CF.YELLOW}emissions{CF.RESET} will alter your final score in the game.\n\n"
          f"The game will give you your first {CF.YELLOW}clue{CF.RESET} "
          f"and after unraveling it you can start travelling to the first {CF.YELLOW}airport{CF.RESET}."
          f"\nIf you get the given {CF.YELLOW}clue{CF.RESET} correct the game will give you a clue to reach the next airport."
          f"\n\nWith the clues, you also have a chance to be given a {CF.GREEN}positive{CF.RESET} OR {CF.RED}negative{CF.RESET} {CF.YELLOW}coincidence{CF.RESET}.\n"
          f"If you solve the clue the possibility to get a positive coincidence is much higher "
          f"\nAND if you travel to the wrong airport you are more likely to experience negative coincidence."
          f"\n\nIf you reach the {CF.YELLOW}final destination{CF.RESET} where {CF.RED}the Rat{CF.RESET} is within the given rounds: {CF.GREEN}you'll win{CF.RESET}."
          f"\n\nAfter reaching the goal the game will calculate your final points: "
          f"\n{CF.GREEN}Your money{CF.RESET} * {CF.GREEN}rounds left{CF.RESET} + ({CF.YELLOW}Emission budget{CF.RESET} - {CF.RED}actual emissions{CF.RESET})"
          f"\n\nIf you don't find the Rat within the ten rounds: {CF.RED}you'll lose{CF.RESET}.\n"
          f"{CF.GREEN}You can play the tutorial after logging in to learn the basics!{CF.RESET}\n"
          "---------------------------------------------------------------------------------------"
          "---\n\n")

POS_COINCIDENCES = [
    "Nice! You found a 100€ bill on the airport floor.\n(100e will be added to your account)",
    "You were helpful to a lost elderly. For the kind act he rewarded you with a 50€ bill!\n(50€ will be added to "
    "your account)",
    "Lucky you! The flight company made a mistake with your tickets. You'll be getting 80€ cashback!\n(80€ will be "
    "added to your account)",
    "There was a free seat at a more eco-friendly airplane!\n(10kg was removed from your emissions)",
    "The airplane took a shorter route. Emissions were 10kg less than expected.\n(10kg of emissions will be removed)",
    "Nothing of note has happened."
]

NEG_COINCIDENCES = [
    "The airport lost your luggage... You'll have to wait one night at the airport.\n(One turn is used)",
    "Your flight was canceled, because of a raging storm. Your replacing flight leaves tomorrow morning. \n(One turn "
    "is used)",
    "You checked-in late to your flight. You'll have to pay a 100€ fee for the manual check-in.\n(100€ will be "
    "removed from your account)",
    "Your luggage was over weight. The fee for extra kilos is 50 €.\n(50 € will be removed from your account)",
    "The aircraft underestimated the flight's emissions. The emissions were 10kg higher than expected.\n(10kg of "
    "emissions will be added)",
    "Nothing of note has happened."
]


def clear():  # tyhjentää konsolin tarpeettomasta tekstistä joka printattiin aiemmin
    return os.system('cls')


def sql_scores(leaderboard: bool):
    if leaderboard:  # Top 10 kaikkien pelaajien pisteet
        sql = "select points, screen_name from goal "
        sql += "order by points desc limit 10;"
    else:  # Aktiivisen pelaajan parhaat pisteet
        sql = f"select points from goal where screen_name = '{pelaaja['name']}' "
        sql += "order by points desc limit 10;"

    _, result = sql_execute(sql, True)

    if not result:
        print("ERROR fetching scores in sql_scores()")
        return False

    clear()

    if leaderboard:
        print("+----------------------------------------------------+")
        print("| The leaderboard of top 10 scores in Chase the Rat: |")
        print("+----------------------------------------------------+")
        for entry in result:
            print(
                f"  {entry[0]}\t\t{entry[1]}")
        print("+----------------------------------------------------+")
    else:
        print("+----------------------------------------------------+")
        print("|            Your personal best scores:              |")
        print("+----------------------------------------------------+")
        for entry in result:
            print(
                f"  {entry[0]}")
        print("+----------------------------------------------------+")

    input("\nPress Enter to continue...")

    return True


# Ensin hakee pelaajan id-numeron, sitten tallentaa goaliin pelaajan lasketut pisteet
def sql_insert_score():
    sql = f"select id from game where screen_name = '{pelaaja['name']}';"

    _, result = sql_execute(sql, True)
    if not result:
        print("ERROR fetching player id in sql_insert_score()")
        return False

    player_id = result[0][0]
    player_score = math.floor((pelaaja["money"] * (10 - pelaaja["round"] if pelaaja["round"]
                              < 10 else 1) + (ROTTA["emissions"] - pelaaja["emissions"]) / 1000))

    sql = "insert into goal (id, screen_name, points) "
    sql += f"values ({player_id}, '{pelaaja['name']}', {player_score});"

    cursor = sql_execute(sql, False)
    if cursor.rowcount < 1:
        print("ERROR inserting player record in sql_insert_score()")
        return False

    return True


# Lyhennys sql:n kanssa kommunikoinnissa
def sql_execute(code: str, result: bool):
    cursor = connection.cursor()
    cursor.execute(code)
    if result:
        result = cursor.fetchall()
        return cursor, result
    else:
        return cursor


# Tietokantaan rekisteröityminen ja kirjautuminen
def sql_login(username: str):
    if username.lower() == "exit":
        exit()

    sql = "select screen_name from game "
    sql += f"where screen_name = '{username}';"

    cursor, result = sql_execute(sql, True)

    #########################
    #########################
    # Jos käyttäjänimeä ei löydy tietokannasta game -> screen_name
    if not result:
        print("User not found, create a new user? You can also type 'exit' to exit game. (Y = yes / N = no)")
        login_input = input("Y / N ").lower()

        while login_input not in ["y", "n", "exit"]:
            login_input = input(
                f"{CF.RED}Invalid command, enter Y, N or exit:{CF.RESET} ").lower()

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
                        f"{CF.RED}Entered PIN code is invalid. Please enter a 4-number PIN code:{CF.RESET} ")

            # Jos PIN-koodi on oikea, syötetään uusi käyttäjä tietokantaan.
            sql_new_user = "insert into game (co2_consumed, co2_budget, screen_name, location, money, passcode) "
            sql_new_user += f"values (0, 0, '{username}', 'EFHK', 0, {int(new_PIN)});"

            cursor.reset()
            cursor.execute(sql_new_user)

            new_user = input(
                "User created! You can now log in: ").upper()

            if new_user == "EXIT":
                exit()

            return sql_login(new_user)
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

        cursor, result = sql_execute(sql_old_PIN, True)

        if not result:
            print(f"{CF.RED}Invalid username or PIN code.{CF.RESET}")
            return False

        #####################
        #####################
        # Onnistunut sisäänkirjautuminen!
        if username == result[0][0] and old_user_PIN == result[0][1]:

            pelaaja["name"] = result[0][0]
            print("Successfully logged in!")
            return True
        else:
            print(f"{CF.RED}Something went wrong with login credentials...{CF.RESET}")
            return False


# Hakee tietokannasta lentokentän ja maan nimen, ja ICAO-koodin
def sql_destination(icao: str):
    sql = "select airport.name, country.name, airport.ident from country, airport "
    sql += f"where country.iso_country = airport.iso_country and airport.ident = '{icao}';"

    # Erotetaan sqlPointerin osoitin ja tulokset käyttöä varten
    cursor, result = sql_execute(sql, True)

    if cursor.rowcount <= 0:  # Ei tuloksia
        print(f"{CF.RED}Something went wrong. Check the ICAO code.{CF.RESET}")
        return -1
    else:
        # result on lista, jossa on tuple, jonka ensimmäinen elementti on haettu maan nimi.
        # result = [(Finland,)] / result[0] = (Finland,) / result[0][0] = Finland
        return [result[0][2], result[0][0], result[0][1]]


# Noutaa tietokannasta koordinaatit lähtö- ja saapumispaikkaan
def sql_coordinate_query(start: str, dest: str):
    location_list = []

    # Kaksi eri hakua, aloitusmaan ja päämäärän etäisyyden selvittämiseksi.
    for x in range(2):
        sql = "select longitude_deg, latitude_deg from airport "
        # Jos x on 0, kyseessä on ensimmäinen haku, eli käytetään start-muuttujaa, ja toisella kerralla dest-muuttujaa.
        sql += f"where ident = '{start if x == 0 else dest}';"

        # SQL:n käyttö
        cursor, result = sql_execute(sql, True)

        if cursor.rowcount <= 0:
            print(
                f"{CF.RED}ERROR calculating coordinates in sql_coordinate_query(){CF.RESET}")
            return -1
        else:
            # Lisätään locationList-listaan tuple, jossa koordinaatit
            location_list.append(result[0])
    # Palauttaa listan, jossa kahdet koordinaatit tuplemuodossa
    return location_list


# Ottaa parametriksi ICAO-tekstin, ja hakee tietokannasta oikean vihjeen. Palauttaa vihjeen tekstin.
def sql_hint(icao: str):
    sql = "select hint from hints "
    sql += f"where ident = '{icao}';"

    _, result = sql_execute(sql, True)

    if not result:
        return f"{CF.RED}ERROR fetching hint from hints!{CF.RESET}"
    else:
        return result[0][0]


# Pelaajan orientointi pelaamiseen
def tutorial():
    # Muuttujat pelaajan inputia varten ohjeistuksen aikana.
    learn_fly, learn_help_menu, learn_work = False, False, False,

    # Alifunktio etenemistä varten.
    def progress():
        status()

        # Opetetaan pelaajalle lentämistä.
        if learn_fly:
            tut_progress = input("\nType in 'fly': ").strip().lower()

            while tut_progress != "fly":
                if tut_progress == "exit":
                    exit()
                status()
                tut_progress = input(
                    "\nThat's not quite it. Type in 'fly': ").strip().lower()

            status()
            print(f"\nType {CF.YELLOW}'?'{CF.RESET} to open Help menu, {CF.BLUE}'return'{CF.RESET} to return,"
                  f" {CF.RED}'exit'{CF.RESET} to exit.")
            tut_progress = input(
                "\nWhere do you wish to fly?: ").strip().upper()

            while tut_progress != "ESSA":
                if tut_progress == "exit":
                    exit()
                status()
                print(f"\nType {CF.YELLOW}'?'{CF.RESET} to open Help menu, {CF.BLUE}'return'{CF.RESET} to return,"
                      f" {CF.RED}'exit'{CF.RESET} to exit.")
                tut_progress = input(
                    "\nThat's not quite it. Type in 'ESSA': ").strip().upper()

            travel("ESSA", True)
            input("\nPress Enter to continue...")
            return
        # Lentämisen opettaminen loppuu
        # Opetetaan pelaajalle apuvalikko
        if learn_help_menu:
            tut_progress = input("\nType in '?': ").strip().lower()
            while tut_progress != "?":
                if tut_progress == "exit":
                    exit()
                status()
                tut_progress = input(
                    "\nThat's not quite it. Type in '?': ").strip().lower()
            else:
                help_menu()
                return
        # Apuvalikon opettaminen loppuu
        # Opetetaan pelaajalle työntekoa
        if learn_work:
            tut_progress = input("\nType in 'stay': ").strip().lower()
            while tut_progress != "stay":
                if tut_progress == "exit":
                    exit()
                status()
                tut_progress = input(
                    "\nThat's not quite it. Type in 'stay': ").strip().lower()

            stay()
            return

        tut_progress = input("\nPress Enter to continue...").strip().lower()
        if tut_progress == "exit":
            exit()
        return

    pelaaja["coincidence"] = (f"{CF.GREEN}Welcome to Chase the Rat!\n"
                              f"Normally in-game, this is where the {CF.YELLOW}possible recent event{CF.GREEN}\n"
                              f"is displayed, but during the tutorial, we'll use this space to\n"
                              f"get you up to speed about the game. Don't worry about the rest,\n"
                              f"you'll learn quick! Press Enter to continue, or type exit to\n"
                              f"leave the game.{CF.RESET}")
    progress()

    pelaaja["coincidence"] = (f"{CF.GREEN}Above me you can see information about your situation in\n"
                              f"in a pretty box. It displays your current {CF.YELLOW}location{CF.GREEN}, amount of "
                              f"{CF.YELLOW}money{CF.GREEN},\n"
                              f"flight {CF.YELLOW}emissions{CF.GREEN} and game {CF.YELLOW}round{CF.GREEN}.{CF.RESET}")
    progress()

    pelaaja["coincidence"] = (f"{CF.GREEN}You change locations by flying between airports. To fly,\n"
                              f"you need {CF.YELLOW}money{CF.GREEN}. When you fly, you amass CO2 {CF.YELLOW}emissions"
                              f"{CF.GREEN} from the flights.\n"
                              f"This affects your end score negatively, so try to avoid meaningless\n"
                              f"flying! You have ten {CF.YELLOW}rounds{CF.GREEN} to catch the Rat, or you fail the "
                              f"game.\n"
                              f"Each action, for example flying, takes a round.{CF.RESET}")
    progress()

    pelaaja["coincidence"] = (f"{CF.GREEN}Below you can find the {CF.YELLOW}hint for your next destination{CF.GREEN}, "
                              f"and at\n"
                              f"the bottom are the {CF.YELLOW}possible airports{CF.GREEN} for you to fly to.\n"
                              f"The hint guides you to the right airport so you can catch\n"
                              f"the Rat as soon as possible.{CF.RESET}")
    progress()

    pelaaja["coincidence"] = (f"{CF.GREEN}But just showing it to you is lame, so let's fly! Type\n"
                              f"'{CF.BLUE}fly{CF.GREEN}' to open the flight menu, and fly to Stockholm-Arlanda "
                              f"Airport\n"
                              f"by typing in '{CF.BLUE}ESSA{CF.GREEN}'.{CF.RESET}\n")
    learn_fly = True
    progress()
    learn_fly = False

    pelaaja["coincidence"] = (f"{CF.GREEN}Well done, we are in Sweden now! I can aleady taste the korv.\n"
                              f"Note that you just lost {CF.RED}money{CF.GREEN} and a {CF.RED}round{CF.GREEN}, "
                              f"increased your {CF.RED}emissions{CF.GREEN}\n"
                              f"and possibly experienced a coincidence that affected you. You\n"
                              f"need to keep your resources in check, if you want to reach the Rat in time!{CF.RESET}")
    progress()

    pelaaja["coincidence"] = (f"{CF.GREEN}You can type in '{CF.BLUE}?{CF.GREEN}' to open the {CF.YELLOW}help menu"
                              f"{CF.GREEN}. You can read\n"
                              f"the rules, check the leaderboards or your own previous points.\n"
                              f"Actually, let's do it now. Type in '{CF.BLUE}?{CF.GREEN}', and fiddle around as much\n"
                              f"you want. We can continue this when you come back.{CF.RESET}")
    learn_help_menu = True
    progress()
    learn_help_menu = False

    pelaaja["money"] = 0
    pelaaja["coincidence"] = (f"{CF.GREEN}Oh no! Something horrible has happened, and you lost all\n"
                              f"your money! Thanks Obama! Now you need to {CF.YELLOW}work{CF.GREEN} to gain more "
                              f"capital\n"
                              f"and continue your chase. Type in '{CF.YELLOW}stay{CF.GREEN}' "
                              f"to, well, stay and work.{CF.RESET}")
    learn_work = True
    progress()
    learn_work = False

    pelaaja["coincidence"] = (f"{CF.GREEN}You may have to work if you can't get your flights right, or experience\n"
                              f"unfortunate events.{CF.RESET}")
    progress()

    pelaaja["coincidence"] = (f"{CF.GREEN}This concludes the tutorial. You are now ready to start\n"
                              f"the game, and find that damn Rat! Good luck!{CF.RESET}")
    progress()


# Funktio rotan tietojen luomiselle
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
        # Tehdään funktiossa etäisyyden mittaus jokaisen rotan matkan perusteella. -1 sen takia, että [entry + 1]
        # tuottaisi virheen, koska mennään listan ulkopuolelle.
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

    # Lista Rotan sijainneista, Rotan emissiot ja Rotan matkojen hinta
    return output, math.floor(total_grams), math.floor(total_price)


# Ottaa argumentiksi listan, jossa kaksi tuplea koordinaateilla (minkä sqlCoordinateQuery palauttaa) ja
# booleanin, joka indikoi, palauttaako funktio kilometrit vai päästöt grammoina
def check_for_dist(locs, emissions: bool):
    output = distance.distance(locs[0], locs[1]).km
    # "Ternary operator" eli if else -toteamus yhdellä rivillä. Jos emissions on False, palauta output, jos
    # True, palauta output * 115 (päästöt grammoina)
    return output if not emissions else output * 115


# Määrittelee yksittäisen lennon hinnan
def trip_price(start, dest):
    coords = sql_coordinate_query(start, dest)
    trip = check_for_dist(coords, False)
    return math.floor(100 + trip / 15)


# Palauttaa pelissä seuraavan tason vihjeen
def display_hint(current_location: str, can_advance: bool):
    # Säilöö pelaajan sijainnin "index-numeron" DEST_ICAO sanakirjasta
    location = [i for i in DEST_ICAO if DEST_ICAO[i] == current_location][0]

    # hint_index on ROTAN listassa oleva numero, joka vastaa DEST_ICAOSSA maan ICAO-koodia
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
        hint_index = 5

    if not can_advance and hint_index != 5:
        hint_index -= 1

    return sql_hint(DEST_ICAO[ROTTA["destinations"][hint_index]])


# Hakee SQL:stä listan mahdollisia lentokohteita ja palauttaa näistä listan. Voi myös printtaa.
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
    print(f"\n+---------------------------------------------------------+\n"
          f"  Location: ({loc[0]}) {loc[1]}, {loc[2]}\n"
          f"  Money: {pelaaja['money']} €\n"
          f"  CO2 Emissions: {math.floor(pelaaja['emissions'] / 1000)} kg\n"
          f"  Round: {pelaaja['round']}/10\n"
          f"+---------------------------------------------------------+\n")

    # Mahdollinen edellisen kierroksen sattuma
    print(f"{pelaaja['coincidence']}\n")

    # Printtaa pelaajan tämänhetkisen vihjeen
    print(
        "Rumour for the Rat's next destination:\n" + "\x1B[3m" +
        f'"{display_hint(pelaaja["location"], pelaaja["can_advance"])}"' + "\x1B[0m" + "\n")

    # Listaa pelaajalle mahdolliset lentokohteet
    print(f"{CF.YELLOW}{CB.BLACK}Possible flight locations:{CF.RESET}{CB.RESET}")
    possible_flight_locations(
        pelaaja["location"], pelaaja["can_advance"], True)
#############################


# Tarjoaa apua ja pistetaulukoita pelaajalle, "return" vie takaisin päävalikkoon
def help_menu():
    user_input_tips = {
        f'{CF.CYAN}Return{CF.RESET}': 'Continue the game.',
        f'{CF.YELLOW}Rules{CF.RESET}': 'Display the rules of the game.',
        f'{CF.GREEN}Leaderboard{CF.RESET}': 'Displays top 10 scores.',
        f'{CF.BLUE}Personal{CF.RESET}': 'Displays your own previous scores.',
        f'{CF.RED}Exit{CF.RESET}': 'Exits the game. Always available.',
    }

    while True:
        clear()
        status()
        print("\n------------------------------\n"
              "Quick commands: \n")
        for i, i2 in user_input_tips.items():  # Tulostaa kaikki mahdolliset komennot
            print(f"{i}: {i2}")

        help_input = input("\nPlease enter a quick command: ").strip().lower()

        if help_input == "exit":  # Lopeta peli
            exit()
        elif help_input == "return":
            return
        elif help_input == "rules":  # Tulostaa pelin ohjeet
            clear()
            print(OHJEET)
            input("\nPress Enter to continue...\n")
            status()
            help_menu()
            return
        elif help_input == "leaderboard":  # Tulostaa top 10 pisteet
            sql_scores(True)
            status()
            help_menu()  # Palaa takaisin apuvalikkoon
            return
        elif help_input == "personal":  # Tulostaa omat pisteet
            sql_scores(False)
            status()
            help_menu()  # Palaa takaisin apuvalikkoon
            return
        else:
            # Tuntematon komento
            input(f"\n{CF.RED}Unknown command.{CF.RESET} Press Enter to continue.")


# Arpoo pelaajalle sattuman, joka voi tapahtua lentäessä.
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


# Päivittää tietoja, kun tehdään onnistunut lento.
def travel(icao: str, right: bool):
    # Emissionsiin lasketaan lennon päästöt
    emissions = math.floor(check_for_dist(
        sql_coordinate_query(pelaaja["location"], icao), True))
    # Hinta pitää laskea vielä funktion sisäisesti koska Python on ohjelmointikieli
    price = trip_price(pelaaja["location"], icao)

    dest = sql_destination(icao)

    if right:
        print(
            f"{CF.GREEN}You have travelled to the correct airport:{CF.RESET} {dest[1]}.")
        pelaaja["can_advance"] = True
    else:
        print(
            f"{CF.RED}You have travelled to the wrong airport:{CF.RESET} {dest[1]}.")
        pelaaja["can_advance"] = False
    # Vähentää pelaajan rahoista matkan, päivittää käytetyt kierrokset ja pelaajan tilastot,
    # pelaaja siirtyy seuravaalle tasolle
    pelaaja["money"] -= price
    pelaaja["round"] += 1
    pelaaja["coincidence"] = coincidence(True)
    pelaaja["emissions"] += emissions


# Lentovalikko
def travel_loop():  # THE main loop
    while True:  # kysyy käyttäjältä minne hän haluaa lentää
        clear()
        status()
        print(f"\nType {CF.YELLOW}'?'{CF.RESET} to open Help menu, {CF.BLUE}'return'{CF.RESET} to return,"
              f" {CF.RED}'exit'{CF.RESET} to exit.")
        icao = input("\nWhere do you wish to fly?: ").strip().upper()
        if icao == "?":
            help_menu()
            continue
        elif icao == "EXIT":  # käyttäjä voi poistua milloin haluaa
            exit()
        # käyttäjä voi palata edelliseen kohtaan (looppi päättyy)
        elif icao == "RETURN":
            return

        # ICAO-koodin tunnusnumero DEST_ICAOSSA
        if icao in DEST_ICAO.values():
            icao_index = [i for i in DEST_ICAO if DEST_ICAO[i] == icao][0]
        else:
            input("Invalid ICAO code. Press Enter to continue.")
            continue
        # selvittää lennon hinnan hinta-funktion avulla
        price = trip_price(pelaaja["location"], icao)
        # Lista pelaajalle mahdollisista lentokohteista
        possibilities = possible_flight_locations(
            pelaaja["location"], pelaaja["can_advance"], False)

        # käyttäjä syöttää vahingossa nykyisen sijaintinsa uuden kohteen sijaan --> uudelleen
        if icao == pelaaja["location"]:
            input("You're already in this location. Press Enter to continue.")
            continue
        #  pelaaja valitsee oikean lentokentän (rotan aikaisempi olinpaikka)
        if icao in possibilities and icao_index in ROTTA["destinations"]:

            # jos pelaajalla ei ole varaa lentoon, joutuu pelaaja jäämään kentälle
            if pelaaja["money"] < price:
                input(
                    f"{CF.RED}\nYou cannot afford this flight.{CF.RESET} Press Enter to continue.")
                return

            travel(icao, True)

            input("\nPress enter to continue...")
            return icao
        #  pelaaja valitsee väärän lentokentän sen hetkisen tason vaihtoehdoista
        elif icao in possibilities and icao_index not in ROTTA["destinations"]:

            price = trip_price(pelaaja["location"], icao)

            if pelaaja["money"] < price:
                input(
                    f"{CF.RED}\nYou cannot afford this flight.{CF.RESET} Press Enter to continue.")
                return

            travel(icao, False)

            input("\nPress enter to continue...")
            return icao
        else:  # käyttäjä kirjoittaa virheellisen syötteen, ohjelma pyytää kirjoittamaan uudestaan
            input(
                f"{CF.RED}\nInvalid input, please try again.{CF.RESET} Press Enter to continue.")


# Pelaaja jää lentokentälle ansaitakseen rahaa
def stay():

    def work():
        pelaaja["money"] += 175
        pelaaja["round"] += 1
        input("Press Enter to continue...")

    while True:
        clear()
        status()
        print(
            f"+ You have decided or had to stay at {CF.YELLOW}{pelaaja['location']}{CF.RESET} and work for money!\n|")
        job = input("| Choose a job to work at:\n|\n"
                    f"| {CF.RED}BURGER{CF.RESET} = You're going to be flipping some burgers.\n"
                    f"| {CF.GREEN}FLOWER{CF.RESET} = The flower shop could need a hand.\n"
                    f"| {CF.YELLOW}EXCHANGE{CF.RESET} = The currency excgange needs someone to count the bills "
                    f"(No... you can't take them)\n|\n"
                    f"| Type in: {CF.RED}BUR{CF.RESET} / {CF.GREEN}FLO{CF.RESET} / "
                    f"{CF.YELLOW}EXC{CF.RESET}\n|\n"
                    f"+ ('{CF.RED}exit{CF.RESET}' leaves the game and '{CF.BLUE}return{CF.RESET}' returns to main menu): ").strip().upper()
        if job == "?":  # käyttäjä avaa help-moduulin
            help_menu()
        elif job == "EXIT":  # Käyttäjä voi aina poistua ohjelmasta
            exit()
        elif job == "RETURN":  # Käyttäjä haluaa palata takaisin
            return False
        elif job == "BUR":
            # Pelaaja valitsee työpaikan lentokentältä/ansaitsee rahaa lentämistä varten.
            # Pelaajan ansaitsemat rahat päivitetään pelin tietoihin
            print(
                f"\nYou decided to work at the {CF.RED}Burger Shack{CF.RESET}! Have some money!")
            work()
            return True
        elif job == "FLO":  # työvaihtoehto 2
            print(
                f"\nYou decided to go and {CF.GREEN}wrap some flowers{CF.RESET}! Here's some cash to keep you going!")
            work()
            return True
        elif job == "EXC":  # työvaihtoehto 3
            print(
                f"\nWe will trust that you {CF.YELLOW}count the bills{CF.RESET} correctly! Take some money!")
            work()
            return True
        else:  # käyttäjä on nakkisormi
            print(f"{CF.RED}\nInvalid input, please try again.{CF.RESET}")
            input("Press Enter to continue...")


# Final Round päättää pelin ja pyörittää top 10 players joka tapauksessa.
def final_round():
    if pelaaja["location"] == DEST_ICAO[ROTTA["destinations"][5]]:
        print(f"\t+----------+\n"
              f"\t| {CF.YELLOW}You win!{CF.RESET} |\n"
              f"\t+----------+\n\n"
              f"Your emissions were {math.floor(pelaaja['emissions'] / 1000)}"
              f" kilograms and you have {pelaaja['money']} € left.\n")
        sql_insert_score()
        input("Press Enter to continue...")
        sql_scores(True)
        exit()
    else:
        print(f"\t+-----------+\n"
              f"\t| {CF.RED}You lost!{CF.RESET} |\n"
              f"\t+-----------+\n\n"
              f"Your emissions were {math.floor(pelaaja['emissions'] / 1000)} "
              f"kilograms and you have {pelaaja['money']} € left.\n")
        input("Press Enter to continue...")
        sql_scores(True)
        exit()


# Suvi:Pelin alkutilannefunktio. Sijainti sama kuin Rotalla aluksi. Massi 1000 e, emissiot 0, Kierros 0.
# Tämän funktion täytyy myös pyöräyttää rotan tiedot, jotta alkupaikka on tiedossa.
# Niinpä funktio pyöräyttelee myös rottafunktion.
def game_start():
    # Destinations = [], emissions = int, trip_price = int
    destinations, emissions, rat_price = generate_rotta()

    # Esim: [11, 22, 33, 44, 51], vastaavat ICAO-koodeja flygarilistalla
    rotta_create = {
        "destinations": destinations,  # Lista
        "price": rat_price,
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


#########################################################################################
############################                        #####################################
############################   ALOITETAAN RUNTIME   #####################################
############################                        #####################################
#########################################################################################
# SQL-yhteys
connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    database="velkajahti",
    user="root",
    password=admin_root_name,
    autocommit=True
)
#########################################################################################
# Pelaajan ja rotan init:
ROTTA, pelaaja = game_start()
#########################################################################################
# Ohjeet
instructions = input(
    f"Do you wish to read the instructions? ({CF.GREEN}Y{CF.RESET} / {CF.RED}N{CF.RESET}): ").lower()
if instructions == "exit":
    exit()
# Ohjeiden selitys
elif instructions == "y":
    clear()
    print(OHJEET)
    input("Press Enter to continue...")
#########################################################################################
################################   KIRJAUTUMINEN   ######################################
#########################################################################################
clear()
pelaajan_nimi = input(
    "\nPlease enter your username to log in: ").strip().upper()

# Liian pienet nimet ei vetele
while len(pelaajan_nimi) < 3:
    pelaajan_nimi = input(
        f"{CF.YELLOW}Please enter a username longer than 2 letters:{CF.RESET} ").strip().upper()

# Kirjaudutaan / rekisteröidytään, ja jos
kirjautunut = sql_login(pelaajan_nimi)

# Jos kirjautumisfunktio palauttaa Falsen (ei onnistunut) ja yritetään uudestaan
while not kirjautunut:
    pelaajan_nimi = input(
        "Please enter your username to log in: ").strip().upper()
    kirjautunut = sql_login(pelaajan_nimi)
input("Press Enter to continue...")
#########################################################################################
###################################   TUTORIAL   ########################################
#########################################################################################
# Tutorial
play_tutorial = input(
    f"\nPlay the {CF.MAGENTA}tutorial{CF.RESET} to learn to play the game? ({CF.GREEN}Y{CF.RESET} / "
    f"{CF.RED}N{CF.RESET}): ").lower()

# Pelaajan poispäästäminen
if play_tutorial == "exit":
    exit()

# Päästetään pelaaja pelaamaan tutorial
elif play_tutorial == "y":
    tutorial()
    # Pelaaja ja Rotta pitää resettaa uudelleen pelikokemuksen takia.
    ROTTA, pelaaja = game_start()
    pelaaja["name"] = pelaajan_nimi
    clear()
#########################################################################################
###############################                     #####################################
###############################   PELIN PÄÄLOOPPI   #####################################
###############################                     #####################################
#########################################################################################
# main looppi
pelaajan_input = ""
while pelaajan_input != "exit":
    if pelaaja["location"] == DEST_ICAO[ROTTA["destinations"][5]] or pelaaja["round"] > 10:
        final_round()
    status()
    pelaajan_input = input(
        f"\n'{CF.BLUE}fly{CF.RESET}' to travel, '{CF.YELLOW}?{CF.RESET}' to open menu, "
        f"'{CF.MAGENTA}stay{CF.RESET}' to stay and work,"
        f" '{CF.RED}exit{CF.RESET}' to quit game: ").lower().strip()
    # - pelaajan input
    if pelaajan_input == "?":  # Avaa jelppivalikko
        help_menu()
    elif pelaajan_input == "fly":  # pelaajan syöte käynnistää lento-funktion
        traveled = travel_loop()
        if traveled:
            pelaaja["location"] = traveled
    elif pelaajan_input == "stay":
        stay()

    # - ehtolausekkeet sille mitä pelaaja on kirjoittanut
    # - oikean funktion käynnistäminen

else:
    exit()
#########################################################################################
#########################################################################################
