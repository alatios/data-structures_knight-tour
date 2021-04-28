import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

inputFile = "time_results.txt"
data = pd.read_table(inputFile, delim_whitespace=True)
data.sort_values(by='n', inplace=True, ignore_index=True)

plt.plot(data['n']**2 * np.log(data['n']), data['time'], marker="x", color='orange', linewidth=0)
plt.xlabel("$n^2 \log n$")
plt.ylabel("Time [seconds]")
plt.grid()
plt.savefig("time_vs_n2logn.pdf", bbox_inches='tight')
plt.close()

plt.plot(data['n']**2,data['time'], marker="x", color='orange', linewidth=0)
plt.xlabel("$n^2$")
plt.ylabel("Time [seconds]")
plt.grid()
plt.savefig("time_vs_n2.pdf", bbox_inches='tight')
plt.close()

plt.plot(data['n'],data['time'], marker="x", color='orange', linewidth=0)
plt.xlabel("$n$")
plt.ylabel("Time [seconds]")
plt.grid()
plt.savefig("time_vs_n.pdf", bbox_inches='tight')
plt.close()

print("Analysis complete!")
exit(0)
