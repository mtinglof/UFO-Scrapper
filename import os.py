import os

f = open("whichtomove.txt", "r")

filelist = f.read().split("\n")

for x in range(0, len(filelist)):
    first_location = r"C:/Users/Luca/Desktop/poems/" + str(filelist[x]) + ".tml"
    second_location = r"C:/Users/Luca/Desktop/Corpus/" + str(filelist[x]) + ".tml"
    os.rename(first_location, second_location)