import matplotlib.pyplot as plt
from values import users, show
from utils import init_plots

init_plots()

ax:plt.Axes
axs:list[plt.Axes]

for user in users:
    if user.predictions:
        fig, ax = plt.subplots()
        ax.set_title(f"user {user.id} predictions")
        ax.plot([p.value for p in user.predictions], range(len(user.predictions)))
    
    fig, axs = plt.subplots(len(user.journals))
    axs[0].set_title(f"user {user.id} journals")
    for ax, journal in zip(axs, user.journals):
        ax.bar(range(len(journal.answers)), [answer.value for answer in journal.answers], color='black')
        ax.bar(range(len(journal.answers)), [answer.value * answer.rating for answer in journal.answers], color='red')
        ax.set_ybound(0, 3)

if show: plt.show()
