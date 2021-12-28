import glob
import os
import re


# noinspection PyBroadException
def clean(directory):
    os.chdir(directory)
    listOfFiles = glob.glob("*.jpg")
    for i in range(0, len(listOfFiles)):
        oldFileName = listOfFiles[i]
        print("OLD:", oldFileName, end=" ")
        actualNumber = re.findall(r'\d+', listOfFiles[i])
        number = int(actualNumber[0])
        if 0 <= number <= 9:
            number = "0000" + str(number)
        elif 10 <= number <= 99:
            number = "000" + str(number)
        elif 100 <= number <= 999:
            number = "00" + str(number)
        elif 1000 <= number <= 9999:
            number = "0" + str(number)
        else:
            number = str(number)
        if number not in listOfFiles[i]:
            newFileName = listOfFiles[i].replace(actualNumber[0], number)
            try:
                os.rename(oldFileName, newFileName)
            except:
                print("\nError occurred while renaming ", oldFileName, "! \n Stopping the execution...")
                exit(1)
            print("NEW:", newFileName)
        else:
            print("")

