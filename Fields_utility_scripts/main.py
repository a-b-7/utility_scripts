'''
@Arphaxad

'''
import csv
import logging
import os

# checking result. txt file

print("provide file.txt (case sensitive) for execution ")

if os.path.isfile is False:
    print(" no input file file.txt is fount, exiting... ")

if os.path.isfile("result.txt") or os.path.isfile('final_file.txt'):
    print( " file exist which could be over write, please save or remove them ")
    print (" program is exiting  file...")
    print(" pls fix and rerun, os.exit(0)")
    os._exit(0)
# else:
print("continuing the program")

fr = open("file.txt", mode='r')
nw = open("result.txt", mode='w')
fw = open("final_file.txt",mode = 'w')
c = 0
# print(fr.read()) rewd in once instance
# print(fr.readline(), end ='')
# print(fr.readline(),end ='')
# print(fr.readline(),end ='')
# print(fr.readline(),end ='')
# print(fr.readline(),end ='')
# print(fr.readline(),end ='')
# a = fr.readline()
# nw.write(a)
# a = fr.readline()
# nw.write(a)
# a = fr.readline()
# nw.write(a)
# a = fr.readline()
# nw.write(a)
# a = fr.readline()
# nw.write(a)
# a = fr.readline()
# nw.write(a)
# a = fr.readline()
# nw.write(a)
# a = fr.readline()
# nw.write(a)
# ind = 3
pointer = 3
'''
 reading  single character 
'''
# for l in fr:
# #     print(l)
#     writer = fr.readline(1)
#     if writer == '\n':
#         print(" newlinw here")
#         pointer+=1
# print(pointer)
    # if writer == '':
    #     nw.writelines('')
    # else:
    #  nw.writelines(writer)
    # c+=1
    # if(c==5):
    #     break
# print(c)
# data = fr.readlines()
# for lines in data:
#     print(lines.strip())
No_of_objects = 0
list = []

for lines in fr:
    # writer  = fr.readline()
    writer  = fr.readline()
    
    if pointer == 3:
     
     nw.write(writer)
     list.append(writer)
    #  list.append('|')
     No_of_objects+=1
     pointer=1
    #  pointer+=1
    else:
        pointer+=1
print(" no of objects is ",No_of_objects)
# fw.write(list)
'''
  program for final cration of file

'''

# print(list)
new_list = []

length_list = len(list)
pipe_count = length_list-1

for i in list:
    # print(i,end = '')
    x = len(i)
    word = i[0:x-1]
    new_list.append(word)
    fw.write(word)
    if pipe_count!= 0:
     fw.write('|')
     pipe_count-=1

# print(new_list)
fr.close()
nw.close()
fw.close()

print('*'*40)
print("DO you want to values too? it will return strings for all fields")
print('*'*40)

choice= str(input(" type n for no y for yes.."))

if choice.lower() == 'n':
    print(" exiting..")
    os._exit(0)
else:
 with open("final_file.txt", mode = 'a') as file:
    file.write('\n'*3)
    file.write('*'*20)
    file.write("........................values................")
    file.write('*'*20)
    file.write('\n'*3)

    for i in range (No_of_objects):
        file.write("String")
        if i<(No_of_objects-1):
            file.write("|")

