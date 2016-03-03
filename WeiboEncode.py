#coding:utf-8
import urllib
import base64
import rsa
import binascii
def PostEncode(userName, passWord, serverTime, nonce, pubkey, rsakv):
    "Used to generate POST data"

    #用户名使用base64加密
    encodedUserName = GetUserName(userName)
     #目前密码采用rsa加密
    encodedPassWord = get_pwd(passWord, serverTime, nonce, pubkey)
    postPara = {
      'entry': 'weibo',
      'gateway': '1',
      'from': '',
      'savestate': '7',
      'userticket': '1',
      'ssosimplelogin': '1',
      'vsnf': '1',
      'vsnval': '',
      'su': encodedUserName,
      'service': 'miniblog',
      'servertime': serverTime,
      'nonce': nonce,
      'pwencode': 'rsa2',
      'sp': encodedPassWord,
      'encoding': 'UTF-8',
      'prelt': '115',
      'rsakv': rsakv,     
      'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
      'returntype': 'META'
    }
    #网络编码
    postData = urllib.urlencode(postPara)
    return postData


def GetUserName(userName):
    "Used to encode user name"

    userNameTemp = urllib.quote(userName)
    userNameEncoded = base64.encodestring(userNameTemp)[:-1]
    return userNameEncoded

def get_pwd(password, servertime, nonce, pubkey):
    rsaPublickey = int(pubkey, 16)
    #创建公钥
    key = rsa.PublicKey(rsaPublickey, 65537) 
    #拼接明文js加密文件中得到
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password) 
    #加密
    passwd = rsa.encrypt(message, key) 
    #将加密信息转换为16进制。
    passwd = binascii.b2a_hex(passwd) 
    return passwd

