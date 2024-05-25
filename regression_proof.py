import matplotlib.pyplot as plt
from utils import regression, init_plots
from values import show

init_plots()

fig, ax = plt.subplots()

xs = list(range(4))
ys = [3, 3, 0.1]

ax.plot(xs[:-1], ys, 'o', label='values')
ax.plot(xs, [regression(xs[:-1], ys)(x) for x in xs], '--', label='regression')
ax.legend()
plt.savefig("../figures/example.pdf")

if show: plt.show()
