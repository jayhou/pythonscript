#!/usr/bin/python
__author__ = 'sutr'
"""
Extract RtSportPoint information from Huanghe dump log.
Update info:
2016-5-15: Script created.
"""

import sys


def dump_to_rtSportPoint(argv):
#input_file: input Huang-He dump file
     input_file = argv[1]
     output_file = input_file + '.RtSportPoint.txt'
     fout = open(output_file, 'wt')
     if len(argv) > 2 and argv[2] == '-m':
          format = 1 #matrix format
          fout.write( "timeStamp,index, cadence,altitude,pace,heartRate,heartQuality,heartZone,stepLen,step\n")
     else:
          format = 0 #default     
     
     tag = -1
     lastTime = -1;
     for line in open(input_file, 'rt'):
          line = line.strip('\n')
          if line.find('<---- Heart rate raw data at time') > -1:
               tag = 0
               temp = line.split('time:')
               requestTime = temp[1]
          elif 0 == tag and line.find('<---- data item #') > -1:
               tag = 1
          elif 1 == tag:
               try:
                  data = line.split() #get MinStatistics date
                  
                  strTimeStampRevert = data[0] + ' ' + data[1] + ' ' +  data[2] + ' ' +  data[3]
                  strTimeStamp = data[3] + data[2] + data[1] + data[0]
                  if ((data[3]=='F0') and (data[2]=='F0')):
                      print("fofo has occured %6d" % (int(strTimeStamp, 16) & 0x00ffffff));
                      tag=0;
                      continue;
                  timeStamp = int(strTimeStamp, 16) & 0x00ffffff #second
                  index = int(data[3], 16);
                  #if lastTime >= timeStamp:
                  #    print(lastTime);
                  #else:
                  #    lastTime=timeStamp;
                  strCadence = data[5] + data[4]
                  cadence = int(strCadence, 16) #step count per min.
                  
                  strAltitude = data[7] + data[6]
                  altitude = int(strAltitude, 16) #meter
                  if altitude > 32767: #int16
                      altitude = altitude - 65536                  
                  
                  strPace = data[9] + data[8]
                  pace = int(strPace, 16) #cm per sec.
                  
                  strHeart = data[11] + data[10]
                  heartValues = int(strHeart, 16)
                  heartRate = heartValues & 0xFF
                  heartQuality = (heartValues >> 8) & 0x1F
                  heartZone = heartValues >> 13
                  
                  strStepLen = data[12]
                  stepLen = int(strStepLen, 16) # step length in cm.
                  
                  strStep = data[13]
                  step = int(strStep, 16) #step since last point                  
                  
                  if 1 == format:
                    fout.write( "%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n" %(timeStamp,index,cadence,altitude,pace,heartRate,heartQuality,heartZone,stepLen,step))
                  else:
                    fout.write( "RequestTime:\t%s, " %requestTime)
                    #fout.write( "TimeStamp(str):\t%s %s %s %s, " %(data[0], data[1], data[2], data[3]),
                    fout.write( "TimeStamp(str):\t%s, " %strTimeStampRevert)
                    fout.write( "TimeStamp(int):\t%6d, " %timeStamp)
                    fout.write( "Index(int):\t%3d, " %index)
                    fout.write( "Cadence:\t%3d, " %cadence)
                    fout.write( "Altitude:\t%4d, " %altitude)
                    fout.write( "Pace:\t%4d, " %pace)
                    fout.write( "HeartRate:\t%3d, " %heartRate)
                    fout.write( "HeartQuality:\t%2d, " %heartQuality)
                    fout.write( "HeartZone:\t%1d, " %heartZone)
                    fout.write( "StepLength:\t%3d, " %stepLen)
                    fout.write( "Step:\t%3d\n" %step)
                                                    
                  tag = 0
               except Exception as e:
                  print(e);
                  tag = -1                          
          else:
               tag = -1
     #end for
#end function


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print ('Usage:',sys.argv[0],'input_dump_log [-m]')
        exit(0)
          
    dump_to_rtSportPoint(sys.argv)
