import builtins

from rqalpha.api.helper import get_apis
from rqalpha.events import EVENT
from rqalpha.interface import AbstractMod
from rqalpha.utils.logger import system_log
from rqalpha.api.api_base import export_as_api
from .strategy_loader import ShipaneWrappedStrategyLoader
from . import api


class ShipaneWrapperMod(AbstractMod):
    def __int__(self):
        pass

    def start_up(self, env, mod_config):
        origin = env.strategy_loader
        strategy_loader = ShipaneWrappedStrategyLoader(origin)
        strategy_loader.set_manager_id(mod_config.manager_id)
        env.set_strategy_loader(strategy_loader)
        env.event_bus.add_listener(EVENT.POST_SYSTEM_INIT, self.on_post_system_init)
        for export_name in api.__all__:
            export_as_api(getattr(api, export_name))
        system_log.info("策略实盘易对接完成，策略manager_id为[%s]" % strategy_loader.get_manager_id())

    def on_post_system_init(self, event):
        apis = get_apis()
        for k, v in apis.items():
            setattr(builtins, k, v)
