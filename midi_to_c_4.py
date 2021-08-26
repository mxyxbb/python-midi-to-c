import music21
import re
import os



def buzzerplay(note, notelen, duration):
    global buzzer_num, bunote, bunote_index, buzzer_time, start_time
    for i in range(0, notelen):
        busy = 0
        for j in range(0, buzzer_num):
            if buzzer[j] == 0:
                buzzer[j] = 1
                buzzer_time[j] = duration
                print('buzzer' + str(j) + ':' + note[i])
                break
            else:
                busy = busy + 1
        # print('busy: ' + str(busy))
        if busy == buzzer_num:
            print('buzzer busy!')
    print('busy: ' + str(busy+1))
    bunote[bunote_index] = note
    bunotedura.append(duration)
    buoffset.append(round(start_time, 3))
    bunote_index = bunote_index + 1



def buzzertick():
    global buzzer_num, buzzer_time
    for i in range(0, buzzer_num):
        if buzzer[i] == 1:
            buzzer_time[i] = buzzer_time[i] - 0.001
        if abs(buzzer_time[i]) < 0.001:
            buzzer[i] = 0
            buzzer_time[i] = 0


def printtime(list):
    for i in list:
        print(format(i, '.3f'), end="")
        print(', ', end="")
    print()


def notesplit(note):
    string_waiting = re.split(r'[;,\s\>]\s*', str(note))  # 获取字符串
    midilist = []  # 创建和弦列表
    note_len = len(string_waiting) - 2  # 获取和弦宽度(同时有几个键按下)
    midilist[0:note_len] = string_waiting[1:-1]  # 将每个和弦都存入列表
    return midilist


def durasplit(note):
    notedura = str(note.duration)
    # print(notedura)
    string_dura = re.split(r'[;,\s\>]\s*', notedura)  # 获取字符串
    # print(string_dura[1])
    if string_dura[1] == '1/3':
        return 1 / 3
    elif string_dura[1] == '2/3':
        return 2 / 3
    elif string_dura[1] == '4/3':
        return 4 / 3
    elif string_dura[1] == '5/3':
        return 5 / 3
    elif string_dura[1] == '7/3':
        return 7 / 3
    elif string_dura[1] == '8/3':
        return 8 / 3
    elif string_dura[1] == '10/3':
        return 10 / 3
    elif string_dura[1] == '11/3':
        return 10 / 3
    elif string_dura[1] == '23/3':
        return 23 / 3
    elif string_dura[1] == '44/3':
        return 44 / 3
    elif string_dura[1] == 'unlinked':
        print('unlinked')
        return 1
    else:
        return float(string_dura[1])


def formatstr(test_1):  # convert G#5 to NOTE_GS5
    if re.match("[A-G]", test_1):
        test_1 = "NOTE_" + test_1
    if re.match('NOTE_[A-G]#', test_1):
        test_1 = re.sub(r"#", "S", test_1)
    if re.match("NOTE_[B-G]-", test_1):
        test_1 = test_1[0:5] + chr(ord(test_1[5])-1) + test_1[6:]
        test_1 = re.sub(r"-", 'S', test_1)
    if re.match("NOTE_A-", test_1):
        test_1 = test_1[0:5] + "G" + test_1[6:]
        test_1 = re.sub(r"-", 'S', test_1)
    if re.match("NOTE_[A-G].\d", test_1) == None and re.match("NOTE_[A-G]\d", test_1) == None:
        test_1 = test_1 + '4'
    return test_1


start_time = 0
note_index = 0
midi_length = 0
first_note_flag = 0
buzzer = list()
buzzer_time = list()
buzzer_num = 8
for i in range(0, buzzer_num):
    buzzer.append(0)
    buzzer_time.append(0)

# music_name = "\omr_h"
# music_name = "\Nokia"
# music_name = "\Graze_the_Roof"
# music_name = "\headD"
# music_name = "\Lemon"
# music_name = "\palbg"
# music_name = "/the_internationale_PNO"
# music_name = "/pal1"
# music_name = "/pal3_1"
# music_name = "/pal4_1"
# music_name = "/xiatiandefeng"
# music_name = "/hong_1"
# music_name = "/xxx"
# music_name = "/hlxd_h"
# music_name = "/dlaam"
music_name = "\dshh"

music_channle = 0

mid = music21.converter.parse(r'D:\shared documents\prj\midi'+music_name+".mid")  # 读取midi文件
midi_length = len(mid[music_channle].flat.notes)
# print(mid[music_channle].flat.notes[midi_length-1])

bunote = list()
for i in range(0, midi_length):
    bunote.append(0)
    bunote[i] = list()
bunote_index = 0

bunotedura = list()
# for i in range(0, midi_length):
#     bunotedura.append(0)
#     bunotedura[i] = list()

buoffset = list()
# for i in range(0, midi_length):
#     buoffset.append(0)
#     buoffset[i] = list()


while note_index < midi_length-1:
    if first_note_flag == 0:
        first_note_flag = 1
        note = mid[music_channle].flat.notes[0]
        note_next = mid[music_channle].flat.notes[1]
        midilist = notesplit(note)
        buzzerplay(midilist, len(midilist), durasplit(note))
        print('time' + ":", end="")
        print(format(start_time, '.4f'))
        print('offset: ' + str(note.offset))
        print('offset next: ' + str(note_next.offset))
        print(note_index)
        print(buzzer)
        printtime(buzzer_time)
        print('-------')

    if abs(start_time-float(note_next.offset)) < 0.0005:
        note_index = note_index + 1
        if note_index > midi_length-2:
            # note_index = note_index-2
            break
        note = mid[music_channle].flat.notes[note_index]
        note_next = mid[music_channle].flat.notes[note_index + 1]
        midilist = notesplit(note)
        buzzerplay(midilist, len(midilist), durasplit(note))
        print('time' + ":", end="")
        print(format(start_time, '.10f'))
        print('offset: ' + str(note.offset))
        print('offset next: ', end="")
        print(float(note_next.offset))
        print('note index: ' + str(note_index))
        print(buzzer)
        printtime(buzzer_time)
        print('-------')
        while note.offset == note_next.offset:
            note_index = note_index + 1
            if note_index > midi_length-2:
            #     note_index = note_index-2
                break
            note = mid[music_channle].flat.notes[note_index]
            note_next = mid[music_channle].flat.notes[note_index + 1]
            midilist = notesplit(note)
            buzzerplay(midilist, len(midilist), durasplit(note))
            print('time' + ":", end="")
            print(format(start_time, '.10f'))
            print('offset: ' + str(note.offset))
            print('offset next: ', end="")
            print(float(note_next.offset))
            print('note index: ' + str(note_index))
            print(buzzer)
            printtime(buzzer_time)
            print('--!---!--')
    start_time = start_time + 0.001
    buzzertick()
    
print(bunote)
print(bunotedura)
print(buoffset)

#  convert G#5 to NOTE_B0
ii=0
jj=0
for i in bunote:
    for j in i:
        bunote[ii][jj] = formatstr(j)
        jj = jj + 1
    ii = ii + 1
    jj = 0

#  convert float to int
ii=0
for i in bunotedura:
    bunotedura[ii] = round(i*12)
    ii = ii + 1
#  convert float to int
ii=0
for i in buoffset:
    buoffset[ii] = round(i*12)
    ii = ii + 1

print(bunote)
print(len(bunote))
print(bunotedura)
print(len(bunotedura))
print(buoffset)
print(len(buoffset))




# Open a file
fo = open("music_"+music_name[1:]+".h", "w")
lentowrite = str(len(bunote))
fo.write("uint16_t "+music_name[1:]+"_note[" + lentowrite + "][8]={\n")
for i in bunote[0:-1]: # int a[5][3]={{80,75,92},{61,65,71},{59,63,70},{85,87,90},{76,77,85}};
    fo.write("{")
    for j in i:
        fo.write(j)
        fo.write(",")
    fo.write("},\n")
fo.write("};\n")

fo.write("uint16_t "+music_name[1:]+"_notedura[" + lentowrite + "]={\n")
for i in bunotedura[0:-1]: # int a[5]={80,75,92};
    fo.write(str(i))
    fo.write(",")
fo.write("};\n")

fo.write("uint16_t "+music_name[1:]+"_noteos[" + lentowrite + "]={\n")
for i in buoffset[0:-1]: # int a[5]={80,75,92};
    fo.write(str(i))
    fo.write(",")
fo.write("};\n")

fo.write("uint16_t "+music_name[1:]+"_len=" + lentowrite + ";\n")

# Close opend file
fo.close()

