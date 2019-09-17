import subprocess
import time

def printAndWriteFile(message,  file):
    print(message)
    if file is not None:
        file.write(message + "\n")

def prepareTest(reportFile):
    printAndWriteFile("prepare test....set stay on",reportFile)
    subprocess.call(['adb', 'root'])
    subprocess.call(['adb', 'shell', 'settings put global stay_on_while_plugged_in 3'])
    subprocess.call(['adb', 'logcat', '-c'])
    subprocess.call(['adb', 'shell', 'setprop prop.sys.show_chargingui false'])

def startSport(reportFile):
    printAndWriteFile("start sport ... ",reportFile)
    subprocess.call(['adb', 'shell', 'am force-stop com.huami.watch.newsport'])
    time.sleep(5)
    subprocess.call(['adb', 'shell', 'am start -a com.huami.watch.sport.action.SPORT_GPS_SEARCH --ei sport_type 1'])

def startTest():
    filename = r'wifi_report_' + time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime()) + r'.txt'
    with open(filename, 'w') as reportFile:
        prepareTest(reportFile)
        failed = False
        test_count = 0
        reboot_time_stamp = int(time.time())
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
                    if linestr.find("setWifiEnable") >=0:
                        print(linestr)
                    if linestr.find("Failed to load WiFi driver") >=0:
                        print(linestr)
                        printAndWriteFile("Test Failed find -> " + linestr, reportFile)
                        exit(0)
                    else:
                        current = int(time.time())
                        if current - reboot_time_stamp > (3 * 60):
                            test_count = test_count + 1
                            printAndWriteFile("Test count:" + str(test_count), reportFile)
                            printAndWriteFile("Test Succuss reboot interval" + str(current - reboot_time_stamp), reportFile)
                            subprocess.call(['adb', 'reboot'])
                            reboot_time_stamp = current

def main():
    print("start test >>>>>>>")
    startTest()

main()
