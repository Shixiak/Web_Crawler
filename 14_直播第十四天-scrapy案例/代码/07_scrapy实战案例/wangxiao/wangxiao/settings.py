# Scrapy settings for wangxiao project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'wangxiao'

SPIDER_MODULES = ['wangxiao.spiders']
NEWSPIDER_MODULE = 'wangxiao.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'wangxiao (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

LOG_LEVEL = "WARNING"

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
   "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
   "Cookie": "mantis6894=b98afe03b01f439db1ccd02e6be26977@6894; NTKF_T2D_CLIENTID=guest87D35F7B-BCE1-3344-1A6C-B7349F7A37E5; safedog-flow-item=D14BF2F079849EE671DED19D45D20F7E; pc_783235612_exam=fangchan; pc_778682568_exam=fangchan; sign=jz1; Hm_lvt_fd91d2ffbfa83c234c1cee672a69326c=1628999411,1629341158; agentmembers=notSet; autoLogin=null; userInfo=%7B%22userName%22%3A%22pc_783235612%22%2C%22token%22%3A%22e366f2f4-bf5d-4d32-9890-efbcde543ac2%22%2C%22headImg%22%3Anull%2C%22nickName%22%3A%22186****5987%22%2C%22sign%22%3A%22fangchan%22%2C%22isBindingMobile%22%3A%221%22%2C%22isSubPa%22%3A%220%22%2C%22userNameCookies%22%3A%22x0WDyiWtCnEUVEjvM6TyDA%3D%3D%22%2C%22passwordCookies%22%3A%22NuP%2Bk21mg%2Ftu3w1FHGZ6Vg%3D%3D%22%7D; token=e366f2f4-bf5d-4d32-9890-efbcde543ac2; UserCookieName=pc_783235612; OldUsername2=x0WDyiWtCnEUVEjvM6TyDA%3D%3D; OldUsername=x0WDyiWtCnEUVEjvM6TyDA%3D%3D; OldPassword=NuP%2Bk21mg%2Ftu3w1FHGZ6Vg%3D%3D; UserCookieName_=pc_783235612; OldUsername2_=x0WDyiWtCnEUVEjvM6TyDA%3D%3D; OldUsername_=x0WDyiWtCnEUVEjvM6TyDA%3D%3D; OldPassword_=NuP%2Bk21mg%2Ftu3w1FHGZ6Vg%3D%3D; nTalk_CACHE_DATA={uid:kf_9009_ISME9754_guest87D35F7B-BCE1-33,tid:1629377625474718}; Hm_lpvt_fd91d2ffbfa83c234c1cee672a69326c=1629378003"
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'wangxiao.middlewares.WangxiaoSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'wangxiao.middlewares.WangxiaoDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'wangxiao.pipelines.WangxiaoPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
