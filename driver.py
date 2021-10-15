import glob
import os
from pprint import pprint
import jsonToExcelWriter as xl
import rulesFile
from imageToJson import imageToJson as imgtojson

# result = imgtojson("images/KG-19.jpg")
# pprint(imgtojson("images/KG-19.jpg"), sort_dicts=False)
# pprint(rulesFile.cleanse(result), sort_dicts=False)
# xl.xlHeaderWriter()
# xl.xlDataWriter(imageName="images/KG-19.jpg", jsonFile=result)

directory = input("Enter the directory path: ")
os.chdir(directory)
xl.xlHeaderWriter()
for file in sorted(glob.glob("*.jpg")):
    print(file, ": Processing...", end=" ")
    result = imgtojson(file)
    result = rulesFile.cleanse(result)
    # pprint(rulesFile.cleanse(result), sort_dicts=False)
    xl.xlDataWriter(imageName=file, jsonFile=result)
    # pprint(rulesFile.cleanse(result), sort_dicts=False)
    print("Done\n")
xl.xlFileClose()



