import json
import logging
import re
import requests
from .util import LogProducer


class RefusePickup(LogProducer):
    """Parses a refuse pickup response"""

    input_properties = {
        'route_garbage': r'garbage pickup route for this location is <strong>(?P<value>[^<]+)</strong>',
        'next_pickup_garbage': r'The next garbage collection pickup for this location is: <strong>(?P<value>[^<]+)</strong>',
        'route_recycle': r'recycling pickup route for this location is <strong>(?P<value>[^<]+)</strong>',
        'next_pickup_recycle': r'The next recycling collection pickup for this location is:\s*<strong>(?P<value>[^<]+)</strong>',
        'next_pickup_recycle_after': r'The next estimated pickup time is between <strong>(?P<value>[^<]+)</strong> and <strong>(?P<before>[^<]+)</strong>',
        'next_pickup_recycle_before': r'The next estimated pickup time is between <strong>(?P<after>[^<]+)</strong> and <strong>(?P<value>[^<]+)</strong>',
    }
    """Maps the key to an attr name & value to a regex search"""

    pickup_time = '0700'
    """Define what time the refuse must be outside by to make pickup time"""

    @classmethod
    def from_html(cls, html_contents):
        log = logging.getLogger(cls.__name__)

        log.debug("Parsing {} bytes of HTML".format(len(html_contents)))

        inst = cls()
        for attr_name, regex in cls.input_properties.items():
            log.debug("Searching for '{n}' with '{p}'".format(
                n=attr_name,
                p=regex
            ))
            pattern = re.compile(regex)
            match = pattern.search(html_contents)

            try:
                setattr(inst, attr_name, match.group('value'))
            except AttributeError:
                # No value was found, by default set an empty string
                setattr(inst, attr_name, '')

        return inst

    def to_dict(self):
        """
        Returns pickup information in a JSON blob

        :return: JSON blob of pickup data
        :rtype: dict
        """
        response_dict = {}
        for key, value in self.input_properties.items():
            response_dict.update({
                key: getattr(self, key),
            })
        return response_dict

    def __repr__(self):
        return json.dumps(
            self.to_dict(),
            indent=4,
            separators=(',', ': '))


class RefuseQueryAddress(object):
    """Defines an address to query for refuse pickup scheduling"""

    STREET_TYPES = [
        'AV',  # Avenue
        'BL',  # Boulevard
        'CR',  # Circle
        'CT',  # Court
        'DR',  # Drive
        'LA',  # Lane
        'PK',  # Parkway
        'PL',  # Place
        'RD',  # Road
        'SQ',  # Square
        'ST',  # Street
        'TR',  # Terrace
        'WY',  # Way
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
    def Execute(cls, refuse_address, html_output=None):
        """Queries the form URL & processes the response

        :param refuse_address: Address to lookup
        :type refuse_address: RefuseQueryAddress
        :param html_output: Path to file for debugging HTML output
        :type html_output: None|str
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

        if html_output is not None:
            with open(html_output, 'w') as ofile:
                ofile.write(response.text)

        response_method = getattr(cls.parse_xpath, 'from_html')
        return response_method(response.text)
