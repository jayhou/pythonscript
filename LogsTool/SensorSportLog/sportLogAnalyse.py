#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：sportLogAnalyse.py
# Author: houjie
import sys
import re
from os import path


def format_hearrate_channel_Data(filepaths):
    print(filepaths)
    hfilepath = filepaths + ".heartchannel"
    with open(hfilepath,'w') as hfile:
        with open(filepaths) as file:
            for line in file:
                if line.__contains__("new RtSportPoint"):
                    rtSportPoints = line.split(',')
                    rtSportPointAltitude = "RtSportPoint altitude:" + rtSportPoints[2] + "\n"
                    hfile.write(rtSportPointAltitude)
                if line.__contains__("alt1"):
                    alt1s = line.split(',')
                    alt1Alt = "alt1 altitude:" + alt1s[2] + "\n"
                    hfile.write(alt1Alt)
                if line.__contains__("alt2:"):
                    alt2s = line.split(',')
                    alt2 = alt2s[0] + "\n"
                    hfile.write(alt2)
                if line.__contains__("altcheck:"):
                    hfile.write(line)




def format_simulation_data_from_logs(filepaths):
    print(filepaths)
    dfilepaths = filepaths + "_sdata"
    filedir = path.dirname(filepaths) + "/input_mini.h"
    print(dfilepaths)
    tag_printed = False
    with open(dfilepaths, "w") as dfile:
        with open(filepaths) as file:
            dataLen = 0;
            array_values = ""
            for line in file:
                if line.__contains__('fb:dat1'):
                    #数据长度
                    dataLen = dataLen+1
                    #转换 '52s,fb:dat1,23422,0,0,5000,0,120' 为一个 {23422,0,0,5000,120}
                    index = line.find('fb:dat1')
                    sline = line[index+8:line.__len__()-1]
                    if tag_printed == False:
                        tag_printed = True
                        #第一行打出{23422,0,0,5000,120}数据的含义
                        print("{speed,watts,altitude,rri,steps,hr}\n")
                    sline = '{'+sline + '},\n'
                    #转换完
                    print(sline)
                    array_values = array_values + sline
                    # dfile.write(sline)
                if line.__contains__('fb:cf2'):
                    #从fb:cf2,33,180,85,2,50,0,187,0,0,16,1中提取出配置值
                    newline = line.replace('\n','')
                    words = newline.split(',')
                    codes = "\n****replace/home/jayhou/LShell/FirstBeatSim/delivery-20170814/ete/examples/analyzerExample/mini.c-parts-below-****\n\n" \
                    + "    // *******************************************************************************\n" \
                    + "    // PHASE 2: Setting ETE background parameters.\n" \
                    + "    // *******************************************************************************\n" \
                    + "    fbt_vars.AC               = " + words[5] + ';\n' \
                    + "    fbt_vars.age              = " + words[1] + ';\n' \
                    + "    fbt_vars.height           = " + words[2] + ';\n' \
                    + "    fbt_vars.weight           = " + words[3] + ';\n' \
                    + "    fbt_vars.gender           = " + words[4] + ';\n' \
                    + "    fbt_vars.minHr            = " + words[6] + ';\n' \
                    + "    fbt_vars.maxHr            = " + words[7] + ';\n' \
                    + "    fbt_vars.maxMET           = " + words[8] + ';\n' \
                    + "    fbt_vars.resourceRecovery = " + words[9] + ';\n' \
                    + "    fbt_vars.monthlyLoad      = " + words[10] + ';\n\n'

                    print(words)
                    print(codes)
                    dfile.write(str(words) + "\n")
                    dfile.write(codes)
                if line.__contains__('fb:cf3'):
                    #从fb:cf3,0,0,0,0,0中提取出配置值
                    newline = line.replace('\n','')
                    words = newline.split(',')
                    codes = "\n **** replace /home/jayhou/LShell/FirstBeatSim/delivery-20170814/ete/examples/analyzerExample/mini.c part below-****\n\n" \
                    + "    // *******************************************************************************\n" \
                    + "    // PHASE 3: Setting exercise plan for real time guidance (Optional).\n" \
                    + "    // *******************************************************************************\n" \
                    + "    fbt_exercise.TE = " + words[1] + ';\n' \
                    + "    fbt_exercise.repeats = 0;\n" \
                    + "    fbt_exercise.distance = " + words[2] + ';\n' \
                    + "    fbt_exercise.warmupTime = 0;\n" \
                    + "    fbt_exercise.workTime = 0;\n" \
                    + "    fbt_exercise.restTime = 0;\n" \
                    + "    fbt_exercise.coolTime = 0;\n\n";
                    print(str(words) + '\n')
                    print(codes)
                    dfile.write(str(words) + '\n')
                    dfile.write(codes)
            print("len : " + str(dataLen))
#\n***** 以下代码 替换仿真程序 /home/jayhou/LShell/FirstBeatSim/delivery-20170814/ete/examples/analyzerExample/input_mini.h 中对应的内容 *****\n\n\
            with open(filedir,'w') as h_file:
                h_file.write("\
/**\n\
 * @brief Structure for ACC data.\n\
 */\n\
typedef struct {\n\
    /**\n\
     * @brief Values for X axis.\n\
     */\n\
    int16 x;\n\
    /**\n\
     * @brief Values for Y axis.\n\
     */\n\
    int16 y;\n\
    /**\n\
     * @brief Values for Z axis.\n\
     */\n\
    int16 z;\n\
} example_acc;\n\
\n\
/**\n\
 * @ brief Structure for speed, power, alti, rri, steps and hr data. \n\
 */\n\
typedef struct {\n\
    /**\n\
     * @ brief Values for speed (meters / second). \n\
     */\n\
    fxint speed;\n\
\n\
    /**\n\
     * @brief Values for cycling power (watts).\n\
     */\n\
    fxint power;\n\
\n\
    /**\n\
     * @brief Values for altitude (meters)).\n\
     */\n\
    fxint alti;\n\
\n\
    /**\n\
     * @brief Values for beat-to-beat interval (milliseconds)).\n\
     */\n\
    uint16 rri;\n\
\n\
    /**\n\
     * @brief Values for step rate(steps / minute).\n\
     */\n\
    uint8 steps;\n\
\n\
    /**\n\
     * @brief Values for heart rate(beats / minute)).\n\
     */\n\
    uint8 hr;\n\
} example_data;\n\
\n\
/**\n\
 * @brief Sampling rate 12.5 Hz.\n\
 */\n\
fxint input_fs = 0;\n\
\n\
/**\n\
 * @brief Length of input_acc_01 array.\n\
 */\n\
const uint32 input_acc_length = 0;\n\
\n\
/**\n\
 * @brief The actual acceleration data for x, y, and z axes.\n\
 */\n\
const example_acc input_acc[1] = {{0}};\n\
\n\
/**\n\
 * @brief Length of input_data_01 array.\n\
 */\n\
const uint32 input_data_length = %d;\n\
\n\
/**\n\
 * @brief The actual data for speed, power, alti, rri, steps and hr.\n\
 */\n\
const example_data input_data[%d] = {\n\
%s\
};\
" % (dataLen,dataLen,array_values))

def show_first_beat_logs(filepaths):
    print(filepaths)
    wfilepaths = filepaths + "_fb"
    wfilepath_csv = filepaths + ".csv"
    print(wfilepaths)
    with open(wfilepaths,'w') as wfile:
        min_heart_rate = 1000;
        max_heart_rate = -1;
        with open(filepaths) as file:
            with open(wfilepath_csv,'w') as csv_file:
                csv_file.write("fb,ETEcorrectedHr,ETEtrainingEffect,ETEenergyExpenditureCumulative, \
                  ETEmaximalMET,  ETEmaximalMETminutes,  ETEresourceRecovery, \
                  ETEdailyPerformance,  ETEminimalHr,  ETEmaximalHr, \
                  ETEphraseNumber,  ETEphraseVariable[0],  ETEphraseVariable[1]\r\n")
                for line in file:
                    if line.__contains__('fb:'):
                        #这里处理 fb:被放在上一行末尾，没有正确换行的部分
                        # speed,1,0.000,0.000,0.925,59s,fb:dat1,0,0,0,5000,82,73
                        # -> 59s,fb:dat1,0,0,0,5000,82,73
                        index = line.find('fb:')
                        if index > 4:
                            print(line)
                            sline = line.find('fb:')
                            if line[sline-4] == ',':
                                line = line[sline-3:line.__len__()-1]
                            else:
                                line = line[sline-4:line.__len__()]
                            print(line)
                        #处理完

                        words = line.split(",")
                        if line.__contains__("dat1"):
                            if words.__len__() < 8:
                                wfile.writelines(line)
                                continue
                            try:
                                newline = "\r\n" + line + " >> " + "FirstBeat Input " + " Speed:" + words[2] \
                                          + " | watts:" + words[3] \
                                          + " | altitude:" + words[4] \
                                          + " | rri:" + words[5] \
                                          + " | steps:" + words[6] \
                                          + " | Heart Rate:" + words[7]
                                if min_heart_rate > int(words[7]):
                                    min_heart_rate = int(words[7])
                                if max_heart_rate < int(words[7]):
                                    max_heart_rate = int(words[7])
                            except Exception as e:
                                print(e)
                                continue

                        elif line.__contains__("fb:tha"):
                            newline = line + " >> " + " vo2max trend"
                        elif line.__contains__("fb:res1"):
                            newline = line
                            csv_file.write(line)
                            if words.__len__() < 10:
                                wfile.writelines(newline)
                                continue
                            newline = line + " >> " + "FirstBeat Output " + " ETEmaximalMET:" + words[4] \
                            + " | ETEmaximalMETminutes:" + words[5] \
                            + " | ETEminimalHr:" + words[8] \
                            + " | ETEmaximalHr:" + words[9] + "\r\n"
                        elif line.__contains__("fb:cf2"):
                            newline = line + " >> " + " Age: " + words[1] \
                            + " | Height: " + words[2] \
                            + " | Weight: " + words[3] \
                            + " | Gender: " + words[4] \
                            + " | AC: " + words[5] \
                            + " | MinHr: " + words[6] \
                            + " | MaxHr: " + words[7] \
                            + " | MaxMET: " + words[8] \
                            + " | ResourceRecovery: " + words[9] \
                            + " | MonthlyLoad: " + words[10] \
                            + " | SportType:" + words[11]

                        else:
                            newline = line
                        wfile.writelines(newline)
        wfile.write("Max Heart Rate:" + str(max_heart_rate) + "   Min Heart Rate:" + str(min_heart_rate))


def show_od_logs(filepaths):
    print(filepaths)
    wfilepaths = filepaths + "_"
    print(wfilepaths)
    with open(wfilepaths,'w') as wfile:
        with open(filepaths) as file:
            for line in file:
                if line.__contains__('od,'):
                    words = line.split(',')
                    lineWordsCount = words.__len__()
                    if words.__len__() < 15:
                        print(line)
                    #以数字开头，以's'结尾
                    if re.match(r'^[0-9][0-9]*s$',words[0]):
                        if lineWordsCount >= 15:
                            newline = "  Running Seconds:" + words[0] + ' | ' + "Timestamp:" + words[1] \
                                  + " | " + " GPSfromNMEA TS:" + words[3] + " | " + "[" + words[4] + "," + words[5] + "]" \
                                  + " | " + " GPSPoint Speed:" + words[6] \
                                  + " | " + " Step Frequence:" + words[7]
                            newline += " | " + " mSportAcm.mDistance:" + words[8] \
                                       + " | " + " gGPSPoint.mPointType:" + words[9] \
                                       + " | " + " result:" + words[10] \
                                       + " | " + " PACE_SM_TO_MK * gSportStat.mRealtimeAvg.mPace:" + words[14] + '\r\n'
                        if words[0] == "00s":
                            newline = "\r\n\r\n" + newline
                        else:
                            newline = line.replace(","," | ");
                    else:
                        newline = "\t\t | " + line
                    wfile.write(newline)
                    for index in range(len(newline)):
                        wfile.write('-')
                    wfile.write('\r\n')


#main start
"""
--od 
--fb 输出fb信息 算法输入输出信息
--format-sim-data 根据log输出仿真用的代码
--heart-channel
"""
if sys.argv[1] == "--od":
    show_od_logs(sys.argv[2])
elif sys.argv[1] == "--fb":
    show_first_beat_logs(sys.argv[2])
elif sys.argv[1] == "--format-sim-data":
    format_simulation_data_from_logs(sys.argv[2])
elif sys.argv[1] == "--heart-channel":
    format_hearrate_channel_Data(sys.argv[2])
