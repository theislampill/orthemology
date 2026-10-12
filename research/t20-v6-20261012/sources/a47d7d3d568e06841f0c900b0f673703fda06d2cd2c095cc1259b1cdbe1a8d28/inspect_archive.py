#!/usr/bin/env python3
"""Validate and safely extract a one-root research ZIP. Does not run its code."""
import argparse
from pathlib import Path
from package_tools import safe_extract

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('archive',type=Path)
    p.add_argument('new_destination',type=Path)
    a=p.parse_args()
    try:
        result=safe_extract(a.archive,a.new_destination)
    except (OSError,ValueError) as e:p.exit(1,'REFUSED: '+str(e)+'\n')
    print(result)

if __name__=='__main__':main()
