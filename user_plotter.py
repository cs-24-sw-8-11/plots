import matplotlib.pyplot as plt
from sys import argv
from statistics import mean
from time import time
from utils import regression, init_plots
from values import day, week, users, show

init_plots()

user = [user for user in users if user.username == argv[-1]][0]

journal_values = {}
now = time()

ax:plt.Axes
for journal in user.journals:
    fig, ax = plt.subplots()
    ax.set_title("Answers")
    ax.plot(range(len(journal.answers)), [answer.value * answer.rating for answer in journal.answers])

    delta = now - journal.timestamp
    journal_values[delta] = mean([answer.value * answer.rating for answer in journal.answers])

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

if show: plt.show()