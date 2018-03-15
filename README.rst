************************************************
Shipane SDK wrapper for Rqalpha
************************************************

介绍
========
本mod基于实盘易的 官方SDK_ ，目的是使用不侵入策略代码的方式本地接入实盘易。信号发送使用了 推送模型_ 中的 同步仓位模式_。

.. _推送模型: https://github.com/sinall/ShiPanE-Python-SDK#id21
.. _同步仓位模式: https://github.com/sinall/ShiPanE-Python-SDK/blob/master/shipane_sdk/base_manager.py#L231
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

.. code-block:: python

    # /bin/env python
    # -*- coding: utf-8 -*-
    from collections import defaultdict

    from rqalpha import run_file
    from rqalpha.api import *


    def init(context):
        logger.info("init")
        context.symbol = [
            "000001.XSHE",
            "002415.XSHE",
            "600004.XSHG",
            "600006.XSHG",
        ]
        update_universe(context.symbol)
        if not hasattr(context, "fired"):
            context.fired = defaultdict(lambda: False)


    def before_trading(context):
        pass


    def handle_bar(context, bar_dict):
        # test order
        for symbol in context.symbol:
            if not context.fired:
                # order_percent并且传入1代表买入该股票并且使其占有投资组合的100%
                percent = 1.0 / len(context.symbol)
                logger.info("Buy %s" % symbol)
                order_target_percent(symbol, percent)
                p = context.portfolio.positions[symbol]
                logger.info("Position of %s,总: %s 今: %s 昨: %s " % (
                    symbol, p.quantity, p.quantity - p.sellable, p.sellable
                ))
                context.fired[symbol] = True
            else:
                percent = 0.9 / len(context.symbol)
                logger.info("Sell %s" % symbol)
                order_target_percent(symbol, percent)
                logger.info("Position of %s,总: %s 今: %s 昨: %s " % (
                    symbol, p.quantity, p.quantity - p.sellable, p.sellable
                ))
                context.fired[symbol] = False


    # 您可以指定您要传递的参数
    if __name__ == "__main__":
        import os

        config = {
            "base": {
                "start_date": "2016-06-01",
                "end_date": "2016-06-05",
                "accounts": {"stock": 100000},
                "frequency": "1m",
                "benchmark": None,
                "data_bundle_path": os.path.expanduser("~/.rqalpha/bundle"),
                "strategy_file": __file__,
                "run_type": "p"
            },
            "extra": {
                "log_level": "verbose",
            },
            "mod": {
                "fxdayu_source": {
                    "enabled": True,
                    "source": "quantos",
                    "enable_cache": False,
                },
                "shipane_wrapper": {
                    "enabled": True,
                    "manager_id": "manager-1"  # 此处和实盘易配置中的manager.id一致
                }
            }
        }

        run_file(__file__, config=config)

..

.. note::

    上述代码以实时交易的模式运行rqalpha，其中实时数据源使用了rqalpha-mod-fxdayu-source中提供的quantos(tushare-pro)数据源。
    所以需要关于quantos接口的一些配置，详见 rqalpha-mod-fxdayu-source配置_ ，建议通过环境变量来配置。

    环境变量配置示例：

    .. code-block:: shell

        QUANTOS_USER=13XXXXXXX60
        QUANTOS_TOKEN=eyJhXXXXXXXXXXXXXXUzI1NiJ9.eyJjcmVhdGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXMTM5NTUxMzM3NjAifQ.ZW_HgnsYl_XXXXXXXXXXXXXXXXXXXXH5r7Qo8lw

    quantos 账号只需要去其 官网_ 申请

.. _官网: https://www.quantos.org/
.. _rqalpha-mod-fxdayu-source配置: https://github.com/xingetouzi/rqalpha-mod-fxdayu-source#%E9%85%8D%E7%BD%AE%E9%80%89%E9%A1%B9

+ shipane_sdk_config.yaml

::

    # *********************************************************
    # 实盘易 SDK 配置
    # 如无特别说明，配置项修改后，将在策略重启后生效
    # 注意：
    # - 请勿在策略运行期间修改结构，比如 id 等关键信息
    # - 配置项冒号后需保留一个空格
    # - <xxx> 为必选项，[xxx] 为可选项；需要将括号移除
    # - <xxx|yyy> 为多选一项，使用其中一项即可
    # *********************************************************

    # *********************************************************
    # 代理配置
    # *********************************************************
    proxies:
        -   id: default
            base-url: http://www.iguuu.com/proxy/trade
            # 爱股网用户名
            username: <username>
            # 爱股网密码
            password: <password>

    # *********************************************************
    # 实盘易配置
    # *********************************************************
    gateways:
        # 实盘易-1 配置
        -   id: gateway-1
            # 连接方式
            # DIRECT：直连，适用于有公网 IP 的环境
            # PROXY： 通过爱股网代理连接
            connection-method: <DIRECT|PROXY>
            # IP 地址
            host: xxx.xxx.xxx.xxx
            # 端口
            port: 8888
            # 代理 ID
            # 连接方式为“代理”时需要设置
            proxy: default
            # 实例 ID，即运行实盘易的计算机名
            # 连接方式为“代理”时需要设置
            instance-id: <instance-id>
            # 密钥
            key: [key]
            # 超时
            timeout:
                # 连接超时
                connect: 5.0
                # 读取超时
                read: 10.0
            # 交易客户端
            clients:
                # 客户端-1
                # 注意：id 需全局唯一
                -   id: client-1
                    # 查询串，对应于 API 的 client 参数
                    # 其中 xxxx 为交易账号或交易账号后半段
                    query: account:xxxx
                    # 是否默认？
                    # 1 个实盘易只允许设置 1 个交易客户端为默认
                    default: true
                    # 其他资产价值
                    # 基金及其他非场内资产价值，该项配置用于校验账户
                    other-value: 0
                    # 总资产价值偏差率
                    # 该项配置用于校验账户
                    total-value-deviation-rate: 0.001
                    # 保留名单，每行一个
                    # 股票代码，注意使用 str 标签
                    # 例如：!!str 000001
                    # 注意：该配置在下次 handle_data 调用时生效
                    reserved-securities:
                        # 含有非数字的代码
                        - \D
                        # B股代码
                        - ^[92]
                        # 港股代码
                        - ^[\d]{5}$
                        # 逆回购代码
                        - ^(204|131)
                        # 新标准券代码
                        - !!str 888880
                # 客户端-2
                -   id: client-2
                    query: account:xxxx
                    other-value: 0
                    total-value-deviation-rate: 0.001
                    reserved-securities:
                        - \D
                        - ^[92]
                        - ^[\d]{5}$
                        - ^(204|131)
                        - !!str 888880
        # 实盘易-2 配置
        -   id: gateway-2
            # 连接方式
            connection-method: DIRECT
            host: xxx.xxx.xxx.xxx
            port: 8888
            key:
            timeout:
                connect: 5.0
                read: 10.0
            clients:
                -   id: client-3
                    query: title:monijiaoyi
                    default: true
                    other-value: 0
                    total-value-deviation-rate: 0.001
                    reserved-securities:
                        - \D
                        - ^[92]
                        - ^[\d]{5}$
                        - ^(204|131)
                        - !!str 888880
                -   id: client-4
                    query: title:xxx,account:xxx
                    other-value: 0
                    total-value-deviation-rate: 0.001
                    reserved-securities:
                        - \D
                        - ^[92]
                        - ^[\d]{5}$
                        - ^(204|131)
                        - !!str 888880

    # *********************************************************
    # 策略配置
    # 实体关系
    #
    # manager 1 ---- N trader 1 ---- 1 交易客户端(client)
    #
    # *********************************************************
    managers:
        # manager-1 配置
        -   id: manager-1
            traders:
                # trader-1
                -   id: trader-1
                    client: client-1
                    # 是否开启？
                    # 正式运行时设置为 true
                    enabled: true
                    # 是否排练？排练时不会下单。
                    # 正式运行时设置为 false
                    dry-run: true
                    # 工作模式
                    # 1. SYNC：  指按模拟交易的持仓进行同步
                    # 2. FOLLOW：指按模拟交易的下单进行跟单
                    # 目前米筐只支持 SYNC 模式
                    mode: SYNC
                    # 同步选项
                    # 如果该策略无需同步操作，可以省略 sync 配置项
                    # 注意：该配置在下次 handle_data 调用时生效
                    sync:
                        # 同步前是否撤销模拟盘未成交订单
                        # 如果该选项未启用，并且模拟盘有未成交订单，SDK 将不会做同步
                        pre-clear-for-sim: false
                        # 同步前是否撤销实盘未成交订单
                        pre-clear-for-live: false
                        # 最小订单金额，低于该值的订单将被忽略，以防因为价格波动导致的频繁调仓
                        # 取值可以为数值，或者百分比
                        min-order-value: 1%
                        # 最大订单金额，用于分单
                        # 取值为数值
                        max-order-value: 200000
                        # 轮次间隔时间，单位为毫秒
                        # 建议不小于 5 秒，以防交易软件持仓刷新过慢
                        round-interval: 5000
                        # 批次间隔时间，单位为毫秒
                        batch-interval: 1000
                        # 下单间隔时间，单位为毫秒
                        order-interval: 1000
                        # 默认为 2 轮，该选项用于增加额外轮次
                        # 额外轮次
                        extra-rounds: 0
        -   id: manager-2
            traders:
                -   id: trader-2
                    client: client-1
                    enabled: true
                    dry-run: true
                    mode: SYNC
                    sync:
                        pre-clear-for-sim: false
                        pre-clear-for-live: false
                        min-order-value: 1%
                        max-order-value: 200000
                        round-interval: 5000
                        batch-interval: 1000
                        order-interval: 1000
                        extra-rounds: 0

.. note::

    以上模板需要按自己的实盘易运行情况和交易需求来配置

+ 运行

将以上两个文件放置于同一目录下，做好相应配置，从该目录运行strategy.py

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