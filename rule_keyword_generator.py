#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#A script that looks for names of classes and ids in cosmetic adblock/ublock rules for the use in heuristic filters
#sticky_keyword_generator.py this script
#generic_rule_names.txt whole classes and ids
#generic_rule_prefixes.txt the first up to n-1th part of a name seperated by "-"
#generic_rule_suffixes.txt the last part of a name seperated by "-"
#generic_rule_singles.txt names that cannot be seperated by "-"

#License: GPL3.0

from StringIO import StringIO
from urllib2 import urlopen
from urlparse import urlparse
from collections import defaultdict
import re
import operator

source='https://raw.githubusercontent.com/yourduskquibbles/webannoyances/master/ultralist.txt'

#fetching rules from.
print("downloading rules from " + source + "...")
response = urlopen(source)
print("processing...")
lines = response.readlines()
l_names = []
l_prefixes = []
l_suffixes = []
l_singles = []

for line in lines:
    element = re.search(r'^(?!:!*[^#]*)(?:###|##\.)([0-9a-zA-Z\._-]+)', line)
    if element:
        names = element.group(1).split(".")
        for name in names:
            if not name in l_names:
                l_names+=[name]
            subnames=name.split("-")
            if len(subnames)>1:
                for i in range(len(subnames)):
                    if i==len(subnames)-1:
                        if not subnames[i] in l_suffixes:
                            l_suffixes+=[subnames[i]]
                    else:
                        if not subnames[i] in l_prefixes:
                            l_prefixes+=[subnames[i]]
            else:
                if not subnames[0] in l_singles:
                    l_singles += [subnames[0]]



#write list to disk
print("writing to disk")

outfile = open('generic_rule_names.txt', 'w')
for line in l_names:
  outfile.write("%s\n" % line)
outfile.close()

outfile = open('generic_rule_prefixes.txt', 'w')
for line in l_prefixes:
  outfile.write("%s\n" % line)
outfile.close()

outfile = open('generic_rule_suffixes.txt', 'w')
for line in l_suffixes:
  outfile.write("%s\n" % line)
outfile.close()

outfile = open('generic_rule_singles.txt', 'w')
for line in l_singles:
  outfile.write("%s\n" % line)
outfile.close()