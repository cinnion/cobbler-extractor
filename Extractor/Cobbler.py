#!/usr/bin/env python3.6
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
from typing import Dict, Tuple, Callable
from numbers import Number


__all__ = [
    'CobblerServer',
    'CobblerRecord',
    'KeywordMap'
]
__version__ = 0.5
__date__ = '2018-05-01'
__updated__ = '2018-05-25'

KeywordMap = Dict[str, Tuple[str, Callable]]


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

    kw_map: KeywordMap = {
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

        return args

    def __str__(self):
        args = []

        for kw in self.kw_map:
            if hasattr(self, kw):
                val = getattr(self, kw)

                if val is None or (not isinstance(val, Number) and len(val) == 0)or '<<inherit>>' == val or ('owners' == kw and val == ['admin']):
                    continue
                elif self.kw_map[kw][1] is not None:
                    f = getattr(self, self.kw_map[kw][1])
                    val = f(kw, val)
                elif isinstance(val, dict):
                    val = ' '.join("{!s}={!s}".format(k, v)
                                   for (k, v) in val.items())

                if val is not None:
                    arg = '--' + self.kw_map[kw][0] + \
                        '={}'.format(quote(str(val)))
                    args.append(arg)

        mapped_args = ' \\\n        '.join(args)

        return mapped_args

    def boolNumberNotZero(self, kw, val):
        '''
        Convert a time value to a string but skip zero values
        '''
        if val is not None and val:
            val = 1
        else:
            val = None
        return val

    def namedValues(self, kw, val):
        '''
        Output a value as a list of key=value pairs
        '''
        opts = []
        for (k, v) in val.items():
            if '~' == v:
                opts.append('{!s}'.format(k))
            else:
                opts.append('{!s}={!s}'.format(k, v))

        rv = ' '.join("{!s}={!s}".format(k, v)
                      for (k, v) in val.items())

        rv = ' '.join(opts)

        return rv

    def skip(self, kw, val):
        return

    def spaceList(self, kw, val):
        '''
        Take a list of values and output it as a list of space separated values
        '''
        rv = ' '.join(val)
        return rv

    def timeStr(self, kw, val):
        '''
        Convert a time value to a string
        '''
        val = str(val)
        return val

    def timeStrNotZero(self, kw, val):
        '''
        Convert a time value to a string but skip zero values
        '''
        if val is not None and val != 0.0:
            val = str(val)
        else:
            val = None
        return val


if __name__ == "__main__":
    x = CobblerServer('foo')
    pp(x.get_distros())
