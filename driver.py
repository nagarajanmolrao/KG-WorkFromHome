import glob
import os
from pprint import pprint
import jsonToExcelWriter as xl
import rulesFile
from imageToJson import imageToJson as iToJ
import cleanFileNames

# result = imgtojson("images/KG-19.jpg")
# pprint(imgtojson("images/KG-19.jpg"), sort_dicts=False)
# pprint(rulesFile.cleanse(result), sort_dicts=False)
# xl.xlHeaderWriter()
# xl.xlDataWriter(imageName="images/KG-19.jpg", jsonFile=result)


# def processImage(file):
#     print("Processing ", file)
#     result = iToJ(file)
#     result = rulesFile.cleanse(result)
#     # pprint(rulesFile.cleanse(result), sort_dicts=False)
#     xl.xlDataWriter(imageName=file, jsonFile=result)
#     # pprint(rulesFile.cleanse(result), sort_dicts=False)
#     print(file, "Done\n")


directoryFlag = False
while not directoryFlag:
    directory = input("Enter the directory path: ")
    if os.path.exists(directory):
        directoryFlag = True
# noinspection PyUnboundLocalVariable
cleanFileNames.clean(directory)
os.chdir(directory)
xl.xlHeaderWriter()
for file in glob.glob("*.jpg"):
    print(file, ": Processing...", end=" ")
    # noinspection PyBroadException
    try:
        result = iToJ(file)
    except:
        print("Error: Image to JSON")
        continue
    # noinspection PyBroadException
    try:
        result = rulesFile.cleanse(result)
    except:
        print("Error: Applying rules")
    xl.xlDataWriter(imageName=file, jsonFile=result)
    # pprint(rulesFile.cleanse(result), sort_dicts=False)
    print("Done\n")
xl.xlFileClose()
