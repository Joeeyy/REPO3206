#!/usr/bin/env python3
# -*- coding: utf-8 -*-
table = list(b'0123456789.-E')  # 已知可构造字符
di = {}
l = len(table)
temp = 0
while temp != l:
    for j in range(temp, l):
        if ~table[j] & 0xff not in table:  # 非运算
            table.append(~table[j] & 0xff)
            di[~table[j] & 0xff] = {'op': '~', 'c': table[j]}  # 加入字典
            # print(f'~ {str(bytes([table[j]]))[1:]} = {str(bytes([~table[j]&0xff]))[1:]}')  # 打印构造过程
    for i in range(l):
        for j in range(max(i+1, temp), l):
            t = table[i] & table[j]  # 与运算
            if t not in table:
                table.append(t)
                di[t] = {'op': '&', 'c1': table[i], 'c2': table[j]}  # 加入字典
                # print(f'{str(bytes([table[i]]))[1:]} & {str(bytes([table[j]]))[1:]} = {str(bytes([t]))[1:]}')  # 打印构造过程
            t = table[i] | table[j]  # 或运算
            if t not in table:
                table.append(t)
                di[t] = {'op': '|', 'c1': table[i], 'c2': table[j]}  # 加入字典
                # print(f'{str(bytes([table[i]]))[1:]} | {str(bytes([table[j]]))[1:]} = {str(bytes([t]))[1:]}')  # 打印构造过程
    temp = l
    l = len(table)

table.sort()
print(bytes(table))


def howmake(ch: int) -> str:
    if ch in b'0123456789':
        return '(((1).(' + chr(ch) + ')){1})'
    elif ch in b'.':
        return '(((1).(0.1)){2})'
    elif ch in b'-':
        return '(((1).(-1)){1})'
    elif ch in b'E':
        return '(((1).(0.00001)){4})'
    d = di.get(ch)
    if d:
        op = d.get('op')
        if op == '~':
            c = '~'+howmake(d.get('c'))
        elif op == '&':
            c = howmake(d.get('c1')) + '&' + howmake(d.get('c2'))
        elif op == '|':
            c = howmake(d.get('c1')) + '|' + howmake(d.get('c2'))
        return f'({c})'
    else:
        print('input error!')
        return


if __name__=='__main__':
    while True:
        payload = input('>')
        result = []
        for i in payload:
            result.append(howmake(ord(i)))
        result = '.'.join(result)
        print(f'({result})')