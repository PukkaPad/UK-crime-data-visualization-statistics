# !/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd 
import numpy as np
from collections import Counter
import os
import glob
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import re
import textwrap
from itertools import cycle
from pylab import rcParams
rcParams['figure.figsize'] = 15, 5


#import plotly.plotly as py
#import plotly.graph_objs as go

path = r'./data/'
all_files = glob.glob(os.path.join(path, "*.csv"))
frame = pd.DataFrame()
list_ = []

for file_ in all_files:
    df = pd.read_csv (file_)
    print "reading ", file_
    list_.append(df)
frame = pd.concat(list_)
#print frame

frame['Time'] = pd.to_datetime(frame['Month'], format = '%Y-%m')
#print frame

counter = Counter(frame['Crime type']) # this gives me the total frequency from all the files
#print counter

groupedFrame = frame.groupby(['Time', 'Crime type']).size().reset_index(name='Frequency')
df = pd.DataFrame(groupedFrame)
#print test

# this is beautiful!
pivot_df = df.pivot_table('Frequency', ['Time'], 'Crime type')


# Creatig simple time series:

series = dict()

for column in pivot_df:

    #remove whitespace from column
    pattern = re.compile(r'\s+')
    colname = re.sub(pattern, '', column)
    #print 'colname', colname

    series[colname] = pivot_df[column].index.to_pydatetime()
    years_colname = mdates.YearLocator()
    months_colname = mdates.MonthLocator()
    daysFmt_colname = mdates.DateFormatter('%Y')

    fig_colname = plt.figure()
    ax_colname = fig_colname.add_subplot(111)
    ax_colname.plot (series[colname], pivot_df[column], color = 'black')
    # #ax1.plot (pivot_df['Violent crime'], color = 'black') works too

    ax_colname.xaxis.set_major_locator(years_colname)
    ax_colname.xaxis.set_major_formatter(daysFmt_colname)
    ax_colname.xaxis.set_minor_locator(months_colname)

    ax_colname.set_xlabel('Date')
    ax_colname.set_ylabel('# of reported crime')
    ax_colname.set_title("Metropolitan Police:" + str(column))
    
    # #tick_range = np.arange(9000, 15001, 1000)
    # #ax.set_yticks(tick_range)
    # regarding those two comented lines above, I could set a min and max for y range. It would be the right thing to do. But for some of the crimes, the plots wouldnt look good. So I am not doing it this time.


    ax_colname.grid(True)
    # #fig1.tight_layout()

    fig_colname.savefig('./plots/ts_' + str(colname) +'.png', orientation = 'portrait')

    # #####################
    #colname = colname.strip()
    #print 'Saving ts_',colname,'.png'
    print 'Saving ts_'+str(colname)+'.png'

print 'Done! :-)'
plt.show()

# Plot histogram of all data
fig_AllData = plt.figure()
ax_AllData = fig_AllData.add_subplot(111)
key = counter.keys()
value = counter.values()

xs = [i + 0.1 for i, _ in enumerate(key)]
plt.bar (xs, counter.values(), color = 'black')

keyWrap=[textwrap.fill(text,15) for text in key]

plt.xticks([i + 0.5 for i, _ in enumerate(key)], keyWrap, fontsize=10, ha = 'right', rotation = 45)

plt.ylabel('# of reported crime (Dec 2010 to Dec 2016)')
plt.title("Metropolitan Police Reported Crime")
plt.tight_layout()
# add a footnote, this will put text 75 points below the left side of the x-axis
plt.annotate('* Please note that not all crime type have been recorded for the whole period displayed.\n For example, "Other theft" started appearing on the records by the end of 2011, "Violence and sexual offences" by the beginning of 2013.\n This probably shows an effort for detailing the record of crimes over time.', (0,0), (0, -75), xycoords='axes fraction', textcoords='offset points', va='top', fontsize = 8)
plt.savefig('./plots/bar_AllCrime.png', orientation = 'portrait', bbox_inches='tight')
print 'Saved bar_AllCrime.png'


###### Plot all data ino one time series
lines = ["-d","--","-.",":v", "-,", "--o"]
linecycler = cycle(lines)
fig = plt.figure()
fig.subplots_adjust(left = 0.1)
ax = fig.add_subplot(111)
NUM_COLORS = int(len(pivot_df.columns))

for i in range(NUM_COLORS):
    #c = [float(i)/float(NUM_COLORS), 0.0, float(NUM_COLORS-i)/float(NUM_COLORS)] #R,G,B
    plt.plot(pivot_df.ix[:,i], next(linecycler))
    #plt.plot(pivot_df.ix[:,i], color = next(colors))
    #plt.plot(pivot_df.ix[:,i], color = c)
    #
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    # adjusting spacing
    #plt.tight_layout()
#plt.show()
plt.xlabel('Date [Year]')
plt.ylabel('# of reported crime')
fig.savefig('./plots/ts_AllCrime.png', bbox_inches='tight')
