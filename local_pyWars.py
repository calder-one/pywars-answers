#! /usr/bin/env python2
import itertools
import code
import sys
import pickle
import time

class exercise():

    def __init__(self, dataset = "default"):
        self.serverip = "There is no server ip this time.  There is no server."
        self.serverport = "There is no port.  Just run .question(), .data(), .answer()"
        self.player_name="Not Registered"
        self.player_pw = ""
        if dataset == "default":
            dataset = "pylite{0}.data".format(sys.version_info.major)
        if dataset.lower()=="victors":
            dataset = "hof.data"
        try:
            self._dataq = pickle.load(open(dataset,"rb"))
            self.num_questions = len(self._dataq)
            self._datas=[0] * self.num_questions
        except Exception as e:
            print("Unable to load supporing data file. %s %s" % (dataset,str(e)))


    def login(self,username,password):
        self.player_name = username
        self.player_pw = password
        return "You have been logged on."

    def logout(self):
        return "You have been logged out."

    def password(self,username, password):
        return "There is no password in the offline server to reset."

    def new_acct(self,username, password =""):
        self.player_name = username
        return "There is no need to create an account in the local version."

    def register(self, teamname, password=""):
        """Use this method to register your teams.  Pass it your team name and your team password.   To join an existing team you must know the team password.  Once registered all points scored from your IP will be credited to the team.  NOTE: When you initially register for a team or change teams ALL points associated with your IP will be lost.  SO REGISTER FIRST!!   For example >>> gameobject.register('myteam','mypassword')"""
        self.player_name=teamname
        self.player_pw = password
        return "You have been registered."

    def points(self, number):
        """Use this method to see how many points a given question is worth. The argument must be an integer of the question number you want the point value of.   For example, gameobject.point(1) will return how many points question 1 is worth if answered correctly."""
        return 1

    def question(self, number):
        """Use this method to read a question.  It takes one argument.  The argment must be an integer of the question number you want to read.  For example, to see question number 1 you would do this:  >>> gameobject.question(1)  """
        if number >= self.num_questions: return "Invalid Question Number"
        return self._dataq[number].get("Q")

    def score(self,who=""):
        """This method prints the current scoreboard.  Example >>> print gameobject.score()"""
        return "Player %s \nPOINTS :%03d  - You answered question(s) %s" % (self.player_name,  sum(self._datas), ",".join(itertools.compress(list(map(str,list(range(self.num_questions)))), self._datas) )  )

    def data(self, number):
        """This method will give you the data for a given question that you are supposed to manipulate.  This method takes one argument.  That argument is an integer for the data element you want to retrieve.  For example, the data element of question one is retrieved by executing >>> gameobject.data(1)    For many functions this is a dynamic element and it changes every time you query it.   You will typically pass the data returned by this method to a function that will calculate the answer to the question so you can submit it to answer.   For example, after creating a function called 'solvenum1()' get the answer by calling solvnum1(gameobject.data(1))"""
        if number >= self.num_questions: return "Invalid Question Number"
        self.data_time = time.time()
        return self._dataq[number].get("D")

    def answer(self, number, myanswer):
        """ This method is used to submit an answer.  It takes two arguments.  The first argument is an integer for the question you are answering and the second is the answer.  Typically you will submit the answer by calling a function that calculates the answer based on the data element.  For example, after writing 'solvenum1()'  you would submit your answer by calling >>> gameobject.answer(1, solvenum1(gameobject.data(1)))"""
        if number >= self.num_questions:
            return "Invalid Question Number"
        if (time.time() - self.data_time) > 3:
            return "Timeout!  You must submit your answer less than 3 seconds after you query the .data()"
        if str(self._dataq[number].get("A")).replace(" ","") == str(myanswer).replace(" ",""):
            self._datas[number]=1
            return "Correct"
        else:
            return "%s is Incorrect"  % (str(myanswer))

def startclient():
    if len(sys.argv)>1:
        d = exercise('victors')
    else:
        d= exercise()
    print("The variable 'd' has been loaded with the pywars client.  Try 'print(d.score())'")
    print("If you want to use a different variable just assign it to d.  For example, 'game = d'.")
    code.interact(banner='Welcome to pyWars!', local=locals())


print("This copy of pyWars is licensed exclusively to the attendee of SANS SEC573 to which it was given.\nThis software and all SEC573 Labs are protected by the SANS courseware copyright and licensing agreement.\n")
if __name__=="__main__":
    startclient()
