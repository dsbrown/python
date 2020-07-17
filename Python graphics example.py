import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib as mpl
from pandas import DataFrame, Series
import pandas as pd


url="http://ipsdatasciencemetrics-1a-i-3fb2431f.us-east-1.com:1080/rack_down_alarms"
fil = pd.read_csv(url, sep='\t')
fil['Counter'] = 1

#print(fil)
test = fil['Ticket Create Day'].value_counts()

plotts = fil['Ticket Create Day'].value_counts().plot(kind="barh", rot=0)

plt.show(plotts) # horizontal pareto of daily alarm totals


### split daily rack down counts out by impact level ###
by_impact = fil.groupby(['Ticket Create Day', 'Impact'])
agg_counts = by_impact.size().unstack().fillna(0)

print(agg_counts)
plt.show(agg_counts.plot(kind = 'barh', stacked = True))

normd_agg = agg_counts.div(agg_counts.sum(1), axis=0)
plt.show(normd_agg.plot(kind = 'barh', stacked = True))

### pivot tables of data ###
site_agg = fil.pivot_table('Counter', index = 'Ticket Create Date', columns = 'Site', aggfunc = 'sum').fillna(0)
print(site_agg)

print "Success!"
