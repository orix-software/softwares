
from os import path
import os, sys
import pathlib

def CreateTargetFolder(dest, destetc, letter):
    folder = dest+'/'+letter
    folderdb = destetc+'/'+letter
    #print(folder)
    directory = os.path.dirname(folder)

    if not os.path.exists(folder) and folder!="":
        print("######################## Create "+folder)
        os.mkdir(folder)

    if not os.path.exists(folderdb) and folderdb!="" and destetc!="":
        # destroms,"",letter)
        print("######################## Create "+folderdb)
        os.mkdir(folderdb)

def RuleLoader(flags_software):
    # Rules for software in the launcher
    # Does the first download is an atmos mode ?
    # Yes we place it

    # Definition of FLAGS
    # A : Atmos and tape file
    # O : Oric-1 and tape file
    print("Flags ruleLoader : "+ flags_software)
    flag =""
    # Priority : Atmos
    if (flags_software.find('A') != -1 and flags_software.find('K') != -1):
        return 'A'

    if (flags_software.find('O') != -1 and flags_software.find('K') != -1):
        return 'O'

    return flag

def isOric1(flags_software):
    # rules for software in the launcher ?
    # Does the first download is an atmos mode ?
    # Yes we place it

    # Definition of FLAGS
    # A : Atmos and tape file
    # O : Oric-1 and tape file
    print("Flags ruleLoader : "+ flags_software)
    flag = ""
    if (flags_software.find('O') != -1 and flags_software.find('K') != -1):
        flag='O'
    return flag

def isAtmos(flags_software):
    # rules for software in the launcher ?
    # Does the first download is an atmos mode ?
    # Yes we place it

    # Definition of FLAGS
    # A : Atmos and tape file
    # O : Oric-1 and tape file
    print(f"Flags ruleLoader : { flags_software }")
    flag = ""
    if (flags_software.find('A') != -1 and flags_software.find('K') != -1):
        flag = 'A'
    return flag

def isOrix(flags_software):
    print("Flags ruleLoader : "+ flags_software)
    flag = ""
    if (flags_software.find('Z') != -1 ):
        flag = 'Z'
    return flag

def initFolder(dest):
    if not os.path.exists(dest):
        pathlib.Path(dest).mkdir(parents=True)

def isRom(flags_software):
    # rules for software in the launcher ?
    # Does the first download is an atmos mode ?
    # Yes we place it

    # Definition of FLAGS
    # A : Atmos and tape file
    # O : Oric-1 and tape file

    flag = ""
    if (flags_software.find('R') != -1):
        flag ='R'
        print("Is ROM : "+ flags_software)
    return flag

def getFileExtension(filename):
    return filename[-3:].lower()

def removeFrenchChars(mystr):
    mystr=mystr.replace(u'\xe1', "a") #
    mystr=mystr.replace(u'\xbf', "!") #
    mystr=mystr.replace(u'\xed', "i") #
    mystr=mystr.replace(u'\xf3', "o") #
    mystr=mystr.replace(u'\xfb', "u") # û
    mystr=mystr.replace(u'\xaa', "u")
    mystr=mystr.replace(u'\xa7', "c")
    mystr=mystr.replace(u'\xa0', u'a')
    mystr=mystr.replace(u'\xa2', u'a')
    mystr=mystr.replace(u'\xa8', u'e') # e tréma
    mystr=mystr.replace(u'\xa3', u'') # point
    mystr=mystr.replace(u'\xaf', u'e') # point
    mystr=mystr.replace(u'\xbb', u'c') # ç
    mystr=mystr.replace(u'\xb9', u'u') # ù
    mystr=mystr.replace(u'\xb4', u'o') # ù
    mystr=mystr.replace(u'\xae', "i")
    mystr=mystr.replace(u'\xeb', u'e') # e tréma lower case
    mystr=mystr.replace(u'\xe8', u'e') # è
    mystr=mystr.replace("Ã¨", "e") # è pour mystère de Kikekankoi
    mystr=mystr.replace(u"€™", "'")
    mystr=mystr.replace(u"Ã¢â‚¬â„¢", "'")
    mystr=mystr.replace("Ã©", "e")
    mystr=mystr.replace("é", "e")
    mystr=mystr.replace("ê", "e")
    mystr=mystr.replace("ë", "e")
    mystr=mystr.replace("ç", "c")
    mystr=mystr.replace("°", " ")
    mystr=mystr.replace("Â", " ")
    mystr=mystr.replace("à", "a")
    mystr=mystr.replace("â", "a")
    mystr=mystr.replace("ô", "o")
    mystr=mystr.replace("ï", "i")
    mystr=mystr.replace("î", "i")
    mystr=mystr.replace("©", "")
    mystr=mystr.replace("Ã", "e")
    mystr=mystr.replace("Â£", "£")

    return mystr
