import codecs

from rqalpha.core.strategy_loader import UserFuncStrategyLoader
from rqalpha.interface import AbstractStrategyLoader
from rqalpha.utils.strategy_loader_help import compile_strategy
from pathlib import Path

from rqalpha_mod_shipane_wrapper.api import get_file

CODE_DIR = Path(__file__).absolute().parent / "code"


def read_file(path):
    with codecs.open(path, encoding="utf-8") as f:
        return f.read()


def get_codes():
    paths = {}
    codes = {}
    for key in ["wrapper", "empty_before_trading", "empty_init", "empty_handle_bar"]:
        paths[key] = str(CODE_DIR / (key + ".py"))
        codes[key] = read_file(paths[key])
    return paths, codes


class ShipaneWrappedStrategyLoader(AbstractStrategyLoader):
    def __init__(self, origin):

        self._origin = origin
        self._manager_id = None

    def set_manager_id(self, manager_id):
        self._manager_id = manager_id

    def get_manager_id(self):
        return self._manager_id

    def load(self, scope):
        if not self._manager_id:
            raise RuntimeError("You should set manage id first")
        scope = self._origin.load(scope)
        if isinstance(self._origin, UserFuncStrategyLoader):
            scope["get_file"] = get_file
        paths, codes = get_codes()
        for key in ["init", "handle_bar", "before_trading"]:
            if key not in scope:
                key = "empty_" + key
                scope = compile_strategy(codes[key], paths[key], scope)
        scope = compile_strategy(codes["wrapper"], paths["wrapper"], scope)
        return scope
