import matplotlib.pyplot as plt
from subprocess import check_output
from sys import argv
import json
from statistics import mean
from time import time

second = 1
minute = second*60
hour = minute*60
day = hour*24
week = day*7

def regression(xs:list[float], ys:list[float]):
    x_mean = mean(xs)
    y_mean = mean(ys)
    numerator = 0.0
    denominator = 0.0
    for x, y in zip (xs, ys):
        numerator += (x-x_mean) * (y-y_mean)
        denominator += pow(x - x_mean, 2)
    slope = numerator / denominator
    intercept = y_mean - slope * x_mean

    return lambda x: intercept + (slope * x)

test = regression(range(5), range(5))

assert test(6) == 6

db = argv[1] if len(argv) > 1 else "db.db3"
user = argv[2] if len(argv) > 2 else "user123"

user_data = json.loads(check_output([
    "sqlite3",
    db,
    f"select * from users where username = '{user}'",
    "-json"
]).decode())[0]

journals = json.loads(check_output([
    "sqlite3",
    db,
    f"select * from journals where userId = '{user_data['id']}'",
    "-json"
]).decode())

answers = {}

for journal in journals:
    answers[journal["id"]] = json.loads(check_output([
        "sqlite3",
        db,
        f"select * from answers where journalId = '{journal['id']}'",
        "-json"
    ]).decode())

journal_values = {}
now = time()

ax:plt.Axes
for jid, value in answers.items():
    fig, ax = plt.subplots()
    ax.set_title("Answers")
    ax.plot(range(len(value)), [answer["value"] * answer["rating"] for answer in value])

    journal = [j for j in journals if j["id"] == jid][0]
    delta = now - journal["timestamp"]
    journal_values[delta] = mean([answer["value"] * answer["rating"] for answer in value])

xs = [week - key for key in journal_values.keys()]
ys = journal_values.values()

f = regression(xs, ys)

fig, ax = plt.subplots()

print(xs)
print(ys)

print([f(i) for i in xs])

def one_more(xs:list[int]):
    return list(xs) + [week+day]


ax.plot([x/day for x in xs], ys)
ax.plot([x/day for x in one_more(xs)], [f(x) for x in one_more(xs)], '--')

ax.set_xbound(0, 8)
ax.set_ybound(0, 3)

plt.show()