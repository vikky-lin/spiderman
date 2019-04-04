# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_warning_msg_to_mail(params):
    # 发送通知消息到邮箱
    server = smtplib.SMTP('smtp.163.com', 25)
    server.login('18814127719@163.com', '********')
    msg = MIMEText("爬虫被封警告！爬虫主机IP：" + params['host_ip'] + "，爬虫所属项目:" + params['spider_project'] +
                   "，爬虫名:" + params['spider_name'] + "，正在爬取地址:" + params['url'] + "，爬取使用代理IP:" +
                   params['proxy_ip'], 'plain', 'utf-8')
    msg['From'] = '18814127719@163.com <18814127719@163.com>'
    msg['Subject'] = Header(u'爬虫被封禁警告！', 'utf8').encode()
    msg['To'] = u'lyg <932985635@qq.com>'
    server.sendmail('18814127719@163.com', ['932985635@qq.com'], msg.as_string())


# params = {}
# params["host_ip"] = '1'
# params["spider_project"] = '1'
# params["spider_name"] = '1'
# params["url"] = '1'
# params["proxy_ip"] = '1'
# send_warning_msg_to_mail(params)
