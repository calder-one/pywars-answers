from __future__ import print_function
from __future__ import division

try:
    input = raw_input
except:
    pass

num1 = int(input("Enter integer 1 :"))
num2 = int(input("Enter integer 2 :"))
print("{0} + {1} = {2}".format(num1,num2,num1+num2))
print("{0} * {1} = {2}".format(num1,num2,num1*num2))
print("{0} / {1} = {2:0>6.2f}".format(num1,num2,num1/num2))

