from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

s_reg=int(input("Pls Enter Starting Registration Number"))
l_reg= int(input("Pls Enter Last Registration Number (including)"))


targetUrl = "https://results.beup.ac.in/ResultsBTech4thSem2024_B2022Pub.aspx?Sem=IV&RegNo=22105128055"

dataHtml = urlopen(targetUrl)

htmldata=dataHtml.read()

dataHtml.close()

resultSoup= soup(htmldata,'html.parser')

### here we have whole htmlPage in resultSoup
# tableData=resultSoup.find_all("table",{"class":"style1"})
# if(len(tableData)<1):
#     print("inside if")
# print(tableData)
#
# # collecting all tables
tableData=resultSoup.find_all("table",{"class":"style1"})
# going to 2nd table
table1=tableData[1]
# collecting all rows in side the table
rowData=table1.find_all("tr",{})


# 1st Row (Reg : 22XXXXXXXXX)

d=rowData[0].find_all("td",{})[1:]



# Reg no.
d_result=d[0].find_all("span",{})

reg = d_result[0].text
# 2nd Row( Student name : HXXXXX)
d=rowData[1].find_all("td",{})[1:]

#Name Of student
d_result=d[0].find_all("span",{})

name = d_result[0].text

# print(f"Name :{name}, Reg : {reg}")


#  now collecting Sgpa And Cgpa

# got the target table in tableData2
tableData2=resultSoup.find_all("table",{"id":"ContentPlaceHolder1_DataList5"})

SgpaTable=tableData2[0]

spans=SgpaTable.find_all("span",{"id":"ContentPlaceHolder1_DataList5_GROSSTHEORYTOTALLabel_0"})

d=spans[0]

# SGPA Collected and stored
sgpa= d.text


# print(sgpa)

# got the target table in tableData3
tableData3=resultSoup.find_all("table",{"id":"ContentPlaceHolder1_GridView3"})



CgpaTable=tableData3[0]

CgpaRow= CgpaTable.find_all("tr",{})[1:]

d=CgpaRow[0].find_all("td",{})
# got the cgpa
cgpa = d[-1].text



print(name,reg,sgpa,cgpa)