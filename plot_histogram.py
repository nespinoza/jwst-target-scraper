import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('ticks')

def read_file(fname = 'targets_cycle1.csv'):

    fin = open(fname, 'r')

    # Skip first line:
    fin.readline()

    # Define arrays that will save info:
    targets, instruments, hours, pids, pis, titles = [], [], [], [], [], []

    while True:
        
        line = fin.readline()

        print(line)        
        if line != '':

            target, instrument, hrs, pid, pi, title = line.split(',')

            targets.append(target)
            instruments.append(instrument)
            hours.append(np.double(hrs))
            pids.append(pid)
            pis.append(pi)
            titles.append(title)

        else:

            break

    return targets, instruments, hours, pids, pis, titles

targets, instruments, hours, pids, pis, titles = read_file()

results = {}

for i in range(len(instruments)):

    if ('coronagraphic' not in instruments[i].lower()) and ('imaging' not in instruments[i].lower()) \
        and ('ifu' not in instruments[i].lower()) and ('interferometry' not in instruments[i].lower()) \
        and ('phasing' not in instruments[i].lower()):
        if instruments[i] not in list(results.keys()): 

            results[instruments[i]] = 0.

        else:

            results[instruments[i]] += hours[i]

counters = np.arange(len(list(results.keys())))
values = np.zeros(len(counters))

c = 0
for instrument in list(results.keys()):

    values[c] = results[instrument]
    c += 1
    print(instrument)

# Minimal text labels:
original = ['MIRI Medium Resolution Spectroscopy', 'NIRCam Grism Time Series', \
            'NIRSpec Bright Object Time Series', 'MIRI Low Resolution Spectroscopy', \
            'NIRISS Single-Object Slitless Spectroscopy', 'NIRSpec Fixed Slit Spectroscopy']

replacement = ['MIRI MRS', 'NIRCam', 'NIRSpec BOTS', 'MIRI LRS', 'NIRISS/SOSS', 'NIRSpec FSS']

print(list(results.keys()))
print(replacement)

print('total time:',np.sum(values))
plt.bar(counters, values, color = 'cornflowerblue') 
plt.xticks(counters, replacement, rotation=45, fontsize=14)
plt.ylabel('Charged time (hours)',fontsize=14)
plt.tight_layout()
plt.show()
