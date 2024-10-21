#!/usr/bin/env python3.6
"""
Created on May 25, 2018

@author:     Douglas Needham

@copyright:  2018-2024 Douglas Needham. All rights reserved.

@license:    BSD-3-Clause

@contact:    douglas.w.needham@gmail.com
"""

from operator import attrgetter
from pprint import pp

from Extractor.Cobbler import CobblerServer, CobblerRecord, KeywordMap

__all__ = [
    'Images',
    'Image'
]
__version__ = 0.7
__date__ = '2018-05-25'
__updated__ = '2024-10-20'


class Image(CobblerRecord):
    """
    This is used to hold and output distributions.
    """

    kw_map: KeywordMap = {
        'uid': ('uid', 'skip'),
        'ctime': ('ctime', 'timeStr'),
        'mtime': ('mtime', 'timeStr'),
        'depth': ('depth', 'skip'),
        'parent': ('parent', None),

        'arch': ('arch', None),
        'breed': ('breed', None),
        'comment': ('comment', None),
        'file': ('file', None),
        'image_type': ('image-type', None),
        'network_count': ('network-count', None),
        'os_version': ('os-version', None),
        'owners': ('owners', None),
        'kickstart': ('kickstart', None),

        'virt_auto_boot': ('virt-auto-boot', None),
        'virt_bridge': ('virt-bridge', None),
        'virt_cpus': ('virt-cpus', None),
        'virt_file_size': ('virt-file-size', None),
        'virt_disk_driver': ('virt-disk-driver', None),
        'virt_path': ('virt-path', None),
        'virt_ram': ('virt-ram', None),
        'virt_type': ('virt-type', None),
    }

    def __init__(self, **kwargs):
        """
        Constructor, taking parameters named following the CLI parameter names and setting an attribute with the value.
        """
        self.name = kwargs.get('name')
        super().__init__(message='Unrecognized distro keyword: {} (Image={})', **kwargs)


class Images(object):
    """
    This is used to extract the distributions from cobbler and output them as cobbler CLI commands
    """

    def __init__(self, server: CobblerServer, **_kwargs):
        """
        Constructor
        """
        self.server = server

        self.image_list = []

        image_list = self.server.get_images()
        for image in image_list:
            self.image_list.append(self.create_image(**image))

        self.image_list = sorted(self.image_list, key=attrgetter('name'))
        self.loaded = True

    def __str__(self):
        cmds = []
        for image in self.image_list:
            cmds.append(str(image))

        return '\n\n'.join(cmds) + '\n'

    @staticmethod
    def create_image(**kwargs):
        i = Image(**kwargs)
        return i


if __name__ == "__main__":

    s = CobblerServer('foo')
    pp(Images(s))
