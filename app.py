from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import pandas as pd
import os
import time as T
s_reg=int(input("Pls Enter Starting Registration Number"))
l_reg= int(input("Pls Enter Last Registration Number (including)"))

batch=s_reg//1000000000



ses= s_reg//1000000
sem=int(input("Enter Your Semester (Eg. if 2nd Sem Enter : 2 )"))

if sem==1:
    s="I"
elif sem==2:
    s="II"
elif sem == 3:
    s = "III"
elif sem == 4:
    s = "IV"
elif sem == 5:
    s = "V"
elif sem == 6:
    s = "VI"
elif sem == 7:
    s = "VII"
elif sem == 8:
    s = "VIII"

#creating Results Folder


foldername= "Results"

if not os.path.exists(foldername):
    os.makedirs(foldername)

file_name=f"Results/{sem}th_Result_{ses}.csv"

if os.path.exists(file_name):
    os.remove(file_name)


#  experiment --->












# Experiment ->>





for r in range(s_reg,l_reg+1):

    targetUrl = f"https://results.beup.ac.in/ResultsBTech3rdSem2023_B2022Pub.aspx?Sem={s}&RegNo={r}"
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
    if  not os.path.exists(f"Results/{sem}th_Result_{ses}.csv"):
        df.to_csv(f"Results/{sem}th_Result_{ses}.csv",index=False)
    else:
        df.to_csv(f"Results/{sem}th_Result_{ses}.csv",mode='a',header=False,index=False)

    print(name, reg, sgpa, cgpa)
    # T.sleep(2)


