#!/usr/bin/env python3
import sys
print("The number of arguments is %d" % len(sys.argv))
for eacharg in sys.argv:
    print(eacharg, sys.argv.index(eacharg))

