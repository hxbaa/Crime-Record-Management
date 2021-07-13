from sqlite3.dbapi2 import Date, connect
import pandas as pd
import matplotlib.pyplot as plt
import time
import sys
import sqlite3
from datetime import datetime
import random

from pandas.core import accessor

pd.options.mode.chained_assignment = None
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 5000)

mydb = sqlite3.connect("db.sql")
mycursor = mydb.cursor()


def print_command(Number, Message):
    print("\n", "="*Number, Message.upper(), "="*Number, "\n")


def login():
    while True:
        print_command(10, "LOGIN")
        query = "select username,password from users"
        mycursor.execute(query)
        res = mycursor.fetchall()
        response = []
        temp = []
        for i in res:
            for j in i:
                temp.append(j)
            response.append(temp)
            temp = []

        UserName = input("ENTER USERNAME: ")
        Password = input("ENTER PASSWORD: ")
        check = [UserName, Password]
        if check in response:
            print_command(5, "LOGIN successfull")
            break
        else:
            print_command(5, "Login FAILED")
    while True:
        main()


def main():
    print("="*10, "MAIN MENU", "="*10, "\n")
    print("OPTION 1: ADD CRIME RECORD")
    print("OPTION 2: MODIFY CRIME RECORD")
    print("OPTION 3: VIEW CRIME RECORDS")
    print("OPTION 4: ADD OFFENCE TYPE")
    print("OPTION 5: MODIFY OFFENCE TYPE")
    print("OPTION 6: VIEW OFFENCE TYPES")
    print("OPTION 7: VISUAL ANALYSIS")
    print("OPTION 8: CLOSE APPLICATION")
    temp = [1, 2, 3, 4, 5, 6, 7, 8]
    while True:
        response = input("\nENTER OPTION: ")
        try:
            response = int(response)
            if response in temp:
                break
            else:
                print_command(5, "ENTER VALID OPTION")

        except Exception:
            continue

    if response == 1:
        AddCrimeRec()
    elif response == 2:
        ModifyCrimeRec()
    elif response == 3:
        ViewCrimeRec()
    elif response == 4:
        AddOffenceType()
    elif response == 5:
        ModifyOffenceType()
    elif response == 6:
        ViewOffenceTypes()
    elif response == 7:
        DataVisualization()
    elif response == 8:
        sys.exit()


def AddCrimeRec():
    print_command(10, "ADD CRIME RECORD")
    query = "select RecNo from CrimeRecords"
    mycursor.execute(query)
    res = mycursor.fetchall()
    RecNos = []
    for i in res:
        for j in i:
            RecNos.append(str(j))

    query = "select OffenceNo from OffenceType"
    mycursor.execute(query)
    res = mycursor.fetchall()
    OffenceNos = []
    for i in res:
        for j in i:
            OffenceNos.append(str(j))

    while True:
        NewRecNo = random.randint(1000, 9999)
        if NewRecNo not in RecNos:
            NewRecNo = NewRecNo
            break
        else:
            continue

    CurrentDate = str(datetime.now())[0:10]
    query = "select * from OffenceType"
    mycursor.execute(query)
    res = mycursor.fetchall()
    df = pd.DataFrame(
        res, columns=["Offence Number".upper(), "Offence Name".upper(), "IPC SECTION"])

    print(df[:-2])
    while True:

        NewOffenceNo = input("ENTER OFFENCE NUMBER: ")

        if NewOffenceNo not in OffenceNos:
            print_command(5, "OFFENCE NUMBER INVALID")
        else:
            NewOffenceNo = int(NewOffenceNo)
            break
    while True:
        Complaint = input("COMPLAINT GIVEN BY: ")
        if Complaint.strip() != "":

            Complaint = Complaint.upper()
            Complaint = Complaint.strip()
            break
        else:
            print_command(5, "ENTER A NAME")
    while True:
        Address = input("ADDRESS OF {}: ".format(Complaint))
        Address = Address.strip()
        if Address != "":
            break
        else:
            print_command(5, "ENTER A ADDRESS")
    while True:
        Phone = input("PHONE NUMBER OF {}: ".format(Complaint))
        Phone = Phone.strip()
        if Phone != "":
            break
        else:
            print_command(5, "ENTER A PHONE NUMBER")
    while True:
        AccuseName = input("Name of Accuse *If unknown press enter*: ")
        AccuseName = AccuseName.strip()
        if AccuseName != "":
            while True:
                AccuseNationality = input(
                    "Nationality of {}".format(AccuseName))
                AccuseNationality = AccuseNationality.strip()
                if AccuseNationality != "":
                    while True:
                        AccuseDob = input("DOB of {}".format(AccuseName))
                        AccuseDob = AccuseDob.strip()
                        if AccuseDob != "":
                            while True:
                                AccuseAddress = input(
                                    "Address of {}".format(AccuseName))
                                AccuseAddress = AccuseAddress.strip()
                                if AccuseAddress != "":
                                    break
                                else:
                                    print_command(5, "ENTER VALID ADDRESS")
                            break
                        else:
                            print_command(5, "Enter valid DOB")
                    break
                else:
                    print_command(5, "Enter valid Nationality")
            break
        else:
            AccuseName = AccuseDob = AccuseNationality = AccuseAddress = ""
            break

    while True:
        Status = input("STATUS (OPEN/CLOSED): ")
        if Status.lower() in ["open", "closed"]:
            Status = Status.upper()
            break
        else:
            print_command(5, "ENTER A VALID STATUS (OPEN/CLOSED)")

    LastUpdated = CurrentDate

    Notes = input("NOTES: ")
    query = "insert into CrimeRecords values({},'{}',{},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
        NewRecNo, CurrentDate, NewOffenceNo, Complaint, Address, AccuseName, AccuseNationality, AccuseDob, AccuseAddress, Phone, Status, LastUpdated, Notes)
    mycursor.execute(query)
    mydb.commit()
    pass


def ModifyCrimeRec():
    pass


def ViewCrimeRec():
    print_command(10, "VIEW CRIME RECORDS")
    print("OPTION 1: SEARCH BY RECORD NUMBER")
    print("OPTION 2: SEARCH BY OFFENCE NUMBER")
    while True:
        res = input("ENTER OPTION NUMBER: ")
        temp = [1, 2]
        try:
            res = int(res)
            if res not in temp:
                print_command(5, "Enter valid option")
            else:
                break
        except Exception:
            print_command(5, "Enter valid option")
    query = "Select * from CrimeRecords"
    mycursor.execute(query)
    data = mycursor.fetchall()

    df = pd.DataFrame(data, columns=["Record Number", "Date", "Offence", "Complaint", "Address", "Phone Number",
                                     "Accuse Name", "Accuse Nationality", "Accuse DOB", "Accuse Address", "Status", "Last Updated", "NOTES"])

    query = "select OffenceNo,OffenceName from OffenceType"
    mycursor.execute(query)
    data = mycursor.fetchall()
    old = []
    new = []
    for i in data:
        for j in range(len(i)):
            if j == 0:
                old.append(i[j])
            else:
                new.append(i[j])

    df["Offence"] = df["Offence"].replace(old, new)

    def SearchByRecNo():
        print_command(8, "Search by record number")
        while True:
            RecNo = input("Record Number: ")
            try:
                RecNo = int(RecNo)
                break
            except Exception:
                print_command(5, "ENTER VALID RECORD NUMBER")

        results = df[df["Record Number"] == RecNo]
        if results.empty:
            print_command(
                5, "NO CRIMINAL RECORD ASSOCIATED WITH RECORD NUMBER {}".format(RecNo))
        else:
            print_command(5, "CRIMINAL RECORD FOUND")
            print(results)

    def SearchByOffenceNumber(old, new, Data):
        dic = {}
        for i in range(len(old)):
            dic[old[i]] = new[i]
        print_command(8, "SEARCH BY OFFENCE NUMBER")
        query = "select * from OffenceType"
        mycursor.execute(query)
        res = mycursor.fetchall()
        df = pd.DataFrame(
            res, columns=["Offence Number".upper(), "Offence Name".upper(), "IPC SECTION"])
        print(df)
        OffenceNos = df["OFFENCE NUMBER"].values
        while True:
            OffenceNo = input("OFFENCE NUMBER: ")
            try:
                OffenceNo = int(OffenceNo)
                if OffenceNo in OffenceNos:
                    break
                else:
                    print_command(5, "ENTER VALID OFFENCE NUMBER")
            except Exception:
                print_command(5, "ENTER VALID OFFENCE NUMBER")
        ToSearch = dic[OffenceNo]
        print(ToSearch)
        result = Data[Data["Offence"] == ToSearch]
        if result.empty:
            print_command(
                5, "NO CRIMINAL RECORDS ASSOCIATED WITH {} IS FOUND".format(ToSearch))
        else:
            print_command(5, "{} CRIMINAL RECORDS FOUND".format(len(result)))
            print(result)

    if res == 1:
        SearchByRecNo()
    elif res == 2:
        SearchByOffenceNumber(old, new, df)


def AddOffenceType():
    pass


def ModifyOffenceType():
    pass


def ViewOffenceTypes():
    connection = sqlite3.connect("db.sql")
    cursor = connection.cursor()
    cursor.execute("SELECT * from OffenceType;")
    results = cursor.fetchall()
    df=pd.DataFrame(results)
    df.columns=['Offence No.','Offence Type','IPC Section']
    print(df)
    cursor.close()
    connection.close()

def DataVisualization():
    pass


if __name__ == "__main__":
    print_command(20, "CRIME RECORD MANAGEMent")
    login()
