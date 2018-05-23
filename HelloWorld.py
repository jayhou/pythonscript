#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：test.py
# import re

# print("你好，世界")
# print("我的python学习过程")
#
# if True:
#     print("这是 True")
#     print("这是练习缩进控制模块")
# else:
#     print("这块不会被执行，除非改成if False")
#   # print("这样会执行出错，需要和上一行相同的缩进")
# #像上面一样，这是单行注释
# '''
# 这是使用单引号的多行注释
# 这是使用单引号的多行注释
# '''
# """
# 这是使用多引号的多行注释
# 这是使用多引号的多行注释
# """
# stringTest = """据说三引号可以写很长，还可以换行
# 继续写。"""
# stringTest2 = '''据说三个单引号和三个双引号的效果一样
# 也可以换行继续写'''
# print(stringTest)
# print(stringTest2)
# #result = input("试试这个从终端输入的函数...")
# #print(result)
#
# #一下是Python基础类型练习
# meter = 1000
# miles = 1000.0
# country = "China：中国！"
# print(meter)
# print(miles)
# print(country)
#
# #多变量复制
# a = b = c = 1024
# print(a + b + c)
# print(str(a) + str(b) + str(c))

# line = "05s"
#
# matchObj = re.match(r'^[0-9][0-9]*s$', line, re.I)
#
# if matchObj:
#     print("line:"+line)
# else:
#     print("No match!!")



str = 'Hello World'
print(str)
print(str[0])
print(str[2:5])
print(str[2:])
print(str * 2)
print(str + ' TEST')



list = ['robot', 256, 2.23, 'JayChou', 172]
tinyList = ['Joilin', 2012]

print(list)
print(list[0])
print(list[1:3])
print(list[2:])
print(tinyList * 2)
print(list + tinyList)


tuple = ('JayHou', 8888, 6666, 'Jolin', 20.2)
tinytuple = ('Alaskai', 555)


print(tuple)               # 输出完整元组
print (tuple[0])            # 输出元组的第一个元素
print (tuple[1:3])          # 输出第二个至第三个的元素
print (tuple[2:])          # 输出从第三个开始至列表末尾的所有元素
print (tinytuple * 2)       # 输出元组两次
print (tuple + tinytuple)  # 打印组合的元组

list[2] = 1000
#tuple[2] = 100000    #元组不能赋值


dict = {}
dict[2] = 'people'
dict['people'] = 2
tinydict = {'name':'JayHou', 'age':30, 'Job':'coder'}

print(dict)
print(dict[2])
print(dict['people'])
print(dict[dict[2]])
print(dict[dict['people']])

print(tinydict)
print(tinydict.keys())
print(tinydict.values())

#数据类型转换
res1 = bytearray([255,255,255,255])
bytelist = []
for index in range (480 * 12):
    bytelist.append(255)
res2 = bytearray(bytelist)
res3 = res1+res2
print(res1)
print(len(res2))
print(res3)
str = ['a','b','c','d','e','f','g']

str1 = str[:3]
str2 = str[3:]
print(str1)
print(str2)