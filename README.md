# spiderman

# [spiderman](https://github.com/vikky-lynn/spiderman) [![License: Apache2.0](https://img.shields.io/badge/License-Apache2.0-green.svg)](http://www.apache.org/licenses/LICENSE-2.0)

> scrapy project integrated with useful utils,focus on programing your spider logic.


## Introduction
[spiderman]()wait

## Installation
spiderman works on Python3. 


### spiderman
You can install it via pip
```
$ pip install pyspiderman -U
```

or clone it and install it
```
$ git clone --recursive https://github.com/vikky-lin/spiderman.git
$ cd spiderman
$ pip install -r requirements.txt
```
* remake on scrapydweb
  1. download [scrapydweb](https://github.com/vikky-lin/scrapydweb/archive/master.zip)(I have made some change on scrapydweb,to support monitoring on grafana)
  2. unzip scrapydweb-master,cd scrapydweb-master,copy "scrapydweb" file
  3. replace the "scrapudweb" file that you have install by pip(in the "site-packages" file of your own python environment)
* start Mysql and create database <spiderdb>
  execute spiderman/spider_monitor_database/spiderdb.sql in mysql.
* create your workspace
  choose any path you like,mkdir <SpiderMan> 
* start scrapyd server(optional)
  if you already have a running scrapyd server,skip this step.
  otherwise,you can start a scrapyd server by cmd "scrapyd"
* start scrapydweb
  1. cd SpiderMan
  2. $ cd scrapydWeb(visit [doc](https://github.com/my8100/scrapydweb/blob/master/README_CN.md) to get help for scrpaydweb config)
* start grafana
  1. download [grafana]() to <SpiderMan> 
  2. $ cd bin & click <grafana-server.exe> to start grafana
* visit scrapydweb
  visit http://127.0.0.1:5000(default)

## Basic Usage
  spiderman 
## Documentation
* [中文文档]()
* [English]()


## Test
```shell
$ cd test
$ nosetests --with-coverage --cover-package spiderman --cover-package test
```

## Author
spiderman is developed and maintained by vikky-lynn ([1309550760@qq.com](1309550760@qq.com))

## License
spiderman is released under the MIT License. See LICENSE for more information.
