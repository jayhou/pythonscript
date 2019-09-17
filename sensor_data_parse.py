#!/usr/bin/python
__author__ = 'Kivy Xian'
import struct
import sys

def process_data(header_ushort, data_ushort, data_len):
    global sf
    global mag_time, ppg_time_flag, ppg_time, a_g_time
    global sensor_type_mag, sensor_type_ppg, sensor_type_a_g, sensor_type_acc

    sensor_type = header_ushort[4]
    file_handle = get_file_handle(sensor_type)
    single_data_len = get_data_len(sensor_type)
    data_num = data_len / single_data_len

    for i in range(0, data_num):
        if sensor_type == sensor_type_mag or sensor_type == sensor_type_acc:
            if data_ushort[4 * i + 0] == -1 and data_ushort[4 * i + 1] == -1:
                mag_time = gen_uint_from_ushort(data_ushort[4 * i + 2], data_ushort[4 * i + 3])
            else:
                bytes_w = struct.pack("Is H2s H H H \n",  mag_time, 's', data_ushort[4 * i + 3], 'ms',  data_ushort[4 * i + 0],
                data_ushort[4 * i + 1], data_ushort[4 * i + 2])
        elif sensor_type == sensor_type_ppg:
            if data_ushort[2 * i + 0] == -1 and data_ushort[2 * i + 1] == -1:
                ppg_time_flag = 1
            elif ppg_time_flag == 1:
                ppg_time = gen_uint_from_ushort(data_ushort[2 * i + 0], data_ushort[2 * i + 1])
                ppg_time_flag = 0
            else:
                bytes_w = struct.pack("Is H2s H \n", ppg_time, 's', data_ushort[2 * i + 1], 'ms', data_ushort[2 * i + 0])
        elif sensor_type == sensor_type_a_g:
            if data_ushort[7 * i + 0] == -1 and data_ushort[7 * i + 1] == -1 and data_ushort[7 * i + 2] == -1 \
                and data_ushort[7 * i + 3] == -1 and data_ushort[7 * i + 4] == -1:
                    a_g_time = gen_uint_from_ushort(data_ushort[7 * i + 5], data_ushort[7 * i + 6])
            else:
                bytes_w = struct.pack("Is H2s H H H H H H \n", a_g_time, 's', data_ushort[7 * i + 6],'ms', data_ushort[7 * i + 0],
                        data_ushort[7 * i + 1], data_ushort[7 * i + 2], data_ushort[7 * i + 3], data_ushort[7 * i + 4], data_ushort[7 * i + 5])

        sf.write(bytes_w)

if sys.argv.__len__() > 1:
    src_file = sys.argv[1]

sf = open(src_file, "rb")
ppg_f = open("./ppg.txt", "w+")
mag_f = open("./mag.txt", "w+")
acc_f = open("./acc.txt", "w+")
acc_gyro_f = open("./acc_gyro.txt", "w+")
header_len = 14
header_magic = 0xA5B6
header_magic_high = 0xA5
sensor_type_acc = 1
sensor_type_ppg = 2
sensor_type_mag = 7
sensor_type_a_g = 8
acc_time = 0
ppg_time = 0
mag_time = 0
a_g_time = 0
ppg_time_flag = 0

header = sf.read(header_len)

for b in header:
	print(b)
temp_uc_1 = header[0];
temp_uc = struct.unpack('B'*len(header), header)
print("data0 = %s \n" % header)

if header[0] == header_magic_high:
    byte_endian = '>'
else:
    byte_endian = '<'

header_ushort = struct.unpack(byte_endian +'H'*(len(header)//2), header)
print("magic = %x, len = %x,src_file = %s \n" % (header_ushort[0], header_ushort[6], src_file))

while (header_ushort[0] == header_magic):
    data = sf.read(header_ushort[6])
    data_ushort = struct.unpack(byte_endian +'H'*(len(data)//2), data)
    process_data(header_ushort, data_ushort, len(data_ushort))
    header = sf.read(header_len)
    header_ushort = struct.unpack(byte_endian +'H'*(len(header)//2), header)
ppg_f.close()
mag_f.close()
acc_gyro_f.close()
acc_f.close()
sf.close()

def get_file_handle(sensor_type):
    global sensor_type_mag, sensor_type_acc, sensor_type_ppg, sensor_type_a_g
    global acc_f, ppg_f, acc_gyro_f, mag_f
    sf_handle = -1

    if sensor_type == sensor_type_acc:
        sf_handle = acc_f
    elif sensor_type == sensor_type_ppg:
        sf_handle = ppg_f
    elif sensor_type == sensor_type_mag:
        sf_handle = mag_f
    else:
        sf_handle = acc_gyro_f
    
    return sf_handle

def get_data_len(sensor_type):
    global sensor_type_mag, sensor_type_acc, sensor_type_ppg, sensor_type_a_g

    if sensor_type == sensor_type_acc:
        data_len = 4
    elif sensor_type == sensor_type_ppg:
        data_len = 2
    elif sensor_type == sensor_type_mag:
        data_len = 4
    else:
        data_len = 7

    return data_len

def gen_uint_from_ushort(data0, data1):
    global byte_endian

    if byte_endian == '>':
        data = data0 << 16 | data1
    else:
        data = data1 << 16 | data0

    return data


