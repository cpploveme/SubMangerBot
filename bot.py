# -*- coding: UTF-8 -*-

import os
import re
import sys
import time
import json
import yaml
import requests
import random
import string
import urllib
import base64
import telebot
import threading
from datetime import datetime
from urllib import parse
from urllib.parse import unquote

import sqlite3
import telebot
from hashlib import md5
from time import sleep
from loguru import logger
from urllib import parse


version_text = "1.0.18 (23121201) Closed"


def load_bottoken() :
    try :
        with open('./config.yaml', 'r', encoding='utf-8') as f:
            data = yaml.load(stream=f, Loader=yaml.FullLoader)
        return data['telegramtoken']
    except :
        pass

def load_token() :
    try :
        with open('./config.yaml', 'r', encoding='utf-8') as f:
            data = yaml.load(stream=f, Loader=yaml.FullLoader)
        return data['token']
    except :
        pass

def load_administrator() :
    tempid = []
    try :
        with open('./config.yaml', 'r', encoding='utf-8') as f:
            data = yaml.load(stream=f, Loader=yaml.FullLoader)
        for user_id in data['administrator']:
            tempid.append(str(user_id))
    except :
        pass
    return tempid

# 定义bot
bot = telebot.TeleBot(load_bottoken())

bot_name = ""

# 日志功能 记录用户使用的指令和获取的订阅日志
logger.add('bot.log')

# 定义bot管理员的telegram userid
administrator_id = load_administrator()
admin_id = []
admin_backup = []

# 定义白名单群组
white_list = []

# 定义信任群组
trust_list = []

# 定义数据库
conn = sqlite3.connect('My_sub.db', check_same_thread=False)
c = conn.cursor()

# 定义自我介绍内容
intro = '这是一个用 `Telegram Bot Api` 来管理跨境服务提供商的订阅平台捏'

# 定义密码
password = "1145141919810"

# 定义超时尝试次数
try_time = 7

# 定义临期天数
impend = 10

# 定义订阅获取状态
testsub_flag = 0

stop_prune = 0
stop_updatesub = 0

# 定义进度条更新频率
send_percent = 5

# 定义防拉群
anti_group = 1

# 定义唯一管理模式
admin_only = 0

# 定义允许管理邀请
allow_invite = 0

# 定义回调
callback_url = ""

# 定义监测
cron_enable = 0
cron_delay = 3600
cron_list = []

# 定义流量查询
auto_check = {}

# 定义订阅转换
backend = "https://api.nexconvert.com/"
target = "clash"
shortlink = "https://jyf.icu/api/url?url="
config = "https://cdn.jsdelivr.net/gh/lhl77/sub-ini@main/tsutsu-mini-gfw.ini"
parameter = "&emoji=true&remove_emoji=false&interval=3600&udp=true&expand=false&list=false&scv=true&fdn=true&new_name=true"

# 定义User-Agent
sub_ua = 'ClashforWindows/0.18.1'
link_ua = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'

# 创建表
c.execute('''CREATE TABLE IF NOT EXISTS My_sub(URL text, comment text)''')

# 定义代理
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

# 加载管理员名单
def load_admin() :
    try :
        global admin_id
        with open('./config.yaml', 'r', encoding='utf-8') as f:
            data = yaml.load(stream=f, Loader=yaml.FullLoader)
        for user_id in data['admin']:
            admin_id.append(str(user_id))
        admin_id = list(set(admin_id))
    except :
        pass

# 加载管理员名单
def save_admin() :
    try :
        global admin_id
        with open('./config.yaml', 'r', encoding='utf-8') as f:
            data = yaml.load(stream=f, Loader=yaml.FullLoader)
        tempid = []
        for user_id in admin_id:
            tempid.append(int(user_id))
        tempid = list(set(tempid))
        data['admin'] = tempid
        with open('./config.yaml', 'w', encoding='utf-8') as f:
            yaml.dump(data=data, stream=f, allow_unicode=True, sort_keys=False)
    except :
        pass

# 保存监测列表
def save_cron() :
    try :
        with open('./config.yaml', 'r', encoding='utf-8') as f:
            data = yaml.load(stream=f, Loader=yaml.FullLoader)
        data['cron']['list'] = cron_list
        with open('./config.yaml', 'w', encoding='utf-8') as f:
            yaml.dump(data=data, stream=f, allow_unicode=True, sort_keys=False)
    except :
        pass


def reload_config():
    try:
        with open('./config.yaml', 'r', encoding='utf-8') as f:
            data = yaml.load(stream=f, Loader=yaml.FullLoader)
    except:
        pass
    try:
        if int(data['default']) == 1:
            return
    except:
        pass
    global try_time, impend, intro, backend, config, target, shortlink, password, send_percent, anti_group, admin_only, allow_invite, callback_url, cron_enable, cron_delay, cron_list, trust_list
    try:
        try_time = int(data['timeout'])
    except:
        pass
    try:
        impend = int(data['impend'])
    except:
        pass
    try:
        intro = data['intro']
    except:
        pass
    try:
        password = data['password']
    except:
        pass
    try:
        shortlink = data['shortlink']
    except:
        pass
    try:
        anti_group = int(data['avoidJoinGroups'])
    except:
        pass
    try:
        admin_only = int(data['adminOnlyMode'])
    except:
        pass
    try:
        allow_invite = int(data['allowAdminToInvite'])
    except:
        pass
    try:
        send_percent = int(data['refreshFrequency'])
    except:
        pass
    try:
        callback_url = data['callbackUrl']
    except:
        pass
    try:
        backend = data['convert']['backend']
    except:
        pass
    try:
        config = data['convert']['config']
    except:
        pass
    try:
        target = data['convert']['target']
    except:
        pass
    try:
        parameter = data['convert']['parameter']
    except:
        pass
    try:
        sub_ua = data['overridedUA']['subscribtion']
    except:
        pass
    try:
        link_ua = data['overridedUA']['request']
    except:
        pass
    try:
        cron_enable = int(data['cron']['enable'])
    except:
        pass
    try:
        cron_delay = int(data['cron']['interval'])
    except:
        pass
    try:
        for cron_id in data['cron']['list']:
            if not cron_id in cron_list:
                cron_list.append(cron_id)
    except:
        pass
    try:
        for trust_id in data['trust']:
            if not trust_id in trust_list:
                trust_list.append(trust_id)
    except:
        pass
    try:
        for user_id in data['admin']:
            admin_id.append(str(user_id))
        admin_id = list(set(admin_id))
    except:
        pass

def save_config():
    try:
        with open('./config.yaml', 'r', encoding='utf-8') as f:
            data = yaml.load(stream=f, Loader=yaml.FullLoader)
    except:
        pass
    tempid = []
    for user_id in admin_id:
        tempid.append(int(user_id))
    tempid = list(set(tempid))
    data['admin'] = tempid
    data['password'] = password
    data['intro'] = intro
    data['shortlink'] = shortlink
    data['impend'] = int(impend)
    data['timeout'] = int(try_time)
    data['adminOnlyMode'] = int(admin_only)
    data['avoidJoinGroups'] = int(anti_group)
    data['allowAdminToInvite'] = int(allow_invite)
    data['refreshFrequency'] = int(send_percent)
    if not callback_url == "":
        data['callbackUrl'] = callback_url
    trust_list = list(set(trust_list))
    data['trust'] = trust_list
    data['convert'] = {'backend': backend, 'config': config, 'target': target, 'parameter': parameter}
    data['overridedUA'] = {'request': link_ua, 'subscribtion': sub_ua}
    data['cron'] = {'enable': cron_enable, 'interval': cron_delay, 'list': cron_list}
    
    with open('./config.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(data=data, stream=f, allow_unicode=True, sort_keys=False)

def convert_time_to_str(time):
    if (time < 10):
        time = '0' + str(time)
    else:
        time = str(time)
    return time


def sec_to_data(y):
    h = int(y // 3600 % 24)
    d = int(y // 86400)
    h = convert_time_to_str(h)
    d = convert_time_to_str(d)
    return d + "天" + h + '小时'


def StrOfSize(size):
    def strofsize(integer, remainder, level):
        if integer >= 1024:
            remainder = integer % 1024
            integer //= 1024
            level += 1
            return strofsize(integer, remainder, level)
        elif integer < 0:
            integer = 0
            return strofsize(integer, remainder, level)
        else:
            return integer, remainder, level

    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    integer, remainder, level = strofsize(size, 0, 0)
    if level + 1 > len(units):
        level = -1
    return ('{}.{:>03d} {}'.format(integer, remainder, units[level]))

def remove_convert(url):
    if "sub?target=" in url:
        pattern = r"url=([^&]*)"
        match = re.search(pattern, url)
        if match:
            encoded_url = match.group(1)
            decoded_url = unquote(encoded_url)
            url = decoded_url
        else:
            pass
    try:
        headers = {'User-Agent': sub_ua}
        res = requests.get(url, headers=headers, allow_redirects=False, timeout=try_time)
        url = res.headers['location']
    except:
        pass
    if "sub?target=" in url:
        pattern = r"url=([^&]*)"
        match = re.search(pattern, url)
        if match:
            encoded_url = match.group(1)
            decoded_url = unquote(encoded_url)
            url = decoded_url
        else:
            pass
    return url

def cry(text):
    master_kek_00 = 'f759024f8199101dddc1ef91e6eecf37'
    master_kek_01 = 'bd27264ae07e979756411d0c66e679e3'
    master_kek_02 = 'a3d4a8e153b8e6ae6e6aef3e8f219cb4'
    master_kek_03 = '1558f525ae8c5be9243fb6d8a8b0a8ee'
    master_kek_04 = '9fbeb1957fc1629e08b753a9086d6e01'
    master_kek_05 = '94a92da1d73c2b3e165c891ced5607fc'
    master_kek_08 = 'e42f1ec8002043d746575ae6dd9f283f'
    master_kek_09 = 'cec2885fbeef5f6a989db84a4cc4b393'
    master_kek_0a = 'dd1a730232522b5cb4590cd43869ab6a'
    master_kek_0b = 'fc6f0c891d42710180724ed9e112e72a'
    master_kek_0c = '43f7fc20fcec22a5b2a744790371b094'
    master_kek_0d = '8dc9a8223671daa73ccd8b93cdaaed9f'
    master_kek_0e = 'f3f857257c3f63ca63b9c9710b8f673e'
    master_kek_0f = '1e8f01c4927a76a66097df44c3bad27d'

    gen = ((len(text) % 8 + 114514) * 3) % 16
    if gen == 0:
        salt = master_kek_00
    if gen == 1:
        salt = master_kek_01
    if gen == 2:
        salt = master_kek_02
    if gen == 3:
        salt = master_kek_03
    if gen == 4:
        salt = master_kek_04
    if gen == 5:
        salt = master_kek_05
    if gen == 6:
        salt = master_kek_06
    if gen == 7:
        salt = master_kek_07
    if gen == 8:
        salt = master_kek_08
    if gen == 9:
        salt = master_kek_09
    if gen == 10:
        salt = master_kek_0a
    if gen == 11:
        salt = master_kek_0b
    if gen == 12:
        salt = master_kek_0c
    if gen == 13:
        salt = master_kek_0d
    if gen == 14:
        salt = master_kek_0e
    if gen == 15:
        salt = master_kek_0f
    
    temp = md5()
    temp.update((text + salt).encode('utf-8'))
    return temp.hexdigest()
    

# 初始化
def botinit():
    global bot_name
    bot_name = '@' + bot.get_me().username
    if not cry(bot.get_me().username)  == load_token():
        print('授权密钥不正确 Bot已退出')
        os._exit(0)
    
    #bot.delete_my_commands(scope=None, language_code=None)

    #bot.set_my_commands(
    #    commands=[
    #        telebot.types.BotCommand("help", "帮助菜单")
    #    ],
    #)

    f = open("airport.list","a", encoding="utf8")

    reload_config()
    
    logger.debug(f"[初始化完成]")
    load_admin()
    for send_id in administrator_id :
        try :
            bot.send_message(send_id, '[初始化完成]')
        except :
            continue


# 接收用户输入的指令
@bot.message_handler(commands=['add', 'del', 'search', 'update', 'sort','notice', 'chat', 'auto', 'log', 'database', 'a', 'd', 's', 'u', 'n', 'r', 'c'])
def handle_command(message):
    if not message.chat.type == "private" :
        if not bot_name in message.text :
            if not str(message.from_user.id) in admin_id:
                return
    if str(message.from_user.id) in admin_id:
        command = message.text.split()[0]
        logger.debug(f"用户{message.from_user.id}使用了{command}功能")
        if '/add' in command :
            add_sub(message)
        elif '/del' in command :
            delete_sub(message)
        elif '/search' in command :
            search_sub(message)
        elif '/update' in command :
            update_sub(message)
        elif '/sort' in command :
            sort_sub(message)
        elif '/notice' in command :
            notice(message)
        elif '/chat' in command :
            chat(message)
        elif '/auto' in command :
            auto_sub(message)
        elif '/log' in command:
            get_log(message)
        elif '/database' in command :
            get_database(message)
        elif '/a' in command :
            add_sub(message)
        elif '/d' in command :
            delete_sub(message)
        elif '/s' in command :
            search_sub(message)
        elif '/u' in command :
            update_sub(message)
        elif '/n' in command :
            notice(message)
        elif '/c' in command :
            chat(message)
    else:
        bot.reply_to(message, "[WRONG][你没有操作权限]")
    

# 取消信任群组
@bot.message_handler(commands=['distrust'])
def get_id(message):
    if not message.chat.type == "private" :
        if not bot_name in message.text :
            if not str(message.from_user.id) in administrator_id:
                return
    try :
        if str(message.from_user.id) in administrator_id :
            global trust_list
            trust_list.remove(message.chat.id)
            bot.reply_to(message, "[✅][已取消信任该群组]")
            logger.debug(f"用户{message.from_user.id}使用了取消信任了{message.chat.id}群组")
    except :
        return

# 信任群组
@bot.message_handler(commands=['trust'])
def get_id(message):
    if not message.chat.type == "private" :
        if not bot_name in message.text :
            if not str(message.from_user.id) in administrator_id:
                return
    try :
        if str(message.from_user.id) in administrator_id :
            global trust_list
            trust_list.append(message.chat.id)
            bot.reply_to(message, "[✅][已信任该群组]")
            logger.debug(f"用户{message.from_user.id}使用了信任了{message.chat.id}群组")
    except :
        return

# 管理员名单
@bot.message_handler(commands=['list'])
def get_id(message):
    if not message.chat.type == "private" :
        if not bot_name in message.text :
            if not str(message.from_user.id) in administrator_id:
                return
    try :
        if str(message.from_user.id) in administrator_id :
            id_text = ""
            for id in admin_id :
                id_text = id_text + str(id) + "\n"
            bot.reply_to(message, id_text)
    except :
        return

# 离开群聊
@bot.message_handler(commands=['leave'])
def get_id(message):
    if not message.chat.type == "private" :
        if not bot_name in message.text :
            if not str(message.from_user.id) in admin_id:
                return
    try :
        global white_list
        if message.chat.id in white_list :
            white_list.remove(message.chat.id)
        bot.leave_chat(message.chat.id)
        logger.debug(f"用户{message.from_user.id}使用了离开群聊{message.chat.id}")
    except :
        return

# 防拉群
@bot.message_handler(func=lambda m: True, content_types=['new_chat_members'])
def auto_leave(message):
    if not message.json['new_chat_participant']['username'] in bot_name :
       return
    if anti_group == 0:
        return
    try :
        if anti_group == 1:
            temp_id = admin_id
        else:
            temp_id = administrator_id
        if not str(message.from_user.id) in temp_id:
            if not message.chat.id in white_list :
                try :
                    bot.reply_to(message, "❌ 机器人已启动防拉群模式 请联系管理拉群")
                    bot.leave_chat(message.chat.id)
                    logger.debug(f"在群聊{message.chat.id}自动离开了")
                except :
                    pass
        else :
            white_list.append(message.chat.id)
    except :
        try :
            bot.reply_to(message, "❌ 机器人已启动防拉群模式 请联系管理拉群")
            bot.leave_chat(message.chat.id)
            logger.debug(f"在群聊{message.chat.id}自动离开了")
        except :
            pass
    
@bot.my_chat_member_handler()
def leave_ban(message: telebot.types.ChatMemberUpdated):
    try :
        if new.status == "left" :
            white_list.remove(message.chat.id)
    except :
        pass

# 获取数据库
def get_database(message):
    try :
        if password in message.text:
            with open('./My_sub.db', 'rb') as f:
                bot.send_document(message.chat.id, f)
                f.close()
        else :
            bot.send_message(message.chat.id, "[WRONG][获取数据库失败]")
    except :
        bot.send_message(message.chat.id, "[WRONG][获取数据库失败]")

# 获取日志
def get_log(message):
    try :
        if password in message.text :
            with open('./bot.log', 'rb') as f:
                bot.send_document(message.chat.id, f)
                f.close()
        else :
            bot.send_message(message.chat.id, "[WRONG][获取日志失败]")
    except :
        bot.send_message(message.chat.id, "[WRONG][获取日志失败]")

# 下载仓库
@bot.message_handler(commands=['install'])
def save_database(message) :
    if not bot_name in message.text :
        if not message.chat.type == "private" :
            return
    if str(message.from_user.id) in administrator_id :
        try :
            if password in message.text:
                fil = bot.get_file(message.reply_to_message.document.file_id)
                f = requests.get(f"https://api.telegram.org/file/bot{load_bottoken()}/{fil.file_path}", timeout=try_time)
                with open("My_sub.db", "wb") as code:
                    code.write(f.content)
                bot.reply_to(message, "[✅][下载成功]")
            else :
                bot.reply_to(message, "[WRONG][下载失败]")
        except :
            bot.reply_to(message, "[WRONG][下载失败]")
    else:
        bot.reply_to(message, "[WRONG][你没有操作权限]")

# 添加关键词
@bot.message_handler(commands=['addkeyword'])
def save_airport(message) :
    if not message.chat.type == "private" :
        if not bot_name in message.text :
            if not str(message.from_user.id) in admin_id :
                return
    if str(message.from_user.id) in administrator_id :
        try :
            a = message.text.split()[1]
            b = message.text.split()[2]
            
            r = open('airport.list',encoding='utf8')
            while True :
                line = r.readline()
                if not line :
                    break
                keyword = line.split()[0]
                if a in keyword :
                    bot.reply_to(message, "[WRONG][已有该关键词]")
                    return
            
            with open("airport.list","a", encoding="utf8") as f :
                f.write(a + ' ' + b + '\n')
            bot.reply_to(message, "[✅][添加成功]")
        except :
            bot.reply_to(message, "[WRONG][添加失败]")
    else:
        bot.reply_to(message, "[WRONG][你没有操作权限]")

# 删除机场关键词
@bot.message_handler(commands=['delkeyword'])
def del_airport(message):
    if not message.chat.type == "private" :
        if not bot_name in message.text :
            if not str(message.from_user.id) in admin_id :
                return
    if str(message.from_user.id) in administrator_id :
        try :
            name_list = []
            a = message.text.split()[1]
            r = open('airport.list',encoding='utf8')
            flag = 0
            while True :
                line = r.readline()
                if not line :
                    break
                keyword = line.split()[0]
                if not a == keyword :
                    name_list.append(line)
                else :
                    flag = 1
            if flag == 0 :
                bot.reply_to(message, "[WRONG][删除失败]")
            else :
                with open("airport.list","w", encoding="utf8") as f :
                    for name in name_list :
                        f.write(name)
                bot.reply_to(message, "[✅][删除成功]")
        except :
            bot.reply_to(message, "[WRONG][删除失败]")
    else:
        bot.reply_to(message, "[WRONG][你没有操作权限]")

# 授权
@bot.message_handler(commands=['grant'])
def grant(message):
    if not bot_name in message.text :
        if not message.chat.type == "private" :
            return
    
    if str(message.from_user.id) in administrator_id :
        try :
            id_text = message.text.split()
            if len(id_text) < 2:
                logger.debug(f"用户{message.from_user.id}在群聊{message.reply_to_message.chat.id}授予了{message.reply_to_message.from_user.id}管理员权限")
                if not str(message.reply_to_message.from_user.id) in admin_id :
                    admin_id.append(str(message.reply_to_message.from_user.id))
            else:
                for i in id_text[1:]:
                    if not i in admin_id :
                        logger.debug(f"用户{message.from_user.id}授予了{i}管理员权限")
                        admin_id.append(i)
            save_admin()
            bot.reply_to(message, "[✅][授权成功]")
        except :
            bot.reply_to(message, "[WRONG][授权失败]")
    else:
        bot.reply_to(message, "[WRONG][你没有操作权限]")

# 取消授权
@bot.message_handler(commands=['ungrant'])
def ungrant(message):
    if not bot_name in message.text :
        if not message.chat.type == "private" :
            return

    if str(message.from_user.id) in administrator_id :
        try :  
            id_text = message.text.split()
            if len(id_text) < 2:
                logger.debug(f"用户{message.from_user.id}在群聊{message.reply_to_message.chat.id}取消了{message.reply_to_message.from_user.id}管理员权限")
                if str(message.reply_to_message.from_user.id) in admin_id :
                    admin_id.remove(str(message.reply_to_message.from_user.id))
            else:
                for i in id_text[1:]:
                    if i in admin_id :
                        logger.debug(f"用户{message.from_user.id}取消了{i}管理员权限")
                        admin_id.remove(i)
            save_admin()
            bot.reply_to(message, "[✅][消权成功]")
        except :
            bot.reply_to(message, "[WRONG][消权失败]")
    else:
        bot.reply_to(message, "[WRONG][你没有操作权限]")

# 清理授权
@bot.message_handler(commands=['grantclear'])
def grant(message):
    if not message.chat.type == "private" :
        if not bot_name in message.text :
            if not str(message.from_user.id) in administrator_id :
                return

    if str(message.from_user.id) in administrator_id :
        try :
            global admin_id
            admin_id = []
            save_admin()
            bot.reply_to(message, "[✅][清理成功]")
        except :
            bot.reply_to(message, "[WRONG][清理失败]")
    else:
        bot.reply_to(message, "[WRONG][你没有操作权限]")

# 关机
@bot.message_handler(commands=['stop'])
def stop(message):
    if not message.chat.type == "private" :
            if not str(message.from_user.id) in administrator_id:
                return
    if str(message.from_user.id) in admin_id:
        if password in message.text:
            try :
                bot.reply_to(message, "[✅][接收命令成功]")
                print('关机中')
                for send_id in administrator_id :
                    try :
                        bot.send_message(send_id, '[关机中...]')
                    except :
                        continue
                os._exit(0)
            except :
                print('关机失败')
                for send_id in administrator_id :
                    try :
                        bot.send_message(send_id, '[WRONG][关机失败]')
                    except :
                        continue
        else : 
            bot.reply_to(message, "[WRONG][密码错误]")
    else:
        bot.reply_to(message, "[WRONG][你没有操作权限]")

# 注册监测任务
@bot.message_handler(commands=['register'])
def register_cron(message):
    if not message.chat.type == "private" :
        if not bot_name in message.text :
            if '@' in message.text :
                return
    if str(message.from_user.id) in admin_id :
        try :
            task_name = str(message.chat.id)
            try:
                for cron in cron_list:
                    try:
                        if message.chat.id == list(cron.keys())[0]:
                            cron_list.remove(cron)
                    except:
                        pass
            except:
                pass
            try:
                cron_list.remove(message.chat.id)
            except:
                pass
            try:
                cron_list.append({message.chat.id: message.text.split()[1]})
                task_name = task_name + ':' + message.text.split()[1]
            except:
                cron_list.append(message.chat.id)
            save_cron()
            bot.reply_to(message, f"\[✅]\[注册任务 `{task_name}` 成功]", parse_mode = 'Markdown')
        except :
            bot.reply_to(message, "[WRONG][注册失败]")
    else:
        bot.reply_to(message, "[WRONG][你没有操作权限]")

# 取消监测任务
@bot.message_handler(commands=['unregister'])
def unregister_cron(message):
    if not message.chat.type == "private" :
        if not bot_name in message.text :
            if '@' in message.text :
                return
    if str(message.from_user.id) in admin_id :
        try :
            task_name = str(message.chat.id)
            for cron in cron_list:
                try:
                    if message.chat.id == list(cron.keys())[0]:
                        task_name = task_name + ':' + list(cron.values())[0]
                        cron_list.remove(cron)
                except:
                    pass
            try:
                cron_list.remove(message.chat.id)
            except:
                pass
            save_cron()
            bot.reply_to(message, f"\[✅]\[取消任务 `{task_name}` 成功]", parse_mode = 'Markdown')
        except :
            bot.reply_to(message, "[WRONG][取消失败]")
    else:
        bot.reply_to(message, "[WRONG][你没有操作权限]")

# 重启
#@bot.message_handler(commands=['restart'])
def restart(message):
    if not message.chat.type == "private" :
            if not str(message.from_user.id) in administrator_id:
                return
    if str(message.from_user.id) in admin_id:
        try :
            bot.reply_to(message, "[✅][接收命令成功]")
            print('重启中')
            bot.stop_polling()
            bot.polling(none_stop=True)
            for send_id in administrator_id :
                try :
                    bot.send_message(send_id, '[重启中...]')
                except :
                    continue
            
            #f = requests.get(bot_web, timeout=try_time)
            #with open("bot.py", "wb") as code:
                #code.write(f.content)
            
            os.execlp(sys.executable, sys.executable, "submanger.exe", *sys.argv)
            sys.exit()
        except :
            print('重启失败')
            for send_id in administrator_id :
                try :
                    bot.send_message(send_id, '[WRONG][重启失败]')
                except :
                    continue
    else:
        bot.reply_to(message, "[WRONG][你没有操作权限]")

# 重载配置
@bot.message_handler(commands=['reload'])
def reload(message):
    if not message.chat.type == "private" :
        if not bot_name in message.text :
            if not str(message.from_user.id) in admin_id:
                return
    if str(message.from_user.id) in administrator_id :
        try :
            reload_config()
            bot.reply_to(message, "[✅][重载成功]")
        except :
            bot.reply_to(message, "[WRONG][重载失败]")
    else:
        bot.reply_to(message, "[WRONG][你没有操作权限]")

# 保存配置
@bot.message_handler(commands=['save'])
def save(message):
    if not message.chat.type == "private" :
        if not bot_name in message.text :
            if not str(message.from_user.id) in admin_id:
                return
    if str(message.from_user.id) in administrator_id :
        try :
            save_config()
            bot.reply_to(message, "[✅][保存成功]")
        except :
            bot.reply_to(message, "[WRONG][保存失败]")
    else:
        bot.reply_to(message, "[WRONG][你没有操作权限]")

# 设置配置
@bot.message_handler(commands=['set'])
def set_value(message):
    if not message.chat.type == "private" :
        if not bot_name in message.text :
            if not str(message.from_user.id) in admin_id:
                return
    if str(message.from_user.id) in administrator_id :
        try :
            reload_config()
            try:
                with open('./config.yaml', 'r', encoding='utf-8') as f:
                    data = yaml.load(stream=f, Loader=yaml.FullLoader)
            except:
                pass
            try:
                text = message.text.split()[2]
            except:
                text = ""
            for i in range(3, len(message.text.split())):
                item = message.text.split()[i]
                text = text + " " + item
            if len(message.text.split()[1].split('.')) == 1:
                data[message.text.split()[1].split('.')[0]] = text
            elif len(message.text.split()[1].split('.')) == 2:
                data[message.text.split()[1].split('.')[0]][message.text.split()[1].split('.')[1]] = text
            else:
                bot.reply_to(message, "[WRONG][迭代深度错误]")
                return
            with open('./config.yaml', 'w', encoding='utf-8') as f:
                yaml.dump(data=data, stream=f, allow_unicode=True, sort_keys=False)
            reload_config()
            bot.reply_to(message, f"\\[✅]\\[已将配置 `{message.text.split()[1]}` 的值设置为]\n\n`{text}`", parse_mode = 'Markdown')
        except :
            bot.reply_to(message, "[WRONG][设置失败]")
    else:
        bot.reply_to(message, "[WRONG][你没有操作权限]")

# 获取配置
@bot.message_handler(commands=['value'])
def get_value(message):
    if not message.chat.type == "private" :
        if not bot_name in message.text :
            if not str(message.from_user.id) in admin_id:
                return
    if str(message.from_user.id) in administrator_id :
        try :
            reload_config()
            try:
                with open('./config.yaml', 'r', encoding='utf-8') as f:
                    data = yaml.load(stream=f, Loader=yaml.FullLoader)
            except:
                pass
            if len(message.text.split()) == 1:
                bot.reply_to(message, f"\\[✅]\\[全部配置的值为]\n\n`{str(data)}`", parse_mode = 'Markdown')
            else:
                for item in message.text.split()[1].split('.'):
                    data = data[item]
                bot.reply_to(message, f"\\[✅]\\[配置 `{message.text.split()[1]}` 的值为]\n\n`{str(data)}`", parse_mode = 'Markdown')
        except :
            bot.reply_to(message, "[WRONG][读取失败]")
    else:
        bot.reply_to(message, "[WRONG][你没有操作权限]")

# 发送消息
def chat(message):
    if not message.chat.type == "private" :
        return
    cont = ""
    try:
        c = message.text.split()[1:]
        for s in c :
            cont = cont + " " + s
        bot.reply_to(message, "[✅][发送成功]")
    except:
        bot.send_message(message.from_user.id, "[WRONG][输入格式有误 请检查后重新输入]")
        return
    for send_id in admin_id :
        try :
            if "None" in str(message.from_user.username) :
                bot.send_message(send_id, f"\\[来自 [{str(message.from_user.id)}](tg://openmessage?user_id={str(message.from_user.id)}) 的消息]{cont}", parse_mode = 'Markdown')
            else :
                bot.send_message(send_id, f"[来自 @{str(message.from_user.username)} 的消息]{cont}")
        except :
            continue

# 发送通知
def notice(message):
    if not message.chat.type == "private" :
        return
    cont = ""
    try:
        c = message.text.split()[1:]
        for s in c :
            cont = cont + " " + s
        bot.reply_to(message, "[✅][发送成功]")
    except:
        bot.send_message(message.from_user.id, "[WRONG][输入格式有误 请检查后重新输入]")
        return
    for send_id in admin_id :
        try :
            if "None" in str(message.from_user.username) :
                bot.send_message(send_id, f"\\[来自 [{str(message.from_user.id)}](tg://openmessage?user_id={str(message.from_user.id)}) 的通知]{cont}", parse_mode = 'Markdown')
            else :
                bot.send_message(send_id, f"[来自 @{str(message.from_user.username)} 的通知]{cont}")
        except :
            continue

# 订阅链接赠与
@bot.message_handler(commands=['invite'])
def startinvite(message):
    if not message.chat.type == "private" :
        if not bot_name in message.text :
            if '@' in message.text :
                return
    if str(message.from_user.id) in administrator_id or (allow_invite == 1 and str(message.from_user.id) in admin_id):
        if message.reply_to_message :
            reply = message.reply_to_message
            try :
                sub_id = int(message.text.split()[1])
            except :
                bot.reply_to(message, "[WARNING][命令格式不对呢]")
                return
        else :
            bot.reply_to(message, "[WARNING][请回复用户消息呢]")
            return
        logger.debug(f"用户{message.from_user.id}赠与了用户{message.reply_to_message.from_user.id}订阅")
        global auto_check
        identifier = ''.join(random.choices('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=8))
        try:
            identifier = message.text.split()[2]
        except:
            pass
        name = bot_name.replace('@', '')
        url = f'https://t.me/{name}?start=' + identifier
        c.execute("SELECT rowid,URL,comment FROM My_sub WHERE rowid=?", (sub_id,))
        result = c.fetchone() 
        subname = result[2]
        keyboard = []
        keyboard.append([telebot.types.InlineKeyboardButton(text='获取订阅', url=url)])
        reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
        sent_message = bot.reply_to(message.reply_to_message, text=  f'用户 `{message.reply_to_message.from_user.first_name}` 您被 `{message.from_user.first_name}` 赠与了订阅 `{subname}` 请点击下方按键获取', parse_mode = 'Markdown', reply_markup=reply_markup)
        auto_check[identifier] = {'state': 3, 'user' : message.reply_to_message.from_user.id, 'chat' : sent_message.chat.id, 'message': sent_message.message_id, 'identifier': identifier, 'result': result}
    else:
        bot.reply_to(message, "[WRONG][你没有操作权限]")
    

# 启动对话
@bot.message_handler(commands=['start'],func = lambda message:message.chat.type == "private")
def start(message):
    if not message.chat.type == "private" :
        if not bot_name in message.text :
            if not str(message.from_user.id) in admin_id:
                return
    auto_reply_text = message.text.replace('/start', '').strip()
    try:
        if len(auto_reply_text) > 0:
            identifier = auto_reply_text
            user = auto_check[identifier]['user']
            chat_id = auto_check[identifier]['chat']
            message_id = auto_check[identifier]['message']
            state = auto_check[identifier]['state']
            if user == message.from_user.id:
                if state == 3:
                    result = auto_check[identifier]['result']
                    headers = {'User-Agent': sub_ua}
                    output_test = ''
                    try :
                        try:
                            res = requests.get(result[1], headers=headers, timeout=try_time)
                        except:
                            output_text = '连接错误'
                        if res.status_code == 200:
                            try:
                                info = res.headers['subscription-userinfo']
                                info_num = re.findall(r'\d+', info)
                                time_now = int(time.time())
                                output_text_head = '上行：`' + StrOfSize(int(info_num[0])) + '`\n下行：`' + StrOfSize(int(info_num[1])) + '`\n剩余：`' + StrOfSize(int(info_num[2]) - int(info_num[1]) - int(info_num[0])) + '`\n总共：`' + StrOfSize(int(info_num[2])) + '`'
                                if len(info_num) >= 4:
                                    timeArray = time.localtime(int(info_num[3]) + 28800)
                                    dateTime = time.strftime("%Y-%m-%d", timeArray)
                                    if time_now <= int(info_num[3]):
                                        lasttime = int(info_num[3]) - time_now
                                        output_text = output_text_head + '\n过期时间：`' + dateTime + '`\n剩余时间：`' + sec_to_data(lasttime) + '`'
                                    elif time_now > int(info_num[3]):
                                        output_text = output_text_head + '\n此订阅已于 `' + dateTime + '`过期'
                                else:
                                    output_text = output_text_head + '\n过期时间：`没有说明`'
                            except:
                                output_text = '`无流量信息`'
                        else:
                            output_text = '`无法访问`'

                        try :
                            d = int(lasttime // 86400)
                            if d < impend :
                                if not '临期' in result[2] :
                                    c.execute("UPDATE My_sub SET URL=?, comment=? WHERE rowid=?", (result[1], result[2] + '-临期', result[0]))
                                    conn.commit()
                        except :
                            pass
                    except:
                        output_text = '`无流量信息`'                    
                    logger.debug(f"用户{message.from_user.id}从BOT接受赠与了订阅{result}")
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="订阅已接收")
                    bot.send_message(message.from_user.id, '编号 `{}`\n订阅 `{}`\n说明 `{}`\n\n{}'.format(result[0], result[1], result[2], output_text),parse_mode='Markdown')
                    auto_check[message.from_user.id] = {'state': 4, 'chat' : chat_id, 'message': message_id, 'identifier': identifier}
        else:
            bot.send_message(message.chat.id, intro, parse_mode = 'Markdown')
            logger.debug(f"用户{message.from_user.id}开始了对话")
    except:
        bot.send_message(message.chat.id, intro, parse_mode = 'Markdown')
        logger.debug(f"用户{message.from_user.id}开始了对话")

def StrSize(size):
    def strofsize(integer, remainder, level):
        if integer >= 1024:
            remainder = integer % 1024
            integer //= 1024
            level += 1
            return strofsize(integer, remainder, level)
        elif integer < 0:
            integer = 0
            return strofsize(integer, remainder, level)
        else:
            return integer, remainder, level

    units = ['B', 'K', 'M', 'G', 'T', 'P', 'EB', 'ZB', 'YB']
    integer, remainder, level = strofsize(size, 0, 0)
    if level + 1 > len(units):
        level = -1
    return ('{}{}'.format(integer, units[level]))

# 自动添加
def auto_sub(message):
    try:
        url_list = []
        try : 
            url_list = re.findall("https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]", message.reply_to_message.text)
        except :
            url_list = re.findall("https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]", message.text)
        for urla in url_list :
            try :
                url = remove_convert(urla)
                c.execute("SELECT * FROM My_sub WHERE URL LIKE ?", ('%' + url + '%',))
                if c.fetchone():
                    bot.reply_to(message, "[WRONG][订阅已存在]")
                    continue
                comment = ""
                name = ""
                size = ""
                flag = 0
                try:
                    r = open('airport.list',encoding='utf8')
                    while True :
                        line = r.readline()
                        if not line :
                            break
                        a = line.split()[0]
                        b = line.split()[1]
                        if a in url :
                            name = b
                            flag = 1
                            break
                except:
                    pass
                if flag == 0 :
                    if "api/v1/client/subscribe?token" in url:
                        if "&flag=clash" not in url:
                            url = url + "&flag=clash"
                        else:
                            pass
                        try:
                            response = requests.get(url, timeout=try_time)
                            header = response.headers.get('Content-Disposition')
                            if header:
                                pattern = r"filename\*=UTF-8''(.+)"
                                result = re.search(pattern, header)
                                if result:
                                    filename = result.group(1)
                                    filename = parse.unquote(filename)
                                    airport_name = filename.replace("%20", " ").replace("%2B", "+")
                                    if not "Access denied" in airport_name:
                                        if not "Blocked" in airport_name:
                                            if not "Cloudflare" in airport_name:
                                                if not "nginx" in airport_name:
                                                    name = airport_name
                                                    flag = 1
                        except:
                            pass
                    else:
                        headers = {'User-Agent': link_ua}
                        try:
                            pattern = r'(https?://)([^/]+)'
                            match = re.search(pattern, url)
                            base_url = None
                            if match:
                                base_url = match.group(1) + match.group(2)
                            response = requests.get(base_url, headers=headers, timeout=try_time)
                            html = response.content
                            soup = BeautifulSoup(html, 'html.parser')
                            title = soup.title.string
                            if not "Access denied" in title:
                                if not "Blocked" in title:
                                    if not "Cloudflare" in title:
                                        if not "nginx" in title:
                                            name = title
                                            flag = 1
                        except:
                            pass
                if flag == 0 :
                    for send_id in administrator_id :
                        try :
                            bot.send_message(send_id, f'无法识别订阅\n`{url}`', parse_mode = 'Markdown')
                        except :
                            continue
                    bot.reply_to(message, f"\\[WRONG]\\[无法识别的订阅 请手动添加]\n`{url}`", parse_mode = 'Markdown')
                    continue
                try :
                    headers = {'User-Agent': sub_ua}
                    res = requests.get(url, headers=headers, timeout=try_time)
                    if res.status_code == 200:
                        info = res.headers['subscription-userinfo']
                        info_num = re.findall(r'\d+', info)
                        size = StrSize(int(info_num[2]))
                        comment = name + "-" + size
                        if int(info_num[2]) - int(info_num[1]) - int(info_num[0]) < 10 :
                            bot.reply_to(message, "[WARNING][订阅无流量]")
                    else :
                        bot.reply_to(message, "[WRONG][无法获取订阅 请检查后手动添加]")
                        continue
                except :
                    bot.reply_to(message, "[WRONG][无法获取订阅 请检查后手动添加]")
                    continue
                
                c.execute("INSERT INTO My_sub VALUES(?,?)", (url, comment))
                conn.commit()
                bot.reply_to(message, f"\[✅]\[订阅 `{comment}` 添加成功]", parse_mode = 'Markdown')
            except :
                pass      
    except :
        bot.send_message(message.chat.id, "[WRONG][输入格式有误 请检查后重新输入]")

# 测活
@bot.message_handler(commands=['prune'])
def get_test(message) :
    if not message.chat.type == "private" :
        if not bot_name in message.text :
            if not str(message.from_user.id) in admin_id :
                return
    if str(message.from_user.id) in admin_id :
        try :
            try :
                search_str = message.text.split()[1]
            except :
                search_str = 'h'
            global testsub_flag, stop_prune
            if testsub_flag == 1 :
                bot.reply_to(message, "[WRONG][订阅正在获取中]")
                return
            testsub_flag = 1
            sent_message = bot.reply_to(message, "准备获取订阅中...")
            search_str1 = '失效'
            c.execute("SELECT rowid,URL,comment FROM My_sub WHERE URL LIKE ? OR comment LIKE ?",('%' + search_str1 + '%', '%' + search_str1 + '%'))
            result = c.fetchall()
            expto = len(result)
            c.execute("SELECT rowid,URL,comment FROM My_sub WHERE URL LIKE ? OR comment LIKE ?",('%' + search_str + '%', '%' + search_str + '%'))
            result = c.fetchall()
            total = len(result)
            if total == 0 :
                bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id, text="[WRONG][无订阅]")
                testsub_flag = 0
                return
            keyboard = []
            keyboard.append([telebot.types.InlineKeyboardButton('❎ 停止获取', callback_data='stop_prune')])
            reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
            i = 0
            sending_time = 0
            global send_percent
            expire = []
            random.shuffle(result)
            for item in result:
                i = i + 1
                cal = i / total * 100
                if cal > sending_time:
                    sending_time += send_percent
                    equal_signs = int(cal / 5)
                    space_count = 20 - equal_signs
                    temp_text = "正在获取订阅中...\n\n \[`" + "=" * equal_signs + " " * space_count + "`]\n\n目前剩余任务数量为: `" + str(total - i + 1) + "`"
                    equal_signs = int(len(expire) / (((len(expire) + 1) * total / i) * 80 / 100 + expto * 20 / 100) * 20)
                    space_count = 20 - equal_signs
                    temp_text = temp_text + "\n\n \[`" + "=" * equal_signs + " " * space_count + "`]\n\n目前失效任务数量为: `" + str(len(expire)) + "`"
                    bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id, text=temp_text, parse_mode = 'Markdown', reply_markup=reply_markup)
                url = item[1]
                c.execute("SELECT * FROM My_sub WHERE URL LIKE ?", ('%' + url + '%',))
                result = c.fetchall()
                if len(result) > 1:
                    c.execute("DELETE FROM My_sub WHERE rowid=?", (item[0],))
                    conn.commit()
                    continue
                headers = {'User-Agent': sub_ua}
                if stop_prune == 1:
                    stop_prune = 0
                    testsub_flag = 0
                    reply_markup = []
                    bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id, text="[获取已停止]", reply_markup=reply_markup)
                    return
                try:
                    res = requests.get(url, headers=headers, timeout=try_time)
                except:
                    expire.append(item[0])
                    c.execute("UPDATE My_sub SET URL=?, comment=? WHERE rowid=?", (item[1], item[2].replace('-过期', '').replace('-临期', '').replace('-失效', '').replace('-耗尽', '') + '-失效', item[0]))
                    conn.commit()
                    continue
                c.execute("UPDATE My_sub SET URL=?, comment=? WHERE rowid=?", (item[1], item[2].replace('-过期', '').replace('-临期', '').replace('-失效', '').replace('-耗尽', ''), item[0]))
                conn.commit()
                try:
                    info = res.headers['subscription-userinfo']
                    info_num = re.findall(r'\d+', info)
                    time_now = int(time.time())
                    if int(info_num[2])-int(info_num[1])-int(info_num[0])<=1:
                        c.execute("UPDATE My_sub SET URL=?, comment=? WHERE rowid=?", (item[1], item[2].replace('-过期', '').replace('-临期', '').replace('-失效', '').replace('-耗尽', '') + '-耗尽', item[0]))
                        conn.commit()
                except:
                    pass
                try:
                    if res.status_code == 200:
                        info = res.headers['subscription-userinfo']
                        info_num = re.findall(r'\d+', info)
                        time_now = int(time.time())
                        if len(info_num) >= 4:
                            lasttime = int(info_num[3]) - time_now
                            d = int(lasttime // 86400)
                            if time_now > int(info_num[3]):
                                c.execute("UPDATE My_sub SET URL=?, comment=? WHERE rowid=?", (item[1], item[2].replace('-过期', '').replace('-临期', '').replace('-失效', '').replace('-耗尽', '') + '-过期', item[0]))
                                conn.commit()
                            elif d < impend :
                                c.execute("UPDATE My_sub SET URL=?, comment=? WHERE rowid=?", (item[1], item[2].replace('-过期', '').replace('-临期', '').replace('-失效', '').replace('-耗尽', '') + '-临期', item[0]))
                                conn.commit()  
                except:
                    pass
                try:
                    u = re.findall('proxies:', res.text)[0]
                    if u == "proxies:":
                        pass
                except:
                    try:
                        text = res.text[:64]
                        text = base64.b64decode(text)
                        text = str(text)
                        if filter_base64(text):
                            pass
                        else:
                            expire.append(item[0])
                            c.execute("UPDATE My_sub SET URL=?, comment=? WHERE rowid=?", (item[1], item[2].replace('-过期', '').replace('-临期', '').replace('-失效', '').replace('-耗尽', '') + '-失效', item[0]))
                            conn.commit()
                    except:
                        expire.append(item[0])
                        c.execute("UPDATE My_sub SET URL=?, comment=? WHERE rowid=?", (item[1], item[2].replace('-过期', '').replace('-临期', '').replace('-失效', '').replace('-耗尽', '') + '-失效', item[0]))
                        conn.commit()
            reply_markup = []
            bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id, text="防删除哒咩", reply_markup=reply_markup)
            bot.delete_message(sent_message.chat.id, sent_message.message_id)
            expire = list(set(expire))
            expire.sort()
            if len(expire) == 0:
                message_raw = "无失效订阅"
            else:
                message_raw = "已失效订阅共 `" + str(len(expire)) + "` 条\n\n编号如下\n`"
                for id in expire:
                    message_raw = message_raw + str(id) + " "
                message_raw = message_raw + "`"
            for send_id in administrator_id :
                try :
                    bot.send_message(send_id, message_raw, parse_mode = 'Markdown')
                except :
                    continue
            if not message.from_user.id in administrator_id :
                bot.send_message(message.from_user.id, message_raw, parse_mode = 'Markdown')
            bot.reply_to(message, "[✅][更新成功]")
            testsub_flag = 0
        except :
            testsub_flag = 0
            bot.reply_to(message, "[WRONG][更新失败]")
    else:
        bot.reply_to(message, "[WRONG][你没有操作权限]")

# 更新临期订阅
@bot.message_handler(commands=['updatesub'])
def get_impend(message) :
    if not message.chat.type == "private" :
        if not bot_name in message.text :
            if not str(message.from_user.id) in admin_id :
                return
    if str(message.from_user.id) in admin_id :
        try :
            logger.debug(f"用户{message.from_user.id}使用了获取临期功能")
            try :
                search_str = message.text.split()[1]
            except :
                search_str = '临期'
            global testsub_flag, stop_updatesub
            if testsub_flag == 1 :
                bot.reply_to(message, "[WRONG][临期订阅正在获取中]")
                return
            testsub_flag = 1
            sent_message = bot.reply_to(message, "准备获取订阅中...")
            
            w = open('Sub/Sub.txt', 'wb+')
            c.execute("SELECT rowid,URL,comment FROM My_sub WHERE URL LIKE ? OR comment LIKE ?",('%' + search_str + '%', '%' + search_str + '%'))
            result = c.fetchall()
            
            total = len(result)
            
            if total == 0 :
                bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id, text="[WRONG][无临期订阅]")
                return
            keyboard = []
            keyboard.append([telebot.types.InlineKeyboardButton('❎ 停止获取', callback_data='stop_updatesub')])
            reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
            i = 0
            sending_time = 0
            global send_percent
            for item in result:
                try :
                    if stop_updatesub == 1:
                        stop_updatesub = 0
                        testsub_flag = 0
                        reply_markup = []
                        bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id, text="[获取已停止]", reply_markup=reply_markup)
                        return
                    i = i + 1
                    cal = i / total * 100
                    if cal > sending_time:
                        sending_time += send_percent
                        equal_signs = int(cal / 5)
                        space_count = 20 - equal_signs
                        bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id, text="正在获取订阅中\n\n \[`" + "=" * equal_signs + " " * space_count + "`]\n\n目前剩余任务数量为: `" + str(total - i + 1) + "`", parse_mode = 'Markdown', reply_markup=reply_markup)
                    url = item[1]
                    n = requests.get(backend + 'sub?target=mixed&url=' + url)
                    n = n.content.decode().replace('=', 'A')
                    if not '!' in n:
                        if not 'contain' in n:
                            w.write(n.encode())
                except :
                    pass
            reply_markup = []
            bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id, text="防删除哒咩", reply_markup=reply_markup)
            bot.delete_message(sent_message.chat.id, sent_message.message_id)
            bot.reply_to(message, "[✅][更新成功]")
            testsub_flag = 0
        except :
            bot.reply_to(message, "[WRONG][更新失败]")
            testsub_flag = 0
    else:
        bot.reply_to(message, "[WRONG][你没有操作权限]")

# 添加数据
def add_sub(message):
    try:
        url_comment = message.text.split()[1:]
        url = remove_convert(url_comment[0])
        comment = url_comment[1]
        c.execute("SELECT * FROM My_sub WHERE URL LIKE ?", ('%' + url + '%',))
        if c.fetchone():
            bot.reply_to(message, "[WRONG][订阅已存在]")
        else:
            c.execute("INSERT INTO My_sub VALUES(?,?)", (url, comment))
            conn.commit()
            bot.reply_to(message, "[✅][添加成功]")
    except:
        bot.send_message(message.chat.id, "[WRONG][输入格式有误 请检查后重新输入]")


# 删除数据
def delete_sub(message):
    try:
        id_text = message.text.split()
        for row_num in id_text[1:]:
            c.execute("DELETE FROM My_sub WHERE rowid=?", (row_num,))
            conn.commit()
        bot.reply_to(message, "[✅][删除成功]")
    except:
        bot.send_message(message.chat.id, "[WRONG][输入格式有误 请检查后重新输入]")

# 整理编号
def sort_sub(message):
    try:
        c.execute("VACUUM")
        conn.commit()
        bot.reply_to(message, "[✅][整理成功]")
    except:
        bot.send_message(message.chat.id, "[WRONG][整理失败]")

items_per_page = 20
result = None
callbacks = {}

# 查找数据
def search_sub(message):
    global items_per_page, total, result, current_page
    try:
        search_str = message.text.split()[1]
        c.execute("SELECT rowid,URL,comment FROM My_sub WHERE URL LIKE ? OR comment LIKE ?",
                  ('%' + search_str + '%', '%' + search_str + '%'))
        result = c.fetchall()
        if result:
            try :
                current_page = int(message.text.split()[2])
            except :
                current_page = 1
            
            pages = [result[i:i + items_per_page] for i in range(0, len(result), items_per_page)]
            total = len(pages)
            current_items = pages[current_page - 1]
            keyboard = []
            
            if current_page < 1:
                bot.reply_to(message, "[WRONG][页数超出范围了]")
                return
            elif current_page > total:
                bot.reply_to(message, "[WRONG][页数超出范围了]")

            for i in range(0, len(current_items), 2):
                row = current_items[i:i + 2]
                keyboard_row = []
                for item in row:
                    button = telebot.types.InlineKeyboardButton(item[2][0:10], callback_data=item[0])
                    keyboard_row.append(button)
                keyboard.append(keyboard_row)
            if total > 1:
                page_info = f'{current_page} / {total}'
                if current_page == 1 : 
                    prev_button = telebot.types.InlineKeyboardButton('      ', callback_data='blank')
                else :
                    prev_button = telebot.types.InlineKeyboardButton('上一页', callback_data='prev')
                if current_page == total : 
                    next_button = telebot.types.InlineKeyboardButton('      ', callback_data='blank')
                else :
                    next_button = telebot.types.InlineKeyboardButton('下一页', callback_data='next')
                page_button = telebot.types.InlineKeyboardButton(page_info, callback_data=f'page_info {current_page} {total}')
                page_buttons = [prev_button, page_button, next_button]
                keyboard.append(page_buttons)
            keyboard.append([telebot.types.InlineKeyboardButton('❎ 关闭', callback_data='close')])
            reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
            sent_message = bot.reply_to(message, f'已查询到{str(len(result))}条订阅', reply_markup=reply_markup)
            global sent_message_id
            sent_message_id = sent_message.message_id
            user_id = message.from_user.id
            callbacks[sent_message_id] = {'total': total, 'current_page': current_page, 'result': result, 'sent_message_id': sent_message_id}
        else:
            keyboard = []
            keyboard.append([telebot.types.InlineKeyboardButton('❎ 关闭', callback_data='close')])
            reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
            bot.reply_to(message, '[WRONG][没有查找到结果]', reply_markup = reply_markup)
    except Exception as t:
        print(t)
        bot.send_message(message.chat.id, "[WRONG][输入格式有误 请检查后重新输入]")

def update_buttons(callback_query, user_id):
    global callbacks
    callback_data = callback_query.data
    message = callback_query.message
    message_id = message.message_id
    current_page = callbacks[message_id]['current_page']
    total = callbacks[message_id]['total']
    result = callbacks[message_id]['result']
    if callback_data == 'prev' and current_page > 1:
        current_page -= 1
    elif callback_data == 'next' and current_page < total:
        current_page += 1
    pages = [result[i:i + items_per_page] for i in range(0, len(result), items_per_page)]
    current_items = pages[current_page - 1]
    keyboard = []
    for i in range(0, len(current_items), 2):
        row = current_items[i:i + 2]
        keyboard_row = []
        for item in row:
            button = telebot.types.InlineKeyboardButton(item[2][0:10], callback_data=item[0])
            keyboard_row.append(button)
        keyboard.append(keyboard_row)
    if total > 1:
        page_info = f' {current_page} / {total}'
        if current_page == 1 : 
            prev_button = telebot.types.InlineKeyboardButton('      ', callback_data='blank')
        else :
            prev_button = telebot.types.InlineKeyboardButton('上一页', callback_data='prev')
        if current_page == total : 
            next_button = telebot.types.InlineKeyboardButton('      ', callback_data='blank')
        else :
            next_button = telebot.types.InlineKeyboardButton('下一页', callback_data='next')
        page_button = telebot.types.InlineKeyboardButton(page_info, callback_data=f'page_info {current_page} {total}')
        page_buttons = [prev_button, page_button, next_button]
        keyboard.append(page_buttons)
    keyboard.append([telebot.types.InlineKeyboardButton('❎ 关闭', callback_data='close')])
    reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
    bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message_id, reply_markup=reply_markup)
    callbacks[message_id]['current_page'] = current_page

# 修改备注
@bot.message_handler(commands=['comment'])
def update_sub(message):
    if not message.chat.type == "private" :
        if not bot_name in message.text :
            if not str(message.from_user.id) in admin_id:
                return
    if str(message.from_user.id) in admin_id:
        try:
            row_num = message.text.split()[1]
            comment = message.text.split()[2]
            c.execute("UPDATE My_sub SET comment=? WHERE rowid=?", (comment, row_num))
            conn.commit()
            bot.reply_to(message, "[✅][更新成功]")
        except:
            bot.send_message(message.chat.id, "[WRONG][输入格式有误 请检查后重新输入]")

# 编号获取
@bot.message_handler(commands=['get'])
def get_sub(message):
    if not message.chat.type == "private" :
        if not bot_name in message.text :
            if not str(message.from_user.id) in admin_id:
                return
    if str(message.from_user.id) in admin_id:
        try:
            row_num = int(message.text.split()[1])
            c.execute("SELECT rowid,URL,comment FROM My_sub WHERE rowid=?", (row_num,))
            result = c.fetchone()
            headers = {'User-Agent': sub_ua}
            output_test = ''
            try :
                try:
                    res = requests.get(result[1], headers=headers, timeout=try_time)
                except:
                    output_text = '连接错误'
                if res.status_code == 200:
                    try:
                        info = res.headers['subscription-userinfo']
                        info_num = re.findall(r'\d+', info)
                        time_now = int(time.time())
                        output_text_head = '上行：`' + StrOfSize(int(info_num[0])) + '`\n下行：`' + StrOfSize(int(info_num[1])) + '`\n剩余：`' + StrOfSize(int(info_num[2]) - int(info_num[1]) - int(info_num[0])) + '`\n总共：`' + StrOfSize(int(info_num[2])) + '`'
                        if len(info_num) >= 4:
                            timeArray = time.localtime(int(info_num[3]) + 28800)
                            dateTime = time.strftime("%Y-%m-%d", timeArray)
                            if time_now <= int(info_num[3]):
                                lasttime = int(info_num[3]) - time_now
                                output_text = output_text_head + '\n过期时间：`' + dateTime + '`\n剩余时间：`' + sec_to_data(lasttime) + '`'
                            elif time_now > int(info_num[3]):
                                output_text = output_text_head + '\n此订阅已于 `' + dateTime + '`过期'
                        else:
                            output_text = output_text_head + '\n过期时间：`没有说明`'
                    except:
                        output_text = '`无流量信息`'
                else:
                    output_text = '`无法访问`'

                try :
                    d = int(lasttime // 86400)
                    if d < impend :
                        if not '临期' in result[2] :
                            c.execute("UPDATE My_sub SET URL=?, comment=? WHERE rowid=?", (result[1], result[2] + '-临期', result[0]))
                            conn.commit()
                except :
                    pass
            except:
                output_text = '`无流量信息`'
            keyboard = []
            keyboard.append([telebot.types.InlineKeyboardButton('❎ 关闭', callback_data='close')])
            reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
            if message.chat.id in trust_list :
                bot.send_message(message.chat.id, '编号 `{}`\n订阅 `{}`\n说明 `{}`\n\n{}'.format(result[0], result[1], result[2], output_text),parse_mode='Markdown', reply_markup = reply_markup)
            else :
                bot.send_message(message.from_user.id, '编号 `{}`\n订阅 `{}`\n说明 `{}`\n\n{}'.format(result[0], result[1], result[2], output_text),parse_mode='Markdown', reply_markup = reply_markup)
            logger.debug(f"用户{message.from_user.id}从BOT获取了{result}")
        except:
            bot.send_message(message.chat.id, "[WARNING][该订阅已被管理员删除]")

# 页数跳转
@bot.message_handler(commands=['page'])
def page_change(message):
    if not message.chat.type == "private" :
        if not bot_name in message.text :
            if not str(message.from_user.id) in admin_id:
                return

    if str(message.from_user.id) in admin_id:
        if message.reply_to_message :
            reply = message.reply_to_message
            try :
                current_page = int(message.text.split()[1])
            except :
                bot.reply_to(message, "[WARNING][命令格式不对呢]")
                return
        else :
            bot.reply_to(message, "[WARNING][请回复订阅消息呢]")
            return
        
        message_temp = message.reply_to_message
        message_id = message_temp.message_id
        total = callbacks[message_id]['total']
        result = callbacks[message_id]['result']
        if current_page < 1:
            bot.reply_to(message, "[WARNING][页数超出范围了]")
            return
        elif current_page > total:
            bot.reply_to(message, "[WARNING][页数超出范围了]")
            return
        pages = [result[i:i + items_per_page] for i in range(0, len(result), items_per_page)]
        current_items = pages[current_page - 1]
        keyboard = []
        for i in range(0, len(current_items), 2):
            row = current_items[i:i + 2]
            keyboard_row = []
            for item in row:
                button = telebot.types.InlineKeyboardButton(item[2][0:10], callback_data=item[0])
                keyboard_row.append(button)
            keyboard.append(keyboard_row)
        if total > 1:
            page_info = f' {current_page} / {total}'
            if current_page == 1 : 
                prev_button = telebot.types.InlineKeyboardButton('      ', callback_data='blank')
            else :
                prev_button = telebot.types.InlineKeyboardButton('上一页', callback_data='prev')
            if current_page == total : 
                next_button = telebot.types.InlineKeyboardButton('      ', callback_data='blank')
            else :
                next_button = telebot.types.InlineKeyboardButton('下一页', callback_data='next')
            page_button = telebot.types.InlineKeyboardButton(page_info, callback_data=f'page_info {current_page} {total}')
            page_buttons = [prev_button, page_button, next_button]
            keyboard.append(page_buttons)
        keyboard.append([telebot.types.InlineKeyboardButton('❎ 关闭', callback_data='close')])
        reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
        bot.edit_message_reply_markup(chat_id=message_temp.chat.id, message_id=message_id, reply_markup=reply_markup)
        callbacks[message_id]['current_page'] = current_page
    else:
        bot.reply_to(message, "[WRONG][你没有操作权限]")

# 更新数据
def update_sub(message):
    try:
        row_num = message.text.split()[1]
        url_comment = message.text.split()[2:]
        url = url_comment[0]
        comment = url_comment[1]
        c.execute("UPDATE My_sub SET URL=?, comment=? WHERE rowid=?", (url, comment, row_num))
        conn.commit()
        bot.reply_to(message, "[✅][更新成功]")
    except:
        bot.send_message(message.chat.id, "[WRONG][输入格式有误 请检查后重新输入]")

# 交换订阅
@bot.message_handler(commands=['swap'])
def swap_sub(message) :
    if not message.chat.type == "private" :
        if not bot_name in message.text :
            if not str(message.from_user.id) in admin_id :
                return
    if str(message.from_user.id) in admin_id :
        try :
            try :
                row_num1 = int(message.text.split()[1])
                row_num2 = int(message.text.split()[2])
            except :
                bot.send_message(message.chat.id, "[WRONG][输入格式有误 请检查后重新输入]")
                return
            c.execute("SELECT rowid,URL,comment FROM My_sub WHERE rowid=?", (row_num1,))
            result1 = c.fetchone()
            c.execute("SELECT rowid,URL,comment FROM My_sub WHERE rowid=?", (row_num2,))
            result2 = c.fetchone()
            c.execute("UPDATE My_sub SET URL=?, comment=? WHERE rowid=?", (result2[1], result2[2], row_num1))
            c.execute("UPDATE My_sub SET URL=?, comment=? WHERE rowid=?", (result1[1], result1[2], row_num2))
            bot.reply_to(message, "[✅][交换成功]")
        except :
            bot.reply_to(message, "[WRONG][交换失败]")
    else:
        bot.reply_to(message, "[WRONG][你没有操作权限]")


# 接收xlsx表格
#@bot.message_handler(content_types=['document'], func = lambda message:message.chat.type == "private")
def handle_document(message):
    if str(message.from_user.id) in admin_id:
        file_id = message.document.file_id
        file_info = bot.get_file(file_id)
        try:
            file = bot.download_file(file_info.file_path)
            with open('sub.xlsx', 'wb') as f:
                f.write(file)
            df = pd.read_excel('sub.xlsx')
            for i in range(len(df)):
                c.execute("SELECT * FROM My_sub WHERE URL=?", (df.iloc[i, 0],))
                if not c.fetchone():
                    c.execute("INSERT INTO My_sub VALUES(?,?)", (df.iloc[i, 0], df.iloc[i, 1]))
                    conn.commit()
            bot.reply_to(message, "[✅][导入成功]")
        except:
            bot.send_message(message.chat.id, "[WRONG][导入的文件格式错误 请检查文件后缀是否为xlsx后重新导入]")
    else:
        bot.reply_to(message, "[WARNING][你不是管理员 禁止操作]")

def subinfo(message, url):
    headers = {'User-Agent': sub_ua}
    try:
        message_raw = url
        final_output = ''
        reply_list = []
        try : 
            reply_list = re.findall("https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]", message.reply_to_message.text)
        except :
            pass
        url_list = re.findall("https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]",message_raw)
        try :
            url_list.extend(reply_list)
        except :
            pass
        url_list = list(set(url_list))
        for urla in url_list:
            url = remove_convert(urla)
            logger.debug(f"用户{message.from_user.id}使用了/subinfo功能查询了{url}订阅")
            try:
                res = requests.get(url, headers=headers, timeout=try_time)
            except:
                final_output = final_output +'订阅链接：`' + url + '`\n连接错误' + '\n\n'
                continue
            if res.status_code == 200:
                try:
                    comment = ""
                    name = ""
                    size = ""
                    flag = 0
                    try :
                        r = open('airport.list',encoding='utf8')
                        while True :
                            line = r.readline()
                            if not line :
                                break
                            a = line.split()[0]
                            b = line.split()[1]
                            if a in url :
                                name = b
                                flag = 1
                                break
                    except :
                        pass
                    if flag == 0 :
                        if "api/v1/client/subscribe?token" in url:
                            if "&flag=clash" not in url:
                                url = url + "&flag=clash"
                            else:
                                pass
                            try:
                                response = requests.get(url, timeout=try_time)
                                header = response.headers.get('Content-Disposition')
                                if header:
                                    pattern = r"filename\*=UTF-8''(.+)"
                                    result = re.search(pattern, header)
                                    if result:
                                        filename = result.group(1)
                                        filename = parse.unquote(filename)
                                        airport_name = filename.replace("%20", " ").replace("%2B", "+")
                                        if not "Access denied" in airport_name:
                                            if not "Blocked" in airport_name:
                                                if not "Cloudflare" in airport_name:
                                                    if not "nginx" in airport_name:
                                                        name = airport_name
                                                        flag = 1
                            except:
                                pass
                        else:
                            headers = {
                                'User-Agent': link_ua}
                            try:
                                pattern = r'(https?://)([^/]+)'
                                match = re.search(pattern, url)
                                base_url = None
                                if match:
                                    base_url = match.group(1) + match.group(2)
                                response = requests.get(base_url, headers=headers, timeout=try_time)
                                html = response.content
                                soup = BeautifulSoup(html, 'html.parser')
                                title = soup.title.string
                                if not "Access denied" in title:
                                    if not "Blocked" in title:
                                        if not "Cloudflare" in title:
                                            if not "nginx" in title:
                                                name = title
                                                flag = 1
                            except:
                                pass
                    info = res.headers['subscription-userinfo']
                    info_num = re.findall(r'\d+', info)
                    time_now = int(time.time())
                    if flag == 1:
                        output_text_head = '订阅链接：`' + url + '`\n机场名称：`' + name + '`\n已用上行：`' + StrOfSize(int(info_num[0])) + '`\n已用下行：`' + StrOfSize(int(info_num[1])) + '`\n剩余：`' + StrOfSize(int(info_num[2]) - int(info_num[1]) - int(info_num[0])) + '`\n总共：`' + StrOfSize(int(info_num[2]))
                    else:
                        output_text_head = '订阅链接：`' + url + '`\n已用上行：`' + StrOfSize(int(info_num[0])) + '`\n已用下行：`' + StrOfSize(int(info_num[1])) + '`\n剩余：`' + StrOfSize(int(info_num[2]) - int(info_num[1]) - int(info_num[0])) + '`\n总共：`' + StrOfSize(int(info_num[2]))
                    if len(info_num) >= 4:
                        timeArray = time.localtime(int(info_num[3]) + 28800)
                        dateTime = time.strftime("%Y-%m-%d", timeArray)
                        if time_now <= int(info_num[3]):
                            lasttime = int(info_num[3]) - time_now
                            output_text = output_text_head + '`\n过期时间：`' + dateTime + '`\n剩余时间：`' + sec_to_data(lasttime) + '`'
                        elif time_now > int(info_num[3]):
                            output_text = output_text_head + '`\n此订阅已于`' + dateTime + '`过期'
                    else:
                        output_text = output_text_head + '`\n到期时间：`没有说明`'
                except:
                    output_text = '订阅链接：`' + url + '`\n无流量信息'
            else:
                output_text = '订阅链接：`' + url + '`\n无法访问\n'
            final_output = final_output + output_text + '\n\n'
        return (final_output)
    except:
        return ('参数错误')

@bot.message_handler(commands=['subinfo', 'info', 'i'])
def get_subinfo(message):
    if not message.chat.type == "private" :
        if not bot_name in message.text :
            if not str(message.from_user.id) in admin_id:
                return
    if admin_only == 1:
        if not str(message.from_user.id) in admin_id :
            bot.reply_to(message, "[WRONG][你没有操作权限]")
            return
    info_text = subinfo(message, message.text)
    try:
        bot.reply_to(message, info_text,parse_mode='Markdown')
    except:
        return

def sub_convert(message):
    try:
        try : 
            reply_list = re.findall("[-A-Za-z0-9+&@#/%?=~_|!:,.;]+://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]", message.reply_to_message.text)
        except :
            pass
        url_list = re.findall("[-A-Za-z0-9+&@#/%?=~_|!:,.;]+://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]", message.text)
        try :
            url_list.extend(reply_list)
        except :
            pass
        result = "[订阅链接]("+ backend + "sub?target=" + target + "&url=" + parse.quote_plus(remove_convert(url_list[0]))
        logger.debug(f"用户{message.from_user.id}使用了/convert功能转换了{url_list[0]}订阅")
        for url in url_list[1:]:
            logger.debug(f"用户{message.from_user.id}使用了/convert功能转换了{url}订阅")
            if len(url) != 0:
                    result = result + "|" + parse.quote_plus(remove_convert(url))
        result = result + "&config=" + config + parameter + ")"
        return result
    except:
        return ('参数错误')

@bot.message_handler(commands=['convert'])
def get_subzh(message):
    if not message.chat.type == "private" :
        if not bot_name in message.text :
            if not str(message.from_user.id) in admin_id:
                return
    if admin_only == 1:
        if not str(message.from_user.id) in admin_id :
            bot.reply_to(message, "[WRONG][你没有操作权限]")
            return
    atext = sub_convert(message)
    bot.reply_to(message, atext, parse_mode = 'Markdown')

@bot.message_handler(commands=['short'])
def get_subzh(message):
    if not message.chat.type == "private" :
        if not bot_name in message.text :
            if not str(message.from_user.id) in admin_id:
                return
    if admin_only == 1:
        if not str(message.from_user.id) in admin_id :
            bot.reply_to(message, "[WRONG][你没有操作权限]")
            return
    url = ""
    try : 
        url = re.findall("[-A-Za-z0-9+&@#/%?=~_|!:,.;]+://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]", message.reply_to_message.text)
    except :
        url = re.findall("[-A-Za-z0-9+&@#/%?=~_|!:,.;]+://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]", message.text)
    url = url[0]
    try :
        data = requests.get(shortlink + url, timeout=try_time)
        url = re.findall("https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]",data.content.decode())
        url = url[0]
    except :
        pass
    
    bot.reply_to(message, url, parse_mode = 'Markdown')

class sspanel():
    def __init__(self,url,proxy=None):
        self._proxies = proxy
        self._name=''
        self._url = url
        self._reg_url=''
        self._login_url = ''
        self._user_url = ''
        self._sub=''
    
    def set_env(self):
        self._name = urllib.parse.urlparse(self._url).netloc
        self._reg_url = 'https://' + self._name + '/auth/register'
        self._login_url = 'https://' + self._name + '/auth/login'
        self._user_url = 'https://' + self._name + '/user'

    def register(self,email,password):
        headers= {
            "User-Agent":link_ua,
            "referer": self._reg_url
        }
        data={
            "email":email,
            "name":password,
            "passwd":password,
            "repasswd":password,
            "invite_code":None,
            "email_code":None
        }
        geetest={
                "geetest_challenge": "98dce83da57b0395e163467c9dae521b1f",
                "geetest_validate": "bebe713_e80_222ebc4a0",
                "geetest_seccode": "bebe713_e80_222ebc4a0|jordan"}
        data.update(geetest)
        with requests.session() as session:
            resp = session.post(self._reg_url,headers=headers,data=data,timeout=5,proxies=self._proxies)

            data ={
                'email': email,
                'passwd': password,
                'code': '',
                'remember_me': 1,
            }
            try:
                resp = session.post(self._login_url,headers=headers,data=data,timeout=5,proxies=self._proxies)
            except:
                pass

            resp = session.get(self._user_url,headers=headers,timeout=5,proxies=self._proxies)
            try:
                token = re.search("https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+clash=1", resp.text).group(0)
            except:
                token= re.search("https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+sub=3", resp.text).group(0)
            self._sub = token
        return token

        
    def getSubscribe(self):
        password=''.join(random.sample(string.ascii_letters + string.digits + string.ascii_lowercase, 10))
        email=password+"@gmail.com"
        subscribe=self.register(email,password)
        return subscribe

class v2board():
    def __init__(self,url,proxy=None):
        self._proxies = proxy
        self._name=''
        self._url = url
        self._reg_url=''
        self._sub=''
    
    def set_env(self):
        self._name = urllib.parse.urlparse(self._url).netloc
        self._reg_url = 'https://' + self._name + '/api/v1/passport/auth/register'
        self._sub = 'https://' + self._name + '/api/v1/client/subscribe?token={token}'

    def register(self,email,password):
        headers= {
            "User-Agent":link_ua,
            "Refer": self._url
        }
        data={
            "email":email,
            "password":password,
            "invite_code":None,
            "email_code":None
        }
        req=requests.post(self._reg_url,headers=headers,data=data,timeout=5,proxies=self._proxies)
        return req
        
    def getSubscribe(self):
        password=''.join(random.sample(string.ascii_letters + string.digits + string.ascii_lowercase, 10))
        email=password+"@gmail.com"
        req=self.register(email,password)
        token=req.json()["data"]["token"]
        subscribe=self._sub.format(token=token)
        return subscribe

@bot.message_handler(commands=['free'])
def get_baipiao(message):
    if not message.chat.type == "private" :
        if not bot_name in message.text :
            if not str(message.from_user.id) in admin_id:
                return
    if admin_only == 1:
        if not str(message.from_user.id) in admin_id :
            bot.reply_to(message, "[WRONG][你没有操作权限]")
            return
    url = message.text.split()[1]
    if not '://' in url :
        url = 'https://' + url
    sent_message = bot.reply_to(message, '[✅][获取中...]')
    link = ""
    try :
        v2b = v2board(url)
        v2b.set_env()
        link = v2b.getSubscribe()
        bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id, text = '`' + link + '`', parse_mode = 'Markdown')
    except :
        try :
            ss = sspanel(url)
            ss.set_env()
            link = ss.getSubscribe()
            bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id, text = '`' + link + '`', parse_mode = 'Markdown')
        except :
            bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id, text = '[WRONG][获取失败]')

def auto_checksubinfo(url):
    headers = {'User-Agent': sub_ua}
    try:
        message_raw = url
        final_output = ''
        reply_list = []
        try : 
            reply_list = re.findall("https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]", message.reply_to_message.text)
        except :
            pass
        url_list = re.findall("https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]",message_raw)
        try :
            url_list.extend(reply_list)
        except :
            pass
        url_list = list(set(url_list))
        for url in url_list:
            try:
                res = requests.get(url, headers=headers, timeout=try_time)
            except:
                final_output = final_output +'订阅链接域名：`' + urllib.parse.urlparse(url).netloc + '`\n连接错误' + '\n\n'
                continue
            if res.status_code == 200:
                try:
                    info = res.headers['subscription-userinfo']
                    info_num = re.findall(r'\d+', info)
                    time_now = int(time.time())
                    output_text_head = '订阅链接域名：`' + urllib.parse.urlparse(url).netloc + '`\n已用上行：`' + StrOfSize(int(info_num[0])) + '`\n已用下行：`' + StrOfSize(int(info_num[1])) + '`\n剩余：`' + StrOfSize(int(info_num[2]) - int(info_num[1]) - int(info_num[0])) + '`\n总共：`' + StrOfSize(int(info_num[2]))
                    if len(info_num) >= 4:
                        timeArray = time.localtime(int(info_num[3]) + 28800)
                        dateTime = time.strftime("%Y-%m-%d", timeArray)
                        if time_now <= int(info_num[3]):
                            lasttime = int(info_num[3]) - time_now
                            output_text = output_text_head + '`\n过期时间：`' + dateTime + '`\n剩余时间：`' + sec_to_data(lasttime) + '`'
                        elif time_now > int(info_num[3]):
                            output_text = output_text_head + '`\n此订阅已于`' + dateTime + '`过期'
                    else:
                        output_text = output_text_head + '`\n到期时间：`没有说明`'
                except:
                    output_text = '订阅链接域名：`' + urllib.parse.urlparse(url).netloc + '`\n无流量信息'
            else:
                output_text = '订阅链接域名：`' + urllib.parse.urlparse(url).netloc + '`\n无法访问\n'
            final_output = final_output + output_text + '\n\n'
        return (final_output)
    except:
        return ('参数错误')

@bot.message_handler(commands=['connect'])
def page_change(message):
    if not message.chat.type == "private" :
        if not bot_name in message.text :
            if not str(message.from_user.id) in admin_id:
                return
    if str(message.from_user.id) in admin_id:
        command = message.text.split()[1]
        if command == "index":
            try:
                search_str = message.text.split()[2]
                c.execute("SELECT rowid,URL,comment FROM My_sub WHERE URL LIKE ? OR comment LIKE ?",('%' + search_str + '%', '%' + search_str + '%'))
                result = c.fetchall()
                try :
                    current_page = int(message.text.split()[3])
                except :
                    current_page = 1

                pages = [result[i:i + items_per_page] for i in range(0, len(result), items_per_page)]
                total = len(pages)
                current_items = pages[current_page - 1]
                
                output_text = str(len(result)) + ' ' + str(current_page) + ' ' + str(total) + ' '
                for item in current_items:
                    output_text = output_text + str(item[0]) + ' ' + str(item[2]).replace(' ', '') + ' '
                output_text = base64.b64encode(output_text.encode('utf-8'))
                bot.reply_to(message, output_text)
            except:
                output_text = "None"
                output_text = base64.b64encode(output_text.encode('utf-8'))
                bot.reply_to(message, output_text)
                return
        elif command == "get":
            row_num = int(message.text.split()[2])
            c.execute("SELECT rowid,URL,comment FROM My_sub WHERE rowid=?", (row_num,))
            result = c.fetchone()
            if result:
                output_text = str(result[0]) + ' ' + str(result[1]).replace(' ', '') + ' ' + str(result[2]).replace(' ', '')
                logger.debug(f"用户{message.from_user.id}从BOT获取了{result}")
            else:
                output_text = "None"
            output_text = base64.b64encode(output_text.encode('utf-8'))
            bot.reply_to(message, output_text)  
    else:
        bot.reply_to(message, "[WRONG][你没有操作权限]")

# 测试延迟
@bot.message_handler(commands=['ping'])
def get_ping(message):
    if not message.chat.type == "private" :
        if not bot_name in message.text :
            if '@' in message.text :
                return
    if admin_only == 1:
        if not str(message.from_user.id) in admin_id :
            bot.reply_to(message, "[WRONG][你没有操作权限]")
            return
    start = datetime.now()
    message =  bot.reply_to(message,"Ping : ",disable_notification=True)
    end = datetime.now()
    msg_delay = (end-start).microseconds/1000
    start = datetime.now()
    bot.edit_message_text(f"Ping : `{msg_delay:.2f}ms`",message.chat.id,message.id,parse_mode='Markdown')
    end = datetime.now()
    msg_delay = (msg_delay + (end-start).microseconds/1000) / 2
    start = datetime.now()
    bot.edit_message_text(f"Ping : `{msg_delay:.2f}ms`",message.chat.id,message.id,parse_mode='Markdown')
    end = datetime.now()
    msg_delay = (msg_delay + (end-start).microseconds/1000) / 2
    bot.edit_message_text(f"Ping : `{msg_delay:.2f}ms`",message.chat.id,message.id,parse_mode='Markdown')
    
# 版本信息
@bot.message_handler(commands=['version'])
def get_version(message):
    if not message.chat.type == "private" :
        if not bot_name in message.text :
            if '@' in message.text :
                return
    if admin_only == 1:
        if not str(message.from_user.id) in admin_id :
            bot.reply_to(message, "[WRONG][你没有操作权限]")
            return
    bot.reply_to(message, "Version: `" + version_text + "`", parse_mode = 'Markdown')

# 使用帮助
@bot.message_handler(commands=['help'])
def help_sub(message):
    if not message.chat.type == "private" :
        if not bot_name in message.text :
            if '@' in message.text :
                return
    
    if admin_only == 1:
        doc = '''[已开启唯一管理模式]
    '''
    else:
        doc = '''[游客]
查询订阅 /subinfo
转换订阅 /convert
生成短链 /short
注册试用 /free
消息延迟 /ping
版本信息 /version
    '''
    if str(message.from_user.id) in admin_id :
        doc = doc + '''
[管理]
'''
        if admin_only == 1:
            doc = '''[管理]
查询订阅 /subinfo
转换订阅 /convert
生成短链 /short
注册试用 /free
消息延迟 /ping
版本信息 /version
'''
        doc = doc + '''发送消息 /chat 内容
发送通知 /notice 内容
添加订阅 /add 订阅链接 备注
删除订阅 /del 编号
查找订阅 /search 内容
更新订阅 /update 编号 订阅链接 备注
整理订阅 /sort
自动添加 /auto 回复/内容
获取订阅 /get 编号
页面跳转 /page 页数
交换订阅 /swap 编号 编号
修改备注 /comment 编号 备注
更新临期 /updatesub
测活订阅 /prune'''
        if allow_invite == 1:
            doc = doc + '''
赠与订阅 /invite'''
        doc = doc + '''
注册任务 /register
取消任务 /unregister
离开群聊 /leave
        '''
    if str(message.from_user.id) in administrator_id :
        doc = doc + '''
[超管]
给予授权 /grant
取消授权 /ungrant
清除授权 /grantclear
授权列表 /list
信任群组 /trust
取消信任 /distrust'''
        if not str(message.from_user.id) in admin_id or allow_invite == 0:
            doc = doc + '''
赠与订阅 /invite'''
        doc = doc + '''
添加域名 /addkeyword
删除域名 /delkeyword
获取数据 /database
安装数据 /install
查询日志 /log
重载配置 /reload
保存配置 /save
获取配置 /value
设置配置 /set
    '''    
    bot.send_message(message.chat.id, doc)

# 回调
@bot.message_handler()
def auto_message(message):
    if callback_url == "":
        return
    try:
        headers = {'User-Agent': link_ua}
        data = json.dumps(str(message))
        res = requests.post(callback_url, headers=headers, data=data, timeout=try_time)
        if res.status_code == 403:
            return
        bot.reply_to(message, res.text.encode().decode("unicode_escape"), parse_mode = 'Markdown')
    except:
        pass


# 按钮点击事件
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global sent_message_id, current_page, callbacks
    user_id = call.from_user.id
    if str(call.from_user.id) in admin_id:
        if call.data == 'close':
            reply_markup = []
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="防删除哒咩", reply_markup=reply_markup)
            delete_result = bot.delete_message(call.message.chat.id, call.message.message_id)
            if delete_result is None:
                sent_message_id = None
        elif call.data == 'prev' or call.data == 'next':
            update_buttons(call, user_id)
        elif call.data.startswith('page_info'):
            result = callbacks[call.message.message_id]['result']
            v2b = ssp = imp = old = fai = 0
            for sub in result:
                if "/api/v1/" in sub[1] :
                    v2b = v2b + 1
                if "/link/" in sub[1] :
                    ssp = ssp + 1
                if "临期" in sub[2] :
                    imp = imp + 1
                if "过期" in sub[2] :
                    old = old + 1
                if "失效" in sub[2] :
                    fai = fai + 1
            bot.answer_callback_query(call.id, f"第 {call.data.split()[1]} 页  共 {call.data.split()[2]} 页\n\nV2Board 订阅 共 {v2b} 个\nSSPanel 订阅 共 {ssp} 个\n\n临期订阅 共 {imp} 个\n过期订阅 共 {old} 个\n失效订阅 共 {fai} 个", show_alert=True)
        elif call.data == 'blank':
            pass
        elif call.data == 'stop_prune':
            global stop_prune
            stop_prune = 1
        elif call.data == 'stop_updatesub':
            global stop_updatesub
            stop_updatesub = 1
        else:
            try:
                row_num = call.data
                c.execute("SELECT rowid,URL,comment FROM My_sub WHERE rowid=?", (row_num,))
                result = c.fetchone()
                headers = {'User-Agent': sub_ua}
                output_test = ''
                try :
                    try:
                        res = requests.get(result[1], headers=headers, timeout=try_time)
                    except:
                        output_text = '连接错误'
                    if res.status_code == 200:
                        try:
                            info = res.headers['subscription-userinfo']
                            info_num = re.findall(r'\d+', info)
                            time_now = int(time.time())
                            output_text_head = '上行：`' + StrOfSize(int(info_num[0])) + '`\n下行：`' + StrOfSize(int(info_num[1])) + '`\n剩余：`' + StrOfSize(int(info_num[2]) - int(info_num[1]) - int(info_num[0])) + '`\n总共：`' + StrOfSize(int(info_num[2])) + '`'
                            if len(info_num) >= 4:
                                timeArray = time.localtime(int(info_num[3]) + 28800)
                                dateTime = time.strftime("%Y-%m-%d", timeArray)
                                if time_now <= int(info_num[3]):
                                    lasttime = int(info_num[3]) - time_now
                                    output_text = output_text_head + '\n过期时间：`' + dateTime + '`\n剩余时间：`' + sec_to_data(lasttime) + '`'
                                elif time_now > int(info_num[3]):
                                    output_text = output_text_head + '\n此订阅已于 `' + dateTime + '`过期'
                            else:
                                output_text = output_text_head + '\n过期时间：`没有说明`'
                        except:
                            output_text = '`无流量信息`'
                    else:
                        output_text = '`无法访问`'

                    try :
                        d = int(lasttime // 86400)
                        if d < impend :
                            if not '临期' in result[2] :
                                c.execute("UPDATE My_sub SET URL=?, comment=? WHERE rowid=?", (result[1], result[2] + '-临期', result[0]))
                                conn.commit()
                    except :
                        pass
                except:
                    output_text = '`无流量信息`'
                keyboard = []
                keyboard.append([telebot.types.InlineKeyboardButton('❎ 关闭', callback_data='close')])
                reply_markup = telebot.types.InlineKeyboardMarkup(keyboard)
                if call.message.chat.id in trust_list :
                    bot.send_message(call.message.chat.id, '编号 `{}`\n订阅 `{}`\n说明 `{}`\n\n{}'.format(result[0], result[1], result[2], output_text),parse_mode='Markdown', reply_markup = reply_markup)
                else :
                    bot.send_message(call.from_user.id, '编号 `{}`\n订阅 `{}`\n说明 `{}`\n\n{}'.format(result[0], result[1], result[2], output_text),parse_mode='Markdown', reply_markup = reply_markup)
                logger.debug(f"用户{call.from_user.id}从BOT获取了{result}")
            except:
                bot.send_message(call.message.chat.id, "[WARNING][该订阅已被管理员删除]")
    else:
        try :
            logger.debug(f"用户{call.from_user.id}尝试使用按钮")
            bot.answer_callback_query(call.id, f"❌ 你没有权限 请不要点按钮呢", show_alert=True)
        except :
            pass

def cron_sub():
    while True:
        try:
            try:
                with open('./config.yaml', 'r', encoding='utf-8') as f:
                    data = yaml.load(stream=f, Loader=yaml.FullLoader)
                global cron_enable, cron_delay
                cron_enable = int(data['cron']['enable'])
                cron_delay = int(data['cron']['interval'])
            except:
                pass
            if not cron_enable == 0:
                c.execute("SELECT rowid,URL,comment FROM My_sub")
                result = c.fetchall()
                random.shuffle(result)
                for item in result:
                    headers = {'User-Agent': sub_ua}
                    url = item[1]
                    try:
                        res = requests.get(url, headers=headers, timeout=try_time)
                    except:
                        c.execute("UPDATE My_sub SET URL=?, comment=? WHERE rowid=?", (item[1], item[2].replace('-过期', '').replace('-临期', '').replace('-失效', '').replace('-耗尽', '') + '-失效', item[0]))
                        conn.commit()
                        continue
                    c.execute("UPDATE My_sub SET URL=?, comment=? WHERE rowid=?", (item[1], item[2].replace('-过期', '').replace('-临期', '').replace('-失效', '').replace('-耗尽', ''), item[0]))
                    conn.commit()
                    try:
                        info = res.headers['subscription-userinfo']
                        info_num = re.findall(r'\d+', info)
                        time_now = int(time.time())
                        if int(info_num[2])-int(info_num[1])-int(info_num[0])<=1:
                            c.execute("UPDATE My_sub SET URL=?, comment=? WHERE rowid=?", (item[1], item[2].replace('-过期', '').replace('-临期', '').replace('-失效', '').replace('-耗尽', '') + '-耗尽', item[0]))
                            conn.commit()
                    except:
                        pass
                    try:
                        if res.status_code == 200:
                            info = res.headers['subscription-userinfo']
                            info_num = re.findall(r'\d+', info)
                            time_now = int(time.time())
                            if len(info_num) >= 4:
                                lasttime = int(info_num[3]) - time_now
                                d = int(lasttime // 86400)
                                if time_now > int(info_num[3]):
                                    c.execute("UPDATE My_sub SET URL=?, comment=? WHERE rowid=?", (item[1], item[2].replace('-过期', '').replace('-临期', '').replace('-失效', '').replace('-耗尽', '') + '-过期', item[0]))
                                    conn.commit()
                                elif d < impend :
                                    c.execute("UPDATE My_sub SET URL=?, comment=? WHERE rowid=?", (item[1], item[2].replace('-过期', '').replace('-临期', '').replace('-失效', '').replace('-耗尽', '') + '-临期', item[0]))
                                    conn.commit()  
                    except:
                        pass
                    try:
                        u = re.findall('proxies:', res.text)[0]
                        if u == "proxies:":
                            pass
                    except:
                        try:
                            text = res.text[:64]
                            text = base64.b64decode(text)
                            text = str(text)
                            if filter_base64(text):
                                pass
                            else:
                                c.execute("UPDATE My_sub SET URL=?, comment=? WHERE rowid=?", (item[1], item[2].replace('-过期', '').replace('-临期', '').replace('-失效', '').replace('-耗尽', '') + '-失效', item[0]))
                                conn.commit()
                        except:
                            c.execute("UPDATE My_sub SET URL=?, comment=? WHERE rowid=?", (item[1], item[2].replace('-过期', '').replace('-临期', '').replace('-失效', '').replace('-耗尽', '') + '-失效', item[0]))
                            conn.commit()
                        
                for cron in cron_list:
                    flag = False
                    try :
                        for i in cron:
                            send_id = i
                            search_str = cron.get(i)
                            flag = True
                    except :
                        send_id = cron
                        search_str = 'h'
                    c.execute("SELECT rowid,URL,comment FROM My_sub WHERE URL LIKE ? OR comment LIKE ?",('%' + search_str + '%', '%' + search_str + '%'))
                    result = c.fetchall()
                    al = []
                    imp = []
                    old = []
                    fai = []
                    emp = []
                    for sub in result:
                        if "-临期" in sub[2]:
                            imp.append(sub)
                        if "-过期" in sub[2]:
                            old.append(sub)
                        if "-失效" in sub[2]:
                            fai.append(sub)
                        if "-耗尽" in sub[2]:
                            emp.append(sub)
                        if "临期" in sub[2] or "-耗尽" in sub[2] or "-过期" in sub[2] or "-失效" in sub[2]:
                            al.append(sub)
                    text = f'订阅监测报告\n\n计划: `every {cron_delay}s`\n任务: `{send_id}`'
                    if flag:
                        text = text + f' : `{search_str}`'
                    text = text + f'\n概要: `{len(result) - len(al)}/{len(result)}`\n'
                    if not len(al) == 0:
                        text = text + '详情:\n'
                        if len(imp) == 0:
                            pass
                        elif len(imp) > 10:
                            text = text + '> 临期订阅\n - `'
                            for sub in imp:
                                text = text + str(sub[0]) + ' '
                            text = text + '`\n'
                        else:
                            text = text + '> 临期订阅\n'
                            for sub in imp:
                                sn = sub[2].replace('-过期', '').replace('-临期', '').replace('-失效', '').replace('-耗尽', '')[0:10]
                                text = text + f' - `{sub[0]} {sn}`\n'
                        if len(emp) == 0:
                            pass
                        elif len(emp) > 10:
                            text = text + '> 耗尽订阅\n - `'
                            for sub in emp:
                                text = text + str(sub[0]) + ' '
                            text = text + '`\n'
                        else:
                            text = text + '> 耗尽订阅\n'
                            for sub in emp:
                                sn = sub[2].replace('-过期', '').replace('-临期', '').replace('-失效', '').replace('-耗尽', '')[0:10]
                                text = text + f' - `{sub[0]} {sn}`\n'
                        if len(old) == 0:
                            pass
                        elif len(old) > 10:
                            text = text + '> 过期订阅\n - `'
                            for sub in old:
                                text = text + str(sub[0]) + ' '
                            text = text + '`\n'
                        else:
                            text = text + '> 过期订阅\n'
                            for sub in old:
                                sn = sub[2].replace('-过期', '').replace('-临期', '').replace('-失效', '').replace('-耗尽', '')[0:10]
                                text = text + f' - `{sub[0]} {sn}`\n'
                        if len(fai) == 0:
                            pass
                        elif len(fai) > 10:
                            text = text + '> 失效订阅\n - `'
                            for sub in fai:
                                text = text + str(sub[0]) + ' '
                            text = text + '`\n'
                        else:
                            text = text + '> 失效订阅\n'
                            for sub in fai:
                                sn = sub[2].replace('-过期', '').replace('-临期', '').replace('-失效', '').replace('-耗尽', '')[0:10]
                                text = text + f' - `{sub[0]} {sn}`\n'
                    try:
                        bot.send_message(send_id, text, parse_mode = 'Markdown')
                    except:
                        pass
                sleep(cron_delay)
            else:
                sleep(10)
        except:
            sleep(10)

def pollbot():
    logger.debug(f"[程序已启动]")
    for send_id in administrator_id :
        try :
            bot.send_message(send_id, '[程序已启动]')
        except :
            continue
    print('')
    botinit()
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            pass

if __name__ == '__main__':
    t1 = threading.Thread(target = pollbot)
    t2 = threading.Thread(target = cron_sub)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
