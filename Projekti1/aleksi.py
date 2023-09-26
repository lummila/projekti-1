# Hiiohoi
import mysql.connector


def getColumn(column: str):
    pointer = connection.cursor()
    sql = f"select {column} from game where screen_name = '{currentUser}';"
    pointer.execute(sql)
    result = pointer.fetchall()

    if not result:
        print("ERROR in getColumn() arguments.")
        return False
    else:
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

    sql += f"where screen_name = '{currentUser}';"
    pointer.execute(sql)

    return True


def login(username: str):
    pointer = connection.cursor()
    username = username.lower()

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
            sqlNewPIN = "insert into game (co2_consumed, co2_budget, screen_name, location, money, passcode) "
            sqlNewPIN += f"values (0, 0, '{username}', 'EFHK', 0, {int(newPIN)});"

            pointer.reset()
            pointer.execute(sqlNewPIN)
            newUser = input(
                "User created! You can now log in: ").lower()

            if newUser == "exit":
                exit()

            return login(newUser)
    # UUDEN KÄYTTÄJÄN LUONTI LOPPUU
    #########################
    #########################
    else:
        oldUserPIN = input("Input your 4-digit PIN code: ")

        # Käyttäjän pitää aina päästä ulos
        if oldUserPIN.lower() == "exit":
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
            print(
                f"Login successful with {result[0][0]} and {result[0][1]}!")
            return True
        else:
            print("Something went wrong with login...")
            return False


connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    database="velkajahti",
    user="root",
    password="metropolia",
    autocommit=True
)

print("---------------------------------")
currentUser = input("Enter username: ").lower()
login = login(currentUser)

if not login:
    print("Exiting game.")
    exit()

collu = input("What column to alter? ").lower()
muny = input("Add / Remove / Set? ").lower()
amount = int(input("Enter amount: "))

if "exit" in [collu, muny, amount]:
    print("Exiting game.")
    exit()

print(getColumn(collu))
updateValue(collu, muny, amount)
print(getColumn(collu))
