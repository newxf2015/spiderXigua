# -*-coding:utf-8 -*-
# Author: xiongfeng
# Date: 2019.1.27

import requests, json, re, sys, os, urllib, argparse, time
from urllib.request import urlretrieve
from urllib.parse import urlparse
from contextlib import closing
import base64
import binascii
import random
from bs4 import BeautifulSoup
from contextlib import closing
from urllib import parse
import js2py
import numpy as np
import xml2ass
#			GET /search_content/?format=json&autoload=true&count=20&keyword=%E8%87%AA%E5%8A%A8%E9%A9%BE%E9%A9%B6&cur_tab=1&offset=0 HTTP/1.1
#			Host: www.ixigua.com
#			Connection: keep-alive
searchUrl='https://www.ixigua.com/search_content/?format=json&autoload=true&count=20&keyword={}&cur_tab=1&offset={}'
videoUrl='https//ib.365yg.com/video/urls/v/1/toutiao/mp4/{}?r={}&s={}&callback=tt_playerxpzbd'
remoteUrl='//ib.365yg.com/video/urls/v/1/toutiao/mp4/'
jspath='C:\js\crc32.js'
"""
解码视频地址的request header
GET /video/urls/v/1/toutiao/mp4/732ab42ac42b4d1b800b7f5146b760ef?r=5666291838306883&s=692329934&callback=tt_playerxpzbd HTTP/1.1
    /video/urls/v/1/toutiao/mp4/d204aed731a04ec6a83193e2056bfc9a?r=8814994310051226&s=3301711353&callback=tt_playerxpzbd
Host: ib.365yg.com
Connection: keep-alive
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
Accept: */*
Referer: https://www.ixigua.com/a6409818269074588161/
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9

import base64
main_url = "aHR0cDovL3Y3LnBzdGF0cC5jb20vZmJiZmE2Yjc4ZjM4MThhM2M0OTVhMmRkYjAyOWY5NTAvNTc5\nMWMzODAvdmlkZW8vYy8zNDMwNzcxZjMyNmY0ZDUxOTRiNTYyMzdhNmEyMzFmYy8=\n"
base64.standard_b64decode(main_url)
"""
class Xigua:
	def __init__(self, dirname, keyword):
		self.dn_headers = {
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'en-US,en;q=0.9',
			'Referer': 'https://www.ixigua.com/'
		}
		self.search_headers = {
			'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
			'X-Requested-With': 'XMLHttpRequest',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
			'Content-Type': 'application/x-www-form-urlencoded',
			'Referer': 'https://www.ixigua.com/search/?keyword=%s' %parse.quote(keyword),
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'en-US,en;q=0.9',
			}			
		self.video_headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'en-US,en;q=0.9'
			}
		self.videojs_headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
			'Accept': '*/*',
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'en-US,en;q=0.9',
			}
		self.danmu_header = {
			'User-Agent': 'python-requests/2.21.0',
			'Accept-Encoding': 'gzip, deflate',
			'Accept': '*/*',
			}

		self.sess = requests.Session()

		self.dir = dirname

	def video_downloader(self, video_url, video_name):
		"""
		视频下载
			无
		"""
		size = 0
		with closing(self.sess.get(video_url, headers=self.dn_headers, stream=True, verify=False)) as response:
			chunk_size = 1024
			content_size = int(response.headers['content-length'])
			if response.status_code == 200:
				sys.stdout.write('  [文件大小]:%0.2f MB\n' % (content_size / chunk_size / 1024))
				video_name = os.path.join(self.dir, video_name)
				with open(video_name, 'wb') as file:
					for data in response.iter_content(chunk_size = chunk_size):
						file.write(data)
						size += len(data)
						file.flush()

						sys.stdout.write('  [下载进度]:%.2f%%' % float(size / content_size * 100) + '\r')
						# sys.stdout.flush()
						if size / content_size == 1:
							print('\n')
			else:
				print('链接异常')
	def get_download_url(self, arcurl,title):
		"""
		获取视频下载地址
		Parameters:
			arcurl: 视频播放地址
			oid：弹幕地址参数
		Returns:
			download_url：视频下载地址
		"""
		req = self.sess.get(url=arcurl, headers=self.video_headers, verify=False)
		#pattern = '.__playInfo__=(.*)</script><script>var imgUrl = '
		#soup = BeautifulSoup(req.text, "html.parser")

		#pt = re.compile(r"var BASE_DATA = '(.*?)';$", re.MULTILINE | re.DOTALL)

		#script = soup.find("script", text=pt)
		#print (pt.search(script.text))
		#print(re.findall(pattern,req.text))
		#print("script:%s" %pt.search(script))
		soup = BeautifulSoup(req.text,"html.parser")
		#pattern = re.compile(r"var BASE_DATA = (.*?);$", re.MULTILINE | re.DOTALL)
		pattern = re.compile(r"videoId: '(.*?)'$", re.MULTILINE | re.DOTALL)
		script = soup.find("script", text=pattern)
		#print (pattern.search(script.text).group(1))
		try:
			#获取video id
			info = pattern.search(script.text).group(1)	
			#url=soup.find_all('source',{'class'}
			#r = str(random.random())[2:]
			
			url = remoteUrl+info
			data=open('crc32.js','r',encoding= 'utf8').read()
			#print('%s-----------------------%s' %(info,data))
			data=js2py.eval_js(data)
			#获取video的地址
			vdjsurl=data(info)
                        #print('%s-----------------------' %vdjsurl)
			vreq = self.sess.get(url= vdjsurl,headers=self.videojs_headers, verify=False)
			vdjson = json.loads(vreq.text)
			vdata=vdjson['data']
			video_list= vdata['video_list']
			main_url=video_list['video_1']['main_url']
			videourl=base64.standard_b64decode(main_url)
			#print("main_url:===============%s============="  %main_url)
                        #b'http://v11-tt.ixigua.com/6e575c28897a37da3fab19b2fd090e07/5c45e4fb/video/m/220da00211d334b484891d0abd0a80d824711614d3b100002fb724aa253d/?rc=anE3cTxuaHk6azMzaTczM0ApQHRAbzM4NTk8MzQzMzc0NTUzNDVvQGgzdSlAZjN1KWRzcmd5a3VyZ3lybHh3ZjUzQGRhaWQ1bnNwL18tLWMtL3NzLW8jbyMtLjQuMjYtLjI0Ly4uNi06I28jOmEtcSM6YHZpXGJmK2BeYmYrXnFsOiMuL14%3D'
			#print("%s" %videourl)
			eq=self.sess.get(videourl,headers=self.danmu_header,verify=False,stream=True)
			filename=self.dir + '/' + title +info + '.mp4'
			videosize=video_list['video_1']['size']
			size = 0
			with open(filename,'wb') as f:
				for chunk in eq.iter_content(chunk_size=2048):
					f.write(chunk)
					size+=len(chunk)
					f.flush()
					sys.stdout.write('  [下载进度]:%.2f%%' % float(size / videosize * 100) + '\r')
					if size / videosize == 1:
						print('\n')
			#print('----------------------%s'%data(info))		
			#print('url----------%s----------:%s' %(url,r))
			#n = url + '?r=' + r
			#c=binascii.crc32(url)
			#print('--------end check---------%s-----' %c)
			#c = binascii.crc32(r)
			#print('--------end check--------------')
			#s = sel.right_shift(c	, 0)
			#print('s param=-----------------%s ' %s)
			#reqv = self.sess.get(videoUrl.format(info,c,s))
			#vjson= json.loads(reqv.text)
                        #if ('data' in vjson.keys()):
			#data=vjson['data']
                        #if('video_list' in data.keys()):
			#video_list= data['video_list']
			#main_url=video_list['video_1']['main_url']
			#print('main_url=-------------%s' %main_url)
			#print("info====%s" %info)
			#videoId: '732ab42ac42b4d1b800b7f5146b760ef'
                        #获取tt_video.js JS 脚本
			#tt_js=soup.find_all('script',{'src':re.compile('.*?tt-video\.js')})
			#获取有效js地址
			#print('tt_js=------------%s' %tt_js[0])
			#ttjs=tt_js[0]['src']
			#print('ttjs=------------%s' %ttjs)
			#ttjsurl='https:' + parse.quote(ttjs)
			#https://s3.pstatp.com/toutiao/video_player/dist/tt-video.js
			#print("js url-------------------= %s" %ttjsurl)
			#remoteURL:"//ib.365yg.com/video/urls/v/1/toutiao/mp4/
			#jsreq=self.sess.get(url=ttjsurl)
			#rem=re.compile(r'remoteURL: "(.*?),"$', re.MULTILINE | re.DOTALL)
			#print("remoteURL=====================:%s" %rem.search(jsreq.text))
		except:
			return '',''
	def search_video(self,search_url):
                req = self.sess.get(url=search_url, headers=self.search_headers, verify=False)
                html = json.loads(req.text)
                titles = []
                urls = []
                videosizes = []
                for each in html['data']:
                        if ('title' in each.keys() and 'display_url' in each.keys() and  'video_duration' in each.keys()):
                                titles.append(each['title'])
                                videosizes.append(each['video_duration'])
                                urls.append(each['display_url'])
                return titles,urls,videosizes
	def search_videos(self, keyword, pages):
                """
                搜索视频
                Parameters:
                        keyword: 搜索关键字
                        pages：下载页数
                Returns:无
                """
                if self.dir not in os.listdir():
                        os.mkdir(self.dir)
                lensize=0
                try:
                        for page in range(1, pages+1):
                                search_url = searchUrl.format(keyword, lensize)
                                print("%s" %search_url)
                                titles, urls, videosizes= self.search_video(search_url)
                                lensize=lensize + len(urls) + 1
                                print('第[ %d ]页:视频数%d 视频列表:' %(page,len(urls)))
                                #for index, url,videosize in enumerate(urls):
                                if len(urls) == 0:
                                        print("---------无效数据，下载结束--------------")
                                        return
                                for i in range(len(urls)):
                                        title = titles[i]
                                        url = urls[i]
                                        size = videosizes[i]
                                        print('视频标题:%s 视频大小:%s 视频地址:%s' %(title,size,url))
                                        #解析视频的下载地址
                                        if size < 420:
                                                self.get_download_url(url,title)
                                                time.sleep(0.1)
                                titles.clear()
                                urls.clear()
                                videosizes.clear()
                except:
                        return
if __name__ == '__main__':
	if len(sys.argv) == 1:
		sys.argv.append('--help')
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--dir', required=True, help=_('download path'))
	parser.add_argument('-k', '--keyword', required=True, help=_('search content'))
	parser.add_argument('-p', '--pages', required=True, help=_('the number of pages for downloading'), type=int, default=1)
	
	args = parser.parse_args()
	Xg = Xigua(args.dir,args.keyword)
	Xg.search_videos(args.keyword, args.pages)

	print('全部下载完成!')
