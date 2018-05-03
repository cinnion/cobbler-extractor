#!/usr/bin/env python3
'''
Created on Apr 29, 2018

@author: cinnion
'''

from xmlrpc.client import Server
from pprint import pprint as pp
import os


class Cobbler(Server):
    '''
    This is the module for talking to the cobbler server
    '''

    def __init__(self, protocol='http', host='cobbler', api='cobbler_api', **kwargs):
        '''
        Constructor
        '''
        if protocol not in ('http', 'https'):
            raise OSError("unsupported cobbler xmlrpc protocol")

        self.protocol = protocol
        self.host = host
        self.api = api
        url = self.protocol + '://' + self.host + '/' + self.api

        self.server = super().__init__(url, allow_none=True)


if __name__ == "__main__":
    x = Cobbler('foo')
    pp(x.get_distros())
