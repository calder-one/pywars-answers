import threading
import time
import sys
from optparse import OptionParser
from Queue import Queue
import signal


parser = OptionParser(
    usage='%prog -g "GPU Count" -G "GPU Time" -t "Thread Count" -c "CPU Delay" -p <password count>')
parser.add_option('-v', '--verbose', action='store_true',
                  help='Print verbose output.', dest='verbose')
parser.add_option('-g', '--gpucount', type='int', default=1,
                  help='Number of GPUs in the system - Default=1.', dest='gpucount')
parser.add_option('-G', '--gputime', type='float', default=0.1,
                  help='Number of seconds required by GPU to calculate a hash - Default=0.1', dest='gputime')
parser.add_option('-t', '--threadcount', type='int', default=1,
                  help='Number of threads to share the GPU(s) - Default=1.', dest='threadcount')
parser.add_option('-c', '--cpudelay', type='float', default=0.0,
                  help='An artificial CPU delay to slow down the program making it easier to watch-Default=0.0', dest='cpudelay')
parser.add_option('-p', '--password_count', type='int', default=100,
                  help='The number of passwords guesses put in the thread queue-Default=100', dest='passcount')

(options, args) = parser.parse_args()


def safeprint(instr):
    screenlock.acquire()
    print instr
    screenlock.release()


def password_guesser():
    while not exit_thread.isSet():
        if options.verbose:
            safeprint(
                threading.currentThread().name + ": Retrieve next password from queue.")
        passwordguess = pwqueue.get()
        if passwordguess == "!EXITTHREAD!":
            break
        time.sleep(delay)
        gpulock.acquire()
        if options.verbose:
            safeprint(threading.currentThread(
            ).name + ": Acquired GPU to calculate hash for " + passwordguess.strip())
        if options.verbose:
            safeprint(threading.currentThread(
            ).name + "* Calculating the hash in the GPU.  This will take " + str(gpu_time + delay) + " seconds.")
        time.sleep(gpu_time + delay)
        if options.verbose:
            safeprint(threading.currentThread().name +
                      ": Hash calculated! Release GPU and compare results")
        gpulock.release()
        time.sleep(delay)
        pwqueue.task_done()
    if options.verbose:
        safeprint(
            threading.currentThread().name + ": End of Password queue reached.")

exit_thread = threading.Event()
exit_thread.clear()

# The NumberofOvens indicates how many ovens there are to be shared by the
# bakers
NumberofGPUs = options.gpucount
# The NumberofCakes indicates how many cakes each baker will cook befor
# quitting
NumberofThreads = options.threadcount
delay = options.cpudelay
gpu_time = options.gputime

pwqueue = Queue()
for passwd in range(options.passcount):
    pwqueue.put("AwesomePasswordGuess#" + str(passwd))

for x in range(NumberofThreads):
    pwqueue.put("!EXITTHREAD!")

# Create the resource locks
screenlock = threading.Lock()
gpulock = threading.Semaphore(NumberofGPUs)

# Start the number of specified threads

start_time = time.time()
for x in range(NumberofThreads):
    th = threading.Thread(target=password_guesser)
    try:
        th.start()
    except:
        print "Error starting Thread " + str(x) + " No more threading resources available."

threads_running = True
try:
    while not pwqueue.empty():
        pass
except KeyboardInterrupt:
    safeprint(
        "**************** KEYBOARD INTERRUPT RECIEVED : Telling threads to exit ************")
    exit_thread.set()

for x in threading.enumerate():
    if x.name != "MainThread":
        x.join()
elapsed = start_time - time.time()
print "Elapsed time is " + str(abs(elapsed)) + " seconds."
