# -*- coding: utf-8 -*-

import sys,re

def main():
    argvs = sys.argv[1:]
    sem_reg = re.compile('^(\d+\.)?(\d+\.)?(\*|\d+)$')

    if not len(argvs)==2:
        sys.exit("Usage example:\n$ python smvr-len.py 1.0.1 1.2.2")

    for a in argvs:
        if not sem_reg.match(a):
            sys.exit("Please correctly input semmantic version strings (ex: 1.3.5)")

    print distance(argvs[0],argvs[1])

def distance(current_str,target_str):
    v=current_str.split('.')
    o=target_str.split('.')

    vl=len(o)-len(v)
    at=None
    if vl<0:
        at=o
    elif vl>0:
        at=v
    for i in range(abs(vl)):
        at.append('0')

    d=0
    for i in range(max(len(v),len(o))):
        on = int(v[i])
        nn = int(o[i])
        if abs(d)>0:
            #old->new
            if d>0:
                d += nn
            #new->old
            else:
                d -= on
        else:
            d += nn - on
    return d

if __name__ == "__main__":
    main()
