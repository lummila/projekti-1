#  Hello there
import random 
import math
import mysql.connector
user_command = ""

'''

#  DEMO DEMO DEMO DEMO DEMO DEMO DEMO DEMO (REQUIRES DATABASE IMPLEMENTATION TO PROCEED FURTHER
DEST_ICAO2 = {"LEBL": 51, "LPTT": 52, "GCTS": 53, "GCFP": 54, "GCLV": 55}
DEST_TIPS2 = {51: "The promised land of bullfights and delicious food!",
              52: "The country of amazing wine. The people also sound like drunk Spaniards.",
              53: "The largest one of the Spanish islands on the coast of western Africa",
              54: "Easternmost one of the Spanish islands on the coast of western Africa.",
              55: "The dream island location of elderly Finnish pensioners on the coast of Western Africa."
              }


def icao_to_hint():
    while True:
        user_icao = input("Input the ICAO of the desired airport: ").upper()
        if user_icao in DEST_ICAO2:
            dict_num = DEST_ICAO2[user_icao]
            print(DEST_TIPS2[dict_num])
            return False
        else:
            print("Invalid input, please try again.")


icao_to_hint()


current_stage = 0
rounds_left = 10


def main_core(current_stage, rounds_left):
    print("")  ##  <--- INSERT INSTRUCTIONS HERE


def game_instructions():
    return f""
'''
def user_needs_help():  #  Provides the user a quick guide during the game. The user can continue playing when user inputs "exit".
    user_input_tips = {
        'Exit: ': 'Exit the help module.',
        'Status: ': 'Show current score and available data.'
    }
    while True:
        user_input = input("Please enter a command or '?' to get help: ")
        if user_input == "?":
            print("Quick commands:")
            for i, i2 in user_input_tips.items():  #  prints out key input tips for the user
                print(f"{i}, {i2}")
        elif user_input.lower() == "exit":  #  exits the "instructions" loop with given user input
            return False
        elif user_input.lower() == "status":  #  provides the user the current game status and progress
            pointer = connection.cursor()
            sql = (f"SELECT goal.Points, Co2_consumed, Co2_budget, Money, Location "
                   f"FROM goal, game WHERE Screen_name = {'USERNAME HERE'}")
            pointer.execute(sql)
            result = pointer.fetchall()
            return f'{result}'



user_needs_help()



# SQL-yhteyden luominen tietokannan käyttöä varten
connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    database="flight_game",
    user="root",
    password="metropolia",
    autocommit=True
)














