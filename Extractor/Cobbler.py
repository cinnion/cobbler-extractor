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
    'KeywordMap',
    'DepricatedKeywords',
]
__version__ = 0.5
__date__ = '2018-05-01'
__updated__ = '2018-05-25'

KeywordMap = Dict[str, Tuple[str, Callable]]
DepricatedKeywords = Dict[str, str]

_showAdds = False


class CobblerServer(Server):
    '''
    This is the module for talking to the cobbler server
    '''

    def __init__(self, protocol='http', host='cobbler', api='cobbler_api', showAdds=None, **kwargs):
        '''
        Constructor
        '''
        global _showAdds

        if protocol not in ('http', 'https'):
            raise OSError("unsupported cobbler xmlrpc protocol")

        self.protocol = protocol
        self.host = host
        self.api = api
        url = self.protocol + '://' + self.host + '/' + self.api

        if showAdds is not None:
            _showAdds = showAdds

        self.server = super().__init__(url, allow_none=True)


class CobblerRecord(object):
    '''
    This holds the base functionallity for handling the records for distros, profiles, systems, etc.
    '''

    joinWrap = ' \\\n        '

    kw_map: KeywordMap = {
    }

    dep_kw_map: DepricatedKeywords = {
    }

    altered_fields = {
        'kernel_options': 'kopts',
        'kernel_options_post': 'kopts-post',
        'ks_meta': 'ksmeta'
    }

    def __init__(self, message='Unrecognized keyword: {} ({})', **kwargs):
        '''
        Constructor, taking parameters named following the CLI parameter names and setting an attribute with the value.
        '''
        self.name = kwargs.get('name')
        for kw in kwargs:
            if kw in self.kw_map:
                setattr(self, kw, kwargs[kw])
            elif kw in self.dep_kw_map:
                setattr(self, self.dep_kw_map[kw], kwargs[kw])
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

        global _showAdds

        command = ''
        objectType = type(self).__name__

        if objectType != 'SystemInterface':
            command = 'cobbler ' + objectType.lower() + \
                ' add --name={}'.format(quote(self.name))

            if _showAdds:
                command = 'echo ' + command + '\n' + command

            command += self.joinWrap

        args = []

        for kw in self.kw_map:
            if hasattr(self, kw):
                val = getattr(self, kw)
                if kw in self.altered_fields:
                    option = self.altered_fields[kw]
                else:
                    option = kw.replace('_', '-')

                if val is None or (not isinstance(val, Number) and len(val) == 0) or '<<inherit>>' == val or ('owners' == kw and val == ['admin']):
                    continue
                elif self.kw_map[kw][1] is not None:
                    f = getattr(self, self.kw_map[kw][1])
                    val = f(kw, val)
                elif isinstance(val, dict):
                    val = ' '.join("{!s}={!s}".format(k, v)
                                   for (k, v) in val.items())

                if val is not None:
                    arg = '--' + option + \
                        '={}'.format(quote(str(val)))
                    args.append(arg)

        mapped_args = self.joinWrap.join(args)

        return command + mapped_args

    def boolNotFalse(self, kw, val):
        '''
        Convert a boolean value to a string but skip zero values
        '''
        if val is not None and val:
            val = 'True'
        else:
            val = None
        return val

    def boolNumberNotZero(self, kw, val):
        '''
        Convert a boolean value to a number but skip zero values
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
