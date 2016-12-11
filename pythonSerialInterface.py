import serial
import particlefilter
import numpy as np
import json

port = 'COM14'
ser = serial.Serial(port,115200)

listOfReadings = []
while True:
    line = ser.readline() #'sonarreading;echange in m'
    sonarReading = float(line[0:line.index(',')])
    cutline = line[line.index(',')+1:len(line)]
    echangeReading = float(cutline[0:cutline.index(',')])
    user = int(input('Save? '))
    if(user == 1):
        listOfReadings.append(sonarReading)
        print(sonarReading)
    elif(user == 2):
        json.dump(listOfReadings, open("readings.list",'w'))
        break
    # print sonarReading
