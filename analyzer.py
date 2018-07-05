#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file should be called every day from 9.00 pm to 5.00 am

import matplotlib.pyplot as plt
import csv
import math
import datetime
import numpy as np

#Viene estratto un campione di db ogni 10 secondi
ROOT = "/home/monti/.soundmeter/"
dbList = []
dataList = []
DB_THRESHOLD = 120.0
TIME_ANALYSIS = 6 * 20 #30 # un ora: i campioni sono estratti ogni 10 secondi
PERCENTAGE_GOOD_RESULT = 80

def readData(data):
    with open(data, 'rb') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        for row in data:
            if row == [] or row[0] == "Timeout" or "Stoppe" in row[1] or "Timeou" in row[1]:   # skip delle righe vuote
                pass
            else:           # inserisci i db nella lista
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
    plt.xticks(rotation=90, fontsize=6) # label in verticale
    plt.ylabel('decibel')
    plt.title('Decibel gathered data')
    plt.legend()
    #plt.show()
    plt.savefig( ROOT + 'plot_data/' + str(datetime.date.today()) + '.png')

    # clear della figura
    plt.clf()
    # semplified decibel gathered data
    plt.plot(dataList2, dbList2)
    plt.xlabel('time')
    plt.xticks(rotation=90, fontsize=6) # label in verticale
    plt.ylabel('decibel')
    plt.title('Semplified Decibel gathered data')
    plt.legend()
    #plt.show()
    plt.savefig( ROOT + 'plot_data/semplified_' + str(datetime.date.today()) + '.png')

def analyzeData():
    start_noise_index = 0
    stop_noise_index = 0
    reversedbList = list(reversed(dbList))

    print "MEDIA: " + str(math.fsum(dbList)/len(dbList))

    # quando inizia la baracca?
    for i in range(0, len(dbList)):
        if dbList[i] >= DB_THRESHOLD: # se troviamo un db >= 120
                dbResult = ScrollListHigher(dbList,i)
                #print str(i) + ")" + str(dbResult)
                if dbResult == -2: # finestra temporale troppo piccola, quindi non abbiamo campioni a sufficienza
                    break
                elif dbResult > PERCENTAGE_GOOD_RESULT: # 80%
                    start_noise_index = i # abbiamo trovato un punto di inizio della festa
                    break

    # quando finisce la baracca?

    for j in range(0, len(reversedbList)):
        #print j + start_noise_index
        if reversedbList[j] <= DB_THRESHOLD: # se troviamo un db <= 120
                dbResult = ScrollListLower(dbList, j)
                #print str(i) + ")" + str(dbResult)
                if dbResult == -2: # finestra temporale troppo piccola, quindi non abbiamo campioni a sufficienza
                    break
                elif dbResult > PERCENTAGE_GOOD_RESULT: # 80%
                    stop_noise_index = j + start_noise_index # abbiamo trovato un punto di inizio della festa
                    break

    if start_noise_index == 0 and stop_noise_index == 0:
        print "Non hanno fatto festa"
    else:
        print dataList[start_noise_index]
        #print stop_noise_index
        print dataList[len(dbList) - (stop_noise_index + 1)] # l'indice è riferito alla lista reverse quindi l'indice è di questo tipo



# return percent of the items >= DB_THRESHOLD as a integer
def ScrollListHigher(dbList, i):
    count_high_db = 0
    try:
        # da 0 a len(dbList)-i -> poi indice = j + i (i praticamente è l'offset)
        for j in range (0, TIME_ANALYSIS ): # scorriamo la lista in un ora di campionamenti
            if dbList[j + (i + 1)] >= DB_THRESHOLD:
                count_high_db += 1
    except IndexError:
        # Finestra temporale troppo piccola
        return -2
    else:
        #print count_high_db
        return (float(count_high_db) / float(TIME_ANALYSIS)) * 100

# return percent of the items >= DB_THRESHOLD as a integer
def ScrollListLower(dbList, i):
    count_low_db = 0
    try:
        for j in range (0, TIME_ANALYSIS ): # scorriamo la lista in mezzora di campionamenti
            if dbList[j + (i + 1)] <= DB_THRESHOLD:
                count_low_db += 1
    except IndexError:
        # Finestra temporale troppo piccola
        return -2
    else:
        #print count_low_db
        return (float(count_low_db) / float(TIME_ANALYSIS)) * 100

# in bash lanciamo ansiweather e creiamo il file csv con il simbolo del meteo a Bologna (quello che ritorna in output il comando).
# tale funzione dovrà convertire il simbolo in
def analyzeWeather(data):
    weather = ""
    with open(data, 'rb') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        for row in data:
            weather = row[0]

    # elimino /r oppure /n
    weather = weather[0:3]

    weather_filtered = True

    # setto un flag in base al tempo che il meteo mi ritorna
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

    #analizzo i dati solamente se il tempo lo permette
    if weath:
        analyzeData()
