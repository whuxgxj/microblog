# -*- coding: utf-8 -*-
import urllib2
import cookielib
import WeiboEncode
import WeiboSearch


class WeiboLogin:
  def __init__(self, user, pwd,header, enableProxy = False):
    "初始化WeiboLogin，enableProxy表示是否使用代理服务器，默认关闭"
    print "Initializing WeiboLogin..."
    self.userName = user
    self.passWord = pwd
    self.enableProxy = enableProxy
    self.serverUrl = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.11)&_=1379834957683"
    self.loginUrl = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.11)"
    self.postHeader = header
#EnableCookie函数比较简单
  def EnableCookie(self, enableProxy):
    "Enable cookie & proxy (if needed)."

    #建立cookie
    cookiejar = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cookiejar)
    if enableProxy:
      #使用代理
      proxy_support = urllib2.ProxyHandler({'http':'http://127.0.0.1:8087',
                                            'https':'https://127.0.0.1:8087'})
      opener = urllib2.build_opener(proxy_support, cookie_support, urllib2.HTTPHandler)
      print "Proxy enabled"
    else:
      opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
      #构建cookie对应的opener
      urllib2.install_opener(opener)

  def GetServerTime(self):
    "Get server time and nonce, which are used to encode the password"

    print "Getting server time and nonce..."
    #得到网页内容
    serverData = urllib2.urlopen(self.serverUrl).read()
    print serverData
    try:
      #解析得到serverTime，nonce等
      serverTime, nonce, pubkey, rsakv = WeiboSearch.sServerData(serverData)
      return serverTime, nonce, pubkey, rsakv
    except:
      print 'Get server time & nonce error!'
      return None

  def Login(self):
    "登陆程序"
    self.EnableCookie(self.enableProxy)#cookie或代理服务器配置

    #登陆的第一步
    serverTime, nonce, pubkey, rsakv = self.GetServerTime()
    #加密用户和密码
    postData = WeiboEncode.PostEncode(self.userName, self.passWord, serverTime, nonce, pubkey, rsakv)
    print "Post data length:\n", len(postData)
    req = urllib2.Request(self.loginUrl, postData, self.postHeader)
    print "Posting request..."
    #登陆的第二步——解析新浪微博的登录过程中3
    result = urllib2.urlopen(req)

    text = result.read()
    try:
      #解析重定位结果
      loginUrl = WeiboSearch.sRedirectData(text)
      urllib2.urlopen(loginUrl)
    except:
      print 'Login error!'
      return False

    print 'Login sucess!'
    return True
