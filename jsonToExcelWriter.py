import xlsxwriter

columnMap = {"Domain Name": "Domain Name", "Domain Reg Name": "Domain Registrar Name",
             "Domain Reg URL": "Domain Registrar URL", "Registrant Name": "Registrant Name",
             "Registrant Company": "Registrant Company", "Registrant Address": "Registrant Address",
             "Registrant E-mail": "Registrant Email", "Registrant Phone": "Registrant Phone",
             "Admin Name": "Administrative Name", "Admin Company": "Administrative Company",
             "Admin Address": "Administrative Address", "Admin E-mail": "Administrative Email",
             "Admin Phone": "Administrative Phone", "Tech Name": "Technical Name",
             "Tech Company": "Technical Company", "Tech Address": "Technical Address",
             "Tech Email": "Technical Email", "Tech Phone": "Technical Phone", "Billing Name": "Billing Name",
             "Billing Company": "Billing Company", "Billing Email": "Billing Email",
             "Billing Phone": "Billing Phone", "Server Name": "Server Name", "Domain Status": "Domain Status",
             "Expiry Date": "Expiry /Date"}

wb = ""
mainSheet = ""
currentRow = 1


def openExcelSheet(fileName):
    global wb
    global mainSheet
    wb = xlsxwriter.Workbook(fileName)
    mainSheet = wb.add_worksheet("Sheet 1")


def xlHeaderWriter():
    global wb
    global mainSheet
    openExcelSheet("Work.xlsx")
    headerFormat = wb.add_format()
    headerFormat.set_bold()
    headerFormat.set_border(1)
    headerFormat.set_align("left")
    headerFormat.set_valign("center")
    headerFormat.set_bg_color("#FFC000")
    for item in ["A", "I", "N", "S", "W"]:
        mainSheet.set_column(str(item + ":" + item), 20)
    for item in ["B", "E", "F", "J", "K", "O", "P", "T", "U", "X", "Y"]:
        mainSheet.set_column(str(item + ":" + item), 30)
    for item in ["D", "H", "M", "R", "V", "Z"]:
        mainSheet.set_column(str(item + ":" + item), 40)
    for item in ["C", "G", "L", "Q"]:
        mainSheet.set_column(str(item + ":" + item), 50)
    for i, key in enumerate(columnMap.keys()):
        mainSheet.write(0, i + 1, key, headerFormat)
    mainSheet.write(0, 0, "Image Name", headerFormat)


def xlDataWriter(imageName, jsonFile):
    global columnMap
    global wb
    global mainSheet
    global currentRow
    cellFormat = wb.add_format()
    cellFormat.set_border(1)
    cellFormat.set_text_wrap()
    cellFormat.set_align("left")
    cellFormat.set_valign("center")
    mainSheet.write(currentRow, 0, imageName, cellFormat)
    for i, key in enumerate(columnMap.keys()):
        mainSheet.write(currentRow, i + 1, jsonFile[columnMap[key]], cellFormat)
    currentRow = mainSheet.dim_rowmax + 1


def xlFileClose():
    global wb
    global mainSheet
    print("saving file...")
    wb.close()
