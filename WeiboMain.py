# -*- coding: utf-8 -*-
import urllib2
import WeiboEncode
import WeiboSearch
from numpy import *
import GetWeiboPage
import WeiboLogin
import PagePlyr
import getWeibo_cn
import os
import os.path
import time
import random
from pyExcelerator import *
import sys
from pandas import DataFrame
reload(sys)
sys.setdefaultencoding('utf-8')

# 输入待抓取用户uid以及要抓取的页面总数


def log_scrab(uid, num):
    # # 输入邮箱（账号）,密码
    # weiboLogin = WeiboLogin.WeiboLogin('whuxgxj@sina.com', '052cd138049')
    # # 模拟登陆
    # weiboLogin.Login()
    # 初始化页面获取类
    WBmsg = GetWeiboPage.getWeiboPage()
    for n in range(1, num):
        # 生成页面url地址
        url = 'http://weibo.com/' + uid + \
            '?is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page=' + \
            str(n)
        # 抓取第一屏信息
        WBmsg.get_firstpage(url, n, uid)
        # 抓取第二屏
        WBmsg.get_secondpage(url, n, uid)
        # 抓取第三屏
        WBmsg.get_thirdpage(url, n, uid)
        print n, url

# 处理已抓取网页


def merge_html(uid):
    dir = ".\\" + uid
    filepaths = os.listdir(dir)
    wb_detail = []
    wb_all = {}
    wb_all = wb_all.fromkeys(wb_detail, [])
    wb_frame = DataFrame(wb_all, index=[])
    for filepath in filepaths:
        filepath = os.path.join(dir, filepath)
        print filepath
        json_file = PagePlyr.get_json_content(filepath)
        if json_file == None:
            # os.remove(filepath)
            continue
        all_weibo = PagePlyr.parse_page(json_file)
        wb_frame = wb_frame.append(all_weibo, ignore_index=True)
    return wb_frame


# 获取某条微博点赞用户的uid列表
def get_uid():
    url = "http://weibo.cn/attitude/D9fIu1KEC"
    uid_list = []
    for i in range(1, 65018):
        urls = url + "?&page=" + str(i)
        uid = getWeibo_cn.get_cn_url(urls)
        uid_list = uid_list + uid
        print i, len(uid_list)
        time.sleep(random.uniform(0, 2))
        f = open("uid.txt", "a")
        for each in uid:
            f.write(each + "\n")
        f.close()
    # 将uid列表写入文档


# 抓取用户个人资料网页


def get_uid_html():
    ui = open("uid.txt", "r")
    uids = ui.readlines()
    ui.close()
    for each in uids:
        t = random.randint(1, 10)
        print uids.index(each) - 7083, t
        each = each.strip('\n')
        url = "http://weibo.com/p/100505" + each + "/info?mod=pedit_more"
        getWeibo_cn.get_info_user(url, each)
        time.sleep(t)


# 读取用户信息网页，生成用户个人信息表
def get_usr_info_table():
    info = ".\infos"
    url_path = os.listdir(info)
    usr_detail = []
    usr_all = {}
    usr_all = usr_all.fromkeys(usr_detail, [])
    usr_frame = DataFrame(usr_all, index=[])
    for each in url_path:
        filepath = os.path.join(info, each)
        try:
            html_wb, html_self = getWeibo_cn.get_info_detail(filepath)
            usr_info = getWeibo_cn.get_user_info(html_wb, html_self)
            usr_info["id"] = filepath
            for o in usr_info:
                print usr_info[o], o
            usr_frame = usr_frame.append(usr_info, ignore_index=True)
        except Exception, e:
            # os.remove(filepath)
            print e
        # print url_path.index(each)
    return usr_frame


if __name__ == '__main__':
    # 登陆
    weiboLogin = WeiboLogin.WeiboLogin('18571014813', '052cd138049')
    weiboLogin.Login()

    # 登录并抓取用户微博
    uid="yaochen"
    num=189
    log_scrab(uid,num)

    # 处理已抓取的微博页面，并合并新信息到一个新的网页
    wb_detail=merge_html(uid)
    wb_detail.to_csv("weibo_"+uid+".csv",encoding="utf-8",index=False)

    # 读取某条微博点赞页面，获取用户uid
    # get_uid()
    # 读取用户uid列表，抓取用户信息网页
    # get_uid_html()

# 提取用户信息，生成用户个人信息表格
    # usr_detail=get_usr_info_table()
    # usr_detail.to_csv("usr.csv",encoding="utf-8",index=False)
