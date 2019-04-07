# spiderman

# [spiderman](https://github.com/vikky-lynn/spiderman) [![License: Apache2.0](https://img.shields.io/badge/License-Apache2.0-green.svg)](http://www.apache.org/licenses/LICENSE-2.0)

> scrapy project integrated with useful utils,focus on programing your spider logic.

##
![1](https://github.com/vikky-lin/spiderman/blob/master/screenshot/ScrapydWeb.png)  
![2](https://github.com/vikky-lin/spiderman/blob/master/screenshot/Spider%20Monitor.png)  

## Introduction
[spiderman]()

## How to Build scrpay monitor system?
1. **install scrapydweb**
    ```
    $ pip install scrapydweb
    ```
2. **remake on scrapydweb**
   - download [scrapydweb](https://github.com/vikky-lin/scrapydweb/archive/master.zip)(*I have made some change on scrapydweb,to support monitoring on grafana*)  
   - unzip **scrapydweb-master**
   - cd **scrapydweb-master**,copy **scrapydweb** file
   - replace the **scrapudweb** file that you have install by pip(*in the "site-packages" file of your own python environment*)

3. **start Mysql and create database <spiderdb>**
    - execute [spiderman/spider_monitor_database/spiderdb.sql](https://github.com/vikky-lin/spiderman/blob/master/spider_monitor_database/spiderdb.sql) in your mysql server.

4. **create your workspace**
    - choose any path you like,mkdir **SpiderMonitorCenter**
  
5. **start scrapyd server(*optional*)**  
    *if you already have a running scrapyd server,skip this step.*  
    - open command line window
    - cd **SpiderMonitorCenter** 
    - start scrapyd server by cmd <**scrapyd**>

6. **start scrapydweb**
    - open another command line window
    - cd **SpiderMonitorCenter** 
    - start scrapyd server by cmd <**scrapydWeb**>
    visit [doc](https://github.com/my8100/scrapydweb/blob/master/README_CN.md) to get help for scrpaydweb config)

7. **start grafana**
    - download [grafana](https://grafana.com/grafana/download),eg: *grafana-6.0.1*
    - unzip grafana to **SpiderMonitorCenter**
    - cd **bin** & click **grafana-server.exe**(*windows version*) to start grafana
    - visit [http://127.0.0.1:3000]() as default.
    - add mysql datasource  
    ![3](https://github.com/vikky-lin/spiderman/blob/master/screenshot/add%20datasource.png)
    - import **Spider Monitor Platform** dashboard,get json [here](https://github.com/vikky-lin/spiderman/blob/master/granafa%20spider%20dashboard/Spider%20Monitor%20Platform.json)

8. **visit scrapydweb**
    - visit [http://127.0.0.1:5000]() as default.

## spiderman basic usage
1. **get spiderman**
    ```
    $ git clone --recursive https://github.com/vikky-lin/spiderman.git
    $ cd spiderman
    $ pip install -r requirements.txt
    ```
2. **create your own spide**r  
   you can define your spider in <**spiders**>
   
3. **use spiderman utils**  
   I have developed some useful utils in spiderman:
   - DBPool utils
     - OraclePool
     - MysqlPool
     - RedisPool
   - Spider Monitor utils
     - enable **StatsMonitor** middleware in your spider to monitor your spider on grafana.
   - Middlewares
     - RandCookies
     - RandProxy
     - RandUserAgent
     - SeleniumMiddleware
   - VerifyCodeCrack
     - TODO
## TODO

## Author
spiderman is developed and maintained by vikky-lin ([1309550760@qq.com](1309550760@qq.com))

## License
spiderman is released under the License: Apache2.0. See LICENSE for more information.
