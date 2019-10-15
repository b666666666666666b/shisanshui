#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import itertools
import re
import requests
import json
from urllib import parse
import tkinter.messagebox
import tkinter as tk
import pickle
#from PIL import Image, ImageTk

sys.setrecursionlimit(900000000)
token = "1"
ppp = []
uid = 1
page1 = 0
page2 = 0


def usr_sign_up():
    # 确认注册时的相应函数
    def signtowcg():
        # 获取输入框内的内容
        nn = new_name.get()
        np = new_pwd.get()
        npf = new_pwd_confirm.get()
        # 本地加载已有用户信息,如果没有则已有用户信息为空
        try:
            with open('usr_info.pickle', 'rb') as usr_file:
                exist_usr_info = pickle.load(usr_file)
        except FileNotFoundError:
            exist_usr_info = {}

            # 检查用户名存在、密码为空、密码前后不一致
        if nn in exist_usr_info:
            tk.messagebox.showerror('错误', '用户名已存在')
        elif np == '' or nn == '':
            tk.messagebox.showerror('错误', '用户名或密码为空')
        elif np != npf:
            tk.messagebox.showerror('错误', '密码前后不一致')
        # 注册信息没有问题则将用户名密码写入数据库
        else:
            exist_usr_info[nn] = np
            url = "https://api.shisanshui.rtxux.xyz/auth/register"
            headers = {
                'content-type': 'application/json'
            }
            # payload="{\"username\":\""+str("suolun")+"\",\"password\":\""+str("12345678")+"\"}"
            payload = "{\"username\":\"" + str(nn) + "\",\"password\":\"" + str(np) + "\"}"
            print(payload)
            response = requests.request("POST", url, data=payload, headers=headers)
            print(response.text)
            p2 = re.compile(r'id":(.+?)}')
            uid = p2.findall(response.text)[0]
            print(uid)
            tk.messagebox.showinfo('提示', response.text)
            # 注册成功关闭注册框
            window_sign_up.destroy()

    # 新建注册界面
    window_sign_up = tk.Toplevel(root)
    window_sign_up.geometry('350x200')
    window_sign_up.title('注册')
    # 用户名变量及标签、输入框
    new_name = tk.StringVar()
    tk.Label(window_sign_up, text='用户名：').place(x=10, y=10)
    tk.Entry(window_sign_up, textvariable=new_name).place(x=150, y=10)
    # 密码变量及标签、输入框
    new_pwd = tk.StringVar()
    tk.Label(window_sign_up, text='请输入密码：').place(x=10, y=50)
    tk.Entry(window_sign_up, textvariable=new_pwd, show='*').place(x=150, y=50)
    # 重复密码变量及标签、输入框
    new_pwd_confirm = tk.StringVar()
    tk.Label(window_sign_up, text='请再次输入密码：').place(x=10, y=90)
    tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*').place(x=150, y=90)
    # 确认注册按钮及位置
    bt_confirm_sign_up = tk.Button(window_sign_up, text='确认注册',
                                   command=signtowcg)
    bt_confirm_sign_up.place(x=150, y=130)


def menu():
    fm2 = tk.Frame(root)
    fm2.place(width=1440, height=1024)
    b21 = tk.Button(fm2, text='开始游戏', command=game_start, font=("Microsoft Yahei", 20), bg="#FF9800")
    b21.place(x=602, y=298, width=236, height=68)
    b22 = tk.Button(fm2, text='排行榜', command=paihang, font=("Microsoft Yahei", 20), bg="#FF9800")
    b22.place(x=602, y=387, width=236, height=68)
    b23 = tk.Button(fm2, text='历史对战', command=history, font=("Microsoft Yahei", 20), bg="#FF9800")
    b23.place(x=602, y=476, width=236, height=68)
    b24 = tk.Button(fm2, text='注销账户', command=login, font=("Microsoft Yahei", 20), bg="#FF9800")
    b24.place(x=602, y=565, width=236, height=68)
    b25 = tk.Button(fm2, text='退出游戏', command=root.destroy, font=("Microsoft Yahei", 20), bg="#FF9800")
    b25.place(x=1032, y=615, width=126, height=46)


def login():
    global uid
    global token
    fm1 = tk.Frame(root)
    fm1.place(width=1440, height=1024)
    w1 = tk.Label(fm1, text="账号", font=("Microsoft Yahei", 20), bg="#009BFF")
    w1.place(x=466, y=325, width=122, height=51)
    w2 = tk.Label(fm1, text="密码", font=("Microsoft Yahei", 20), bg="#009BFF")
    w2.place(x=466, y=394, width=122, height=51)
    e1 = tk.Entry(fm1, font=("Microsoft Yahei", 18))
    e1.place(x=596, y=326, width=322, height=51)
    e2 = tk.Entry(fm1, show='*', font=("Microsoft Yahei", 18))
    e2.place(x=596, y=395, width=322, height=51)

    def usr_log_in():
        global uid
        global token
        usr_name = e1.get()
        usr_pwd = e2.get()
        url = "https://api.shisanshui.rtxux.xyz/auth/login"
        # payload="{\"username\":\""+str("suolun")+"\",\"password\":\""+str("12345678")+"\"}"
        payload = "{\"username\":\"" + str(usr_name) + "\",\"password\":\"" + str(usr_pwd) + "\"}"
        headers = {'content-type': 'application/json'}
        print(payload)
        response = requests.request("POST", url, data=payload, headers=headers)
        if response.status_code == 200:

            print(response.text)
            aaa = str(response.text)
            print(aaa)
            # token = re.search('token": "(.+)"',aaa)
            p = re.compile(r'token":"(.+?)"')
            token = p.findall(aaa)[0]
            q = re.compile(r'id":(.+?),')
            uid = q.findall(aaa)[0]
            print(uid)
            print(token)
            # token = p.findall(response.text)[0]
            tk.messagebox.showinfo(title='提示', message='登录成功')
            menu()
        else:
            tk.messagebox.showinfo(title='提示', message='登录失败')

    b1 = tk.Button(fm1, text='登录', command=usr_log_in, font=("Microsoft Yahei", 20), bg="#8BC34A")
    b1.place(x=418, y=558, width=190, height=58)
    b2 = tk.Button(fm1, text='注册', command=usr_sign_up, font=("Microsoft Yahei", 20), bg="#8BC34A")
    b2.place(x=664, y=558, width=190, height=58)
    b3 = tk.Button(fm1, text='退出游戏', command=root.destroy, font=("Microsoft Yahei", 20), bg="#8BC34A")
    b3.place(x=937, y=558, width=190, height=58)


def show_game():
    global ppp
    fm3 = tk.Frame(root)
    fm3.place(width=1440, height=1024)
    b1 = tk.Button(fm3, text='再来一局', command=game_start, font=("Microsoft Yahei", 20), bg="#8BC34A")
    b1.place(x=621, y=740, width=198, height=59)
    b2 = tk.Button(fm3, text='退出对局', command=menu, font=("Microsoft Yahei", 20), bg="#8BC34A")
    b2.place(x=621, y=800, width=198, height=59)
    w1 = tk.Label(fm3, text=ppp, font=("Microsoft Yahei", 20), bg="#C0E892")
    w1.place(x=200, y=261, width=800, height=48)


def game_start():
    class pai:
        color = ''
        num = 0

        def __init__(self, c, n):
            self.color = c
            self.num = n

    def getnum(d):
        return d.num

    def validate(header):
        url = 'https://api.shisanshui.rtxux.xyz/auth/validate'
        headers = {
            "x-auth-token": token
        }
        response = requests.request("GET", url, headers=headers)
        print(response.text)

    lista = []
    listc = []
    liste = []
    lians = []
    listf = []
    listsum = []
    '''
    def login(username, password):
        url = "https://api.shisanshui.rtxux.xyz/auth/login"
        headers = {
            'content-type': 'application/json'
        }
        data = {
            "username": username,
            "password": password
        }
        dataa=str(data)
        response = requests.request("POST", url, data=dataa, headers=headers)
        print(respond.text)
        p = re.compile(r'token":"(.+?)"')
        token = p.findall(respond)[0]
        print(token)
        return token
'''
    '''
    def register(username, password):
        url = 'https://api.shisanshui.rtxux.xyz/auth/register'
        data = {
            "username": username,
            "password": password
        }
        print(data)
        respond = requests.post(url, json=data).text
        print(respond)
    '''

    def logout(header):
        url = 'https://api.shisanshui.rtxux.xyz/auth/logout'
        data = {}
        respond = requests.post(url, json=data).text
        print(respond)

    def openn(header):
        url = 'https://api.shisanshui.rtxux.xyz/game/open'
        header = str(header)
        headers = {'x-auth-token': header}
        data = {}
        response = requests.request("POST", url, headers=headers)
        return response

    def submit(idd, listt):
        global ppp
        ppp = listt
        url = "https://api.shisanshui.rtxux.xyz/game/submit"
        headers = {
            'content-type': "application/json",
            'x-auth-token': token
        }
        payload = "{\"id\":"
        payload = payload + str(idd)
        payload = payload + ",\"card\":[\""
        # payload = "{\"id\":"
        # payload=payload+str(idd)
        # payload=payload+"\",\"card\":[\""

        if len(listt) == 1:
            payload = payload + str(listt[0])
        else:
            payload = payload + str(listt[0])
            payload = payload + "\",\""
            payload = payload + str(listt[1])
            payload = payload + "\",\""
            payload = payload + str(listt[2])
        payload = payload + "\"]}"
        # print(payload)
        # dataa=str(data)
        response = requests.request("POST", url, data=payload, headers=headers)
        print(response.text)
        '''
        p = re.compile(r'token":"(.+?)"')
        token = p.findall(respond)[0]
        print(token)
        return token
        '''

    def history(header):
        u = 'https://api.shisanshui.rtxux.xyz/history'
        header = {
            "x-auth-token": token
        }
        response = requests.get(url=u, headers=header).text
        print(response)

    # open(header)
    # history(header)

    # logout(header)

    def zhizunqinglong():
        y = lista[0].color
        for x in lista:
            if x.color != y:
                return False
        return True

    def yitiaolong():
        dict1 = {}
        for x in range(2, 15):
            dict1[x] = 0
        for r in lista:
            dict1[r.num] = dict1[r.num] + 1
        sum1 = 1
        for x in range(2, 15):
            sum1 *= dict1[x]
        if sum1 == 1:
            return True
        else:
            return False

    def shierhuangzu():
        y = 0
        for x in lista:
            if x.num < 11:
                y = y + 1
        if y > 1:
            return False
        else:
            return True

    def santonghuashun():
        list1 = []
        list2 = []
        list3 = []
        list4 = []
        for x in lista:
            if x.color == "$":
                list1.append(x)
            elif x.color == "&":
                list2.append(x)
            elif x.color == "*":
                list3.append(x)
            else:
                list4.append(x)
        list1.sort(key=getnum)
        list2.sort(key=getnum)
        list3.sort(key=getnum)
        list4.sort(key=getnum)
        sumy = 0
        y = 0
        i = 0
        z = 0
        for x in list1:
            s = list1[i]
            if x.num != s.num:
                if x.num == s.num + 1:
                    y = y + 1
                i += 1
        if y == 4:
            sumy += 1
        elif y == 2:
            z = 1
        y = 0
        i = 0
        for x in list2:
            s = list2[i]
            if x.num != s.num:
                if x.num == s.num + 1:
                    y += 1
                i += 1
        if y == 4:
            sumy += 1
        elif y == 2:
            z = 1
        y = 0
        i = 0
        for x in list3:
            s = list3[i]
            if x.num != s.num:
                if x.num == s.num + 1:
                    y += 1
                i += 1
        if y == 4:
            sumy += 1
        elif y == 2:
            z = 1
        y = 0
        i = 0
        for x in list4:
            s = list4[i]
            if x.num != s.num:
                if x.num == s.num + 1:
                    y += 1
                i += 1
        if y == 4:
            sumy += 1
        elif y == 2:
            z = 1
        if sumy + z == 3:
            return True
        else:
            return False

    def sanfentianxai():
        dict1 = {}
        for x in range(2, 15):
            dict1[x] = 0
        for r in lista:
            dict1[r.num] = dict1[r.num] + 1
        y = 0
        for x in range(2, 15):
            if dict1[x] == 4:
                y += 1
        if y == 3:
            return True
        else:
            return False

    def quanda():
        if lista[0].num >= 8:
            return True
        else:
            return False

    def quanxiao():
        if lista[12].num <= 8:
            return True
        else:
            return False

    def couyise():
        dict1 = {}
        dict1["$"] = 0
        dict1["&"] = 0
        dict1["*"] = 0
        dict1["#"] = 0
        for r in lista:
            dict1[r.color] = dict1[r.color] + 1
        if dict1["$"] + dict1["&"] == 13 or dict1["*"] + dict1["#"] == 13:
            return True
        else:
            return False

    def shaungguaichongsan():
        dict1 = {}
        for x in range(2, 15):
            dict1[x] = 0
        for r in lista:
            dict1[r.num] = dict1[r.num] + 1
        santiao = 0
        duizi = 0
        for x in range(2, 15):
            if dict1[x] == 3:
                santiao += 1
            elif dict1[x] == 2:
                duizi += 1
        if santiao == 2 and duizi == 3:
            return True
        else:
            return False

    def sitaosantiao():
        dict1 = {}
        for x in range(2, 15):
            dict1[x] = 0
        for r in lista:
            dict1[r.num] = dict1[r.num] + 1
        santiao = 0
        for x in range(2, 15):
            if dict1[x] == 3:
                santiao += 1
        if santiao == 4:
            return True
        else:
            return False

    def wuduisantiao():
        dict1 = {}
        for x in range(2, 15):
            dict1[x] = 0
        for r in lista:
            dict1[r.num] = dict1[r.num] + 1
        santiao = 0
        duizi = 0
        for x in range(2, 15):
            if dict1[x] == 3:
                santiao += 1
            elif dict1[x] == 2:
                duizi += 1
        if santiao == 1 and duizi == 5:
            return True
        else:
            return False

    def liuduiban():
        dict1 = {}
        for x in range(2, 15):
            dict1[x] = 0
        for r in lista:
            dict1[r.num] = dict1[r.num] + 1
        duizi = 0
        for x in range(2, 15):
            if dict1[x] == 2:
                duizi += 1
        if duizi == 6:
            return True
        else:
            return False

    def sanshunzi():
        dict1 = {}
        for x in range(2, 15):
            dict1[x] = 0
        for r in lista:
            dict1[r.num] = dict1[r.num] + 1
        z = 0
        sumy = 0
        for vi in range(3):
            y = 0
            for r in lista:
                if dict1[r.num] > 1:
                    for x in range(r.num, min(r.num + 5, 15)):
                        if dict1[x] > 0:
                            dict1[x] = dict1[x] - 1
                            y += 1
                            if y == 5:
                                sumy += 1
                                break
                            elif x == 14 and y == 3:
                                z = 1
                                break
                        else:
                            if y == 3:
                                z = 1
                            break
                    break
        for vi in range(3):
            y = 0
            for r in lista:
                if dict1[r.num] > 0:
                    for x in range(r.num, min(r.num + 5, 15)):
                        if dict1[x] > 0:
                            dict1[x] = dict1[x] - 1
                            y += 1
                            if y == 5:
                                sumy += 1
                                break
                            elif x == 14 and y == 3:
                                z = 1
                                break
                        else:
                            if y == 3:
                                z = 1
                            break
                    break
        if sumy + z == 3:
            return True
        else:
            return False

    def santonghua():
        dict1 = {}
        for i in range(4):
            dict1[i] = 0
        for x in lista:
            if x.color == "$":
                dict1[0] += 1
            elif x.color == "&":
                dict1[1] += 1
            elif x.color == "*":
                dict1[2] += 1
            else:
                dict1[3] += 1
        s = 0
        for u in range(4):
            s += pow(2, dict1[u])
        if s == 73 or s == 1034 or s == 290:
            return True
        else:
            return False

    def tonghuashun(listb):
        list1 = []
        list2 = []
        list3 = []
        list4 = []
        for x in listb:
            if x.color == "$":
                list1.append(x)
            elif x.color == "&":
                list2.append(x)
            elif x.color == "*":
                list3.append(x)
            else:
                list4.append(x)
        list1.sort(key=getnum)
        list2.sort(key=getnum)
        list3.sort(key=getnum)
        list4.sort(key=getnum)
        y = 0
        i = 0
        for x in list1:
            s = list1[i]
            if x.num != s.num:
                if x.num == s.num + 1:
                    y = y + 1
                i += 1
        if y == 4:
            return x.num
        y = 0
        i = 0
        for x in list2:
            s = list2[i]
            if x.num != s.num:
                if x.num == s.num + 1:
                    y += 1
                i += 1
        if y == 4:
            return x.num
        y = 0
        i = 0
        for x in list3:
            s = list3[i]
            if x.num != s.num:
                if x.num == s.num + 1:
                    y += 1
                i += 1
        if y == 4:
            return x.num
        y = 0
        i = 0
        for x in list4:
            s = list4[i]
            if x.num != s.num:
                if x.num == s.num + 1:
                    y += 1
                i += 1
        if y == 4:
            return x.num
        return 0

    def zhadan(listb):
        dict1 = {}
        for x in range(2, 15):
            dict1[x] = 0
        for r in listb:
            dict1[r.num] = dict1[r.num] + 1
        y = 0
        for x in range(2, 15):
            if dict1[x] == 4:
                y = x
        return y

    def hulu(listb):
        dict1 = {}
        for x in range(2, 15):
            dict1[x] = 0
        for r in listb:
            dict1[r.num] = dict1[r.num] + 1
        san = 0
        dui = 0
        y = 0
        for x in range(2, 15):
            if dict1[x] == 3:
                san = 1
                y = x
            elif dict1[x] == 2:
                dui = 1
        if san * dui == 1:
            return y
        else:
            return 0

    def tonghua(listb, n):
        dict1 = {}
        for i in range(4):
            dict1[i] = 0
        y = 0
        for x in listb:
            if x.num > y:
                y = x.num
            if x.color == "$":
                dict1[0] += 1
            elif x.color == "&":
                dict1[1] += 1
            elif x.color == "*":
                dict1[2] += 1
            else:
                dict1[3] += 1
        s = 0
        for u in range(4):
            s += pow(2, dict1[u])
        if (n == 5 and s == 35) or (n == 3 and s == 10):
            if n == 5:
                return y
            return 1
        else:
            return 0

    def shunzi(listb, n):
        dict1 = {}
        for x in range(2, 15):
            dict1[x] = 0
        z = 0
        for r in listb:
            if r.num > z:
                z = r.num
            dict1[r.num] = dict1[r.num] + 1
        y = 0
        for r in listb:
            if dict1[r.num] > 0:
                for x in range(r.num, min(r.num + 5, 15)):
                    if dict1[x] > 0:
                        dict1[x] = dict1[x] - 1
                        y += 1
                        if y == 5:
                            break
                        elif x == 14 and y == 3:
                            break
                    else:
                        break
                break
        if y == n:
            return z
        else:
            return 0

    def santiao(listb):
        dict1 = {}
        for x in range(2, 15):
            dict1[x] = 0
        for r in listb:
            dict1[r.num] = dict1[r.num] + 1
        san = 0
        y = 0
        for x in range(2, 15):
            if dict1[x] == 3:
                y = x
                san = 1
        if san == 1:
            return x
        else:
            return 0

    def liandui(listb):
        dict1 = {}
        for x in range(2, 15):
            dict1[x] = 0
        for r in listb:
            dict1[r.num] = dict1[r.num] + 1
        for x in range(2, 14):
            if dict1[x] == 2 and dict1[x + 1] == 2:
                return x + 1
        return 0

    def liangdui(listb):
        dict1 = {}
        y = 0
        for x in range(2, 15):
            dict1[x] = 0
        for r in listb:
            dict1[r.num] = dict1[r.num] + 1
        dui = 0
        f = 1.0
        for x in range(14, 1, -1):
            if dict1[x] == 2:
                dui += 1
                y += x * f
                f *= 0.01
        if dui == 2:
            return y
        return 0

    def duizi(listb, n):
        dict1 = {}
        d = 0
        s = 0
        for x in range(2, 15):
            dict1[x] = 0
        for r in listb:
            dict1[r.num] = dict1[r.num] + 1
        dui = 0
        for x in range(2, 15):
            if dict1[x] == 2:
                d = x
                dui += 1
            elif dict1[x] == 1:
                s = max(s, x)
        if dui == 1:
            return d + s * 0.01
        return 0

    def getscore(li, m):
        listb = li.copy()
        f = 0
        f = tonghuashun(listb)
        if f > 0:
            return 100 + f * 0.01
        f = zhadan(listb)
        if f > 0:
            return 90 + f * 0.01
        f = hulu(listb)
        if f > 0:
            return 80 + f * 0.01
        f = tonghua(listb, m)
        if f > 0:
            return 70 + f * 0.01
        f = shunzi(listb, m)
        if f > 0:
            return 60 + f * 0.01
        f = santiao(listb)
        if f > 0:
            return 50 + f * 0.01
        f = liandui(listb)
        if f > 0:
            return 40 + f * 0.01
        f = liangdui(listb)
        if f > 0:
            return 30 + f * 0.01
        f = duizi(listb, m)
        if f > 0:
            return 20 + f * 0.01
        else:
            dict1 = {}
            for x in range(2, 15):
                dict1[x] = 0
            for r in listb:
                dict1[r.num] = dict1[r.num] + 1
            f = 0.1
            t = 0
            for i in range(14, 1, -1):
                if dict1[i] > 0:
                    t = t + i * f
                    f = f * 0.1
            return 10 + t

    def cmb(list0):

        list1 = list0.copy()
        iter1 = itertools.combinations(list1, 5)
        while 1:
            try:
                tup0 = next(iter1)
                listc = list(tup0)
                list1 = list0.copy()
                for i in range(5):
                    list1.remove(listc[i])
                iter2 = itertools.combinations(list1, 5)
                while 1:
                    try:
                        tup1 = next(iter2)
                        liste = list(tup1)
                        list2 = list0.copy()
                        for i in range(5):
                            list2.remove(listc[i])
                        for i in range(5):
                            list2.remove(liste[i])
                        a = getscore(listc, 5)
                        b = getscore(liste, 5)
                        c = getscore(list2, 3)
                        if a > b and b > c:
                            listsum[1] = a + 2 * b + 3 * c
                            if listsum[1] > listsum[0]:
                                listsum[0] = listsum[1]

                                lians.clear()
                                for k in range(3):
                                    lians.append(list2[k])
                                for k in range(5):
                                    lians.append(liste[k])
                                for k in range(5):
                                    lians.append(listc[k])
                    except StopIteration:
                        break

            except StopIteration:
                return

    listsum.append(0)
    listsum.append(0)
    tok = openn(token)

    tok1 = str(tok.text)
    # tok1=json.loads(tok)
    # str0 = input()
    p1 = re.compile(r'card":"(.+?)"')
    str0 = p1.findall(tok1)[0]
    print("receive origin card:", end=' ')
    print(str0)
    # str0= re.search('card\': \'(.+)\'',tok1)
    # str0=tok1['data']['card']
    p2 = re.compile(r'id":(.+?),')
    idd = p2.findall(tok1)[0]
    print("number of game:", end=' ')
    print(idd)
    # idd=re.search('id\': \'(.+)\'',tok1)
    # idd=tok1['data']['id']
    str1 = str0.replace("10", "T")
    for i in range(0, 39, 3):
        if str1[i + 1] == "T":
            x = pai(str1[i], 10)
        elif str1[i + 1] == "J":
            x = pai(str1[i], 11)
        elif str1[i + 1] == "Q":
            x = pai(str1[i], 12)
        elif str1[i + 1] == "K":
            x = pai(str1[i], 13)
        elif str1[i + 1] == "A":
            x = pai(str1[i], 14)
        else:
            x = pai(str1[i], int(str1[i + 1]))
        lista.append(x)
    lista.sort(key=getnum)
    lan = []
    st = ""
    for i in lista:
        st = st + i.color + str(i.num) + " "
    st = st.replace("11", "J")
    st = st.replace("12", "Q")
    st = st.replace("13", "K")
    st = st.replace("14", "A")
    st = st[0:len(st) - 1]
    lan.append(st)

    if zhizunqinglong():
        submit(idd, lan)
    elif yitiaolong():
        submit(idd, lan)
    elif shierhuangzu():
        submit(idd, lan)
    elif santonghuashun():
        submit(idd, lan)
    elif sanfentianxai():
        submit(idd, lan)
    elif quanda():
        submit(idd, lan)
    elif quanxiao():
        submit(idd, lan)
    elif couyise():
        submit(idd, lan)
    elif shaungguaichongsan():
        submit(idd, lan)
    elif sitaosantiao():
        submit(idd, lan)
    elif wuduisantiao():
        submit(idd, lan)
    elif liuduiban():
        submit(idd, lan)
    elif sanshunzi():
        submit(idd, lan)
    elif santonghua():
        submit(idd, lan)
    else:
        lians = lista.copy()
        cmb(lista)
        lans = []
        st = ""
        for i in range(0, len(lians)):
            st = st + lians[i].color + str(lians[i].num) + " "
        st = st.replace("10", "T")
        st = st.replace("11", "J")
        st = st.replace("12", "Q")
        st = st.replace("13", "K")
        st = st.replace("14", "A")
        st1 = ""
        st2 = ""
        st3 = ""
        for x in range(0, 8):
            st1 = st1 + st[x]
        for x in range(9, 23):
            st2 = st2 + st[x]
        for x in range(24, 38):
            st3 = st3 + st[x]
        st1 = st1.replace("T", "10")
        st2 = st2.replace("T", "10")
        st3 = st3.replace("T", "10")
        print(st1)
        print(st2)
        print(st3)
        lans.append(st1)
        lans.append(st2)
        lans.append(st3)
        submit(idd, lans)
        print("*************************************************************")

        show_game()


def page1_up():
    global page1
    page1 = page1 - 1
    if page1 < 0:
        page1 = 0
    paihang()
    return


def page2_up():
    global page2
    page2 = page2 - 1
    if page2 < 0:
        page2 = 0
    history()
    return


def page1_down():
    global page1
    page1 = page1 + 1
    paihang()
    return


def page2_down():
    global page2
    page2 = page2 + 1
    history()
    return


def paihang():
    global page1

    w = [None] * 50
    fm4 = tk.Frame(root)
    fm4.place(width=1440, height=1024)
    w1 = tk.Label(fm4, text="排行榜", font=("Microsoft Yahei", 20), bg="#C0E892")
    w1.place(x=200, y=261, width=800, height=48)
    url = "https://api.shisanshui.rtxux.xyz/rank"
    response = requests.request("GET", url)

    aa = re.findall('\{(.+?)\}', response.text)
    print(aa)
    if 10 * page1 + 10 > len(aa):
        for i in range(10 * page1, len(aa)):
            w[i % 10] = tk.Label(fm4, text="No." + str(i) + aa[i], font=("Microsoft Yahei", 20), bg="#C0E892")
            w[i % 10].place(x=200, y=309 + (i % 10) * 48, width=800, height=48)
    else:
        for i in range(10 * page1, 10 * page1 + 10):
            w[i % 10] = tk.Label(fm4, text="No." + str(i) + aa[i], font=("Microsoft Yahei", 20), bg="#C0E892")
            w[i % 10].place(x=200, y=309 + (i % 10) * 48, width=800, height=48)
            '''
    for i in aa[10*page:10*page+10]

    w2=tk.Label(fm4,text="排行榜",font=("Microsoft Yahei",20),bg="#C0E892")
    w2.place(x=526,y=309,width=436,height=48)
    w3=tk.Label(fm4,text="排行榜",font=("Microsoft Yahei",20),bg="#C0E892")
    w3.place(x=526,y=357,width=436,height=48)
    w4=tk.Label(fm4,text="排行榜",font=("Microsoft Yahei",20),bg="#C0E892")
    w4.place(x=526,y=405,width=436,height=48)
    w5=tk.Label(fm4,text="排行榜",font=("Microsoft Yahei",20),bg="#C0E892")
    w5.place(x=526,y=453,width=436,height=48)
    w6=tk.Label(fm4,text="排行榜",font=("Microsoft Yahei",20),bg="#C0E892")
    w6.place(x=526,y=501,width=436,height=48)
    w7=tk.Label(fm4,text="排行榜",font=("Microsoft Yahei",20),bg="#C0E892")
    w7.place(x=526,y=549,width=436,height=48)
    w8=tk.Label(fm4,text="排行榜",font=("Microsoft Yahei",20),bg="#C0E892")
    w8.place(x=526,y=597,width=436,height=48)
    w9=tk.Label(fm4,text="排行榜",font=("Microsoft Yahei",20),bg="#C0E892")
    w9.place(x=526,y=645,width=436,height=48)
    '''
    b1 = tk.Button(fm4, text='上一页', command=page1_up, font=("Microsoft Yahei", 20), bg="#FF9800")
    b1.place(x=1032, y=521, width=126, height=46)
    b2 = tk.Button(fm4, text='下一页', command=page1_down, font=("Microsoft Yahei", 20), bg="#FF9800")
    b2.place(x=1032, y=568, width=126, height=46)
    b3 = tk.Button(fm4, text='返回', command=menu, font=("Microsoft Yahei", 20), bg="#FF9800")
    b3.place(x=1032, y=615, width=126, height=46)


def history():
    global token
    global uid
    global page2

    w = [None] * 10
    fm5 = tk.Frame(root)
    fm5.place(width=1440, height=1024)
    url = "https://api.shisanshui.rtxux.xyz/history"
    querystring = {"page": "1", "limit": "100", "player_id": uid}
    headers = {'x-auth-token': token}
    response = requests.request("GET", url, headers=headers, params=querystring)
    ##print(response.text)
    aa = re.findall('\{(.+?)\}', response.text)

    if 10 * page2 + 10 > len(aa):
        for i in range(10 * page2, len(aa)):
            w[i % 10] = tk.Label(fm5, text="No." + str(i) + aa[i], font=("Microsoft Yahei", 20), bg="#C0E892")
            w[i % 10].place(x=1, y=309 + (i % 10) * 48, width=1440, height=48)
    else:
        for i in range(10 * page2, 10 * page2 + 10):
            w[i % 10] = tk.Label(fm5, text="No." + str(i) + aa[i], font=("Microsoft Yahei", 20), bg="#C0E892")
            w[i % 10].place(x=1, y=309 + (i % 10) * 48, width=1440, height=48)
    b1 = tk.Button(fm5, text='上一页', command=page2_up, font=("Microsoft Yahei", 20), bg="#FF9800")
    b1.place(x=1032, y=800, width=126, height=46)
    b2 = tk.Button(fm5, text='下一页', command=page2_down, font=("Microsoft Yahei", 20), bg="#FF9800")
    b2.place(x=1032, y=850, width=126, height=46)
    # aa=re.findall('\{(.+?)\}',response.text)
    '''
    for i in range(10*page2,10*page2+10):
        w[i%10]=tk.Label(fm5,text=aa[i],font=("Microsoft Yahei",20),bg="#C0E892")
        w[i%10].place(x=200,y=309+(i%10)*48,width=800,height=48)
    w1=tk.Label(fm5,text="排行榜",font=("Microsoft Yahei",20),bg="#C0E892")
    w1.place(x=526,y=261,width=436,height=48)
    w2=tk.Label(fm5,text="排行榜",font=("Microsoft Yahei",20),bg="#C0E892")
    w2.place(x=526,y=309,width=436,height=48)
    w3=tk.Label(fm5,text="排行榜",font=("Microsoft Yahei",20),bg="#C0E892")
    w3.place(x=526,y=357,width=436,height=48)
    w4=tk.Label(fm5,text="排行榜",font=("Microsoft Yahei",20),bg="#C0E892")
    w4.place(x=526,y=405,width=436,height=48)
    w5=tk.Label(fm5,text="排行榜",font=("Microsoft Yahei",20),bg="#C0E892")
    w5.place(x=526,y=453,width=436,height=48)
    w6=tk.Label(fm5,text="排行榜",font=("Microsoft Yahei",20),bg="#C0E892")
    w6.place(x=526,y=501,width=436,height=48)
    w7=tk.Label(fm5,text="排行榜",font=("Microsoft Yahei",20),bg="#C0E892")
    w7.place(x=526,y=549,width=436,height=48)
    w8=tk.Label(fm5,text="排行榜",font=("Microsoft Yahei",20),bg="#C0E892")
    w8.place(x=526,y=597,width=436,height=48)
    w9=tk.Label(fm5,text="排行榜",font=("Microsoft Yahei",20),bg="#C0E892")
    w9.place(x=526,y=645,width=436,height=48)
    '''
    b1 = tk.Button(fm5, text='返回', command=menu, font=("Microsoft Yahei", 20), bg="#FF9800")
    b1.place(x=1032, y=900, width=126, height=46)


def signup():
    fm6 = tk.Frame(root)
    fm6.place(width=1440, height=1024)
    w1 = tk.Label(fm6, text="账号", font=("Microsoft Yahei", 20), bg="#009BFF")
    w1.place(x=420, y=325, width=180, height=51)
    w2 = tk.Label(fm6, text="密码", font=("Microsoft Yahei", 20), bg="#009BFF")
    w2.place(x=420, y=394, width=180, height=51)
    w3 = tk.Label(fm6, text="确认密码", font=("Microsoft Yahei", 20), bg="#009BFF")
    w3.place(x=420, y=463, width=180, height=51)
    e1 = tk.Entry(fm6, font=("Microsoft Yahei", 18)).place(x=596, y=326, width=322, height=51)
    e2 = tk.Entry(fm6, font=("Microsoft Yahei", 18), show='*').place(x=596, y=395, width=322, height=51)
    e3 = tk.Entry(fm6, font=("Microsoft Yahei", 18), show='*').place(x=596, y=463, width=322, height=51)
    b2 = tk.Button(fm6, text='注册', command=login, font=("Microsoft Yahei", 20), bg="#8BC34A")
    b2.place(x=664, y=558, width=190, height=58)


def now_battle():
    fm7 = tk.Frame(root)
    fm7.place(width=1440, height=1024)
    b1 = tk.Button(fm7, text='返回', command=menu, font=("Microsoft Yahei", 20), bg="#FF9800")
    b1.place(x=1032, y=615, width=126, height=46)


root = tk.Tk()
root.geometry('1440x1024')
root.title('福建十三水')

login()
tk.mainloop()
# photo=tk.PhotoImage(file="1.jpg")
# w3=tk.Label(fm1,image='photo')
# w3.place(width=1440,height=1024)






