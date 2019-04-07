# spiderman

# [spiderman](https://github.com/vikky-lynn/spiderman) [![License: Apache2.0](https://img.shields.io/badge/License-Apache2.0-green.svg)](http://www.apache.org/licenses/LICENSE-2.0)

> scrapy project integrated with useful utils,focus on programing your spider logic.

##
```
![servers](https://github.com/vikky-lin/spiderman/blob/master/spiderman/screenshot/ScrapydWeb.png)
![Monitor](https://github.com/vikky-lin/spiderman/blob/master/spiderman/screenshot/Spider%20Monitor.png)
```
## Introduction
[spiderman]()wait

## How to Build it?
1. **get spiderman**
    ```
    $ git clone --recursive https://github.com/vikky-lin/spiderman.git
    $ cd spiderman
    $ pip install -r requirements.txt
    ```
2. **remake on scrapydweb**
   - download [scrapydweb](https://github.com/vikky-lin/scrapydweb/archive/master.zip)(I have made some change on scrapydweb,to support monitoring on grafana)
   - unzip scrapydweb-master,cd scrapydweb-master,copy "scrapydweb" file
   - replace the "scrapudweb" file that you have install by pip(in the "site-packages" file of your own python environment)

3. **start Mysql and create database <spiderdb>**

    - execute spiderman/spider_monitor_database/spiderdb.sql in mysql.

4. **create your workspace**

    choose any path you like,mkdir <SpiderMan> 
  
5. **start scrapyd server(optional)**

    *if you already have a running scrapyd server,skip this step.*  
    otherwise,you can start a scrapyd server by cmd "scrapyd" 

6. **start scrapydweb**

    - cd SpiderMan
    - cd scrapydWeb(visit [doc](https://github.com/my8100/scrapydweb/blob/master/README_CN.md) to get help for scrpaydweb config)

7. **start grafana**
    - download [grafana]() to <SpiderMan> 
    - cd bin & click <grafana-server.exe> to start grafana

8. **visit scrapydweb**

    - visit http://127.0.0.1:5000(default)

## spiderman basic usage
    spiderman 



## Author
spiderman is developed and maintained by vikky-lynn ([1309550760@qq.com](1309550760@qq.com))

## License
spiderman is released under the MIT License. See LICENSE for more information.
