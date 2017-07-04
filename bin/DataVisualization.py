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
from bokeh.plotting import figure, output_file, show, save, reset_output
from bokeh.charts import Line, Bar

rcParams['figure.figsize'] = 15, 5


def loadData(path):
    """
    Takes csv files with the following columns: Crime ID, Month, Reported by, Falls within, Longitude, Latitude, Location, LSOA code, LSOA name, Crime type, Last outcome category, Context
    This file will be turned into a DataFrame.

    Args:
        Data path

    Returns:
        Pandas DataFrame.
    """

    # path = r'../data/'
    all_files = glob.glob(os.path.join(path, "*.csv"))
    frame = pd.DataFrame()
    list_ = []

    for file_ in all_files:
        df = pd.read_csv (file_)
        # print "reading ", file_
        list_.append(df)
    frame = pd.concat(list_)

    frame['Time'] = pd.to_datetime(frame['Month'], format = '%Y-%m')
    return frame

def counter_df():
    """
    Takes a data frame and returns a counter object

    Args:
        None

    Returns:
        A python dictionary with key and values, example: Counter({'Anti-social behaviour': 34463, 'Other crime': 28114, 'Violent crime': 11784, 'Burglary': 7897, 'Vehicle crime': 7393, 'Robbery': 2791})
    """

    x = loadData(r'../data/')
    counter = Counter(x['Crime type'])
    return counter

def pivot_df():
    """
    Takes a data frame and returns a pivot DataFrame.

    Args:
        None

    Returns:
        Pandas DataFrame formatted as a pivot table. Example: Time Crime type  Anti-social behaviour  Burglary  Other crime  Robbery
    """

    x = loadData(r'../data/')
    groupedFrame = x.groupby(['Time', 'Crime type']).size().reset_index(name='Frequency')
    df = pd.DataFrame(groupedFrame)
    print df
    # this is beautiful!
    pivot_df = df.pivot_table('Frequency', ['Time'], 'Crime type')
    return pivot_df

def TimeSeries(data):
    """
    This function generates time series of each crime reported.

    Args:
        data: pandas DataFrame instance.

    Returns:
        Time series that will be saved at a ../plots directory

    To do:
        Ckeck if plots directory exists, if it does not, create it.
    """

    series = dict()

    for column in data:

        #remove whitespace from column
        pattern = re.compile(r'\s+')
        colname = re.sub(pattern, '', column)

        #  DatatimeIndex as object
        series[colname] = data[column].index.to_pydatetime()
        years_colname = mdates.YearLocator()
        months_colname = mdates.MonthLocator()
        daysFmt_colname = mdates.DateFormatter('%Y')

        fig_colname = plt.figure()
        ax_colname = fig_colname.add_subplot(111)
        ax_colname.plot (series[colname], data[column], color = 'black')
        # #ax1.plot (data['Violent crime'], color = 'black') works too

        ax_colname.xaxis.set_major_locator(years_colname)
        ax_colname.xaxis.set_major_formatter(daysFmt_colname)
        ax_colname.xaxis.set_minor_locator(months_colname)

        ax_colname.set_xlabel('Date')
        ax_colname.set_ylabel('# of reported crime')
        ax_colname.set_title("Metropolitan Police:" + str(column))

        # #tick_range = np.arange(9000, 15001, 1000)
        # #ax.set_yticks(tick_range)
        # regarding those two comented lines above, I could set a min and max for y range. It would be a good thing to do as all the plots would show the same range fro y axis. But for some of the crimes, the plots wouldnt look good. So I am not setting up y axis this time.


        ax_colname.grid(True)

        fig_colname.savefig('../plots/ts_' + str(colname) +'.png', orientation = 'portrait')

        print 'Saving ts_'+str(colname)+'.png'

    print 'Done! :-)'

def BarPlot(data):
    """
    This function generates bar plot showing the number of reported crimes.

    Args:
        data: dictionary object.

    Returns:
        Bar plot that will be saved at a ../plots directory

    To do:
        Ckeck if plots directory exists, if it does not, create it.
    """

    fig_AllData = plt.figure()
    ax_AllData = fig_AllData.add_subplot(111)
    key = data.keys()
    value = data.values()

    # we only want the indexes
    # bar width by default is 0.8. I add 0.1 to the left coordinates, so each bar is centered
    xs = [i + 0.1 for i, _ in enumerate(key)]
    plt.bar (xs, data.values(), color = 'black')

    keyWrap=[textwrap.fill(text,15) for text in key]

    plt.xticks([i + 0.5 for i, _ in enumerate(key)], keyWrap, fontsize=10, ha = 'right', rotation = 45)

    plt.ylabel('# of reported crime (Dec 2010 to Dec 2016)')
    plt.title("Metropolitan Police Reported Crime")
    plt.tight_layout()
    # add a footnote, this will put text 75 points below the left side of the x-axis
    plt.annotate('* Please note that not all crime type have been recorded for the whole period displayed.\n For example, "Other theft" started appearing on the records by the end of 2011, "Violence and sexual offences" by the beginning of 2013.\n This probably shows an effort for detailing the record of crimes over time.', (0,0), (0, -75), xycoords='axes fraction', textcoords='offset points', va='top', fontsize = 8)
    plt.savefig('../plots/bar_AllCrime.png', orientation = 'portrait', bbox_inches='tight')
    print 'Saved bar_AllCrime.png'

def Bokeh_TimeSeries():
    """
    This function generates time series of each crime reported.

    Args:
        None

    Returns:
        Time series that will be saved at a ../plots directory

    To do:
        Ckeck if plots directory exists, if it does not, create it.
    """
    df = pivot_df()
    series = dict()

    for column in df:

        output_file("../plots/ts_" + column + ".html", title="Metropolitan Police: " + str(column))

        #remove whitespace from column
        pattern = re.compile(r'\s+')
        colname = re.sub(pattern, '', column)

        #  DatatimeIndex as object
        series[colname] = df[column].index.to_pydatetime()

        p = figure(width=1600, height=350, x_axis_type="datetime")
        p.line(series[colname], df[column], color='navy')


        p.title.text = "Metropolitan Police:" + str(column)
        p.title.text_font_size = "25px"
        p.title.align = "center"
        p.grid.grid_line_alpha=1
        p.xaxis.axis_label = 'Date'
        p.yaxis.axis_label = '# of reported crime'

        save(p)
        print 'Saving ts_'+str(colname)+'.html'


    print 'Done! :-)'


# data = counter_df()
# BarPlot(data)

# data = pivot_df()
# TimeSeries(data)

# Bokeh_TimeSeries()