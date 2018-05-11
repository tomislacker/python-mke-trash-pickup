from __future__ import print_function
from nose2.tools import such

from mkerefuse.refuse import RefuseQueryAddress


with such.A('address setup') as it:
    with it.having('a proper address'):
        @it.has_setup
        def setup():
            it.address = RefuseQueryAddress(
                '1234',
                'N',
                'Main',
                'ST')

        @it.should('have a consistent hash')
        def test(case):
            test_hashes = [
                '1234567890abcdef',
                'abcdef1234567890',
            ]
            found_hashes = set([
                it.address.get_hash(hash_salt)
                for hash_salt in test_hashes
            ])
            case.assertEqual(
                len(found_hashes),
                len(test_hashes))

it.createTests(globals())
