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
