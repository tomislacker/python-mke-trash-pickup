from .util import XPathObject


class RefusePickup(XPathObject):
    """Defines attribute to XPath specification matching"""

    input_properties = {
        'success_msg': '//*[@id="nConf"]/h1',
        'route_garbage': '//*[@id="nConf"]/strong[1]',
        'next_pickup_garbage': '//*[@id="nConf"]/strong[2]',
        'route_recyle': '//*[@id="nConf"]/strong[3]',
        'next_pickup_recycle_after': '//*[@id="nConf"]/strong[4]',
        'next_pickup_recycle_before': '//*[@id="nConf"]/strong[5]',
    }
    """Maps the key to an attr name & value to an XPath lookup"""
