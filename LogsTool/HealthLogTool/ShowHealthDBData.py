import sqlite3
import sys
import time


def get_minites_data(minutes_bytes_data):
    sleep_mode = 0
    sleep_active = 0
    step = 0
    heart_rate = 0
    minutes = 0
    if minutes_bytes_data == None:
        line = "没有数据！"
        return line

    line = "\n每分钟数据:\n| min| |   date   | | time| |mod| |act| |stp| |hrt|\n"
    total_step_in_bytes = 0
    for index in range (len(minutes_bytes_data)):
        if index % 12 == 11:
            sleep_mode = minutes_bytes_data[index]
        elif index % 12 == 10:
            sleep_active = minutes_bytes_data[index]
        elif index % 12 == 4:
            step = minutes_bytes_data[index]
            if step!=255:
                total_step_in_bytes += step
        elif index % 12 == 6:
            heart_rate = minutes_bytes_data[index]
        if index % 12 == 11:
            hour = minutes / 60
            min = minutes % 60
            time_str = "%02d:%02d" % ((hour)%24,min)
            if (sleep_mode == 126 ) and (sleep_active == 0) and (step == 0):
                line = line + "|%04d| |%s| |---| |---| |---|\n" % (minutes,time_str)
            else:
                line = line + "|%04d| |%s| |%s| |%03d| |%03d| |%03d| |%03d|\n" % (minutes,sys.argv[2],time_str,sleep_mode,sleep_active,step,heart_rate)
            minutes = minutes + 1
    line = line + "total steps:%d\n" % (total_step_in_bytes)
    return line

with open(sys.argv[1]+".db.res",'w') as resFile:
    if sys.argv.__len__() <= 1:
        print("非法参数输入")
        print("Usage:")
        print("./ShowHealthDBData.py <dbfile_path> <2018-04-17>")
    else:
        dbfile = sys.argv[1]
        formatedDate = sys.argv[2]
        timestamp = time.mktime(time.strptime(formatedDate,"%Y-%m-%d"))
        date = (int)(timestamp/60/60/24) + 1;
        resFile.write("数据库文件：" + dbfile + " 查询日期:" + formatedDate + " 数据库date:" + str(date) + "\n")

        # test.db is a file in the working directory
        conn = sqlite3.connect(dbfile)
        c = conn.cursor()

        # create tables
        sql = "select data from dailymotion where date = " + str(date) + " or date = " + str(date-1) + " order by date asc"
        resFile.write("SQL:" + sql + "\n")
        c.execute(sql)
        fetchrow = c.fetchone()
        if fetchrow == None:
            row1 = None
        else:
            row1 = fetchrow[0]
        fetchrow = c.fetchone()
        if fetchrow == None:
            row2 = None
        else:
            row2 = fetchrow[0]
        res1 = None
        res2 = None
        if(row1==None):
            bytelist = []
            for index in range(480 * 12):
                bytelist.append(255)
            res1 = bytearray(bytelist)
        else:
            res1 = row1[960*12:]
        if row2 != None:
            res2 = row2[:960*12]
        else:
            bytelist = []
            for index in range(960 * 12):
                bytelist.append(255)
            res2 = bytearray(bytelist)

        raw_data = res1+res2

        line = get_minites_data(raw_data)
        resFile.write(line)


        # close the connection with the database
        conn.close()