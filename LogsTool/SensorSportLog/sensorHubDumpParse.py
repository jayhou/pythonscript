#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：sensorHubDumpParse.py
# Author: houjie
import sys
import re
import time


def parse_min_data(filepath):
    print("parse_min_data from:" + filepath)
    totalStep = 0
    outpath = filepath + ".min"
    with open(outpath,'w') as fout:
        with open(filepath) as file:
            currentTimeInSec = 0;
            mindataPatten = re.compile('([0-9A-F][0-9A-F]\s){12}')
            headerPatten = re.compile('(F0\s){2}([0-9A-F][0-9A-F]\s){10}')
            requestPatten = re.compile('.?12\sbytes\shealth')
            date = ""
            for line in file:
                if requestPatten.findall(line):
                    print("" + line)
                    fout.write(line)
                if mindataPatten.findall(line):
                    print("find:" + line)
                    if headerPatten.findall(line):
                        lines = line.split()
                        currentTimeInSec = int(lines[5] + lines[4] + lines[3] + lines[2],16) * 60
                    else:
                        if currentTimeInSec == 0:
                            print("error, miss header!")
                            return
                        data = line.split()
                        timeArray = time.localtime(currentTimeInSec)
                        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                        lastDate = date
                        date = time.strftime("%Y-%m-%d",timeArray)
                        if lastDate == "":
                            lastDate = date
                        if date != lastDate:
                            print("date changed! clear total step!")
                            fout.write(">>>>   " + lastDate + " total step:" + str(totalStep) + "   <<<<\n\n")
                            totalStep = 0
                        if data[6]=='FF':
                            heart = '---'
                        else:
                            heart = str(int(data[6], 16))

                        parsedData = "  Sleep Mode:[" + str(int(data[11],16)) + "],\t"\
                                     + "Sleep Active:[" + str(int(data[10],16)) + "],\t"\
                                     + "Step:[" + str(int(data[5]+data[4],16))+"],\t"\
                                     + "Heart Rate:[" + heart + "]\t<<<<<<<<< from " + line
                        lastTotalStep = totalStep
                        totalStep += int(data[5]+data[4],16)
                        if lastTotalStep != totalStep:
                            fout.write("\ntotal step update from " + str(lastTotalStep) + " -> " + str(totalStep) + '\n')
                        fout.write(otherStyleTime + parsedData)
                        currentTimeInSec = currentTimeInSec + 60
            fout.write(">>>>   " + lastDate + " total step:" + str(totalStep) + "   <<<<\n\n")
            totalStep = 0



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