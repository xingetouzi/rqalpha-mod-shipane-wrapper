# -*- coding: utf-8 -*-
import itertools
from datetime import timedelta

from rqalpha import run_file
from rqalpha.api import *
from rqalpha.utils.datetime_func import convert_dt_to_int
import pandas as pd


def init(context):
    logger.info("init")
    context.s1 = "000001.XSHE"
    update_universe(context.s1)
    context.fired = False


def before_trading(context):
    pass


def handle_bar(context, bar_dict):
    logger.info(bar_dict[context.s1])
    bar = bar_dict[context.s1]
    now_int = convert_dt_to_int(context.now)
    bar_int = convert_dt_to_int(bar.datetime)
    try:
        assert - timedelta(minutes=1) < bar.datetime - context.now < timedelta(minutes=1)
    except AssertionError as e:
        print(now_int)
        print(bar)
        raise e
    frequencies = ["1m", "5m", "15m"]
    lengths = [10, 100]
    for l, f in itertools.product(lengths, frequencies):
        df1 = pd.DataFrame(history_bars(context.s1, l, f))
        df2 = pd.DataFrame(history_bars(context.s1, l, f, include_now=True))
        try:
            assert df2["datetime"].iloc[-1] == bar_int
            assert df1["datetime"].iloc[-1] == df2["datetime"].iloc[-1] or \
                   df1["datetime"].iloc[-1] == df2["datetime"].iloc[-2]
        except AssertionError as e:
            print(now_int)
            print(bar_int)
            print(df1)
            print(df2)
            raise e

    # test order
    if not context.fired:
        # order_percent并且传入1代表买入该股票并且使其占有投资组合的100%
        logger.info("Buy")
        order_target_percent(context.s1, 1)
        context.fired = True
    else:
        logger.info("Sell")
        order_target_percent(context.s1, 0.95)
        context.fired = False


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
                "enabled": True
            }
        }
    }
    run_file(__file__, config=config)
