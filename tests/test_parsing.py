from __future__ import print_function
from nose2.tools import such

from mkerefuse.refuse import RefusePickup


def setup_parser(html_path):
    """
    Reads test HTML & instantiates a new `RefusePickup`

    :param html_path: Path to HTML file with a test response
    :type html_path: str
    :return: RefusePickup instance
    :rtype: mkerefuse.RefusePickup
    """
    with open(html_path, 'r') as infile:
        return RefusePickup.from_html(infile.read())


with such.A('successfully fetched response') as it:
    with it.having('garbage day, in Winter'):
        @it.has_setup
        def setup():
            it.parser = setup_parser('tests/data/garbageday.html')

        @it.should('have the correct garbage route')
        def test(case):
            case.assertEqual(
                it.parser.route_garbage,
                'NA1-2A')

        @it.should('have the correct recycle route')
        def test(case):
            case.assertEqual(
                it.parser.route_recycle,
                'NR1-2-3')

        @it.should('have the correct next garbage pickup')
        def test(case):
            case.assertEqual(
                it.parser.next_pickup_garbage,
                'TUESDAY DECEMBER 27, 2016')

        @it.should('have the correct next recycle pickup range')
        def test(case):
            case.assertEqual(
                it.parser.next_pickup_recycle_after,
                'TUESDAY JANUARY 3, 2017')
            case.assertEqual(
                it.parser.next_pickup_recycle_before,
                'WEDNESDAY JANUARY 4, 2017')

    with it.having('non-garbage day, unknown recycling, in Winter'):
        @it.has_setup
        def setup():
            it.parser = setup_parser(
                'tests/data/nongarbageday-recycle_unknown.html')

        @it.should('have the correct garbage route')
        def test(case):
            case.assertEqual(
                it.parser.route_garbage,
                'SP1-3A')

        @it.should('have the correct recycle route')
        def test(case):
            case.assertEqual(
                it.parser.route_recycle,
                '')

        @it.should('have the correct next garbage pickup')
        def test(case):
            case.assertEqual(
                it.parser.next_pickup_garbage,
                'THURSDAY DECEMBER 29, 2016')

        @it.should('have the correct next recycle pickup range')
        def test(case):
            case.assertEqual(
                it.parser.next_pickup_recycle_after,
                '')
            case.assertEqual(
                it.parser.next_pickup_recycle_before,
                '')

            # Recycle single day (for Summer) should be empty
            case.assertEqual(
                it.parser.next_pickup_recycle,
                '')

    with it.having('non-garbage day, in Summer'):
        @it.has_setup
        def setup():
            it.parser = setup_parser('tests/data/nongarbageday-recycle_summer.html')

        @it.should('have the correct garbage route')
        def test(case):
            case.assertEqual(
                it.parser.route_garbage,
                'SP1-3A')

        @it.should('have the correct recycle route')
        def test(case):
            case.assertEqual(
                it.parser.route_recycle,
                'SP8-2-04')

        @it.should('have the correct next garbage pickup')
        def test(case):
            case.assertEqual(
                it.parser.next_pickup_garbage,
                'FRIDAY APRIL 14, 2017')

        @it.should('have the correct next recycle pickup')
        def test(case):
            case.assertEqual(
                it.parser.next_pickup_recycle,
                'WEDNESDAY APRIL 12, 2017')

            # Recycle ranges (for Winter) should be empty
            case.assertEqual(
                it.parser.next_pickup_recycle_after,
                '')
            case.assertEqual(
                it.parser.next_pickup_recycle_before,
                '')

it.createTests(globals())
