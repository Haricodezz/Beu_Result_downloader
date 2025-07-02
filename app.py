from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import pandas as pd
import os
import time as T
s_reg=input("Pls Enter Starting Registration Number")
# l_reg= int(input("Pls Enter Last Registration Number (including)"))

batch="20"+ s_reg[:2]

s_reg= int(s_reg)


#
#
#
# ses= s_reg//1000000
sem=int(input("Enter Your Semester (Eg. if 2nd Sem Enter : 2 )"))

if sem==1:
    s="I"
    S="1st"
elif sem==2:
    s="II"
    S = "2nd"
elif sem == 3:
    s = "III"
    S = "3rd"
elif sem == 4:
    s = "IV"
    S = "4th"
elif sem == 5:
    s = "V"
    S = "5th"
elif sem == 6:
    s = "VI"
    S = "6th"
elif sem == 7:
    s = "VII"
    S = "7th"
elif sem == 8:
    s = "VIII"
    S = "8th"

#creating Results Folder


foldername= "Results"

if not os.path.exists(foldername):
    os.makedirs(foldername)

file_name=f"Results/{sem}th_Result_{batch}.csv"
if os.path.exists(file_name):
    os.remove(file_name)


#  experiment --->

homeUrl= "https://results.beup.ac.in/"

webOpen= urlopen(homeUrl)

homeHtml=webOpen.read()
webOpen.close()

homeSoup= soup(homeHtml,"html.parser")

homeTable=homeSoup.find_all('table',{})

temp=homeTable[0]

homeRow=temp.find_all('tr',{})
# print(homeRow)

def findthe_BtechRow(homeRow):
    temp= homeRow
    count=0
    while True:
        hr=temp[count]
        theRow= hr.find_all('strong',{})

        if len(theRow)==0:
            pass
        elif theRow[0].text=="B.Tech.":
            break
        count=count+1
    return count

d= findthe_BtechRow(homeRow)

# A=homeRow[d+1]
# print(A)
def takeSem(homeRow,n):
    tem = homeRow[d + n +1]
    tem2 = tem.find_all('a', {})
    tem3 = tem2[0]

    pr = tem3.text[8]
    return pr
def takeExamYear(homeRow,n):
    tem = homeRow[d + n + 1]
    tem2 = tem.find_all('a', {})
    tem3 = tem2[0]

    pr = tem3.text[-4:]
    return pr





# print(pr)

totalrow= len(homeRow)

def takeBatch(homeRow,n):
    temp = homeRow[d +n+ 1]
    temp2 = temp.find_all('td', {})
    temp3 = temp2[1]
    pr = temp3.text[-7:-3]
    return pr





btech_result = dict()


for i in range(totalrow-d):
    if d + i + 1 >= totalrow:
        break
    Sem=takeSem(homeRow,i)
    examYear=takeExamYear(homeRow,i)
    CBatch=takeBatch(homeRow,i)

    key_tuple= (Sem,CBatch)

    btech_result[key_tuple]=examYear


sem=str(sem)
yearOfExam= btech_result[(sem,batch)]







# Experiment ->>




for r in range(s_reg,s_reg+65):


    if sem== 8:
         targetUrl= f"https://results.beup.ac.in/ResultsBTech8thSem{yearOfExam}Pub.aspx?Sem={s}&RegNo={r}"
    else :
         targetUrl = f"https://results.beup.ac.in/ResultsBTech{S}Sem{yearOfExam}_B{batch}Pub.aspx?Sem={s}&RegNo={r}"
# 'https://results.beup.ac.in/ResultsBTech3rdSem2023_B2022Pub.aspx?Sem=III&RegNo=22105128054'

    dataHtml = urlopen(targetUrl)

    htmldata = dataHtml.read()

    dataHtml.close()


    resultSoup = soup(htmldata, 'html.parser')

    ### here we have whole htmlPage in resultSoup

    # tableData=resultSoup.find_all("table",{"class":"style1"})
    # if(len(tableData)<1):
    #     print("inside if")
    # print(tableData)
    #
    # # collecting all tables
    tableData = resultSoup.find_all("table", {"class": "style1"})
    if (len(tableData) < 1):
     continue
    # going to 2nd table
    table1 = tableData[1]
    # collecting all rows in side the table
    rowData = table1.find_all("tr", {})

    # 1st Row (Reg : 22XXXXXXXXX)

    d = rowData[0].find_all("td", {})[1:]

    # Reg no.
    d_result = d[0].find_all("span", {})

    reg = d_result[0].text
    # 2nd Row( Student name : HXXXXX)
    d = rowData[1].find_all("td", {})[1:]

    # Name Of student
    d_result = d[0].find_all("span", {})

    name = d_result[0].text

    # print(f"Name :{name}, Reg : {reg}")

    #  now collecting Sgpa And Cgpa

    # got the target table in tableData2
    tableData2 = resultSoup.find_all("table", {"id": "ContentPlaceHolder1_DataList5"})

    SgpaTable = tableData2[0]

    spans = SgpaTable.find_all("span", {"id": "ContentPlaceHolder1_DataList5_GROSSTHEORYTOTALLabel_0"})

    d = spans[0]

    # SGPA Collected and stored
    sgpa = d.text

    # print(sgpa)

    # got the target table in tableData3
    tableData3 = resultSoup.find_all("table", {"id": "ContentPlaceHolder1_GridView3"})

    CgpaTable = tableData3[0]

    CgpaRow = CgpaTable.find_all("tr", {})[1:]

    d = CgpaRow[0].find_all("td", {})
    # got the cgpa
    cgpa = d[-1].text
    #capturing the data in Dictionary

    data = {"Name": name,"Registraion No." : reg,"SGPA":sgpa,"CGPA":cgpa}

    # convert to DataFrame
    df=pd.DataFrame([data])

    # check if file exists then append the data else create file
    if  not os.path.exists(f"Results/{sem}th_Result_{batch}.csv"):
        df.to_csv(f"Results/{sem}th_Result_{batch}.csv",index=False)
    else:
        df.to_csv(f"Results/{sem}th_Result_{batch}.csv",mode='a',header=False,index=False)

    print(name, reg, sgpa, cgpa)
    # T.sleep(2)




# Now Loop for LE students

s_reg=s_reg+1000000900
for r in range(s_reg, s_reg + 10):

    targetUrl = f"https://results.beup.ac.in/ResultsBTech{S}Sem{yearOfExam}_B{batch}Pub.aspx?Sem={s}&RegNo={r}"
    # 'https://results.beup.ac.in/ResultsBTech3rdSem2023_B2022Pub.aspx?Sem=III&RegNo=22105128054'

    dataHtml = urlopen(targetUrl)

    htmldata = dataHtml.read()

    dataHtml.close()

    resultSoup = soup(htmldata, 'html.parser')

    ### here we have whole htmlPage in resultSoup

    # tableData=resultSoup.find_all("table",{"class":"style1"})
    # if(len(tableData)<1):
    #     print("inside if")
    # print(tableData)
    #
    # # collecting all tables
    tableData = resultSoup.find_all("table", {"class": "style1"})
    if (len(tableData) < 1):
        continue
    # going to 2nd table
    table1 = tableData[1]
    # collecting all rows in side the table
    rowData = table1.find_all("tr", {})

    # 1st Row (Reg : 22XXXXXXXXX)

    d = rowData[0].find_all("td", {})[1:]

    # Reg no.
    d_result = d[0].find_all("span", {})

    reg = d_result[0].text
    # 2nd Row( Student name : HXXXXX)
    d = rowData[1].find_all("td", {})[1:]

    # Name Of student
    d_result = d[0].find_all("span", {})

    name = d_result[0].text

    # print(f"Name :{name}, Reg : {reg}")

    #  now collecting Sgpa And Cgpa

    # got the target table in tableData2
    tableData2 = resultSoup.find_all("table", {"id": "ContentPlaceHolder1_DataList5"})

    SgpaTable = tableData2[0]

    spans = SgpaTable.find_all("span", {"id": "ContentPlaceHolder1_DataList5_GROSSTHEORYTOTALLabel_0"})

    d = spans[0]

    # SGPA Collected and stored
    sgpa = d.text

    # print(sgpa)

    # got the target table in tableData3
    tableData3 = resultSoup.find_all("table", {"id": "ContentPlaceHolder1_GridView3"})

    CgpaTable = tableData3[0]

    CgpaRow = CgpaTable.find_all("tr", {})[1:]

    d = CgpaRow[0].find_all("td", {})
    # got the cgpa
    cgpa = d[-1].text
    # capturing the data in Dictionary

    data = {"Name": name, "Registraion No.": reg, "SGPA": sgpa, "CGPA": cgpa}

    # convert to DataFrame
    df = pd.DataFrame([data])

    # check if file exists then append the data else create file
    if not os.path.exists(f"Results/{sem}th_Result_{batch}.csv"):
        df.to_csv(f"Results/{sem}th_Result_{batch}.csv", index=False)
    else:
        df.to_csv(f"Results/{sem}th_Result_{batch}.csv", mode='a', header=False, index=False)

    print(name, reg, sgpa, cgpa)
    # T.sleep(2)




