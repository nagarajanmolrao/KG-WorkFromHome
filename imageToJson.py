import json
import pytesseract
import cv2 as cv
import numpy as np

# from pprint import pprint

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def imageToJson(filename):
    img = cv.imread(cv.samples.findFile(filename))
    cImage = np.copy(img)
    # cv.imshow("OriginalImage", img)
    # cv.waitKey(0)

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # cv.imshow("GrayImage", gray)
    # cv.waitKey(0)
    canny = cv.Canny(gray, 50, 150)
    # cv.imshow("CannyImage", canny)
    # cv.waitKey(0)

    rho = 2
    theta = np.pi / 180
    threshold = 80
    minLinLength = 220
    maxLineGap = 7
    linesP = cv.HoughLinesP(canny, rho, theta, threshold, None, minLinLength, maxLineGap)

    def is_vertical(line):
        return line[0] == line[2]

    def is_horizontal(line):
        return line[1] == line[3]

    horizontal_lines = []
    vertical_lines = []

    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            if is_vertical(l):
                vertical_lines.append(l)

            elif is_horizontal(l):
                horizontal_lines.append(l)
    for i, line in enumerate(horizontal_lines):
        cv.line(cImage, (line[0], line[1]), (line[2], line[3]), (0, 255, 0), 3, cv.LINE_AA)

    for i, line in enumerate(vertical_lines):
        cv.line(cImage, (line[0], line[1]), (line[2], line[3]), (0, 0, 255), 3, cv.LINE_AA)

    # cv.imshow("with_line", cImage)
    # cv.waitKey(0)

    def overlapping_filter(lines, sorting_index):
        filtered_lines = []

        lines = sorted(lines, key=lambda lines: lines[sorting_index])
        separation = 5
        for i in range(len(lines)):
            l_curr = lines[i]
            if (i > 0):
                l_prev = lines[i - 1]
                if ((l_curr[sorting_index] - l_prev[sorting_index]) > separation):
                    filtered_lines.append(l_curr)
            else:
                filtered_lines.append(l_curr)

        return filtered_lines

    horizontal_lines = []
    vertical_lines = []

    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            if (is_vertical(l)):
                vertical_lines.append(l)

            elif (is_horizontal(l)):
                horizontal_lines.append(l)
        horizontal_lines = overlapping_filter(horizontal_lines, 1)
        vertical_lines = overlapping_filter(vertical_lines, 0)

    lines = {}
    for i, line in enumerate(horizontal_lines):
        cv.line(cImage, (line[0], line[1]), (line[2], line[3]), (0, 255, 0), 3, cv.LINE_AA)
        item = str("h" + str(i))
        lines[item] = {}
        lines[item]["x1"] = str(line[0])
        lines[item]["y1"] = str(line[1])
        lines[item]["x2"] = str(line[2])
        lines[item]["y2"] = str(line[3])
        cv.putText(cImage, str(i) + "h", (line[0] + 5, line[1]), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv.LINE_AA)
    for j, line in enumerate(vertical_lines):
        cv.line(cImage, (line[0], line[1]), (line[2], line[3]), (0, 0, 255), 3, cv.LINE_AA)
        item = str("v" + str(j))
        lines[item] = {}
        lines[item]["x1"] = str(line[0])
        lines[item]["y1"] = str(line[1])
        lines[item]["x2"] = str(line[2])
        lines[item]["y2"] = str(line[3])
        cv.putText(cImage, str(j) + "v", (line[0], line[1] + 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv.LINE_AA)

    img = cv.imread(cv.samples.findFile(filename))
    cImage = np.copy(img)

    # with open("lines.json", "r") as file:
    #     lines = json.load(file)

    start_x, start_y = 0, 0
    end_x, end_y = 0, 0
    first_column, second_column = 0, 0

    # Get the most common start_x
    x = []
    for line in lines.keys():
        value = int(lines[line]["x1"])
        x.append(value)
    x0 = int(max(x, key=x.count))

    y = []
    for line in lines.keys():
        value = int(lines[line]["y1"])
        y.append(value)
    y0 = int(max(y, key=y.count))

    # Drawing rectangles on image
    def get_next_line(current_pos, lines):
        # global lines
        line_list = list(lines.keys())
        try:
            res = line_list[line_list.index(current_pos) + 1]
        except (ValueError, IndexError):
            res = None
        return res

    def showImage(cImage, start_x, start_y, end_x, end_y):
        color = (255, 0, 0)
        thickness = 2
        cImage = cv.rectangle(cImage, (start_x, start_y), (end_x, end_y), color, thickness)
        cv.imshow("rectangle", cImage)
        cv.waitKey(0)

    def readFirstColumnText(cImage, start_x, start_y, end_x, end_y):
        croppedImage = cImage[start_y:end_y, start_x:end_x]
        croppedImage = cv.cvtColor(croppedImage, cv.COLOR_BGR2GRAY)
        croppedImage = cv.threshold(croppedImage, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]
        croppedImage = 255 - croppedImage
        return str.strip(pytesseract.image_to_string(croppedImage, lang='eng', config='--psm 6'))
        # cv.imshow("First", croppedImage)
        # cv.waitKey(0)

    def readSecondColumnText(cImage, start_x, start_y, end_x, end_y):
        croppedImage = cImage[start_y:end_y, start_x:end_x]
        croppedImage = cv.cvtColor(croppedImage, cv.COLOR_BGR2GRAY)
        croppedImage = cv.threshold(croppedImage, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]
        croppedImage = 255 - croppedImage
        return str.strip(pytesseract.image_to_string(croppedImage, lang='eng', config='--psm 6'))
        # cv.imshow("Second", croppedImage)
        # cv.waitKey(0)

    imageData = {}
    keyBlackListChars = "»+:;.,<>=-!@#$%^&*()"
    valueBlackListChars = ["\n"]

    def keyCheck(keyL):
        if keyL in ["Biling Name", "Blling Name", "Bling Name"]:
            keyL = "Billing Name"
        if keyL in ["Technical Fhone"]:
            keyL = "Technical Phone"
        if keyL in ["Technical Campany"]:
            keyL = "Technical Company"
        return keyL

    for i in lines.keys():
        next_pos = get_next_line(i, lines)
        if next_pos is None:
            print("Over")
            break
        elif next_pos in "v0v1v2":
            break
        else:
            # Left Column
            start_x = x0
            start_y = int(lines[i]["y1"])
            end_x = int(lines["v1"]["x1"])
            end_y = int(lines[str(next_pos)]["y1"])
            # showImage(cImage, start_x, start_y, end_x, end_y)
            key = readFirstColumnText(img, start_x, start_y, end_x, end_y)
            for item in keyBlackListChars:
                if item in key:
                    key = key.replace(item, '')
            key = key.strip()
            key = keyCheck(key)
            imageData[key] = ""
            # Right Column
            start_x = end_x + 3
            end_x = int(lines["v2"]["x1"])
            # showImage(cImage, start_x, start_y, end_x, end_y)
            keyValue = readSecondColumnText(img, start_x, start_y, end_x, end_y)
            for item in valueBlackListChars:
                if item in keyValue:
                    keyValue = keyValue.replace(item, " ")
            keyValue = keyValue.strip()
            imageData[key] = keyValue

    return imageData
