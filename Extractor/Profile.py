#!/usr/bin/env python3
"""
Created on Apr 29, 2018

@author:     Douglas Needham

@copyright:  2018-2024 Douglas Needham. All rights reserved.

@license:    BSD-3-Clause

@contact:    douglas.w.needham@gmail.com
"""

from operator import attrgetter
from pprint import pp

from Extractor.Cobbler import CobblerServer, CobblerRecord, KeywordMap

__all__ = [
    'Profiles',
    'Profile'
]
__version__ = 0.7
__date__ = '2018-05-01'
__updated__ = '2024-10-20'


class Profile(CobblerRecord):
    """
    This is used to hold and output profiles.
    """

    kw_map: KeywordMap = {
        'uid':                          ('uid', 'skip'),
        'ctime':                        ('ctime', 'skip'),
        'mtime':                        ('mtime', 'skip'),
        'depth':                        ('depth', 'skip'),
        'template_remote_kickstarts':   ('template-remote-kickstarts', None),

        'owners':                       ('owners', 'spaceList'),
        'distro':                       ('distro', None),
        'parent':                       ('parent', None),
        'enable_menu':                  ('enable-menu', None),
        'kickstart':                    ('autoinstall', None),
        'kernel_options':               ('kernel-options', 'namedValues'),
        'kernel_options_post':          ('kernel-options-post', 'namedValues'),
        'ks_meta':                      ('autoinstall-meta', 'namedValues'),
        'proxy':                        ('proxy', None),
        'repos':                        ('repos', 'spaceList'),
        'comment':                      ('comment', None),

        'enable_gpxe':                  ('enable-ipxe', None),
        'dhcp_tag':                     ('dhcp-tag', None),
        'server':                       ('server', None),

        'name_servers':                 ('name-servers', 'spaceList'),
        'name_servers_search':          ('name-servers-search', 'spaceList'),

        'mgmt_classes':                 ('mgmt-classes', None),
        'mgmt_parameters':              ('mgmt-parameters', None),
        'boot_files':                   ('boot-files', None),
        'fetchable_files':              ('fetchable-files', None),
        'template_files':               ('template-files', None),
        'redhat_management_key':        ('redhat-management-key', None),
        'redhat_management_server':     ('redhat-management-server', None),

        'virt_auto_boot':               ('virt-auto-boot', 'boolNumberNotZero'),
        'virt_cpus':                    ('virt-cpus', None),
        'virt_file_size':               ('virt-file-size', None),
        'virt_disk_driver':             ('virt-disk-driver', None),
        'virt_ram':                     ('virt-ram', None),
        'virt_type':                    ('virt-type', None),
        'virt_path':                    ('virt-path', None),
        'virt_bridge':                  ('virt-bridge', None),
    }

    def __init__(self, **kwargs):
        """
        Constructor, taking parameters named following the CLI parameter names and setting an attribute with the value.
        """
        self.name = kwargs.get('name')
        super().__init__('Unrecognized profile keyword: {} (Profile={})', **kwargs)


class Profiles(CobblerServer):
    """
    This is used to extract the profiles from cobbler and output them as cobbler CLI commands
    """

    def __init__(self, server: CobblerServer, **_kwargs):
        """
        Constructor
        """

        self.server = server

        self.profile_list = []

        profile_list = self.server.get_profiles()
        for profile in profile_list:
            self.profile_list.append(self.create_profile(**profile))

        self.profile_list = sorted(
            self.profile_list, key=attrgetter('parent', 'name'))
        self.loaded = True

    def __str__(self):
        cmds = []
        for profile in self.profile_list:
            cmds.append(str(profile))

        return '\n\n'.join(cmds) + '\n'

    @staticmethod
    def create_profile(**kwargs):
        p = Profile(**kwargs)
        return p


if __name__ == "__main__":
    s = CobblerServer('foo')
    pp(Profiles(s))
