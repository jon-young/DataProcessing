#!/usr/bin/env python

"""
Process protein complex files into a two-column format, where 1st column 
contains the complex name and 2nd column contains genes in each complex 

Created: 03 November 2015
"""

import os.path


def cerevisiae():
    writeFile = open(os.path.join('..', 'DataProcessed', 'Sc_prot_cmplx_Hart2007.txt'), 'w')
    readFile = open(os.path.join('..', 'DataDownload', 'Sc_prot_cmplx_Hart2007.htm'))
    for i in range(11):  # skip 1st 11 header lines
        line = readFile.readline()
    for line in readFile:
        if line[0] == 'C':
            tokens = line.rstrip().split('\t')
            if int(tokens[1]) > 1:  # if complex has more than one gene
                cid = tokens[0]
                genes = tokens[3].rstrip('|').split('|')
                for sym in genes:
                    writeFile.write(cid + '\t' + sym + '\n')
    readFile.close()
    writeFile.close()


def main():
    cerevisiae()


if __name__=="__main__":
    main()

