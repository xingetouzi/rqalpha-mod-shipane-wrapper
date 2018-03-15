************************************************
Shipane SDK wrapper for Rqalpha
************************************************

介绍
========
本mod主要基于实盘易的 官方SDK_ 中的，目的是使用不侵入策略代码的方式本地接入实盘易。信号发送使用了推送模型中的同步仓位模式。

.. _官方SDK: https://github.com/sinall/ShiPanE-Python-SDK

特点
=======
+ 不需要修改策略代码，而是通过修改运行rqalpha的config来接入实盘易。
+ 实盘易通过自身的配置文件（默认脚本工作目录下的shipane_sdk_config.yaml)来配置

依赖
=======
+ 使用本mod需要先安装实盘易官方SDK,安装方法请见 这里_

.. _这里: https://github.com/sinall/ShiPanE-Python-SDK#%E5%AE%89%E8%A3%85

+ 本地跑实盘交易需要接入实时数据源，推荐配合该mod一起使用 rqalpha-mod-fxdayu-source_

.. _rqalpha-mod-fxdayu-source: https://github.com/xingetouzi/rqalpha-mod-fxdayu-source

安装
======
1. 安装shipane-sdk

2. 安装本mod

.. code-block:: bash

    $ pip install git+https://github.com/xingetouzi/rqalpha-mod-shipane-wrapper.git
    $ rqalpha mod install shipane-wrapper

用例
======
+ 策略代码strategy.py

.. literalinclude:: ../../example/strategy.py
    :language: python

+ shipane_sdk_config.yaml

.. literalinclude:: ../../example/shipane_sdk_config_template.yaml
    :language: yaml

+ 运行

将以上两个文件放置于同一目录下，从该目录运行strategy.py

.. code-block:: bash

    $ python strategy.py


配置选项
========
============================= ==============================  =================================
选项                           默认值                           含义
============================= ==============================  =================================
shipane_wrapper.enabled       False                           是否开启mod
shipane_wrapper.manager_id    "manager-1"                     和shipane_sdk_config.yaml中保持一致
============================= ==============================  =================================


加入开发
=========
github地址_

.. _github地址: https://github.com/xingetouzi/rqalpha-mod-shipane-wrapper

欢迎提交各种Issue和Pull Request。