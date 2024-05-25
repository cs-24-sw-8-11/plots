import matplotlib.pyplot as plt
from values import users, show
from utils import init_plots

init_plots()

answers = [answer for user in users for journal in user.journals for answer in journal.answers]
ax:plt.Axes

fig, ax = plt.subplots()
ax.bar(range(len(answers)), [answer.value for answer in answers], color='black')
ax.bar(range(len(answers)), [answer.value * answer.rating for answer in answers], color='red', label='scaled')
ax.plot([0, len(answers)-1], [1, 1], label='Neutral/Positive')
ax.plot([0, len(answers)-1], [2, 2], label='Negative/Neutral')
ax.set_ybound(0, 3)
ax.legend(loc='upper right')
ax.set_title("Rating comparison")

plt.savefig("../figures/rating_comparison.pdf")
if show: plt.show()