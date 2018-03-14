__config__ = {
    "manager_id": "manager-1"
}


def load_mod():
    from .mod import ShipaneWrapperMod
    return ShipaneWrapperMod()
