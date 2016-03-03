#-*- coding: utf8-*-
import WeiboLogin
import GetWeiboPage
import PagePlyr
from pandas import DataFrame


class MBScrab:
	def __init__(self,username,pwd,header):
		self.username=username
		self.pwd=pwd
		self.header=header

	def scrab_one_user(self,uid,num):
		##登陆
		weiboLogin = WeiboLogin.WeiboLogin(self.username, self.pwd,self.header)
		weiboLogin.Login()

		##开始获取页面
		WBmsg = GetWeiboPage.getWeiboPage()
		WBmsg.body['uid'] = uid

		##构造微博数据存储结构
		wb_detail = []
		wb_all = {}
		wb_all = wb_all.fromkeys(wb_detail, [])
		wb_frame = DataFrame(wb_all, index=[])
		for n in range(1, num):
	        # 生成页面url地址
			url = 'http://weibo.com/' + uid + '?is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page=' + str(n)

			#print WBmsg.get_firstpage(url,n)
	        all_weibo=PagePlyr.parse_page(PagePlyr.get_json_content(WBmsg.get_firstpage(url,n)))
	        wb_frame=wb_frame.append(all_weibo, ignore_index=True)
	        all_weibo=PagePlyr.parse_page(PagePlyr.get_json_content( WBmsg.get_secondpage(url,n)))
	        wb_frame=wb_frame.append(all_weibo, ignore_index=True)
	        all_weibo=PagePlyr.parse_page(PagePlyr.get_json_content(WBmsg.get_thirdpage(url,n)))
	        wb_frame=wb_frame.append(all_weibo, ignore_index=True)

	        print n
		return wb_frame

header={"user-agent":"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/528.10 (KHTML, like Gecko) Chrome/2.0.157.0 Safari/528.10",}
wbs=MBScrab("18571014813","052cd138049",header)
wbs.scrab_one_user("yangmiblog",3).to_csv("weibo.csv",encoding="utf-8",index=False)      
  
        