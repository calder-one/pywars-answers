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
def answer13(data):
    # 'Build a list of numbers starting at 1 and up to but not including the number in data(). '
    return list(range(1, data))

def answer14(data):
    # 'Count the number of items in the list in data().  The answer is the number of items in the list.'
    return len(data)

def answer15(data):
    # 'Split the data element based on the comma (",") delimiter and return the 10th element '
    return data.split(",")[9]

def answer16(data):
    # 'The data element contains a line from an /etc/shadow file. The shadow file is a colon delimited file.  The 2nd field in the colon delimited field contains the password information
    # The password information is a dollar sign delimited field with three parts.  The first part indicates what cypher is used.  The second part is the password salt.
    # The last part is the password hash.   Retrieve the password salt for the root user.'
    # 'root:$1$Kf2P11jN$370xDLmeGD9m4aF/ciIlC.:14425:0:99999:7:::'
    return data.split(':')[1].split('$')[2]

def answer17(data):
    # 'Add the string "Pywars rocks" to the end of the list in the data element.  Submit the new list. '
    data.append("Pywars rocks")
    return data

def answer18(data):
    # 'Add up all the numbers in the list and submit the total. '
    return sum(data) 

def answer19(data):
    # 'Given a string that contains numbers separated by spaces, add up the numbers and submit the sum.  "1 1 1" -> 3 '
    return sum(map(int, data.split())) 

def answer20(data):
    # 'Create a string by joining together the words "this","python","stuff","really","is","fun" by the character in .data().
    return data.join(["this", "python", "stuff", "really", "is", "fun"])

def answer21(data):
    # 'The answer is the list of numbers between 1 and 1000 that are evenly divisible by the number provided.  2->[2,4,6,8..] 4->[4,8,16..] '
    return list(range(0,1001,data)[1:])

def answer22(data):
    # 'Given a list of hexadecimal digits return a string that is made from their ASCII characters.  Ex [41 4f] -> "AO" '
    answer = ""
    for eachhex in data:
        ascii_char = chr(int(eachhex, 16))
        answer = answer + ascii_char
    return answer

def answer23(data):
    # 'You will be given a list that contains two lists.  Combine the two lists and eliminate duplicates.  The answer is the SORTED combined list.  [[d,b,a,c][b,d]] -> [a,b,c,d] '
    return sorted(set(data[0] + data[1]))

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
    print("#13", d.answer(13, answer13(d.data(13))))
    print("#14", d.answer(14, answer14(d.data(14))))
    print("#15", d.answer(15, answer15(d.data(15))))
    print("#16", d.answer(16, answer16(d.data(16))))
    print("#17", d.answer(17, answer17(d.data(17))))
    print("#18", d.answer(18, answer18(d.data(18))))
    print("#19", d.answer(19, answer19(d.data(19))))
    print("#20", d.answer(20, answer20(d.data(20))))
    print("#21", d.answer(21, answer21(d.data(21))))
    print("#22", d.answer(22, answer22(d.data(22))))
    print("#23", d.answer(23, answer23(d.data(23)))) 

if __name__ == "__main__":
    d = pyWars.exercise()
    d.login("YourUsername","YourPassword")
    main()
    d.logout()
