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
min_keyword_len=3
min_keyword_score=5
max_list_len=0

#fetching rules from.
print("downloading rules from " + source + "...")
response = urlopen(source)
print("processing...")
lines = response.readlines()
l_names = defaultdict()
l_prefixes = defaultdict()
l_suffixes = defaultdict()
l_singles = defaultdict()
l_keywords = defaultdict()
ignore_keywords=defaultdict()

with open("ignore_keywords.txt") as f:
    ignore_keywords = f.readlines()
ignore_keywords = [ignore_keyword.strip() for ignore_keyword in ignore_keywords]

for line in lines:
    element = re.search(r'(?:###|##\.)([0-9a-zA-Z\._-]+)', line)
    if element:
        names = element.group(1).split(".")
        for name in names:
            if len(name)>=min_keyword_len and not name in ignore_keywords:
                if (not name in l_names):
                    #l_names+=[name]
                    l_names[name]=1
                else:
                    l_names[name] += 1
            subnames=name.split("-")
            if len(subnames)>1:
                for i in range(len(subnames)):
                    if len(subnames[0]) >= min_keyword_len and not subnames[0] in ignore_keywords:
                        if not subnames[0] in l_keywords:
                            #l_keywords += [subnames[0]]
                            l_keywords[subnames[0]]=1
                        else:
                            l_keywords[subnames[0]] += 1
                    if i==len(subnames)-1:
                        if len(subnames[0]) >= min_keyword_len and not subnames[0] in ignore_keywords:
                            if not subnames[i] in l_suffixes:
                                #l_suffixes+=[subnames[i]]
                                l_suffixes[subnames[i]]=1
                            else:
                                l_suffixes[subnames[i]] += 1
                    else:
                        if len(subnames[i]) >= min_keyword_len and not subnames[i] in ignore_keywords:
                            if not subnames[i] in l_prefixes:
                                #l_prefixes+=[subnames[i]]
                                l_prefixes[subnames[i]]=1
                            else:
                                l_prefixes[subnames[i]] += 1
            else:
                if (len(subnames[0]) >= min_keyword_len) and (not subnames[0] in ignore_keywords):
                    if not subnames[0] in l_keywords:
                        #l_keywords += [subnames[0]]
                        l_keywords[subnames[0]]=1
                    else:
                        l_keywords[subnames[0]] += 1
                    if not subnames[0] in l_singles:
                        #l_singles += [subnames[0]]
                        l_singles[subnames[0]]=1
                    else:
                        l_singles[subnames[0]] += 1

l_names = sorted(l_names.items(), key=operator.itemgetter(1), reverse=True)
l_prefixes = sorted(l_prefixes.items(), key=operator.itemgetter(1), reverse=True)
l_suffixes = sorted(l_suffixes.items(), key=operator.itemgetter(1), reverse=True)
l_singles = sorted(l_singles.items(), key=operator.itemgetter(1), reverse=True)
l_keywords = sorted(l_keywords.items(), key=operator.itemgetter(1), reverse=True)


#write list to disk
print("writing to disk")

outfile = open('generic_rule_names.txt', 'w')
i=0
for line in l_names:
  if (line[1]<min_keyword_score and min_keyword_score>0) or (i>=max_list_len and max_list_len>0):
      print("stopping at #" + str(i) + " with '" + line[0] + "' at a score of " + str(line[1]))
      break
  outfile.write("%s\n" % line[0])
  i+=1
outfile.close()

outfile = open('generic_rule_prefixes.txt', 'w')
i=0
for line in l_prefixes:
    if (line[1] < min_keyword_score and min_keyword_score > 0) or (i >= max_list_len and max_list_len > 0):
        print("stopping at #" + str(i) + " with '" + line[0] + "' at a score of " + str(line[1]))
        break
    outfile.write("%s\n" % line[0])
    i += 1
outfile.close()

outfile = open('generic_rule_suffixes.txt', 'w')
i=0
for line in l_suffixes:
    if (line[1] < min_keyword_score and min_keyword_score > 0) or (i >= max_list_len and max_list_len > 0):
        print("stopping at #" + str(i) + " with '" + line[0] + "' at a score of " + str(line[1]))
        break
    outfile.write("%s\n" % line[0])
    i += 1
outfile.close()

outfile = open('generic_rule_singles.txt', 'w')
i=0
for line in l_singles:
    if (line[1] < min_keyword_score and min_keyword_score > 0) or (i >= max_list_len and max_list_len > 0):
        print("stopping at #" + str(i) + " with '" + line[0] + "' at a score of " + str(line[1]))
        break
    outfile.write("%s\n" % line[0])
    i += 1
outfile.close()

outfile = open('generic_rule_keywords.txt', 'w')
i=0
for line in l_keywords:
    if (line[1] < min_keyword_score and min_keyword_score > 0) or (i >= max_list_len*3 and max_list_len > 0):
        print("stopping at #" + str(i) + " with '" + line[0] + "' at a score of " + str(line[1]))
        break
    outfile.write("%s\n" % line[0])
    i += 1
outfile.close()