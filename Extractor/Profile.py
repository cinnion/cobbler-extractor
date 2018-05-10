#!/usr/bin/env python3
'''
Created on Apr 29, 2018

@author:     Douglas Needham

@copyright:  2018 Douglas Needham. All rights reserved.

@license:    TBD

@contact:    cinnion@gmail.com
@deffield    updated: Updated
'''

from Extractor.Cobbler import CobblerServer, CobblerRecord
from shlex import quote
from operator import itemgetter, attrgetter
#import sys

__all__ = [
    'Profiles',
    'Profile'
]
__version__ = 0.1
__date__ = '2018-05-01'
__updated__ = '2018-05-01'

"""
[root@downbelow named]# cobbler profile add --help
Usage: cobbler [options]

Options:
  -h, --help            show this help message and exit
  --name=NAME           Name (Ex: F10-i386-webserver)
  --uid=UID             
  --owners=OWNERS       Owners (Owners list for authz_ownership (space
                        delimited))
  --distro=DISTRO       Distribution (Parent distribution)
  --parent=PARENT       Parent Profile
  --enable-gpxe=ENABLE_GPXE
                        Enable gPXE? (Use gPXE instead of PXELINUX for
                        advanced booting options)
  --enable-menu=ENABLE_MENU
                        Enable PXE Menu? (Show this profile in the PXE menu?)
  --kickstart=KICKSTART
                        Kickstart (Path to kickstart template)
  --kopts=KERNEL_OPTIONS
                        Kernel Options (Ex: selinux=permissive)
  --kopts-post=KERNEL_OPTIONS_POST
                        Kernel Options (Post Install) (Ex: clocksource=pit
                        noapic)
  --ksmeta=KS_META      Kickstart Metadata (Ex: dog=fang agent=86)
  --proxy=PROXY         Internal proxy (Internal proxy URL)
  --repos=REPOS         Repos (Repos to auto-assign to this profile)
  --comment=COMMENT     Comment (Free form text description)
  --virt-auto-boot=VIRT_AUTO_BOOT
                        Virt Auto Boot (Auto boot this VM?)
  --virt-cpus=VIRT_CPUS
                        Virt CPUs (integer)
  --virt-file-size=VIRT_FILE_SIZE
                        Virt File Size(GB)
  --virt-disk-driver=VIRT_DISK_DRIVER
                        Virt Disk Driver Type (The on-disk format for the
                        virtualization disk)
  --virt-ram=VIRT_RAM   Virt RAM (MB)
  --depth=DEPTH         
  --virt-type=VIRT_TYPE
                        Virt Type (Virtualization technology to use) (valid
                        options: xenpv,xenfv,qemu,kvm,vmware,openvz,SETTINGS:d
                        efault_virt_type)
  --virt-path=VIRT_PATH
                        Virt Path (Ex: /directory OR VolGroup00)
  --virt-bridge=VIRT_BRIDGE
                        Virt Bridge
  --dhcp-tag=DHCP_TAG   DHCP Tag (See manpage or leave blank)
  --server=SERVER       Server Override (See manpage or leave blank)
  --ctime=CTIME         
  --mtime=MTIME         
  --name-servers=NAME_SERVERS
                        Name Servers (space delimited)
  --name-servers-search=NAME_SERVERS_SEARCH
                        Name Servers Search Path (space delimited)
  --mgmt-classes=MGMT_CLASSES
                        Management Classes (For external configuration
                        management)
  --mgmt-parameters=MGMT_PARAMETERS
                        Management Parameters (Parameters which will be handed
                        to your management application (Must be valid YAML
                        dictionary))
  --boot-files=BOOT_FILES
                        TFTP Boot Files (Files copied into tftpboot beyond the
                        kernel/initrd)
  --fetchable-files=FETCHABLE_FILES
                        Fetchable Files (Templates for tftp or wget/curl)
  --template-files=TEMPLATE_FILES
                        Template Files (File mappings for built-in config
                        management)
  --redhat-management-key=REDHAT_MANAGEMENT_KEY
                        Red Hat Management Key (Registration key for RHN,
                        Spacewalk, or Satellite)
  --redhat-management-server=REDHAT_MANAGEMENT_SERVER
                        Red Hat Management Server (Address of Spacewalk or
                        Satellite Server)
  --template-remote-kickstarts=TEMPLATE_REMOTE_KICKSTARTS

"""


class Profile(CobblerRecord):
    '''
    This is used to hold and output profiles.
    '''

    kw_map = {
        'uid': 'uid',
        'owners': 'owners',
        'distro': 'distro',
        'parent': 'parent',
        'enable_gpxe': 'enable-gpxe',
        'enable_menu': 'enable-menu',
        'kickstart': 'kickstart',
        'kernel_options': 'kopts',
        'kernel_options_post': 'kopts-post',
        'ks_meta': 'ksmeta',
        'proxy': 'proxy',
        'repos': 'repos',
        'comment': 'comment',
        'virt_auto_boot': 'virt-auto-boot',
        'virt_cpus': 'virt-cpus',
        'virt_file_size': 'virt-file-size',
        'virt_disk_driver': 'virt-disk-driver',
        'virt_ram': 'virt-ram',
        'depth': 'depth',
        'virt_type': 'virt-type',
        'virt_path': 'virt-path',
        'virt_bridge': 'virt-bridge',
        'dhcp_tag': 'dhcp-tag',
        'server': 'server',
        'ctime': 'ctime',
        'mtime': 'mtime',
        'name_servers': 'name-servers',
        'name_servers_search': 'name-servers-search',
        'mgmt_classes': 'mgmt-classes',
        'mgmt_parameters': 'mgmt-parameters',
        'boot_files': 'boot-files',
        'fetchable_files': 'fetchable-files',
        'template_files': 'template-files',
        'redhat_management_key': 'redhat-management-key',
        'redhat_management_server': 'redhat-management-server',
        'template_remote_kickstarts': 'template-remote-kickstarts',
    }

    def __init__(self, **kwargs):
        '''
        Constructor, taking parameters named following the CLI parameter names and setting an attribute with the value.
        '''
        self.name = kwargs.get('name')
        super().__init__('Unrecognized profile keyword: {} (Profile={})', **kwargs)

    def __str__(self):
        args = ['--name={}'.format(quote(self.name))]

        mapped_args = super().__str__()
        args.append(mapped_args)

        command = 'cobbler profile add ' + ' \\\n        '.join(args)

        return(command)


class Profiles(CobblerServer):
    '''
    This is used to extract the profiles from cobbler and output them as cobbler CLI commands
    '''

    def __init__(self, server: CobblerServer, **kwargs):
        '''
        Constructor
        '''
        self.server = server

        self.profile_list = []

        profile_list = self.server.get_profiles()
        for profile in profile_list:
            self.profile_list.append(self.create_profile(**profile))

        self.profile_list = sorted(self.profile_list, key=attrgetter('name'))
        self.loaded = True

    def __str__(self):
        cmds = []
        for profile in self.profile_list:
            cmds.append(str(profile))

        return('\n\n'.join(cmds))

    def create_profile(self, **dict):
        p = Profile(**dict)
        return(p)


if __name__ == "__main__":
    x = Profiles()
