#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file should be called every day from 9.00 pm to 5.00 am

import matplotlib.pyplot as plt
import csv
import math
import datetime
import numpy as np


ROOT = "insert_your_path"
dbList = []
dataList = []
DB_THRESHOLD = 120.0
TIME_ANALYSIS = 6 * 20 #30 # un ora: data are extracted every 10 seconds
PERCENTAGE_GOOD_RESULT = 80

def readData(data):
    with open(data, 'rb') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        for row in data:
            if row == [] or row[0] == "Timeout" or "Stoppe" in row[1] or "Timeou" in row[1]:   # skip delle righe vuote
                pass
            else:           # insert decibel in list
                dbList.append(float(row[1]))
                dataList.append(row[0])

def plotData():
    dataList2 = []
    dbList2 = []
    for i in range(0, len(dataList)):
        if i %8 == 0:
            dataList2.append(dataList[i])

    for j in range(0, len(dbList)):
        if j % 8 == 0:
            dbList2.append(dbList[j])

    plt.plot(dataList, dbList)
    plt.xlabel('time')
    plt.xticks(rotation=90, fontsize=6) # vertical label
    plt.ylabel('decibel')
    plt.title('Decibel gathered data')
    plt.legend()
    #plt.show()
    plt.savefig( ROOT + 'plot_data/' + str(datetime.date.today()) + '.png')

    # clear figure
    plt.clf()
    # semplified decibel gathered data
    plt.plot(dataList2, dbList2)
    plt.xlabel('time')
    plt.xticks(rotation=90, fontsize=6) # vertical label
    plt.ylabel('decibel')
    plt.title('Semplified Decibel gathered data')
    plt.legend()
    #plt.show()
    plt.savefig( ROOT + 'plot_data/semplified_' + str(datetime.date.today()) + '.png')

def analyzeData():
    start_noise_index = 0
    stop_noise_index = 0
    reversedbList = list(reversed(dbList))

    print "MEANS: " + str(math.fsum(dbList)/len(dbList))

    # analyze first peak
    for i in range(0, len(dbList)):
        if dbList[i] >= DB_THRESHOLD: # if we find a decibel >= 120
                dbResult = ScrollListHigher(dbList,i)
                #print str(i) + ")" + str(dbResult)
                if dbResult == -2: # temporal window too small, we don't have enough samples
                    break
                elif dbResult > PERCENTAGE_GOOD_RESULT: # 80%
                    start_noise_index = i # we have found a start noise point
                    break

    # analyze last peak
    for j in range(0, len(reversedbList)):
        #print j + start_noise_index
        if reversedbList[j] <= DB_THRESHOLD: # if we find a decibel >= 120
                dbResult = ScrollListLower(dbList, j)
                #print str(i) + ")" + str(dbResult)
                if dbResult == -2: # temporal window too small, we don't have enough samples
                    break
                elif dbResult > PERCENTAGE_GOOD_RESULT: # 80%
                    stop_noise_index = j + start_noise_index # we have found a stop noise point
                    break

    if start_noise_index == 0 and stop_noise_index == 0:
        print "Noise not found!"
    else:
        print dataList[start_noise_index]
        #print stop_noise_index
        print dataList[len(dbList) - (stop_noise_index + 1)] # we have a reverse index in this case (we used the reverse list)



# return percent of the items >= DB_THRESHOLD as a integer
def ScrollListHigher(dbList, i):
    count_high_db = 0
    try:
        # da 0 a len(dbList)-i -> poi indice = j + i (i praticamente è l'offset)
        for j in range (0, TIME_ANALYSIS ): # slide the list for TIME_ANALYSIS time
            if dbList[j + (i + 1)] >= DB_THRESHOLD:
                count_high_db += 1
    except IndexError:
        # temporal window too small
        return -2
    else:
        #print count_high_db
        return (float(count_high_db) / float(TIME_ANALYSIS)) * 100

# return percent of the items >= DB_THRESHOLD as a integer
def ScrollListLower(dbList, i):
    count_low_db = 0
    try:
        for j in range (0, TIME_ANALYSIS ): # slide the list for TIME_ANALYSIS time
            if dbList[j + (i + 1)] <= DB_THRESHOLD:
                count_low_db += 1
    except IndexError:
        # temporal window too small
        return -2
    else:
        #print count_low_db
        return (float(count_low_db) / float(TIME_ANALYSIS)) * 100

# Bash file generate from ansiweather command weather symbol in a csv file
# this function return a flag based on weather symbol
def analyzeWeather(data):
    weather = ""
    with open(data, 'rb') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        for row in data:
            weather = row[0]

    # delete /r or /n
    weather = weather[0:3]

    weather_filtered = True

    # flag setting based on weather
    if weather == '☀':
        weather_filtered = True
    elif weather == '☽':
        weather_filtered = True
    elif weather == '☁':
        weather_filtered = True
    elif weather == '☔':
        weather_filtered = False
    elif weather == '▒':
        weather_filtered = True
    elif weather == '░':
        weather_filtered = True
    elif weather == '❄':
        weather_filtered = True
    elif weather == '⚡':
        weather_filtered = False

    return weather_filtered



if __name__ == "__main__":
    readData( ROOT + 'meter.csv')

    weath = analyzeWeather( ROOT + "weather.csv")
    plotData()

    # analyze data only if weather permits us
    if weath:
        analyzeData()
