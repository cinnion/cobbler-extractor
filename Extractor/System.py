#!/usr/bin/env python3.6
'''
Created on May 25, 2018

@author: cinnion
'''

from Extractor.Cobbler import CobblerServer, CobblerRecord, KeywordMap
from shlex import quote
from operator import itemgetter, attrgetter
#import sys

__all__ = [
    'Systems',
    'System'
]
__version__ = 0.5
__date__ = '2018-05-25'
__updated__ = '2018-05-25'


class System(CobblerRecord):
    '''
    This is used to hold and output distributions.
    '''

    kw_map: KeywordMap = {
        'uid':                          ('uid', 'skip'),
        'ctime':                        ('ctime', 'timeStr'),
        'mtime':                        ('mtime', 'timeStr'),
        'depth':                        ('depth', 'skip'),
        'template_remote_kickstarts':   ('template-remote-kickstarts', None),

        'owners':                       ('owners', 'spaceList'),
        'profile':                      ('profile', None),
        'image':                        ('image', None),
        'status':                       ('status', None),
        'kernel_options':               ('kopts', 'namedValues'),
        'kernel_options_post':          ('kopts-post', 'namedValues'),
        'ks_meta':                      ('ksmeta', 'namedValues'),
        'proxy':                        ('proxy', None),
        'netboot_enabled':              ('netboot-enabled', None),
        'kickstart':                    ('kickstart', None),
        'comment':                      ('comment', None),

        'enable_gpxe':                  ('enable-gpxe', None),
        'server':                       ('server', None),

        'hostname':                     ('hostname', None),
        'gateway':                      ('gateway', None),
        'name_servers':                 ('name-servers', 'spaceList'),
        'name_servers_search':          ('name-servers-search', 'spaceList'),
        'ipv6_default_device':          ('ipv6-default-device', None),
        'ipv6_autoconfiguration':       ('ipv6-autoconfiguration', None),

        'interfaces':                   ('interface', None),

        'mgmt_classes':                 ('mgmt-classes', None),
        'mgmt_parameters':              ('mgmt-parameters', None),
        'boot_files':                   ('boot-files', None),
        'fetchable_files':              ('fetchable-files', None),
        'template_files':               ('template-files', None),
        'redhat_management_key':        ('redhat-management-key', None),
        'redhat_management_server':     ('redhat-management-server', None),
        'repos_enabled':                ('repos-enabled', None),
        'ldap_enabled':                 ('ldap-enabled', None),
        'ldap_type':                    ('ldap-type', None),
        'monit_enabled':                ('monit-enabled', None),

        'virt_path':                    ('virt-path', None),
        'virt_type':                    ('virt-type', None),
        'virt_cpus':                    ('virt-cpus', None),
        'virt_file_size':               ('virt-file-size', None),
        'virt_disk_driver':             ('virt-disk-driver', None),
        'virt_ram':                     ('virt-ram', None),
        'virt_auto_boot':               ('virt-auto-boot', 'boolNumberNotZero'),
        'virt_pxe_boot':                ('virt-pxe-boot', None),

        'power_type':                   ('power-type', None),
        'power_address':                ('power-address', None),
        'power_user':                   ('power-user', None),
        'power_pass':                   ('power-pass', None),
        'power_id':                     ('power-id', None),

        'cnames':                       ('cnames', 'spaceList'),
    }

    if_kw_map: KeywordMap = {
        'mac_address':                  ('mac-address', None),
        'connected_mode':               ('connected-mode', None),
        'mtu':                          ('mtu', None),
        'ip_address':                   ('ip-address', None),
        'interface_type':               ('interface-type', None),
        'bonding':                      ('bonding', None),
        'bonding_master':               ('bonding_master', None),
        'bonding_opts':                 ('bonding-opts', None),
        'bridge_opts':                  ('bridge-opts', None),
        'interface_master':             ('interface-master', None),
        'management':                   ('management', None),
        'static':                       ('static', None),
        'netmask':                      ('netmask', None),
        'if_gateway':                   ('if-gateway', None),
        'dhcp_tag':                     ('dhcp-tag', None),
        'dns_name':                     ('dns-name', None),
        'static_routes':                ('static-routes', None),
        'virt_bridge':                  ('virt-bridge', None),
        'ipv6_address':                 ('ipv6-address', None),
        'ipv6_prefix':                  ('ipv6-prefix', None),
        'ipv6_secondaries':             ('ipv6-secondaries', None),
        'ipv6_mtu':                     ('ipv6-mtu', None),
        'ipv6_static_routes':           ('ipv6-static-routes', None),
        'ipv6_default_gateway':         ('ipv6-default-gateway', None),

        'subnet':                       ('subnet', None),
    }

    def __init__(self, **kwargs):
        '''
        Constructor, taking parameters named following the CLI parameter names and setting an attribute with the value.
        '''
        self.name = kwargs.get('name')
        super().__init__(message='Unrecognized system keyword: {} (System={})', **kwargs)

    def __str__(self):
        args = ['--name={}'.format(quote(self.name))]

        mapped_args = super().__str__()
        args.append(mapped_args)

        command = 'cobbler system add ' + ' \\\n        '.join(args) + '\n'

        return(command)


class Systems(object):
    '''
    This is used to extract the distributions from cobbler and output them as cobbler CLI commands
    '''

    def __init__(self, server: CobblerServer, **kwargs):
        '''
        Constructor
        '''
        self.server = server

        self.system_list = []

        system_list = self.server.get_systems()
        for system in system_list:
            self.system_list.append(self.create_system(**system))

        self.system_list = sorted(self.system_list, key=attrgetter('name'))
        self.loaded = True

    def __str__(self):
        cmds = []
        for system in self.system_list:
            cmds.append(str(system))

        return('\n\n'.join(cmds) + '\n')

    def create_system(self, **kwargs):
        s = System(**kwargs)
        return(s)


if __name__ == "__main__":
    x = Systems()
