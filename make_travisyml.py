from __future__ import print_function
from tox.config import parseconfig

print("language: python")
print("python: 2.7")
print("env:")
for env in parseconfig(None, 'tox').envlist:
    print(" - TOX_ENV={}".format(env))

print("install:")
print(" - pip install tox")
print("script:")
print(" - tox -e $TOX_ENV")
