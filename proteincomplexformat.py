#!/usr/bin/env python

"""
Process protein complex files into a two-column format, where 1st column 
contains the complex name and 2nd column contains genes in each complex 

Created: 03 November 2015
"""

import os


def cerevisiae():
    """Process S. cerevisiae protein complexes from Hart, et al. (2007)"""
    writeFile = open(os.path.join('..', 'DataProcessed', 
        'Sc_prot_cmplx_Hart2007.txt'), 'w')
    readFile = open(os.path.join('..', 'DataDownload', 
        'Sc_prot_cmplx_Hart2007.htm'))
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


def uniprot_to_entrez():
    """Return a dictionary from a file mapping UniProt IDs to Entrez. In the 
    case of 1-to-many, the ID is discarded."""
    uniprot2entrez = dict()
    deleteKeys = set()
    mapFile = open(os.path.join('..', 'DataProcessed', 
        'CORUM_Hs_UniProt_mapped.tab'))
    header = mapFile.readline()
    for line in mapFile:
        tokens = line.rstrip().split('\t')
        if tokens[0] not in uniprot2entrez:
            uniprot2entrez[tokens[0]] = tokens[1]
        else:
            deleteKeys.add(tokens[0])
    mapFile.close()

    for delUniProt in deleteKeys:
        del uniprot2entrez[delUniProt]

    return uniprot2entrez


def corum(organism):
    """Process protein complexes for given organism from CORUM into Entrez"""
    os.chdir(os.path.join(os.sep, 'work', 'jyoung', 'DataProcessing'))
    
    uniprot2entrez = uniprot_to_entrez()

    readFile = open(os.path.join('..', 'DataDownload', 
        'CORUM_allComplexes.csv'))
    writeFile = open(os.path.join('..', 'DataProcessed', 
        'CORUM_'+organism+'_Entrez.txt'), 'w')
    
    header = readFile.readline().rstrip().split(';')
    orgCol = header.index('organism')
    nameCol = header.index('Complex name')
    uniprotCol = header.index('subunits (UniProt IDs)')
    idCol = header.index('Complex id')
    
    for line in readFile:
        tokens = line.rstrip().split(';')
        if tokens[orgCol] == organism:
            uniprotIDs = tokens[uniprotCol]
            if uniprotIDs != '':
                if '(' in uniprotIDs:
                    uniprotIDs = uniprotIDs.replace('(', '').replace(')', '')
                    entrezIDs = {uniprot2entrez[u] for u in 
                            uniprotIDs.split(',') if u in uniprot2entrez}
                else:
                    entrezIDs = {uniprot2entrez[u] for u in 
                            uniprotIDs.split(',') if u in uniprot2entrez}
                if tokens[nameCol] == '':
                    cmplxName = 'CORUM' + tokens[idCol]
                else:
                    cmplxName = tokens[nameCol]
                if len(entrezIDs) > 1:
                    for e in entrezIDs:
                        writeFile.write(cmplxName + '\t' + e + '\n')
    
    readFile.close()
    writeFile.close()

