import sys

def start():
    sourceLogFile = sys.argv[1]
    dataSetOutputFile = sourceLogFile + ".data"
    print("logfile:" + sys.argv[1])
    print("output as:" + dataSetOutputFile)
    with open(sourceLogFile, 'r') as inputFile:
        with open(dataSetOutputFile, 'w') as outputFile:
            while True:
                try:
                    inputline = inputFile.readline()
                    break;
                except UnicodeDecodeError as e:
                    print(e)

            datasetline= ""
            while inputline:
                #print(inputline)
                if inputline.find("gps_alg_jni: before filter:") >= 0:
                    print(inputline)
                    strings = inputline.split('filter:')
                    print(strings[1])
                    datasetline = strings[1]
                    datasetline = datasetline.replace('\n',"")
                    datasetline = datasetline.replace('\r',"")

                if inputline.find("gps_alg_jni: after filter:") >= 0:
                    print(inputline)
                    strings = inputline.split('filter:')
                    print(strings[1])
                    afterstring = strings[1].split(',')
                    if sys.argv[2] == 1:
                        outputFile.write('{' + datasetline + ',' + afterstring[1] + ',' + afterstring[2].replace('\n','') + '},' + '\n')
                    else:
                        outputFile.write(datasetline + ',' + afterstring[1] + ',' + afterstring[2])

                try:
                    inputline = inputFile.readline()
                except UnicodeDecodeError as e:
                    pass


start()