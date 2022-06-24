from __future__ import print_function
#import pyWars
import local_pyWars as pyWars
import codecs

def answer1(datasample):
    # 'ROT-13 encode the .data() string. For example ABCDEFG becomes NOPQRST '
    return datasample+5

def answer2(data):
    # 'ROT-13 encode the .data() string. For example ABCDEFG becomes NOPQRST '
    return codecs.encode(data,"rot13")

def answer3(data):
    # 'Decode the BASE64 encoded .data() string. '
    return codecs.decode(data, "BASE64")

def answer4(data):
    # 'Make .data() all CAPS.   For example Test->TEST '
    return data.upper()

def answer5(data):
    # "The answer is the position of the first letter of the word 'SAND' in the data() string. "
    return data.find("SANS")

def answer6(data):
    # 'Read the .data() string and write it backwards. '
    return data[::-1]

def answer7(data):
    # 'Submit data() forward+backwards+forward. For example SAM -> SAMMASSAM '
    return data+data[::-1]+data

def answer8(data):
    # 'Return the 2nd, 5th and 9th character.  For example 0123456789->148 '
    return data[1]+data[4]+data[8]

def answer9(data):
    # 'Swap the first and last character. For example frog->grof, Hello World->dello Worlh etc. '
    return data[-1] + data[1:-1] + data[0]

def answer10(data):
    # 'Reverse the first half of the data(). For example sandwich->dnaswich '
    return data[:len(data) // 2][::-1 ] + data[len(data) //2:]

def answer11(data):
    # 'Leet speak it (E->3,A->4,T->7,S->5,G->6) convert only uppercase letters. For example LeEtSpEAk->Le3t5p34k '
    return data.replace("E", "3").replace("A", "4").replace("T", "7").replace("S", "5").replace("G", "6")

def answer12(data):
    # 'Read the list from data and return the 3rd element '
    return data[2]

def main():
    print("#1", d.answer(1, answer1(d.data(1))))
    print("#2", d.answer(2, answer2(d.data(2))))
    print("#3", d.answer(3, answer3(d.data(3))))
    print("#4", d.answer(4, answer4(d.data(4))))
    print("#5", d.answer(5, answer5(d.data(5))))
    print("#6", d.answer(6, answer6(d.data(6))))
    print("#7", d.answer(7, answer7(d.data(7))))
    print("#8", d.answer(8, answer8(d.data(8))))
    print("#9", d.answer(9, answer9(d.data(9))))
    print("#10", d.answer(10, answer10(d.data(10))))
    print("#11", d.answer(11, answer11(d.data(11))))
    print("#12", d.answer(12, answer12(d.data(12))))

if __name__ == "__main__":
    d = pyWars.exercise()
    d.login("YourUsername","YourPassword")
    main()
    d.logout()
