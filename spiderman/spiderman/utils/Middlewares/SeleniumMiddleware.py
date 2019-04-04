# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.chrome import options
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
from scrapy.http import HtmlResponse
from scrapy import Request
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.downloadermiddlewares.cookies import CookiesMiddleware
from scrapy.utils.project import get_project_settings
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import requests
from datetime import datetime
import time
import logging
import random
import re
from json import loads
from urllib.request import urlretrieve
import PIL.Image as image
import os
import csv
from scrapy import statscollectors
from queue import Queue

# 浏览器配置
BROWSER_OPTION = options()
BROWSER_OPTION.add_argument('--headless')     # !!!在linux上运行必须加载该配置项
BROWSER_OPTION.add_argument('--disable-gpu')
BROWSER_OPTION.add_argument('--no-sandbox')
BROWSER_OPTION.add_experimental_option("prefs",{"profile.default_content_setting_values":{'notifications':2}}) # 禁止弹窗和图片加载
BROWSER_OPTION.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/440.35 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/440.35 Edge/17.17134"')


class SeleniumMiddleware():
    def __init__(self):
        self.wait = WebDriverWait(self.browser, 20)
        self.timeout = get_project_settings().get("TIMEOUT",10)
        self.browser = webdriver.Chrome(service_args=service_args,chrome_options=BROWSER_OPTION)
        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)
        concurrent_num = get_project_settings().get("CONCURRENT_REQUESTS")
        self.concurrent_requests = min(concurrent_num,16)  # set browser tab num,set this param to increase concurrency
        while len(self.browser.window_handles) < self.concurrent_requests:
            self.browser.execute_script('''window.open("","_blank");''')
        self.handle_queue=Queue(maxsize=self.concurrent_requests)
        for handle in self.browser.window_handles:
            self.handle_queue.put(handle)
        dispatcher.connect(self.spider_closed,signals.spider_closed)

    def spider_closed(self,spider):
        #close chrome where spider close
        self.browser.quit()
    
    def process_request(self, request, spider):
        """
        this middleware just provide simply function.try to overriding it to implement the function you want.
        """
        # logging.info('crawl url:%s'%request.url)
        useSelenium = request.meta.get('useSelenium', False)
        user = request.meta.get('user',False)
        if useSelenium:
            try:
                result=self.requests.get(request.url,None)
                if result == None:
                    # get an idle tab to send request
                    if self.handle_queue.empty():
                        logging.warn('no idle tab left,please wait...')
                        return HtmlResponse(url=request.url,request=request, encoding='utf-8', status=202)
                    handle = self.handle_queue.get()
                    self.browser.switch_to.window(handle)
                    js = r"location.href='%s';" % request.url
                    self.browser.execute_script(js)
                    # mark url
                    self.requests[request.url]={'status':'waiting','handle':handle}
                    return HtmlResponse(url=request.url,request=request, encoding='utf-8', status=202)

                elif result['status']=='waiting':
                    # switch to the tab to check page status using javascript
                    handle = result['handle']
                    self.browser.switch_to.window(handle)
                    document_status=self.browser.execute_script("return document.readyState;")
                    if document_status=='complete':
                        self.requests.pop(request.url)  # finished,pop request from self.requests
                        self.handle_queue.put(handle)
                        logging.info("there are %s idle tab left"%self.handle_queue.qsize())
                        return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',status=200)
                    else:
                        return HtmlResponse(url=request.url, request=request, encoding='utf-8', status=202)

            except Exception as e:
                logging.error("error when processing %s in SeleniumMiddleware: %s"%(request.url,e))
                return HtmlResponse(url=request.url, request=request, encoding='utf-8', status=202)

    """**************************登录模块begin******************************"""

    def login(self,request,user_info):
        # pat = re.compile('免费注册', re.S)
        while 1:
            self.browser.delete_all_cookies()
            self.browser.get(request.url)
            userbotton = self.wait.until(
                    EC.presence_of_element_located((By.ID, "nameNormal")))
            userbotton.click()
            userbotton.send_keys(user_info[0])
            pwbotton = self.wait.until(EC.presence_of_element_located((By.ID, 'pwdNormal')))
            pwbotton.click()
            pwbotton.send_keys(user_info[1])
            self.slide()
            time.sleep(1)
            if request.meta.get('keep_cookies',False):
                self.browser.get('https://www.qichacha.com/search_index?key=%E4%B8%87%E5%B7%9E%E5%8C%BA#province:CQ&')
                self.browser.implicitly_wait(10)
                if '操作过于频繁' in self.browser.page_source:
                    return HtmlResponse(url=request.url, body='{},{}'.format(user_info[0],datetime.now().strftime('%Y%m%d')), request=request, encoding='utf-8',status=200)
                else:
                    cookie_jar = {}
                    for item in self.browser.get_cookies():
                        cookie_jar[item['name']]=item['value']
                    # 将cookies返回
                    return HtmlResponse(url=request.url, body=str({user_info[0]:cookie_jar}), request=request, encoding='utf-8',status=200)
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',status=200)
        

    def slide(self):
        """
        拖动滑块
        """
        # time.sleep(2)
        verify_code_img_path = VERIFY_CODE_IMG_PATH
        # 保存的图片名字
        bg_filename = 'bg.jpg'
        fullbg_filename = 'fullbg.jpg'

        # 获取图片
        bg_location_list, fullbg_location_list = self.get_images(verify_code_img_path+bg_filename, verify_code_img_path+fullbg_filename)

        # 根据位置对图片进行合并还原
        bg_img = self.get_merge_image(verify_code_img_path+bg_filename, bg_location_list)
        fullbg_img = self.get_merge_image(verify_code_img_path+fullbg_filename, fullbg_location_list)

        # 获取缺口位置
        gap = self.get_gap(fullbg_img, bg_img)
        # logging.info('缺口位置:%s'%gap)

        # 移动轨迹
        track = []
        # 往后挪动距离
        back_track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = gap * 4 / 5
        # 计算间隔
        t = random.randint(2,3)/10
        # 初速度
        v = 0

        while current < gap:
            if current < mid:
                # 加速度为正2
                a = 2
            else:
                # 加速度为负3
                a = -3
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))

        slider = self.browser.find_element_by_css_selector('#dom_id_one > div > div.gt_slider > div.gt_slider_knob.gt_show')
        ActionChains(self.browser).click_and_hold(slider).perform()
        time.sleep(0.8)
        for item in track:
            ActionChains(self.browser).move_by_offset(xoffset=item, yoffset=0).perform()

        imitate = ActionChains(self.browser).move_by_offset(xoffset=-1, yoffset=0)
        time.sleep(0.015)
        imitate.perform()
        time.sleep(random.randint(6, 10) / 10)
        imitate.perform()
        time.sleep(0.04)
        imitate.perform()
        time.sleep(0.012)
        imitate.perform()
        time.sleep(0.019)
        imitate.perform()
        time.sleep(0.033)
        ActionChains(self.browser).move_by_offset(xoffset=1, yoffset=0).perform()
        # 放开圆球
        ActionChains(self.browser).pause(random.randint(6, 14) / 10).release(slider).perform()

        time.sleep(1)
        loginbutton = self.browser.find_element_by_css_selector('#user_login_normal > button')
        loginbutton.click()

        time.sleep(2)

        loginned = re.findall("免费注册", self.browser.page_source)
        if len(loginned)==0:
            logging.info("已登录")
        else:
            return self.slide()

    def get_images(self, bg_filename = 'bg.jpg', fullbg_filename = 'fullbg.jpg'):
        """
        获取验证码图片
        :return: 图片的location信息
        """
        bg = []
        fullgb = []

        while bg == [] and fullgb == []:
            bf = BeautifulSoup(self.browser.page_source, 'html.parser')
            bg = bf.find_all('div', class_ = 'gt_cut_bg_slice')
            fullgb = bf.find_all('div', class_ = 'gt_cut_fullbg_slice')
            bg_url = re.findall('url\("(.+)"\);', bg[0]['style'])[0].replace('webp', 'jpg')
            # logging.info(bg_url)
            fullgb_url = re.findall('url\("(.+?)"\);', fullgb[0]['style'])[0].replace('webp', 'jpg')
            
        bg_location_list = []
        fullbg_location_list = []
        for each_bg in bg:
            location = {}
            location['x'] = int(re.findall('background-position: (.*)px (.*)px;',each_bg['style'])[0][0])
            location['y'] = int(re.findall('background-position: (.*)px (.*)px;',each_bg['style'])[0][1])
            bg_location_list.append(location)
        for each_fullgb in fullgb:
            location = {}
            location['x'] = int(re.findall('background-position: (.*)px (.*)px;',each_fullgb['style'])[0][0])
            location['y'] = int(re.findall('background-position: (.*)px (.*)px;',each_fullgb['style'])[0][1])
            fullbg_location_list.append(location)

        urlretrieve(url = bg_url, filename = bg_filename)
        # logging.info('缺口图片下载完成')
        urlretrieve(url = fullgb_url, filename = fullbg_filename)
        # logging.info('背景图片下载完成')
        return bg_location_list, fullbg_location_list

    def get_merge_image(self, filename, location_list):
        """
        根据位置对图片进行合并还原
        :filename:图片
        :location_list:图片位置
        """
        im = image.open(filename)
        new_im = image.new('RGB', (260,116))
        im_list_upper=[]
        im_list_down=[]

        for location in location_list:
            if location['y']==-58:
                im_list_upper.append(im.crop((abs(location['x']),58,abs(location['x'])+10,166)))
            if location['y']==0:
                im_list_down.append(im.crop((abs(location['x']),0,abs(location['x'])+10,58)))

        new_im = image.new('RGB', (260,116))

        x_offset = 0
        for im in im_list_upper:
            new_im.paste(im, (x_offset,0))
            x_offset += im.size[0]

        x_offset = 0
        for im in im_list_down:
            new_im.paste(im, (x_offset,58))
            x_offset += im.size[0]

        new_im.save(filename)

        return new_im

    def is_pixel_equal(self, img1, img2, x, y):
        """
        判断两个像素是否相同
        :param image1: 图片1
        :param image2: 图片2
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同
        """
        # 取两个图片的像素点
        pix1 = img1.load()[x, y]
        pix2 = img2.load()[x, y]
        threshold = 60
        if (abs(pix1[0] - pix2[0] < threshold) and abs(pix1[1] - pix2[1] < threshold) and abs(pix1[2] - pix2[2] < threshold)):
            return True
        else:
            return False

    def get_gap(self, img1, img2):
        """
        获取缺口偏移量
        :param img1: 不带缺口图片
        :param img2: 带缺口图片
        :return:
        """
        left = 43
        for i in range(left, img1.size[0]):
            for j in range(img1.size[1]):
                if not self.is_pixel_equal(img1, img2, i, j):
                    left = i
                    return left
        return left 


    """**************************登录模块end******************************"""

















