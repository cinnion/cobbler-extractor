#!/usr/bin/env python3
'''
Created on Apr 29, 2018

@author: cinnion
'''

from Extractor.Cobbler import Cobbler
from pprint import pprint as pp
from pprint import pformat

cmd_help = """
Usage: cobbler [options]

Options:
  -h, --help            show this help message and exit
  --name=NAME           Name (Ex: Fedora-11-i386)
  --ctime=CTIME         
  --mtime=MTIME         
  --uid=UID             
  --owners=OWNERS       Owners (Owners list for authz_ownership (space
                        delimited))
  --kernel=KERNEL       Kernel (Absolute path to kernel on filesystem)
  --initrd=INITRD       Initrd (Absolute path to kernel on filesystem)
  --kopts=KERNEL_OPTIONS
                        Kernel Options (Ex: selinux=permissive)
  --kopts-post=KERNEL_OPTIONS_POST
                        Kernel Options (Post Install) (Ex: clocksource=pit
                        noapic)
  --ksmeta=KS_META      Kickstart Metadata (Ex: dog=fang agent=86)
  --arch=ARCH           Architecture (valid options:
                        i386,x86_64,ia64,ppc,ppc64,ppc64le,s390,arm)
  --breed=BREED         Breed (What is the type of distribution?)
  --os-version=OS_VERSION
                        OS Version (Needed for some virtualization
                        optimizations)
  --source-repos=SOURCE_REPOS
                        Source Repos
  --depth=DEPTH         Depth
  --comment=COMMENT     Comment (Free form text description)
  --tree-build-time=TREE_BUILD_TIME
                        Tree Build Time
  --mgmt-classes=MGMT_CLASSES
                        Management Classes (Management classes for external
                        config management)
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
  --clobber             allow add to overwrite existing objects
  --in-place            edit items in kopts or ksmeta without clearing the
                        other items

"""


class Distros(Cobbler):
    '''
    This is used to extract a distro from cobbler
    '''

    def __init__(self, cob, **kwargs):
        '''
        Constructor
        '''
        super().__init__(**kwargs)

        self.xyz = cob.get_distros()

        self.distro_list = self.get_distros()

    def __str__(self):
        s = ''
        for d in self.distro_list:
            s += pformat(d) + "\n"

        return(s)


if __name__ == "__main__":
    x = Distros()
    pp(x.get_distros())
