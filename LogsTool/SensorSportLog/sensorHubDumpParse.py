#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：sensorHubDumpParse.py
# Author: houjie
import sys

import time


def parse_min_data(filepath):
    print("parse_min_data from:" + filepath)
    outpath = filepath + ".min"
    with open(outpath,'w') as fout:
        with open(filepath) as file:
            tag = -1
            currentTimeInMil = time.time()
            for line in file:
                if line.__contains__(">---- request 12 bytes health"):
                    tag = 0
                elif tag == 0 and line.__contains__("<---- request data: ---->"):
                    tag = 1
                elif tag == 1 and line.__contains__("<---- data item"):
                    tag = 2
                elif tag == 2 and line.__contains__("F0 F0"):
                    lines = line.split()
                    currentTimeInMil = int(lines[5] + lines[4] + lines[3] + lines[2],16) * 60
                    tag = 3
                elif tag == 3 or tag == 4:
                    if(line.__contains__("<---- data item")):
                        continue
                    elif(line.__contains__(">---- release 12 bytes")):
                        tag = -1
                        continue
                    elif(line.split().__len__()!=12):
                        tag = -1
                        continue
                    data = line.split()
                    if tag == 4:
                        currentTimeInMil = currentTimeInMil + 60
                    tag = 4
                    timeArray = time.localtime(currentTimeInMil)
                    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                    if data[6]=='FF':
                        heart = '---'
                    else:
                        heart = str(int(data[6], 16))

                    parsedData = "  Sleep Mode:[" + str(int(data[11],16)) + "],\t"\
                                 + "Sleep Active:[" + str(int(data[10],16)) + "],\t"\
                                 + "Step:[" + str(int(data[5]+data[4],16))+"],\t"\
                                 + "Heart Rate:[" + heart + "]\t<<<<<<<<< from " + line
                    fout.write(otherStyleTime + parsedData)



def parse_gps_dump(filepath):
    print("parse_gps_dump from:" + filepath)
    outpath = filepath + "_gps"
    isStartSport = False
    with open(filepath) as gps_file:
        with open(outpath,'w') as fout:
            for line in gps_file:
                if line.__contains__("<----Start Sport"):
                    if isStartSport == True:
                        fout.write("*******重复开始运动操作！*******\n")
                    isStartSport = True

                if isStartSport == True:
                    fout.write(line)

                if line.__contains__("<----Stop Sport"):
                    if isStartSport == False:
                        fout.write("*******没有开始运动时结束运动操作！*******\n")
                    isStartSport = False

def parse_heart_rate_route(filepath):
    print("parse_heart_rate_route from:" + filepath)


def parse_sport_stat(filepath):
    print("parse_sport_stat from:" + filepath)


def parse_wake_up(filepath):
    print("parse_wake_up from:" + filepath)

if sys.argv[1] == "--gps":
    parse_gps_dump(sys.argv[2])
elif sys.argv[1] == "--heart-route":
    parse_heart_rate_route(sys.argv[2])
elif sys.argv[1] == "--sport-stat":
    parse_sport_stat(sys.argv[2])
elif sys.argv[1] == "--wake-up":
    parse_wake_up(sys.argv[2])
elif sys.argv[1] == "--min-data":
    parse_min_data(sys.argv[2])