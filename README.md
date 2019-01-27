# spiderXigua
通过网络爬虫爬取西瓜视频的视频
将xigua.py、crc32.js文件拷贝到运行目录
-d 将视频下载到本地的目录
-k  搜索西瓜视频的关键字
-p  下载搜索到从1~N 页的西瓜视频，每页有18个视频，当输入超过检索的最大值将不会下载

只下载duration >420s 的视频  

数据源 www.ixigua.com

监控网络请求的工具Fiddler，Chrome 浏览器

脚本只是为了熟悉Python语言，请勿将爬取视频作为商业盈利

Python 版本 -v 3.7 

运行报module 请自行下载依赖库 pip3.7 install modulename 

因为没加入线程，我的电脑配置比较低，下载可能停顿，那是CPU 100% 不是卡死 

跳过SSL验证 运行时会告警，可以忽略  

由于ixigua反爬虫，当ixigua 检测到同一个IP频繁请求时，会拒绝该IP请求，已做异常处理，不做中断

可自行加相关的机制避免，也可加入线程 降低CPU的使用率 


