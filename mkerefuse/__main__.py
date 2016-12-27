#!/usr/bin/env python3
"""

Looks up addresses to discover future garbage and/or recycle pickup dates
within the city of Milwaukee, WI

Usage:
    mkerefuse --help
    mkerefuse [options]

Options:
    -a, --address STRING        House number
    -d, --direction STRING      Address direction (N, S, E, W)
    -s, --street STRING         Street Name (ex: '27th')
    -t, --street-type STRING    Street Type
    -T, --types                 List all Street Types

    --html FILE                 Save the form output HTML for debug
"""
import logging
import sys
from docopt import docopt
from mkerefuse import __version__
from mkerefuse.util import LogProducer
from mkerefuse.util import setup_logging
setup_logging()

# Define a logger
log = logging.getLogger('mke-refuse')

# Parse arguments
log.debug("Parsing arguments")
args = docopt(__doc__, version=__version__)

# Load the library
from mkerefuse.refuse import RefuseQuery
from mkerefuse.refuse import RefuseQueryAddress

# If the street type listing was asked for, display that and exit
if args['--types']:
    log.debug("Listing Street Type values")
    print("- " + "\n- ".join(RefuseQueryAddress.STREET_TYPES))
    sys.exit(0)

# Define the address
log.debug("Composing query address")
address = RefuseQueryAddress(
    house_number=args['--address'],
    direction=args['--direction'],
    street_name=args['--street'],
    street_type=args['--street-type'])

# Execute the query
log.info("Executing query...")
pickup = RefuseQuery.Execute(address,
                             html_output=args['--html'])
log.info("Query returned")

# Show the results
print(repr(pickup))
