"""
Creates necessary default paths for ipc sockets.
"""

import os

def ifnotexists_mkdirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

ifnotexists_mkdirs('/tmp/feeds/sin/recv')
ifnotexists_mkdirs('/tmp/feeds/sin/prst')
ifnotexists_mkdirs('/tmp/feeds/sin/send')


