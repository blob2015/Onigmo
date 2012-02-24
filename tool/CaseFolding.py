#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Usage:
#   $ wget http://www.unicode.org/Public/UNIDATA/CaseFolding.txt
#   $ python CaseFolding.py CaseFolding.txt > ../enc/unicode/casefold.h

from __future__ import print_function
import sys
import re

def print_case_folding_data(filename):
    pattern = re.compile("([0-9A-Z]{4,6}); ([CFT]); " +
            "([0-9A-Z]{4,6})(?: ([0-9A-Z]{4,6}))?(?: ([0-9A-Z]{4,6}))?;")
    
    fold = {}
    unfold = [{}, {}, {}]
    turkic = []
    
    with open(filename, 'r') as f:
        for line in f:
            res = pattern.match(line)
            if not res:
                continue
            ch_from = int(res.group(1), 16)
            ch_to = []
            
            if res.group(2) == 'T':
                # Turkic case folding
                turkic.append(ch_from)
                continue
            
            # store folding data
            for i in range(3, 6):
                if res.group(i):
                    ch_to.append(int(res.group(i), 16))
            fold[ch_from] = ch_to
            
            # store unfolding data
            key = tuple(ch_to)
            i = len(key) - 1
            unfold[i].setdefault(key, []).append(ch_from)
    
    # move locale dependent data to (un)fold_locale
    fold_locale = {}
    unfold_locale = [{}, {}]
    for ch_from in turkic:
        key = tuple(fold[ch_from])
        i = len(key) - 1
        unfold_locale[i][key] = unfold[i][key]
        del unfold[i][key]
        fold_locale[ch_from] = fold[ch_from]
        del fold[ch_from]
    
    # print the header
    print("/* DO NOT EDIT THIS FILE. */")
    print("/* Generated by tool/CaseFolding.py */\n")
    
    # print folding data
    
    # CaseFold
    print("static const CaseFold_11_Type CaseFold[] = {")
    for k, v in sorted(fold.items()):
        sv = ", ".join(["0x%04x" % i for i in v])
        print(" { 0x%04x, {%d, {%s}}}," % (k, len(v), sv))
    print("};\n")
    
    # CaseFold_Locale
    print("static const CaseFold_11_Type CaseFold_Locale[] = {")
    for k, v in sorted(fold_locale.items()):
        sv = ", ".join(["0x%04x" % i for i in v])
        print(" { 0x%04x, {%d, {%s}}}," % (k, len(v), sv))
    print("};\n")
    
    # print unfolding data
    
    # CaseUnfold_11
    print("static const CaseUnfold_11_Type CaseUnfold_11[] = {")
    for k, v in sorted(unfold[0].items()):
        sv = ", ".join(["0x%04x" % i for i in v])
        print(" { 0x%04x, {%d, {%s }}}," % (k[0], len(v), sv))
    print("};\n")
    
    # CaseUnfold_11_Locale
    print("static const CaseUnfold_11_Type CaseUnfold_11_Locale[] = {")
    for k, v in sorted(unfold_locale[0].items()):
        sv = ", ".join(["0x%04x" % i for i in v])
        print(" { 0x%04x, {%d, {%s }}}," % (k[0], len(v), sv))
    print("};\n")
    
    # CaseUnfold_12
    print("static const CaseUnfold_12_Type CaseUnfold_12[] = {")
    for k, v in sorted(unfold[1].items()):
        sk = ", ".join(["0x%04x" % i for i in k])
        sv = ", ".join(["0x%04x" % i for i in v])
        print(" { {%s}, {%d, {%s }}}," % (sk, len(v), sv))
    print("};\n")
    
    # CaseUnfold_12_Locale
    print("static const CaseUnfold_12_Type CaseUnfold_12_Locale[] = {")
    for k, v in sorted(unfold_locale[1].items()):
        sk = ", ".join(["0x%04x" % i for i in k])
        sv = ", ".join(["0x%04x" % i for i in v])
        print(" { {%s}, {%d, {%s }}}," % (sk, len(v), sv))
    print("};\n")
    
    # CaseUnfold_13
    print("static const CaseUnfold_13_Type CaseUnfold_13[] = {")
    for k, v in sorted(unfold[2].items()):
        sk = ", ".join(["0x%04x" % i for i in k])
        sv = ", ".join(["0x%04x" % i for i in v])
        print(" { {%s}, {%d, {%s }}}," % (sk, len(v), sv))
    print("};\n")
    
    # table sizes
    fold_table_size = len(fold) + len(fold_locale)
    print("#define FOLD_TABLE_SIZE\t\t%d" % int(fold_table_size * 1.2))
    unfold1_table_size = len(unfold[0]) + len(unfold_locale[0])
    print("#define UNFOLD1_TABLE_SIZE\t%d" % int(unfold1_table_size * 1.2))
    unfold2_table_size = len(unfold[1]) + len(unfold_locale[1])
    print("#define UNFOLD2_TABLE_SIZE\t%d" % int(unfold2_table_size * 1.5))
    unfold3_table_size = len(unfold[2])
    print("#define UNFOLD3_TABLE_SIZE\t%d" % int(unfold3_table_size * 1.7))

def main():
    filename = 'CaseFolding.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    print_case_folding_data(filename)

if __name__ == '__main__':
    main()
