#  Hello there
import random 
import math
import mysql.connector
user_command = ""
current_stage = 0  #  final stage = 5
rounds_left = 10  #  player can run out of rounds (0... pretty obvious)

quick_guide = ("\n\n------------------------\n"
               "You have a 10 round limit. You can check how many rounds you"
               " have left through 'status'.\n\n"
               "When chasing the rat, you will be able to choose\nwhether to fly"
               " to the next airport, or \nstay at the current one to earn money."
               " \nEvery single flight or a stay costs ONE round.\n\n"
               "Reach the rat by unravelling clues within the round limit"
               " and win the game!\n"
               "------------------------\n\n")

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

pelaajan_input = input("Provide a command: ")


def user_needs_help(pelaajan_input):  #  Provides the user a quick guide during the game. The user can continue playing when user inputs "exit".
    user_input_tips = {
        'R (Return): ': 'Continue the game',
        'S (Status): ': 'Show current score and available data.',
        'G (Guide):': 'Show quick a quick guide for the game.'
        }
    print("Quick commands: \n")
    for i, i2 in user_input_tips.items():  # prints out input tips for the user
        print(f"{i}, {i2}")
    while True:
        help_input = input("Please enter a quick command (R/S/G): ")
        if help_input.lower().strip() == "r":  #  exits the "instructions" loop with given user input
            return False
        elif help_input.lower().strip() == "s":  #  provides the user important stats and game progress
            print("status()")
        elif help_input.lower().strip() == "g":
            print(quick_guide)
        else:
            print("Unknown command\n")


if pelaajan_input == "?":
    user_needs_help(pelaajan_input)
print("test")

#  pääloooooooppi



''''
def player_stage_up():
    global player_level  #  "global" keyword gains access to a global variable inside a function
    player_level += 1
    return f"Current level: {player_level}"

def rounds_left_decreasing():  #  decreases the amount of rounds the user has left to use
    global rounds_left
    rounds_left -= 1
    return f"Rounds left: {rounds_left}"


current_round = 1
round_limit = 10

#  pääloooooooppi


def main_game_loop():
    #  declaring needed valuables, except we'll be using functions returning values
    player_location = "EFHK"
    rounds_left = 10
    stage = 0

    print(f"You're at EFHK airport, follow the damn train CJ and chase the rat or you lose your money!")

    while rounds_left > 0:
        print(f"\nStage {stage}")
        print(f"Current Location: {player_location}")
        print(f"Rounds Left: {rounds_left}")

        if stage == 1:
            available_airports = []
        elif stage == 2:
            available_airports = []
        elif stage == 3:
            available_airports = []
        elif stage == 4:
            available_airports = []
        elif stage == 5:
            available_airports = []

            # Ask the player for their choice
        pelaajan_input = input("Do you want to fly or stay and earn money? Enter F/S: ").strip().lower()

        if pelaajan_input == "f":  # The player chooses to fly
            destination = input("Enter the ICAO code of the airport you want to fly to: ").strip().upper()
            #  checks if the user provided ICAO is found in the corresponding list of airports
            if destination in available_airports:
                player_location = destination
                rounds_left -= 1
                stage += 1
                print(f"You have arrived at {destination}!")
            else:
                print("Invalid ICAO code. Choose an available airport.")
        elif pelaajan_input == "s":
            # The player chooses to stay and earn money
            rounds_left -= 1
            print("You decided to stay at the airport and earn money.")
        else:
            print("Invalid choice. Choose 'F' to Fly or 'S' to Stay.")

        # Check if the player has reached the final stage and caught the rat
        if stage == 6:
            print("Congratulations! You caught the guy and got your money back!")
            break
    #  player runs out of rounds (10 at the start)
    if rounds_left == 0:
        print("You ran out of rounds. The rat got away. Game over!")
'''


def main_game_loop():
    player_money_left = 1000
    current_stage = 0
    current_airport_icao = "EFHK"
    rounds_left = 10

    while current_stage < 5:
        stage = stage[current_stage]
        hint = "hint function here"
        correct_airport_icao = stage["correct_airport_icao"]
        airport_icao_options = stage["airport_icao_options"]

        print(f"\nStage {current_stage + 1}: {hint}")
        print(f"Current Airport: {current_airport_icao}")
        print(f"Player Coins: {player_money_left}")

        pelaajan_input = input("Enter an ICAO code or 'S' to earn more money: ").strip().upper()

        if pelaajan_input == "S":
            print("You stayed at the airport. You earned 100 credits but it cost you one round!")
            player_money_left += 100
            rounds_left -= 1

        if player_money_left <= 0:
            print("Out of money! Get lost! lol")
            break

        elif pelaajan_input == correct_airport_icao:
            current_stage += 1
            player_money_left -= 100
            current_airport_icao = pelaajan_input

        elif pelaajan_input in airport_icao_options and pelaajan_input != correct_airport_icao:
            current_airport_icao = pelaajan_input
            print(f"Rat wasn't here! You are now at {current_airport_icao}.")
            rounds_left -= 1
            player_money_left -= 100
            print(f"You flew to the wrong airport. The rat had been to {correct_airport_icao}.")
            current_airport_icao = correct_airport_icao
            print(f"You've been transferred to the correct airport: {current_airport_icao}")
            rounds_left -= 1

        elif rounds_left == 0:
            print("You ran out of rounds. YOU LOSE!!!")
            exit()

    print("\nCongratulations! You've reached the final stage and found the rat!")
    exit()

main_game_loop()
