import subprocess
import time
import os

def printAndWriteFile(message,  file):
    print(message)
    if file is not None:
        file.write(message + "\n")

def prepareTest(reportFile):
    printAndWriteFile("prepare test....set stay on",reportFile)
    subprocess.call(['adb', 'root'])
    subprocess.call(['adb', 'shell', 'settings put global stay_on_while_plugged_in 3'])

def startSport(reportFile):
    printAndWriteFile("start sport ... ",reportFile)
    subprocess.call(['adb', 'shell', 'am force-stop com.huami.watch.newsport'])
    time.sleep(5)
    subprocess.call(['adb', 'shell', 'am start -a com.huami.watch.sport.action.SPORT_GPS_SEARCH --ei sport_type 1'])

def startTestSportGps():
    filename = r'report_' + time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime()) + r'.txt'
    with open(filename, 'w') as reportFile:
        prepareTest(reportFile)
        failed = False
        test_count = 0
        while failed is False:
            printAndWriteFile("start check logcat...",reportFile)
            p = subprocess.Popen(['adb', 'logcat'],stdout=subprocess.PIPE)
            while p.poll() is None:
                p.stdout.flush()
                line = p.stdout.readline()
                line = line.strip()
                if line:
                    try:
                        linestr = str(line,'utf-8')
                    except UnicodeDecodeError as e:
                        #print('except:', e)
                        continue
                    #print(linestr)
                    if linestr.find("start charging ui from dim") >= 0:
                        print(linestr)
                        startSport(reportFile)
                    if linestr.find("mFlpService connect failed") >=0:
                        print(linestr)
                        printAndWriteFile("Test Failed find -> " + linestr, reportFile)
                        exit(0)
                    if linestr.find("registerForSessionStatus") >= 0:
                        print(linestr)
                        printAndWriteFile('**********  Test Success! *********** test time:' + str(test_count) + ' find -> ' + linestr, reportFile)
                        test_count = test_count + 1
                        printAndWriteFile("reboot device... wait about 20s...", reportFile)
                        subprocess.call(['adb', 'reboot'])
                        time.sleep(20)
                        break

def main():
    print("start test")
    startTestSportGps()

main()
