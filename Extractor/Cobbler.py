#!/usr/bin/env python3
'''
Created on Apr 29, 2018

@author: cinnion

@contact:    cinnion@gmail.com
@deffield    updated: Updated
'''

from xmlrpc.client import Server
from pprint import pprint as pp
from shlex import quote
import sys
from keyword import kwlist

__all__ = [
    'CobblerServer',
    'CobblerRecord'
]
__version__ = 0.5
__date__ = '2018-05-01'
__updated__ = '2018-05-01'


class CobblerServer(Server):
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


class CobblerRecord(object):
    '''
    This holds the base functionallity for handling the records for distros, profiles, systems, etc.
    '''

    kw_map = {
    }

    def __init__(self, message='Unrecognized keyword: {} ({})', **kwargs):
        '''
        Constructor, taking parameters named following the CLI parameter names and setting an attribute with the value.
        '''
        self.name = kwargs.get('name')
        for kw in kwargs:
            if kw in self.kw_map:
                setattr(self, kw, kwargs[kw])
            elif 'name' == kw:
                continue
            else:
                print(message.format(kw, self.name), file=sys.stderr)

    def __repr__(self):
        args = []

        for kw in self.kw_map:
            if hasattr(self, kw):
                val = getattr(self, kw)
            else:
                val = None
            args[kw] = val

        return(args)

    def __str__(self):
        args = []

        for kw in self.kw_map:
            if hasattr(self, kw):
                val = getattr(self, kw)

                if val is None or '' == val or '<<inherit>>' == val or {} == val or [] == val or ('owners' == kw and val == ['admin']):
                    continue
                elif 'owners' == kw and len(val) > 0:
                    val = ' '.join(val)
                elif kw in ('ctime', 'mtime'):
                    val = str(val)
                elif 'uid' == kw:
                    continue
                elif 'depth' == kw:
                    continue
                elif 'comment' == kw and len(val) == 0:
                    continue
                elif isinstance(val, dict):
                    val = ' '.join("{!s}={!s}".format(k, v)
                                   for (k, v) in val.items())
                elif isinstance(val, str):
                    val = quote(val)
                elif kw in ('virt_file_size', 'virt_path') and isinstance(val, list):
                    print(kw)
                    print(val)
                    val = ', '.join("{!s}={!s}".format(k, v)
                                    for (k, v) in val.items())

                arg = '--' + self.kw_map[kw] + '={}'.format(val)
                args.append(arg)

        mapped_args = ' \\\n        '.join(args)

        return(mapped_args)


if __name__ == "__main__":
    x = CobblerServer('foo')
    pp(x.get_distros())
