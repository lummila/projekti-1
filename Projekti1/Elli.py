import random


# coincidences
# positive:
# "Nice! You found a 100€ bill on the airport floor." 100e will be added to your account
# "You were helpful to a lost elderly. For the kind act he rewarded you with a 50€ bill!" 50e will be added to your account
# "There was a free seat at a more eco-friendly airplane. 20kg was removed from your emissions!" 20kg of emissions will be removed
# "Lucky you! The flight company made a mistake with your tickets. You'll be getting 80€ cashback!" 80e will be added to your account
# "The airplane took a shorter route. Emissions were 10kg less than expected." 10kg of emissions will be removed

# negative
# "The airport lost your luggage... You'll have to wait one night at the airport." one turn is used
# "Your flight was canceled, because of a raging storm. Your replacing flight leaves tomorrow morning." one turn is used
# "You checked-in late to your flight. You'll have to pay a 100€ fee for the manual check-in." 100e will be removed from your account
# "Your luggage was over weight. The fee for extra kilos is 50e." 50e will be removed from your account
# "The aircraft underestimated the flight's emissions. The emissions were 15kg higher than expected." 15kg of emissions will be added

# Instructions
# Welcome to Chase The Rat! You'll need to enter an existing username and a PIN-code to play with your user
# OR if you are a new player you can create your own username and a four-digit PIN-code.
# In this game you'll travel between different airports, trying to find 'the rat' who owes you money.
# The rat has done some airport-hopping and he has travelled somewhere in Europe.
# The game will give you clues of the rat's route and his final location.
# Each game will draw a new route of five airports, the fifth being the current location of the rat, before he leaves Europe and is beyound your reach.
# Your goal is to follow the given clues to try to find him. There are a total of ten rounds in each game for you to try to find the rat.
# You'll need to unravel the clues and follow the route that the rat took.
# You have a limited amount of money to spend on your trip and your emissions will alter your final score in the game.
# The game will start by telling you your first clue and after unravelling it you can start travelling to the first airport.
# If you get the given clue correct, and travel to the right airport, the game will give you a clue to reach the next airport.
# If you travel to the wrong airport you'll miss one round.
# With the clues, you also have chance to be given a coincidence. The coincidences can either have a positive OR negative impact on you.
# But remember: if you solve the clue the possibility to get a positive coincidence is much higher
# AND if you travel to the wrong airport you are more likely to be drawn a negative coincidence.
# Each time you travel you'll use one round and if you travel to a wrong location, you'll have to wait one extra round.
# If you reach the final destination where the rat is within the given rounds: You'll win.
# After reaching the goal the game will calculate your final points by summing up
# how many rounds you used, your emissions and the money that's left.
# If you don't find The rat within the ten rounds: you'll lose.


# help functions instructions:
#

# coincidence functions

# when the player gets to the right location
def draw_positive_coincidence(positive_coincidences, negative_coincidences):
    positive_probability = 80
    coincidences_list = random.choices([positive_coincidences, negative_coincidences],
                                       weights=[80, 20])
    random_coincidence = random.choice(coincidences_list[0])
    return random_coincidence


# when the player gets to the wrong location

def draw_negative_coincidence(negative_coincidences, positive_coincidences):
    negative_probability = 80
    coincidences_list = random.choices([negative_coincidences, positive_coincidences],
                                       weights=[80, 20])
    random_coincidence = random.choice(coincidences_list[0])
    return random_coincidence


positive_coincidences = [{'coincidence': "Nice! You found a 100€ bill on the airport floor. "
                                         "100e will be added to your account"},
                         {'coincidence': "You were helpful to a lost elderly. "
                                         "For the kind act he rewarded you with a 50€ bill! "
                                         "50e will be added to your account"},
                         {'coincidence': "Lucky you! The flight company made a mistake with your tickets. "
                                         "You'll be getting 80€ cashback! 80e will be added to your account"},
                         {'coincidence': "There was a free seat at a more eco-friendly airplane."
                                         "10kg was removed from your emissions!"},
                         {'coincidence': "The airplane took a shorter route. Emissions were 10kg less than expected. "
                                         "10kg of emissions will be removed."},
                         {'coincidence': "You did not get a coincidence."}
                         ]

negative_coincidences = [{'coincidence': "The airport lost your luggage... "
                                         "You'll have to wait one night at the airport. One turn is used"},
                         {'coincidence': "Your flight was canceled, because of a raging storm. "
                                         "Your replacing flight leaves tomorrow morning. One turn is used"},
                         {'coincidence': "You checked-in late to your flight. "
                                         "You'll have to pay a 100€ fee for the manual check-in. "
                                         "100e will be removed from your account"},
                         {'coincidence': "Your luggage was over weight. The fee for extra kilos is 50€. "
                                         "50e will be removed from your account"},
                         {'coincidence': "The aircraft underestimated the flight's emissions. "
                                         "The emissions were 10kg higher than expected. "
                                         "10kg of emissions will be added"},
                         {'coincidence': "You did not get a coincidence."}
                         ]


# when the coincidences come in use
def coincidence():
    if location == ROTTA:
        random_positive_coincidence = draw_positive_coincidence(positive_coincidences, negative_coincidences)
        print(f"{random_positive_coincidence['coincidence']}")
    elif location != ROTTA:
        random_negative_coincidence = draw_negative_coincidence(negative_coincidences, positive_coincidences)
        print(f"{random_negative_coincidence['coincidence']}")
    return


player_create = {
    "location": "EFHK",
    "money": 1000,
    "emissions": 0,
    "round": 0}


# pelaajan arvojen muuttamisfunktio
def change_of_status():
    if POS_COINCIDENCES:
        if [0]:
            player_create['money'] = + 100
        elif [1]:
            player_create['money'] = 'money' + 50
        elif [2]:
            player_create['money'] = 'money' + 80
        elif [3][4]:
            player_create['emissions'] = 'emissions' - 10000
    if NEG_COINCIDENCES:
        if [0][1]:
            player_create['round'] = 'round' + 1
        elif [2]:
            player_create['money'] = 'money' - 100
        elif [3]:
            player_create['money'] = 'money' - 50
        elif [4]:
            player_create['emissions'] = 'emissions' + 10000
    else:
        'no coincidence'


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
          "\n\nIf you don't find The rat within the ten rounds: you'll lose.")
print("-------------------------")
print(OHJEET)
print("-------------------------")

exit()
