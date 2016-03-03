# -*- coding: utf-8 -*-  
import re
import simplejson
from bs4 import BeautifulSoup
from pandas import DataFrame
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#筛选出微博网页中勇于展现用户微博的json文件
def get_json_content(text):
	#读取网页源文件
	#正则筛选
	script=re.findall('<script>FM.view\((.*?)\);?</script>',text,re.S)
	
	for each in script:
		#json解析
		body= simplejson.loads(each)
		html=None
		if "Pl_Official_MyProfileFeed__29" not in body.values():
			continue
		#页面展现文件
		if body["domid"]=="Pl_Official_MyProfileFeed__29":
			html=body["html"]
			break
	#返回提取的html文件
	return html


def text_list(resultSet):
	global result
	result=[]
	for each in resultSet:
		result.append(each.get_text())
	return result

#解析提取的html部分
def parse_page(html):
	#html解析
	soup = BeautifulSoup(html,"lxml")
	#提取微博文本
	text=soup.find_all(attrs={"node-type":"feed_list_content","class":"WB_text W_f14"})
	#提取转发部分
	forward=soup.find_all(attrs={"node-type":"forward_btn_text"})
	#提取评论部分
	comment=soup.find_all(attrs={"node-type":"comment_btn_text"})
	#提取日期
	date=soup.find_all(attrs={"node-type":"feed_list_item_date"})
	#提取来源平台
	source=soup.find_all(attrs={"action-type":"app_source"})
	#提取点赞数
	like=soup.select('li a[title="赞"]')
	#删除无关信息
	for each in date:
		if each.has_attr('suda-data')==False:
			date.remove(each)
	for each in source:
		if each.has_attr('suda-uatrack')==False:
			source.remove(each)
	for each in like:
		if each.has_attr('suda-uatrack')==False:
			like.remove(each)
	#构建数据字典
	wb_de=[]
	wb_al={}
	wb_al=wb_al.fromkeys(wb_de,[])
	wb_fr=DataFrame(wb_al,index=[])
	for i in range(len(text)):
		all_weibo={"text":text_list(text)[i],"date":text_list(date)[i],"source":text_list(source)[i],"forward":text_list(forward)[i],"comment":text_list(comment)[i],"like":text_list(like)[i]}
		wb_fr=wb_fr.append(all_weibo,ignore_index=True)
	    
	return wb_fr


