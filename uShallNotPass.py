#init

import os
import json
from random import randint
from pathlib import Path

from ency import AESCipher

lows = "abcdefghijklmnopqrstuvwxyz"
caps = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
nums = "0123456789"
syms = "!\"£$%^&*()_+-=#~'@;:/?.>,<[}]{`¬\|"

dat = {}
fDat = Path("Data.json")
enC = Path("enc.j")
tempp = Path("temp.t")
pas = ""
#define funcs

def maine():
    updateDat()
    clr()
    print ('Enter number to proceed.')
    print("========================")
    print ('1 : Search Passwords')
    print ('2 : View All')
    print ('3 : Edit Data')
    print ('4 : Generate New')
    print ('5 : Change Password')
    print("========================")
    print("or enter exit")

    func = input("--> ")

    if(func == "1"):
        search = input("Please enter your search term --> ")
        if search == "":
            print("Please enter a search term..")
            input("Press enter to return to main menu..")
            maine()
        else:
            tos = input("Enter search type\n========================\n1 : Search names only\n2 : Search passwords only\n3 : Search names and passwords\n========================\n--> ")
            if tos == "":
                input("Please enter search type\nPress enter to return to main menu..")
            else:
                searchPass(search, tos)
    elif(func == "2"):
        viewAll()
    elif(func == "3"):
        editDat()
    elif(func == "4"):
        GenInit()
    elif(func == "5"):
        changePass()
    elif (func == "exit"):
        clr()
        closeSecurely()
    else:
        print ("Please choose a function..")
        input("Press enter to return to main menu..")
        maine()
def changePass():
    global pas
    clr()
    print("Type new password for database")
    pas = input("--> ")
    print("Next time you close, the database will be packed away with your new password")
    print("Dont forget it..")
    input("Press enter to return to main menu..")
    maine()
def closeSecurely():
    if fDat.exists():
        packDat(fDat, enC, pas)
        deleteDat(fDat)
    quit()

def deleteDat(filly):
    os.remove(filly)

def clr():
    os.system('cls' if os.name == 'nt' else 'clear')

def showAll(i = 0, list = {}):
    if(list == {}):
        global dat
        list = dat
        if(i > 0):
            dat = read(fDat)
    clr()

    print("Name\t\t:\t\tPassword")
    print("================================================")
    for i in list:
        if len(i) > 7:
            print("{}\t:\t\t{}".format(i,list[i]))
        else:
            print("{}\t\t:\t\t{}".format(i,list[i]))

    print("================================================")

def searchPass(s, tos):
    clr()
    global dat
    updateDat()
    print("Searching for \"" + s + "\" ...")
    res = {}
    print (tos)
    for entry in dat:
        nme = str(entry)
        pas = str(dat[entry])

        if tos == "1":
            if s in nme:
                res[nme] = pas
        elif tos == "2":
            if s in pas:
                res[nme] = pas
        else:
            if s in nme:
                res[nme] = pas
            elif s in pas:
                res[nme] = pas

    if len(res) == 0:
        print("Nothing found.")
    else:
        showAll(0, res)

    input("Press enter to return to main menu..")
    maine()

def viewAll():
    showAll(1)

    print("")
    print("enter e to edit values")
    print("Press enter to return to main menu..")
    wag1 = input("--> ")
    if(wag1 == "e"):
        editDat()
    else:
        maine()

def editDat():
    clr()
    showAll(0)
    print ('Enter number to proceed.')
    print("========================")
    print ('1 : Edit or create new entry')
    print ('2 : Delete Entry')
    print ('3 : Rename Entry')
    print ('4 : Wipe Data')
    print ('5 : Save Data')
    print ('6 : Return to main menu')
    print("========================")

    func = input("--> ")

    if(func == "1"):
        print("Please enter a name")
        nme = input("--> ")
        print("Please enter password")
        passs = input("--> ")
        global dat
        if len(dat) < 1:
            dat = {

            }
        dat[nme] = passs
        print(nme + " added successfuly")
        input("Press enter to return to Edit menu")
        editDat()
    elif(func == "2"):
        print("Enter item name to delete")
        dd = input("--> ")
        print("Are you sure you want to delete password named " + dd + " ?  (y/n)")
        conf = input("--> ")
        if (conf == "y"):
            dat.pop(dd, None)
            print(dd + " Deleted")
        input("Press enter to return to Edit menu")
        editDat()
    elif(func == "3"):
        print("Enter item to rename")
        key = input("--> ")
        print("Enter new name for \"" + key + "\"")
        newNme = input("--> ")

        print("Are you sure you want to rename \"" + key + "\" to \"" + newNme + "\" (y/n)")
        conf = input("--> ")
        if (conf == "y"):
            dat[newNme] = dat.pop(key, None)
            print(key + " renamed to " + newNme)
        input("Press enter to return to Edit menu")
        editDat()
    elif(func == "4"):
        print("Are you sure you want to wipe all data ?(y/n)")
        conf = input("--> ")
        if (conf == "y"):
            print("Are you sure you\'re sure?(y/n)")
            conf = input("--> ")
            if (conf == "y"):
                print("Wiping...")
                wipe(fDat)
                wipe(enC)
                print("Done Wiping")
        input("Press enter to return to Edit menu")
        editDat()
    elif(func == "5"):
        print("Saving Data...")
        saveDat()
        print("Data saved successfuly")
        input("Press enter to return to Edit menu")
        editDat()
    elif(func == "6"):
        maine()
    elif (func == "exit"):
        clr()
        closeSecurely()
    else:
        print ("Please choose a function..")
        input("Press enter to return to main menu..")
        maine()

def saveDat():
    global dat
    write(dat, fDat)
    updateDat()

def updateDat():
    global dat
    dat = read(fDat)

def wipe(filly):

    try:
        temp = readByt(filly)
        lenny = len(temp)-1

        i=0
        res = ""
        while i < lenny:
            res = res + "0"
            i = i+1

            j = 0
            while j < 32:
                write(res, filly)
                write("", filly)
                j = j + 1

        deleteDat(filly)
    except Exception as e:
        pass

    updateDat()


def GenInit():
    clr()
    pLen = input ("Enter a password length --> ")
    stronkth = input ("Enter strength w(1-5)s --> ")

    if(stronkth == "1"):
        chars = lows
    elif(stronkth == "2"):
        chars = lows + caps
    elif(stronkth == "3"):
        chars = lows + caps + nums
    elif(stronkth == "4"):
        chars = lows + caps + nums + syms
    elif(stronkth == "5"):
        chars = lows + caps + nums + syms
    else:
        print("Unknown strength value")
        input("Press enter to return to main menu..")
        maine()

    Gen(chars, pLen, stronkth)

def Gen(chars, pLen, stronkth):

    lenny = len(chars) -1
    i = 0
    res = ""

    print ("Generating password...")

    while (i < int(pLen)):
        x = randint(0, lenny)
        res += chars[x]
        i = i + 1

    print ("Done.")
    print("Password Displayed Below -->")
    print("")
    print(res)
    print("")
    print ('Enter character to proceed.')
    print("========================")
    print ('1 : ReGen')
    print ('2 : Gen Menu')
    print ('3 : Main Menu')
    print ('s : Save Password')
    print("========================")

    func = input("--> ")

    if(func == "1"):
        Gen(chars, pLen, stronkth)
    elif(func == "2"):
        GenInit()
    elif(func == "3"):
        maine()
    elif(func == "s"):
        print ("Save current (c) password or other ? (o)")
        cORo = input("--> ")
        if(cORo == "c"):
            print("Please enter name for password")
            nme = input("--> ")
            savePass(nme, res)
            print ("Password added successfuly")
            input ("Press enter to return to main menu..")
            maine()
        elif(cORo == "o"):
            print("Please enter name for password")
            nme = input("--> ")
            print ("Please input password to save")
            passs = input("--> ")
            savePass(nme, passs)
            print ("Password added successfuly")
            input ("Press enter to return to main menu..")
            maine()
        else:
            print("Please enter name for password")
            nme = input("--> ")
            savePass(nme, res)
            print ("Password added successfuly")
            input ("Press enter to return to main menu..")
            maine()
    else:
        print ("Please choose a function..")
        input("Press enter to return to main menu..")
        maine()

def read(filly):
    try:
        with open(filly) as json_data:
            res = json.load(json_data)
        return res
    except Exception as e:
        pass
    return ""
def write(dat, filly):
    with open(filly, 'w') as outfile:
        json.dump(dat, outfile)
def writeByt(dat, filly):
    with open(filly, "wb") as f:
        f.write(dat)
def readByt(filly):
    with open(filly, "rb") as f:
        res = f.read()
    return res


def savePass(nme, passs):
    res = {
        nme : passs
    }

    if fDat.exists():
        dat = read(fDat)
        if(len(dat) > 0):
            dat[nme] = passs
            write(dat, fDat)
        else:
            write(res, fDat)
    else:
        write(res, fDat)


def packDat(filly, out, pas):
    data = readByt(filly)
    dave = AESCipher(pas)
    encd = dave.encrypt(data)
    writeByt(encd, out)

def unpackDat(filly, out, pas):
    data = readByt(filly)
    dave = AESCipher(pas)
    dencd = dave.decrypt(data)
    dencd = dencd.encode()
    writeByt(dencd, out)

#run
def __init__():
    global pas
    clr()
    print("Enter Database Password")
    pas = input("--> ")
    if enC.exists():
        unpackDat(enC, fDat, pas)
    if not fDat.exists():
        with open(fDat, "w") as f:
            f.write("")




__init__()
maine()
closeSecurely()
