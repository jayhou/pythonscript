import sys
import getopt
import re

def usage():
    print("Usage:")
    print("    -h, --help: Usage.")
    print("    -f, --file: the dump file name (absolute path)")
    print("    -a, --all-listener: list all registered property and package")
    print()
    print("Exameple:")
    print("    car_service_dump_analysis_tools.py -f <path> -a")

def parseAndPrintPackageAndRegister(dumpfile):

    with open(dumpfile, "r") as fileinput:
        with open(dumpfile+"_register","w") as outputfile:
            patten = re.compile('Process: \[[0-9]+\] package: \[[a-z.]+\] Actions:')
            packagePattern = re.compile('\[([a-z_]{1}[a-z0-9]*[\.a-z0-9]+)\]')
            registerRecordPattern = re.compile(' { Pid: [0-9]+ Action:registerListener Time:')#[0-9:\.]*} : { propId = [0-9]+ propName =[A-Z_]+')
            for line in fileinput:
                if patten.findall(line):
                    outputfile.write(str(packagePattern.findall(line)))
                    outputfile.write('\n')
                if registerRecordPattern.findall(line):
                    outputfile.write(line)
    print()

filename = ''
try:
    options,args = getopt.getopt(sys.argv[1:],"f:ha",["help","all-listener",""])
except getopt.GetoptError:
    sys.exit()
for name, value in options:
    if name in ("-f","--file"):
        filename = value
    if name in ("-h","--help"):
        usage()
        sys.exit()
    if name in ("-a","--all-listener"):
        if filename == '':
            print("file for analysis not found, use -f or --file to specify a dump file name!")
            sys.exit()
        parseAndPrintPackageAndRegister(filename)
