import mysql.connector
import random
import math
import geopy


def checkForDist(start, dest):
    return geopy.distance.distance(start, dest).km


def travelPrice(start, dest):
    distance = checkForDist(start, dest)
    return int(distance / 100)


def sqlDistanceQuery(start, dest):
    pointer = connection.cursor()
    return


connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    database="flight_game",
    user="root",
    password="metropolia",
    autocommit=True
)
