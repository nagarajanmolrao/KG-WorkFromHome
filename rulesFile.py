def cleanse(jsonVar):
    jsonVar = clean(jsonVar)
    jsonVar = rule_1(jsonVar)
    jsonVar = rule_2(jsonVar)
    jsonVar = rule_3(jsonVar)
    jsonVar = rule_4(jsonVar)
    jsonVar = rule_5(jsonVar)
    jsonVar = rule_6(jsonVar)
    jsonVar = rule_8(jsonVar)

    return jsonVar


# Clean PhoneNumbers, URLs, EmailAddresses
def clean(jsonVar):
    applicableFieldsList = ["Domain Name", "Domain Registrar URL", "Registrant Email", "Registrant Phone",
                            "Administrative Email", "Administrative Phone", "Technical Email", "Technical Phone",
                            "Billing Email", "Billing Phone"]
    blackListChars = [",", ";", "\n", " ", "$"]
    for i in applicableFieldsList:
        text = str(jsonVar[i])
        for j in blackListChars:
            text = text.replace(j, "")
        jsonVar[i] = text
    return jsonVar


# RULE 1: No space before and after Hyphen
def rule_1(jsonVar):
    applicableFieldsList = jsonVar.keys()
    for i in applicableFieldsList:
        hyphenIndex = jsonVar[i].find("-")
        if hyphenIndex != -1:
            text = str(jsonVar[i])
            textList = text.split("-")
            for j in range(0, len(textList)):
                textList[j] = textList[j].strip()
            text = ""
            for k in textList:
                text = text.join(k)
    return jsonVar


# RULE 2: Short forms
def rule_2(jsonVar):
    abbreviations = {
        "Inc.": "Incorporation", "Ltd.": "Limited", "Ave.": "Avenue", "Ct.": "Court", "Ste.": "Suite",
        "Pkwy.": "Parkway", "Ln.": "Lane", "Dr": "Drive", "Dr,": "Drive,^^", "Pl.": "Place", "Blvd.": "Boulevard",
        "Apt.": "Apartment", "Rd.": "Road", "Pvt.": "Private", "Corp.": "Corporation",
        "EW.": "East West", "SN.": "South North", "SW.": "South West", "LLC": "Limited Liability Company",
        "Co.": "Company"
    }
    applicableFieldsList = set(jsonVar.keys()) - set(list(["Registrant Address", "Administrative Address",
                                                           "Technical Address"]))
    for i in applicableFieldsList:
        for abbv in abbreviations.keys():
            if abbv in str(jsonVar[i]):
                text = str(jsonVar[i])
                text = text.replace(abbv, abbreviations[abbv])
                jsonVar[i] = text
    return jsonVar


# RULE 3: (Double Space(^^) after comma(,) in Registrant, Administrative and Technical Address) &
# (Single space(^) after comma(,) in rest of the fields)
def rule_3(jsonVar):
    applicableFieldsList = ["Registrant Address", "Administrative Address", "Technical Address"]
    for i in applicableFieldsList:
        text = str(jsonVar[i])
        text = str(text.replace(",", ",  "))
        # if "^^ " in text:
        #     text = text.replace("^^ ", "^^")
        # if " ^^" in text:
        #     text = text.replace(" ^^", "^^")
        text = text.replace("\n", "")
        jsonVar[i] = text
    applicableFieldsList = set(jsonVar.keys()) - set(applicableFieldsList)
    for i in applicableFieldsList:
        text = str(jsonVar[i])
        text = str(text.replace(",", " "))
        # if "^ " in text:
        #     text = text.replace("^ ", "^")
        # if " ^" in text:
        #     text = text.replace(" ^", "^")
        text = text.replace("\n", "")
        jsonVar[i] = text
    return jsonVar


# RULE 4: Where this is empty and no data, enter "<B>Not Mentioned</B>"
def rule_4(jsonVar):
    applicableFieldsList = jsonVar.keys()
    for i in applicableFieldsList:
        if jsonVar[i] == "":
            jsonVar[i] = "<B>Not Mentioned</B>"
    return jsonVar


# RULE 5: Double Space(^^) after fullstops(.), omit if fullstops is at end
def rule_5(jsonVar):
    applicableFieldsList = set(jsonVar.keys()) - set(list(["Domain Name", "Domain Registrar URL", "Expiry /Date",
                                                           "Registrant Email", "Administrative Email", "Administrative Phone",
                                                           "Technical Email", "Billing Email", "Server Name"]))
    for i in applicableFieldsList:
        text = jsonVar[i]
        fullStopFlag = False
        if text[:-1] == ".":
            text = text[:-1]
            fullStopFlag = True
        text = text.replace(".", "  ")
        if fullStopFlag:
            text = text.join(text, ".")
        # if "^^ " in text:
        #     text = text.replace("^^ ", "^^")
        # if " ^^" in text:
        #     text = text.replace(" ^^", "^^")
        text = text.replace("\n", "")
        jsonVar[i] = text
    return jsonVar


# RULE 6: Date format
def rule_6(jsonVar):
    date = str(jsonVar["Expiry /Date"])
    date = date.split("-")
    dateText = str(int(date[0]))
    superScripts = {"1": "st", "2": "nd", "3": "rd"}
    if str(int(date[0])) in superScripts.keys():
        dateText += superScripts[str(int(date[0]))]
        dateText += " "
    else:
        dateText += "th "
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
    dateText += months[int(date[1]) - 1]
    dateText = dateText + ",  " + date[2] + "."
    jsonVar["Expiry /Date"] = dateText
    return jsonVar


# RULE 8: Add Text Formatting
def rule_8(jsonVar):
    # Domain Name
    if jsonVar["Domain Name"] != "<B>Not Mentioned</B>":
        jsonVar["Domain Name"] = "<U>" + jsonVar["Domain Name"] + "<U>"
    # Administrative Email
    if jsonVar["Administrative Email"] != "<B>Not Mentioned</B>":
        jsonVar["Administrative Email"] = "<I><U>" + jsonVar["Administrative Email"]
    # Registrant Email
    if jsonVar["Registrant Email"] != "<B>Not Mentioned</B>":
        jsonVar["Registrant Email"] = "<I><U>" + jsonVar["Registrant Email"]
    # Billing Email
    if jsonVar["Billing Email"] != "<B>Not Mentioned</B>":
        jsonVar["Billing Email"] = "<I><U>" + jsonVar["Billing Email"]
    # Server Name
    if jsonVar["Server Name"] != "<B>Not Mentioned</B>":
        jsonVar["Server Name"] = "<U>" + jsonVar["Server Name"] + "<U>"
    # Domain Status
    if jsonVar["Domain Status"] != "<B>Not Mentioned</B>":
        jsonVar["Domain Status"] = "<R><B>" + jsonVar["Domain Status"]
    # Technical Email
    if jsonVar["Technical Email"] != "<B>Not Mentioned</B>":
        jsonVar["Technical Email"] = "<I><U>" + jsonVar["Technical Email"]
    return jsonVar
