#!/usr/bin/env python

"""
Methods for constructing sets of genes.

Created: 14 November 2015
"""

def process_file(filename):
    """Read in file containing gene sets (i.e. protein complexes) and return
    dictionary {set:[genes]}"""
    set2genes = dict()
    for line in open(filename):
        fields = line.strip().split('\t')
        set2genes.setdefault(fields[0],[]).append(fields[1])
    return set2genes

