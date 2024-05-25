from os import system
import json
from subprocess import check_output
import sys
from statistics import mean
import matplotlib.pyplot as plt
from values import users, show
from utils import doSQL, init_plots

init_plots()

counts = {
    name:0 for name in ["0.2", "0.4", "0.6", "0.8"]
}

for user in users:
    for name in counts.keys():
        result = doSQL(f"select (select count(*) from answers where answers.journalid = journals.id and answers.rating = {name}) as count from journals where journals.userid = '{user.id}'")
        if result:
            counts[name] += result[0]["count"]

for name, value in counts.items():
    print(f"{name}: {value}")

print(f"mean rating: {mean([final for name, item in counts.items() for final in [float(name) for _ in range(item)]])}")

ax:plt.Axes

fig, ax = plt.subplots()

ax.bar([str(int(float(key)*5)) for key in counts.keys()], [value for value in counts.values()])
plt.savefig("../figures/ratings.pdf")

if show: plt.show()