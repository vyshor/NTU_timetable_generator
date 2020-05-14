import pandas as pd
import os
import copy
import pickle
import timeit
import shutil

TIME = [x for x in range(830, 2330, 100)]
DAYS = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
TYPE = ["LEC/STUDIO", "SEM", "TUT", "LAB"]
DATA = {}

print("Loading... ")
with open('database.p', 'rb') as f:
    DATA = pickle.load(f)


def intodatabase(url):
    with open(url, 'r') as file:
        text = file.read()
    hp = HTMLTableParser()
    table = hp.parse_url(text)  # Grabbing the table from the tuple

    for x in range(len(table)):
        if x % 2 == 0:
            coursecode = str(table[x][1]).split()[4]  # get all the course code possible
            if coursecode not in DATA.keys():
                DATA[coursecode] = {}
            s = str(table[x + 1][1])
            lst = s.split()
            indexes = []
            for word in lst:
                try:
                    if len(word) == 5 and (float(word) > 0 or int(word)):  # check if the thing is an index or not
                        # if word.find('.') != -1:
                        #     word = '00' + str(int(float(word)))
                        indexes.append(word)
                        DATA[coursecode][word] = []
                except:
                    pass

            temp_lst = False
            lastindex = ""
            for word in lst:
                if word in indexes:
                    lastindex = word
                    continue

                if lastindex != "":
                    if word in TYPE:
                        if temp_lst:  # if it is not empty
                            DATA[coursecode][temp_lst[0]].append(temp_lst[
                                                                 1:-1])  # add in all the data except the index at the front and remove last element which is the index for the row in the table
                            temp_lst = [lastindex, word]  # put the index in as first element
                            continue

                        else:  # it is the first index of all indexes
                            temp_lst = [lastindex, word]
                            continue

                    elif temp_lst:
                        temp_lst.append(word)

                    if word == lst[-1] and temp_lst:  # if the element is last in element and temp_lst not empty
                        DATA[coursecode][temp_lst[0]].append(
                            temp_lst[1:])  # add in all the data except the index at the front
                        temp_lst = False


def removeduplicates():
    global DATA
    for course in DATA.keys():
        for index in DATA[course]:
            for lesson in DATA[course][index]:
                for lesson2 in DATA[course][index]:
                    if lesson != lesson2 and [lesson[0], lesson[1], lesson[2], lesson[3]] == [lesson2[0], lesson2[1],
                                                                                              lesson2[2], lesson2[3]]:
                        DATA[course][index].remove(lesson2)


def planning(coursecode):
    global ultimatelist
    possibleorders(coursecode)

    for u in range(len(ultimatelist)):
        print("Loading:", u, "out of", len(ultimatelist))
        clash = False

        cd = [""] * 15
        cd1 = []
        cd2 = []
        for x in range(6):
            cd1.append(copy.deepcopy(cd))
        for x in range(13):
            cd2.append(copy.deepcopy(cd1))
        timetable = cd2  # copy.deepcopy([copy.deepcopy([copy.deepcopy([""] * 15)]* 6)] * 13)  # Monday to Saturday a grid of 13 x 6 x 15, [WEEK][WEEKDAY][TIME]

        for d in range(len(coursecode)):  # for each course
            if not clash:
                course = coursecode[d]
                index = DATA[course][ultimatelist[u][d]]

                for lesson in index:  # for each lesson in the index, tries to see if can add or not, if cannot go next index
                    for week in range(13):
                        for day in range(len(DAYS)):
                            if not clash:
                                if lesson[2] == DAYS[day]:  # if it is the correct day
                                    time = [int(x) for x in lesson[3].split(
                                        '-')]  # index 0 is the starting time, index 1 is the ending time
                                    for x in range(time[0], time[1] + 100, 100):
                                        temp_msg = course + "\n" + lesson[0] + "\nGrp: " + lesson[1] + "\nVenue: " + \
                                                   lesson[
                                                       4] + '\n'
                                        if x == time[0]:  # means start of event
                                            if len(lesson) != 6:
                                                if timetable[week][day][(
                                                                                x - 830) // 100] != "":  # means got clash in timing, for this index, hence go next index
                                                    clash = True

                                                    # print("There is a clash0")
                                                timetable[week][day][(x - 830) // 100] += temp_msg
                                            elif len(
                                                    lesson) == 6:  # means remarks exist and only happen for specific weeks
                                                s = lesson[5][2:]  # remove first two letters which is Wk
                                                if s.find('-') >= 0:  # means contain - sign
                                                    s = [int(z) for z in s.split('-')]
                                                    for z in range(s[0], s[1] + 1):
                                                        if z == week + 1:
                                                            if timetable[week][day][(
                                                                                            x - 830) // 100] != "":  # means got clash in timing, for this index, hence go next index
                                                                clash = True

                                                                # print("There is a clash1")
                                                            timetable[week][day][(x - 830) // 100] += temp_msg
                                                            timetable[week][day][(x - 830) // 100] += lesson[5] + "\n"
                                                elif s.find(',') >= 0:  # means contain , sign
                                                    s = [int(z) for z in s.split(',')]
                                                    for z in s:
                                                        if z == week + 1:
                                                            if timetable[week][day][(
                                                                                            x - 830) // 100] != "":  # means got clash in timing, for this index, hence go next index
                                                                clash = True

                                                                # print("There is a clash2")
                                                            timetable[week][day][(x - 830) // 100] += temp_msg
                                                            timetable[week][day][(x - 830) // 100] += lesson[5] + "\n"
                                                else:
                                                    s = int(s)
                                                    if s == week + 1:
                                                        if timetable[week][day][(
                                                                                        x - 830) // 100] != "":  # means got clash in timing, for this index, hence go next index
                                                            clash = True

                                                            # print("There is a clash3")
                                                        timetable[week][day][(x - 830) // 100] += temp_msg
                                                        timetable[week][day][(x - 830) // 100] += lesson[5] + "\n"
                                        elif time[0] < x < time[1]:  # means during the event
                                            if len(lesson) != 6:
                                                if timetable[week][day][(
                                                                                x - 830) // 100] != "":  # means got clash in timing, for this index, hence go next index
                                                    clash = True

                                                    # print("There is a clash")
                                                timetable[week][day][(x - 830) // 100] += course
                                            elif len(
                                                    lesson) == 6:  # means remarks exist and only happen for specific weeks
                                                s = lesson[5][2:]  # remove first two letters which is Wk
                                                if s.find('-') >= 0:  # means contain - sign
                                                    s = [int(z) for z in s.split('-')]
                                                    for z in range(s[0], s[1] + 1):
                                                        if z == week + 1:
                                                            if timetable[week][day][(
                                                                                            x - 830) // 100] != "":  # means got clash in timing, for this index, hence go next index
                                                                clash = True

                                                                # print("There is a clash4")
                                                            timetable[week][day][(x - 830) // 100] += course + '\n'
                                                            timetable[week][day][(x - 830) // 100] += lesson[5] + "\n"
                                                elif s.find(',') >= 0:  # means contain , sign
                                                    s = [int(z) for z in s.split(',')]
                                                    for z in s:
                                                        if z == week + 1:
                                                            if timetable[week][day][(
                                                                                            x - 830) // 100] != "":  # means got clash in timing, for this index, hence go next index
                                                                clash = True

                                                                # print("There is a clash5")
                                                            timetable[week][day][(x - 830) // 100] += course + '\n'
                                                            timetable[week][day][(x - 830) // 100] += lesson[5] + "\n"
                                                else:
                                                    s = int(s)
                                                    if s == week + 1:
                                                        if timetable[week][day][(
                                                                                        x - 830) // 100] != "":  # means got clash in timing, for this index, hence go next index
                                                            clash = True

                                                            # print("There is a clash6")
                                                        timetable[week][day][(x - 830) // 100] += course + '\n'
                                                        timetable[week][day][(x - 830) // 100] += lesson[5] + "\n"

        # now try to print the timetable
        if clash == False:
            # print("No clash")

            # actualtimetable = [[""] * 15] * 6
            cd = [""] * 15
            cd1 = []
            for x in range(6):
                cd1.append(copy.deepcopy(cd))
            actualtimetable = cd1

            for week in range(13):
                for day in range(len(DAYS)):
                    for time in range(15):
                        if actualtimetable[day][time].find(timetable[week][day][time]) == -1:
                            actualtimetable[day][time] += timetable[week][day][time]

            mydict = {}
            mydict['Courses'] = [""] * len(TIME)
            mydict['Indexes'] = [""] * len(TIME)

            for x in range(len(ultimatelist[u])):
                mydict['Courses'][x] = coursecode[x]
            for x in range(len(ultimatelist[u])):
                mydict['Indexes'][x] = ultimatelist[u][x]
                if type(mydict['Indexes'][x]) == float or mydict['Indexes'][x].find('.') != -1:
                    mydict['Indexes'][x] = "00" + str(int(float(mydict['Indexes'][x])))
            mydict['Time'] = [str(x) + '-' + str(x + 100) for x in TIME]
            for x in range(6):
                mydict[DAYS[x]] = actualtimetable[x]

            df = pd.DataFrame(mydict)
            df = df[['Courses', 'Indexes', 'Time'] + [DAYS[x] for x in range(6)]]
            df.to_excel('excel.xlsx', sheet_name='Sheet1', index=False)

            os.rename('excel.xlsx', '..\\Timetable\\' + str(u) + '.xlsx')
            # print("Saved to excel")


def multiplesum(lst):
    summa = 1
    for x in lst:
        summa *= x
    return summa


def binarysystem(num, y, syslst, comblst):
    if y == 0 and num < syslst[y]:
        comblst[y] = num
        return comblst
    if y == 0:
        return comblst
    else:
        if num != 0:
            minus = num // multiplesum(syslst[:y])  # rounddown
            if minus >= syslst[y]:
                minus = syslst[y] - 1
            comblst[y] = minus
            num = num - multiplesum(syslst[:y]) * minus
            return binarysystem(num, y - 1, syslst, comblst)
        elif num == 0:
            return binarysystem(num, y - 1, syslst, comblst)


ultimatelist = []  # the list of list of indexes combination


def possibleorders(
        coursecode):  # gives a list of courses and returns the a list of combinations of each indexes from each course

    numindexes = []

    for x in range(len(coursecode)):
        course = coursecode[x]
        numindexes.append(len(DATA[course].keys()))

    numcombin = 1
    for x in numindexes:
        numcombin *= x

    for x in range(numcombin):
        print("Possible combinations:", x)
        lst = [0] * len(numindexes)
        for y in range(1, len(numindexes)):
            if x < numindexes[0]:
                lst[0] = x
                for z2 in range(len(coursecode)):
                    course = coursecode[z2]
                    lst2 = list(DATA[course].keys())

                    num = lst[z2]
                    lst[z2] = lst2[num]
                break

            elif multiplesum(numindexes[:y]) <= x < multiplesum(numindexes[:y + 1]):
                lst = binarysystem(x, y, numindexes, lst)
                for z in range(len(coursecode)):
                    course = coursecode[z]
                    lst2 = list(DATA[course].keys())
                    num = lst[z]
                    lst[z] = lst2[num]
                break

        ultimatelist.append(lst)


if __name__ == '__main__':
    text_input = input(
        'Please key in the courses you taking with a space in between each e.g. "CZ1003 CZ1004 MH1712"\n')
    coursecodes = text_input.split(' ')
    for each_course in coursecodes:
        if each_course not in DATA.keys():
            print(each_course + " is not in the database")
            input('')
            exit()

    if len(coursecodes) <= 1:
        print("Error: Need select at least two courses")
        input('')
        exit()
    if os.path.exists("..\\Timetable") and os.path.isdir("..\\Timetable"):
        shutil.rmtree('..\\Timetable')
        os.mkdir('..\\Timetable')
    else:
        os.mkdir('..\\Timetable')
    timer = timeit.default_timer()
    removeduplicates()
    planning(coursecodes)

    timer2 = timeit.default_timer()
    print("Time Taken:", (timer2 - timer) / 60 / 60, "hours")
    print(text_input)
    input('')
