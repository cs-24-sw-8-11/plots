import sys
from utils import doSQL, User, Journal, Prediction, Answer, Question

second = 1
minute = second*60
hour = minute*60
day = hour*24
week = day*7

users = [User(data) for data in doSQL("select * from users where username not like '%user%' and not username = 'admin'")]

WIDTH = 1
HEIGHT = 1

show = not "--dontshow" in sys.argv