from statistics import mean
import matplotlib.pyplot as plt
import datetime
from values import users, show
from utils import init_plots

init_plots()

ratings = {}

for prediction in [prediction for user in users for prediction in user.predictions]:
    ratings[prediction.id] = prediction.rating

genders = [user.userdata.gender for user in users]
males = [g for g in genders if g == 1]
females = [g for g in genders if g == 2]
others = [g for g in genders if g == 3]

print(f"""
    # participants:         {len(users)}
    Mean age:               {round(mean([user.userdata.age for user in users]), 2)}
    Male participants:      {int((len(males)/len(genders))*100)}%
    Female participants:    {int((len(females)/len(genders))*100)}%
    Other participants:     {int((len(others)/len(genders))*100)}%
    Mean education level:   {round(mean([user.userdata.education_level for user in users]), 2)} (1: elementary, 2: high school, 3: bachelor, 4: master)
    Total journals:         {len([journal for user in users for journal in user.journals])}
    Journals per user:      {mean([len(user.journals) for user in users])}
    Predictions per user:   {mean([len(user.predictions) for user in users])}
    Total answers:          {len([answer for user in users for journal in user.journals for answer in journal.answers])}
    Average answer (wo. r): {mean([answer.value for user in users for journal in user.journals for answer in journal.answers])}
""")

# INIT MATPLOTLIB
ax:plt.Axes

# JOURNALS PLOT
fig, ax = plt.subplots()
values = [datetime.datetime.fromtimestamp(journal.timestamp) for user in users for journal in user.journals]
ax.hist(values)
ax.get_xaxis().set_ticks([])
ax.set_xlabel("time")
ax.set_title("Journal history")
plt.savefig("../figures/journal_history.pdf")

# ANSWERS PLOT

fig, ax = plt.subplots()
values = [answer.value for user in users for journal in user.journals for answer in journal.answers]
ax.bar(range(len(values)), values)
ax.set_title("answer values")
plt.savefig("../figures/answer_values.pdf")

# PREDICTIONS PLOT
fig, ax = plt.subplots()

colors = ['black' if prediction.expected is None else 'blue' if prediction.expected else 'red' for user in users for prediction in user.predictions]
values = [prediction.value for user in users for prediction in user.predictions]

ax.bar(range(len(values)), values, color=colors)
ax.set_title("Predictions values")
plt.savefig("../figures/prediction_values.pdf")

if show: plt.show()
