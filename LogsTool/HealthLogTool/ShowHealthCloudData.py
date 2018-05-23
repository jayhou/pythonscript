from urllib import parse,request
import sys
import json
import base64
#TODO: 计算每分钟数据总步数
def get_minites_data(minutes_bytes_data):
    sleep_mode = 0
    sleep_active = 0
    step = 0
    minutes = 0
    line = "\n每分钟数据:\n| min| | time| |mod| |act| |stp|\n"
    total_step_in_bytes = 0
    for index in range (len(minutes_bytes_data)):
        if index % 3 == 0:
            sleep_mode = minutes_bytes_data[index]
        elif index % 3 == 1:
            sleep_active = minutes_bytes_data[index]
        elif index % 3 == 2:
            step = minutes_bytes_data[index]
            total_step_in_bytes += step
        if index % 3 == 2:
            hour = minutes / 60
            min = minutes % 60
            time_str = "%02d:%02d" % (hour,min)
            if (sleep_mode == 126) and (sleep_active == 0) and (step == 0):
                line = line + "|%04d| |%s| |---| |---| |---|\n" % (minutes,time_str)
            else:
                line = line + "|%04d| |%s| |%03d| |%03d| |%03d|\n" % (minutes,time_str,sleep_mode,sleep_active,step)
            minutes = minutes + 1
    line = line + "total steps:%d\n" % (total_step_in_bytes)
    return line
def write_result_to_file(result):
    filepath = "/Users/houjie/Workspace/logs/healthData/" + user_id + "_" + date + "_res.txt"
    print("out put file path:" + filepath)
    result = json.loads(result)
    code = result['code']
    message = result['message']

    data = result['data']
    if len(data) == 0:
        print("服务器上没有数据!!!")
    else:
        dicdata = data[0]
        data_user_id = dicdata['userId']
        data_day = dicdata['day']
        data_device_type = dicdata['deviceType']
        data_device_source = dicdata['deviceSource']

        data_summary = json.loads(dicdata['summary'])

        data_summary_goal = data_summary['goal']
        data_summary_active = data_summary['active']
        data_summary_sit = data_summary['sit']
        data_summary_stp = data_summary['stp']
    #    data_summary_floor_count = data_summary['floor_count']
        data_summary_rhr = data_summary['rhr']
        data_summary_sleep = data_summary['slp']

        heart_rate_raw = dicdata['heartRateData']
        herat_rate_raw_bytes = base64.b64decode(heart_rate_raw)
        data_summary_uuid = dicdata['uuid']
        data_summary_date = dicdata['date_time']
        data_summary_minutes_data = base64.b64decode(dicdata['data'])

        # print("dicdata:" + str(dicdata))
        # print("key data:" + str(data))
        # print("key code:" + str(code))
        # print("key message:" + str(message))
        with open(filepath, 'w') as resFile:
            resFile.write("用户ID:" + str(user_id) + "\n")
            resFile.write("目标步数:" + str(data_summary_goal) + "步\n")
            resFile.write("活动量:" + str(data_summary_active) + "分钟\n")
            resFile.write("坐:" + str(data_summary_sit) + "分钟\n")
    #        resFile.write("爬楼数:" + str(data_summary_floor_count) + "\n")
            resFile.write("静息心率:" + str(data_summary_rhr) + "\n")
            resFile.write("睡眠数据:" + str(data_summary_sleep) + "\n")
            resFile.write("步数详情:" + str(data_summary_stp) + "\n")
            # resFile.write("心率数据:" + heart_rate_raw)

            # resFile.write("心率数据decoded:" + str(herat_rate_raw_bytes))
            resFile.write("心率数据长度:" + str(len(herat_rate_raw_bytes)) + "\n")
            resFile.write("uuid:" + data_summary_uuid + "\n")
            resFile.write("上传日期:" + data_summary_date + "\n")

            # resFile.write("每分钟数据:" + str(data_summary_minutes_data))
            resFile.write("每分钟数据长度:" + str(len(data_summary_minutes_data)) + "\n")
            # resFile.write(" 第一分钟 数据: " + str(int(data_summary_minutes_data[0])) + " " + str(
            #     int(data_summary_minutes_data[1])) + " " + str(int(data_summary_minutes_data[2])))
            # resFile.write("summary:" + str(data_summary))
            resFile.write(get_minites_data(data_summary_minutes_data))
            resFile.write("\n\n" + str(result))
#输出内容:user=admin&password=admin
header_dict = {'User-Agent': 'Mozilla/5.0 (Mac OSX 10.13; Trident/7.0; rv:11.0) like Gecko'}
user_id = sys.argv[1]
date = sys.argv[2]
print("user id:" + user_id)
print("date:" + date)
url='http://midong-algorithm.private.mi-ae.cn/v1/data/band.json?query_type=detail&v=1.0&userid=' + user_id + '&password=xiaomi.comwww.mi.com&device_type=4&from_date='\
    + date + '&to_date=' + date
print("start qurey from url " + url)
req = request.Request(url,headers=header_dict)
res = request.urlopen(req)
res = res.read()
# print(res)
#输出内容(python3默认获取到的是16进制'bytes'类型数据 Unicode编码，如果如需可读输出则需decode解码成对应编码):b'\xe7\x99\xbb\xe5\xbd\x95\xe6\x88\x90\xe5\x8a\x9f'
cloudDatas = res.decode(encoding='utf-8')
write_result_to_file(cloudDatas)
# print(cloudDatas)
#输出内容:登录成功
