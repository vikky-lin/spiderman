# spiderman

# [spiderman](https://github.com/vikky-lynn/spiderman) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> scrapy project integrated with useful utils,focus on programing your spider logic.


## Introduction
[Echarts](https://github.com/ecomfe/echarts) is an open source library from Baidu for data visualization in javascript. It has awesome demo pages so I started to look out for an interface library so that I could use it in Python. I ended up with [echarts-python](https://github.com/yufeiminds/echarts-python) on github but it lacks of documentation and was not updated for a while. Just like many other Python projects, I started my own project, spiderman, referencing echarts-python and another library [pygal](https://github.com/Kozea/pygal).

## Installation
spiderman works on Python2 and Python3. For more information please refer to [changelog.md](https://github.com/chenjiandongx/spiderman/blob/master/changelog.md)


### spiderman
You can install it via pip
```
$ pip install spiderman -U
```

or clone it and install it
```
$ git clone --recursive https://github.com/chenjiandongx/spiderman.git
$ cd spiderman
$ pip install -r requirements.txt
$ python setup.py install
```

## Basic Usage
```python

```

It will create a file named render.html in the root directory, open file with your borwser.  

![usage-0](https://github.com/chenjiandongx/spiderman/blob/master/images/usage-0.gif)




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
