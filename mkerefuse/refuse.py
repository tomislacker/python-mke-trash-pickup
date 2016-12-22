import requests
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

    pickup_time = '0700'
    """Define what time the refuse must be outside by to make pickup time"""


class RefuseQueryAddress(object):
    """Defines an address to query for refuse pickup scheduling"""

    STREET_TYPES = [
        'AV', # Avenue
        'BL', # Boulevard
        'CR', # Circle
        'CT', # Court
        'DR', # Drive
        'LA', # Lane
        'PK', # Parkway
        'PL', # Place
        'RD', # Road
        'SQ', # Square
        'ST', # Street
        'TR', # Terrace
        'WY', # Way
    ]
    """Static list of address suffixes"""

    class AddressDirection(object):
        N = 'N'
        S = 'S'
        E = 'E'
        W = 'W'

        @classmethod
        def FromString(cls, direction):
            cls.IsValid(direction)
            return getattr(
                cls,
                direction[:1].upper())

        @classmethod
        def IsValid(cls, direction):
            assert hasattr(cls, direction[:1].upper())

    def __init__(self, house_number, direction, street_name, street_type):
        """Instantiates a new address

        :param house_number: Address number
        :type house_number: str
        :param direction: Address direction
        :type AddressDirection:
        """
        self.house_number = house_number
        self.direction = self.AddressDirection.FromString(direction)
        self._street_name = street_name
        self._street_type = street_type

        assert self.street_type in self.STREET_TYPES, \
            "Invalid street type: {st}".format(
                st=self.street_type)

    @property
    def street_name(self):
        return self._street_name.upper()

    @property
    def street_type(self):
        return self._street_type.upper()


class RefuseQuery(object):
    """Queries for garbage/recycle pickups based on an address"""

    form_url = 'http://mpw.milwaukee.gov/services/garbage_day'
    """URL to POST form data to"""

    parse_xpath = RefusePickup
    """Class to parse XHTML response with"""

    @classmethod
    def Execute(cls, refuse_address):
        """Queries the form URL & processes the response

        :param refuse_address: Address to lookup
        :type refuse_address: RefuseQueryAddress
        :return: Parsed response
        :rtype: mkerefuse.refuse.RefusePickup
        """
        response = requests.post(
            cls.form_url,
            data={
                'laddr': refuse_address.house_number,
                'sdir': refuse_address.direction,
                'sname': refuse_address.street_name,
                'stype': refuse_address.street_type,
                'Submit': 'Submit',
            })
        response_method = getattr(cls.parse_xpath, 'FromHTML')
        return response_method(response.text)
