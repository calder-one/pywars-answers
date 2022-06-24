import socket
import pickle
import ssl
import codecs
import re
import sys

"""Use this module to interact with the pywars server.  You create a handle to the pyWars object using pywars.exercise().  Then you ask for questions and data to submit a answer."""

def snddata(thesocket, thedata, delimiter=b"#&EOF&#"):
    """Dont call this method directly"""
    senddata=codecs.encode(thedata.encode(),"BASE64").strip()+delimiter
    return thesocket.sendall(senddata)

def rcvdata(thesocket, delimiter=b"#&EOF&#"):
    """Dont call this method directly"""
    data=b""
    while not data.endswith(delimiter):
        data+=thesocket.recv(4096)
    return codecs.decode(data[:-len(delimiter)],"BASE64")


class exercise():
    """ The pyWars exercise object is used to interact with the server."""

    def __init__(self, servip = "10.10.10.10", servport = 10000):
        self.serverip = servip
        self.ports = { 2 : 10000, 3: 20000 } 
        self.python_version = sys.version_info.major
        self.serverport = self.ports.get(self.python_version)
        self.sessionid = "NONE"
        self.pywars_version = 3.0
        self.ssl = False
        self.hold_username = ""
        self.hold_password = ""
        self.show_all_scores = True

    def __send__(self,thesocket,thedata):
        "Do not call this method directly"
        return snddata(thesocket, thedata.strip())

    def __recv__(self,thesocket):
        "Do not call this method directly"
        resp = rcvdata(thesocket)
        code = resp[:3]
        data = resp[4:]
        if code == b"300":
            return code,data
        try:
            data = pickle.loads(data)
        except ValueError:
            print("WARNING: This pyWars client is not using the same version of Python as the server.  Connecting to a different server.")
            code = b"300"
            data = ""
        return code,data

    def new_acct(self,teamname,password):
        """Use this method to create an account.  It takes two arguments, a username and a password."""
        self.hold_username=teamname
        self.hold_password=password
        return self.__say__("NEWUSER","%s,%s" % (teamname ,password) )

    def login(self,teamname="",password=""):
        """Use this method to login your account.  If you pass no arguments it will use what ever username and password were last passed to either login or new_acct."""
        if not teamname:
            teamname = self.hold_username
        if not password:
            password = self.hold_password
        dp = self.__say__("LOGIN","%s,%s" % (teamname ,password))
        if not re.match(r"[a-f0-9]{32}", dp):
            return dp
        self.sessionid = dp
        self.hold_username=teamname
        self.hold_password=password
        return "Login Successful"

    def logout(self):
        """Use this method to logout your account."""
        dp = self.__say__("LOGOUT","LOGOUT")
        self.sessionid="NONE"
        return dp

    def password(self,username,newpass):
        """Use this method to reset your password with assistance from the instructor.  Ask the instructor for help to use this method."""
        dp = self.__say__("PASSWORD", "%s,%s" % (username ,newpass))
        return dp

    def points(self, number):
        """Use this method to see how many points a given question is worth. The argument must be an integer of the question number you want the point value of.   For example, gameobject.point(1) will return how many points question 1 is worth if answered correctly."""
        return self.__say__("POINTS","%s" % (str(number).strip() ))

    def question(self, number):
        """Use this method to read a question.  It takes one argument.  The argment must be an integer of the question number you want to read.  For example, to see question number 1 you would do this:  >>> gameobject.question(1)  """
        return self.__say__("QUESTION","%s" % (str(number).strip() ))

    def score(self,show_who=""):
        """This method prints the current scoreboard. Either all player scores or only your score is deplayed depending upon <exercise variable>.show_all_scores. You can override the default by passing "ALL" or "ME" to this function. Example >>> print(gameobject.score("ME")) """
        scoreboard = "ALL" if self.show_all_scores else "ME"
        if show_who=="ALL":
            scoreboard = "ALL"
        if show_who=="ME":
            scoreboard = "ME"
        return self.__say__("SCORE",scoreboard)
       
    def data(self, number):
        """This method will give you the data for a given question that you are supposed to manipulate.  This method takes one argument.  That argument is an integer for the data element you want to retrieve.  For example, the data element of question one is retrieved by executing >>> gameobject.data(1)    For many functions this is a dynamic element and it changes every time you query it.   You will typically pass the data returned by this method to a function that will calculate the answer to the question so you can submit it to answer.   For example, after creating a function called 'solvenum1()' get the answer by calling solvnum1(gameobject.data(1))"""
        dp = self.__say__("DATA","%s" % (str(number).strip() ))
        return dp
        
    def answer(self, number, myanswer):
        """ This method is used to submit an answer.  It takes two arguments.  The first argument is an integer for the question you are answering and the second is the answer.  Typically you will submit the answer by calling a function that calculates the answer based on the data element.  For example, after writing 'solvenum1()'  you would submit your answer by calling >>> gameobject.answer(1, solvenum1(gameobject.data(1)))"""
        return self.__say__("ANSWER", "%s,%s" % (str(number).strip(), str(myanswer).strip() ))
        
    def __say__(self,cmd, data):
        """Do not call this method directly."""
        if self.ssl:
            mysocket = ssl.wrap_socket(socket.socket())
        else:
            mysocket = socket.socket()
        mysocket.connect((self.serverip, self.serverport))
        transmit_string = "%s:%s:%s:%s:%s"  % (self.pywars_version, self.python_version, cmd, self.sessionid, data)
        self.__send__(mysocket, transmit_string)
        code,responsedata = self.__recv__(mysocket)
        mysocket.close()
        if code == b"200":
            return responsedata
        elif code == b"300":
            newip,newport,ssl_enabled = (self.serverip, self.ports.get(self.python_version),False)
            print("Performing Redirect to {0}:{1}".format(newip,newport))
            self.serverip = newip
            self.serverport = int(newport)
            self.ssl = ssl_enabled == "True"
            return self.__say__(cmd,data)
        else:
            print("'<system message>'\n    {0}".format(responsedata))
            return "</system message>"

class version2():
    """ The pyWars exercise object is used to interact with the server."""

    def __init__(self, servip = "10.10.10.10", servport = 10000):
        self.serverip = servip
        self.serverport = servport
        self.sessionid = "NONE"
        self.python_version = sys.version_info.major
        self.pywars_version = 2.0
        self.ssl = False
        self.hold_username = ""
        self.hold_password = ""

    def new_acct(self,teamname,password):
        """Use this method to create an account."""
        self.hold_username=teamname
        self.hold_password=password
        return self.__say__("NEWUSER","%s,%s" % (teamname ,password) )

    def login(self,teamname="",password=""):
        """Use this method to login your account.  If you pass no arguments it will use what ever username and password were last passed to either login or new_acct."""
        if not teamname:
            teamname = self.hold_username
        if not password:
            password = self.hold_password
        dp = self.__say__("LOGIN","%s,%s" % (teamname ,password))
        if self.python_version==3:
            dp = dp.decode()
        if not re.match(r"[a-f0-9]{32}", dp):
            return dp
        self.sessionid = dp
        self.hold_username=teamname
        self.hold_password=password
        return "Login Successful"

    def logout(self):
        """Use this method to logout your account."""
        dp = self.__say__("LOGOUT","LOGOUT")
        self.sessionid="NONE"
        return dp

    def password(self,username,newpass):
        """Use this method to reset your password with assistance from the instructor."""
        dp = self.__say__("PASSWORD", "%s,%s" % (username ,newpass))
        return dp

    def points(self, number):
        """Use this method to see how many points a given question is worth. The argument must be an integer of the question number you want the point value of.   For example, gameobject.point(1) will return how many points question 1 is worth if answered correctly."""
        return self.__say__("POINTS","%s" % (str(number).strip() ))

    def question(self, number):
        """Use this method to read a question.  It takes one argument.  The argment must be an integer of the question number you want to read.  For example, to see question number 1 you would do this:  >>> gameobject.question(1)  """
        return self.__say__("QUESTION","%s" % (str(number).strip() ))

    def score(self):
        """This method prints the current scoreboard.  Example >>> print(gameobject.score()) """
        return self.__say__("SCORE","SCORE")
       
    def data(self, number):
        """This method will give you the data for a given question that you are supposed to manipulate.  This method takes one argument.  That argument is an integer for the data element you want to retrieve.  For example, the data element of question one is retrieved by executing >>> gameobject.data(1)    For many functions this is a dynamic element and it changes every time you query it.   You will typically pass the data returned by this method to a function that will calculate the answer to the question so you can submit it to answer.   For example, after creating a function called 'solvenum1()' get the answer by calling solvnum1(gameobject.data(1))"""
        dp = self.__say__("DATA","%s" % (str(number).strip() ))
        try:
            if self.python_version==3:
                dp = pickle.loads(dp, encoding="bytes")
                if isinstance(dp,bytes):
                    dp = dp.decode()
            else:  #Python 2
                dp = pickle.loads(dp)
        except Exception as e:
            #If it can't be pickled assume we are getting an error message from the server.  Just return dp.
            pass
        return dp
        
    def answer(self, number, myanswer):
        """ This method is used to submit an answer.  It takes two arguments.  The first argument is an integer for the question you are answering and the second is the answer.  Typically you will submit the answer by calling a function that calculates the answer based on the data element.  For example, after writing 'solvenum1()'  you would submit your answer by calling >>> gameobject.answer(1, solvenum1(gameobject.data(1)))"""
        return self.__say__("ANSWER", "%s,%s" % (str(number).strip(), str(myanswer).strip() ))
        
    def __say__(self,cmd, data):
        """Do not call this method directly."""
        if self.ssl:
            mysocket = ssl.wrap_socket(socket.socket())
        else:
            mysocket = socket.socket()
        mysocket.connect((self.serverip, self.serverport))
        transmit_string = "%s:%s:%s:%s:%s"  % (self.pywars_version, self.python_version, cmd, self.sessionid, data)
        snddata(mysocket, transmit_string)
        # mysocket.send("SCORE")
        dp = rcvdata(mysocket)
        mysocket.close()
        return dp


class version1():
    def __init__(self, servip = "10.10.10.10", servport = 10000):
        self.serverip = servip
        self.serverport = servport     

    def register(self, teamname, password=""):
        """Use this method to register your teams.  Pass it your team name and your team password.   To join an existing team you must know the team password.  Once registered all points scored from your IP will be credited to the team.  NOTE: When you initially register for a team or change teams ALL points associated with your IP will be lost.  SO REGISTER FIRST!!   For example >>> gameobject.register('myteam','mypassword')"""
        mysocket = socket.socket()
        mysocket.connect((self.serverip, self.serverport))
        snddata(mysocket, "REGISTER=" + teamname + ":" + password)
        # mysocket.send("REGISTER="+teamname+":"+password)
        dp = rcvdata(mysocket)
        # dp=mysocket.recv(1024)
        mysocket.close()
        return dp

    def points(self, number):
        """Use this method to see how many points a given question is worth. The argument must be an integer of the question number you want the point value of.   For example, gameobject.point(1) will return how many points question 1 is worth if answered correctly."""
        mysocket = socket.socket()
        mysocket.connect((self.serverip, self.serverport))
        snddata(mysocket, str(number).strip() + "-P")
        # mysocket.send(str(number).strip()+"-P")
        dp = rcvdata(mysocket)
        # dp=mysocket.recv(65535)
        mysocket.close()
        return dp

    def question(self, number):
        """Use this method to read a question.  It takes one argument.  The argment must be an integer of the question number you want to read.  For example, to see question number 1 you would do this:  >>> gameobject.question(1)  """
        mysocket = socket.socket()
        mysocket.connect((self.serverip, self.serverport))
        snddata(mysocket, str(number).strip() + "-Q")
        # mysocket.send(str(number).strip()+"-Q")
        dp = rcvdata(mysocket)
        # dp=mysocket.recv(65535)
        mysocket.close()
        return dp

    def score(self):
        """This method prints the current scoreboard.  Example >>> print gameobject.score()"""
        mysocket = socket.socket()
        mysocket.connect((self.serverip, self.serverport))
        snddata(mysocket, "SCORE")
        # mysocket.send("SCORE")
        dp = rcvdata(mysocket)
        mysocket.close()
        return dp

    def data(self, number):
        """This method will give you the data for a given question that you are supposed to manipulate.  This method takes one argument.  That argument is an integer for the data element you want to retrieve.  For example, the data element of question one is retrieved by executing >>> gameobject.data(1)    For many functions this is a dynamic element and it changes every time you query it.   You will typically pass the data returned by this method to a function that will calculate the answer to the question so you can submit it to answer.   For example, after creating a function called 'solvenum1()' get the answer by calling solvnum1(gameobject.data(1))"""
        mysocket = socket.socket()
        mysocket.connect((self.serverip, self.serverport))
        snddata(mysocket, str(number).strip() + "-D")
        dp = rcvdata(mysocket)
        mysocket.close()
        if b"Invalid Question Number" in dp:
            return dp
        try:
            if self.python_version==3:
                dp = pickle.loads(dp, encoding="bytes")
            else:  #Python 2
                dp = pickle.loads(dp)
        except Exception as e:
            dp = "Unable to parse data from server ",e
        return dp

    def answer(self, number, myanswer):
        """ This method is used to submit an answer.  It takes two arguments.  The first argument is an integer for the question you are answering and the second is the answer.  Typically you will submit the answer by calling a function that calculates the answer based on the data element.  For example, after writing 'solvenum1()'  you would submit your answer by calling >>> gameobject.answer(1, solvenum1(gameobject.data(1)))"""
        mysocket = socket.socket()
        mysocket.connect((self.serverip, self.serverport))
        snddata(mysocket, str(number).strip() + "-A=" + str(myanswer).strip())
        # mysocket.send(str(number).strip()+"-A="+str(myanswer).strip())
        dp = rcvdata(mysocket)
        # dp=mysocket.recv(1024)
        mysocket.close()
        return dp