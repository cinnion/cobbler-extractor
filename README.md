# cobbler-extractor
A tool to extract existing configuration data into a shell script of commands to use in a clean installation.

## Description:

This tool will ultimately be able to extract the configuration data from both
cobbler 2.8 and 3.3 installations (and hopefully 3.3+, unless we change the
arguments).  For right now, the main branch is an early version of the 2.x
extractor, with the v2-to-v3 branch being tested for the 2.8->3.3 versions.

Exporting from Cobbler 2.8 and into 3.3 currently results in errors, which are
being resolved.

## Requirements:

The requirements are as follows:

- Python 3.6+ installed and in your path.

## How to run.

To run the utility, do the following:

```
# cd Extractor
# export PYTHONPATH=../
# ./Extract.py --host yourhost.example.com
```

Adding the `--help` argument, will get you the full list of arguments, such as
those allowing for setting the protocol, doing cleanup statements to delete all
the objects, and more.

