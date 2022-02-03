from sqlite3.dbapi2 import Date, connect
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
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

mydb = sqlite3.connect("db me.sql")
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
    crime={'Case_number':[38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69],
       'Name_of_criminal':['Aira Mella','Bobby Dutt','Cathy melbourne','Rahul Dajia','Shankar Dupia','Rohan Kauar',
                           'Shamzi Shaik','Ravi Spaghet','Simon Kallur','Rajuat Kumar','Amal Somak','Piyush Gorbhai',
                           'Faazi S','Chintu Seti','Reem Shah','Sanjay Rajma','Bunty Buoy','Vicky Tror','Aayush Khan',
                           'Louis B','Sheela Shah','Gopika Motwani','Jolly Sands','Shona Ray','Saksham Manga',
                           'Fisili Manna','Ajay Neth','Kayle Hunter','Hailey Tart','Ram Charath','Chetan Nath', 'Sinha Dopia'],
       'DOB':['28-07-1987','29-01-1970','07-09-1989','12-04-1990','03-09-1987','17-12-1985','22-09-1986','12-10-1980',
              '07-03-1981',' 22-09-1972','05-10-1985','10-09-1979','08-09-1981','05-09-1991','10-09-1986','18-09-1986',
              '22-09-1986','22-07-1986','26-08-1976','19-12-1988','22-09-1980','29-12-1976','12-01-1988','03.11.1986',
              '27-08-1986','21-02-1980','21-09-1978','09-05-1976','22-12-1976','12-11-1989','28-10-1988','02-05-1999'],
       'Natinality':['Irish',' Indian','Australian','Indian','Indian','Indian','Pakistani','American','Indian',' Indian',
                     'Indian','Indian',' Pakistani','Sri Lankan','Indian','Indian','Indian','American','Indian','American',
                     'Indian',' Indian','Irish','Indian','Indian','Australian','Indian','American','Irish','American','Indian','Indian'],
       'Offense':['Robbery','House breaking','Robbery','Smuggling','Smuggling','Robbery','Eve-teasing','Sexual assault',
                  'Murder','Robbery','Murder','Murder','Sexual Assault','Smuggling','Extortation','Molestation','Sexual Assault',
                  'House breaking','Cyber-crime','Cyber-crime',np.nan,'Extortation','Murder','Cyber-crime','House breaking',
                  np.nan,'Molestation','Murder',np.nan,'Robbery',np.nan,'Cyber-crime'],
       'Date_of_case_filed':['23-09-2017','23-09-2017','23-09-2017','23-09-2018','23.09.2017','23-02-2018','23-09-2019','24-09-2017',
                             '18-09-2019','22-05-2019',' 23-09-2017','23-09-2017','23-09-2018','23-09-2018','12-09-2018','13-09-2018',
                             '11-09-2017','08-09-2019','21-10-2018','23-10-2017','24-09-2016','12-12-2017',' 08-11-2017','09-04-2017',
                             '22.09.2017',' 23-05-2016','12-06-2015','03-07-2018','29-09-2017','19-10-2017','17-09-2016','30-09-2019'],
       'Complainant':['Karthi Wills', 'Reeja Raj', 'Rajeev Sinha', 'Shekhar Shosh', 'Shikha', 'Esha bait', 'Lanina Shok', 'Newar Singh', 
                      'Rema Sandeep', 'Sheena Bajaj', 'Rakhi Hari', 'Sanjay Sanjeev', 'Rathore Rav', 'Thenam Mapedi', 'Saona Snaja', 
                      'Sakshi Powar','Sneha Hapde', 'Kevin Roy', 'Arya Ajay', 'Arun Roy', 'Maya Seema', 'Seema Raj', 'Daisy D’Souza',
                      'Lizelle Anand', 'Kimna Jiva', 'Yousuf Zaid', 'Awez Dangar', 'Nagma Meeraj', 'Ali Zais', 'Catherine Zachariah',
                       'Sameeksha Soodna', 'Sameer Ali'],
       'Status':['Closed','Open','Open','Open','Open','Closed','Open','Closed',
                 'Closed','Closed','Closed','Open','Closed','Closed',' Closed',
                 'Closed','Open','Closed','Open','Closed','Closed','Open','Closed','Closed',
                 'Closed','Open','Open','Closed','Closed','Closed','Closed','Closed']}
    cr=pd.DataFrame(crime)
    print(cr['Offense'].unique())
    print('-----------------HOW WOULD YOU LIKE TO MODIFY CRIME RECORDS?-------------------')
    print("There are 3 operations that comes under this function:")
    print("1. Deleting index and columns")
    print("2. Renaming index and columns")
    print("3. Reindexing")
    print("\n Choose your choice:  ")
    inp=int(input())
    if inp==1:
        print('What do you want to delete?')
        print('1. Index')
        print('2. Column')
        inp2=int(input("Enter your choice:  "))
        if inp2==1:
            ind=int(input('Specify your index please'))
            cr1=cr.drop(cr.index[[ind]])
            print("row", ind, "has been successfully deleted from the crime record table")
            print(cr)
        if inp2==2:
            c1=(input("kindly name the column name that you want to delete"))
            cr2=cr.drop([c1], axis = 1, inplace = True)
            print("Your record has been modified")
    if inp==2:
        print("What would you like to RENAME?")
        print("1. index")
        print("2. column")
        inp2o2=int(input("Enter your choice:    "))
        if inp2o2==1:
            x1=input("Enter index that you wish to change:   ")
            nx1=input("ENTER YOUR NEW INDEX:   ")
            cr21=cr.reindex({x1:nx1}, axis='index', inplace=True)
            print(cr21)
        if inp2o2==2:
            cc=input("Enter column name that you want to change:  ")
            cc2=input("Enter your new column name:   ")
            ccr=cr.rename(columns={cc:cc2},inplace=True)
            print("----Column name has been successfully renamed----")
            print("Thank you!")
    if inp==3:
        print("--------------Reindexing--------------")
        x=input("Enter index that you wish to change:   ")
        nx=input("ENTER YOUR NEW INDEX:   ")
        cr3=cr.reindex({x:nx}, axis='index')
        print(cr3)





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
    connection = sqlite3.connect("db me.sql")
    cursor = connection.cursor()
    cursor.execute("SELECT * from OffenceType;")
    results = cursor.fetchall()
    df=pd.DataFrame(results)
    df.columns=['Offence No.','Offence Type','IPC Section']
    print(df)
    cursor.close()
    connection.close()

def DataVisualization():
    crime={'Case_number':[38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69],
       'Name_of_criminal':['Aira Mella','Bobby Dutt','Cathy melbourne','Rahul Dajia','Shankar Dupia','Rohan Kauar',
                           'Shamzi Shaik','Ravi Spaghet','Simon Kallur','Rajuat Kumar','Amal Somak','Piyush Gorbhai',
                           'Faazi S','Chintu Seti','Reem Shah','Sanjay Rajma','Bunty Buoy','Vicky Tror','Aayush Khan',
                           'Louis B','Sheela Shah','Gopika Motwani','Jolly Sands','Shona Ray','Saksham Manga',
                           'Fisili Manna','Ajay Neth','Kayle Hunter','Hailey Tart','Ram Charath','Chetan Nath', 'Sinha Dopia'],
       'DOB':['28-07-1987','29-01-1970','07-09-1989','12-04-1990','03-09-1987','17-12-1985','22-09-1986','12-10-1980',
              '07-03-1981',' 22-09-1972','05-10-1985','10-09-1979','08-09-1981','05-09-1991','10-09-1986','18-09-1986',
              '22-09-1986','22-07-1986','26-08-1976','19-12-1988','22-09-1980','29-12-1976','12-01-1988','03.11.1986',
              '27-08-1986','21-02-1980','21-09-1978','09-05-1976','22-12-1976','12-11-1989','28-10-1988','02-05-1999'],
       'Natinality':['Irish',' Indian','Australian','Indian','Indian','Indian','Pakistani','American','Indian',' Indian',
                     'Indian','Indian',' Pakistani','Sri Lankan','Indian','Indian','Indian','American','Indian','American',
                     'Indian',' Indian','Irish','Indian','Indian','Australian','Indian','American','Irish','American','Indian','Indian'],
       'Offense':['Robbery','House breaking','Robbery','Smuggling','Smuggling','Robbery','Eve-teasing','Sexual assault',
                  'Murder','Robbery','Murder','Murder','Sexual Assault','Smuggling','Extortation','Molestation','Sexual Assault',
                  'House breaking','Cyber-crime','Cyber-crime',np.nan,'Extortation','Murder','Cyber-crime','House breaking',
                  np.nan,'Molestation','Murder',np.nan,'Robbery',np.nan,'Cyber-crime'],
       'Date_of_case_filed':['23-09-2017','23-09-2017','23-09-2017','23-09-2018','23.09.2017','23-02-2018','23-09-2019','24-09-2017',
                             '18-09-2019','22-05-2019',' 23-09-2017','23-09-2017','23-09-2018','23-09-2018','12-09-2018','13-09-2018',
                             '11-09-2017','08-09-2019','21-10-2018','23-10-2017','24-09-2016','12-12-2017',' 08-11-2017','09-04-2017',
                             '22.09.2017',' 23-05-2016','12-06-2015','03-07-2018','29-09-2017','19-10-2017','17-09-2016','30-09-2019'],
       'Complainant':['Karthi Wills', 'Reeja Raj', 'Rajeev Sinha', 'Shekhar Shosh', 'Shikha', 'Esha bait', 'Lanina Shok', 'Newar Singh', 
                      'Rema Sandeep', 'Sheena Bajaj', 'Rakhi Hari', 'Sanjay Sanjeev', 'Rathore Rav', 'Thenam Mapedi', 'Saona Snaja', 
                      'Sakshi Powar','Sneha Hapde', 'Kevin Roy', 'Arya Ajay', 'Arun Roy', 'Maya Seema', 'Seema Raj', 'Daisy D’Souza',
                      'Lizelle Anand', 'Kimna Jiva', 'Yousuf Zaid', 'Awez Dangar', 'Nagma Meeraj', 'Ali Zais', 'Catherine Zachariah',
                       'Sameeksha Soodna', 'Sameer Ali'],
       'Status':['Closed','Open','Open','Open','Open','Closed','Open','Closed',
                 'Closed','Closed','Closed','Open','Closed','Closed',' Closed',
                 'Closed','Open','Closed','Open','Closed','Closed','Open','Closed','Closed',
                 'Closed','Open','Open','Closed','Closed','Closed','Closed','Closed']}
    cr=pd.DataFrame(crime)
    print('--------------------HOW WOULD YOU LIKE TO VIEW OFFENSE RECORD VISUALLY?--------------------------')
    print('1. Bar graph')
    print('2. Horizontal bar graph')
    enter=int(input("enter your choice"))
    b=cr['Offense'].value_counts().plot(kind='bar',color=['red', 'orange', 'blue', 'gold','green', 'yellow', 'black', 'violet']);
    plt.xlabel('Offense')
    plt.ylabel('Number of cases registered in AUGUST 2021')
    plt.show()
    print(b)



if __name__ == "__main__":
    print_command(20, "CRIME RECORD MANAGEMent")
    login()
