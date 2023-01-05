# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 18:14:58 2022

@author: andre
"""

import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
#import seaborn as sns
from collections import defaultdict
from collections import Counter
import heapq
from pandas.plotting import table

#plt.rcParams['font.serif'] = "Georgia"
#plt.rcParams["font.family"] = "serif"

### import data, choose stata file type (.dta) as download from ARDA
### data found at https://www.thearda.com/data-archive/browse-categories?cid=B-B#B-B
### under U.S. Church Membership Data section


subfoldername = "countydata"

##Note: 1952 data does not have adherents! Have commented out, but
##can add back in by putting it back in "todo_list1" below
data52 = pd.read_stata(subfoldername + '/'+ '1952.dta')
data52.name = '1952'
#labels52iterator = pd.read_stata('1952.dta', iterator = True)
#labels52 = labels52iterator.variable_labels()

data71 = pd.read_stata(subfoldername + '/'+ '1971.dta')
data71.name = '1971'
labels71iterator = pd.read_stata(subfoldername + '/'+ '1971.dta', iterator = True)
labels71 = labels71iterator.variable_labels()

data80 = pd.read_stata(subfoldername + '/'+ '1980.dta')
data80.name = '1980'
labels80iterator = pd.read_stata(subfoldername + '/'+ '1980.dta', iterator = True)
labels80 = labels80iterator.variable_labels()

data90 = pd.read_stata(subfoldername + '/'+ '1990.dta')
data90.name = '1990'
labels90iterator = pd.read_stata(subfoldername + '/'+ '1990.dta', iterator = True)
labels90 = labels90iterator.variable_labels()

data2000 = pd.read_stata(subfoldername + '/'+ '2000.dta')
data2000.name = '2000'
labels2000iterator = pd.read_stata(subfoldername + '/'+ '2000.dta', iterator = True)
labels2000 = labels2000iterator.variable_labels()

data2010 = pd.read_stata(subfoldername + '/' + '2010.dta')
data2010.name = '2010'
labels2010iterator = pd.read_stata(subfoldername + '/'+ '2010.dta', iterator = True)
labels2010 = labels2010iterator.variable_labels()

data2020 = pd.read_excel('countydata/2020USRC_CountyData.xlsx')
data2020.name = '2020'
#### 2020 data cleaned separately
#### pre-cleaned and 
#### formatted in the form of identifier--congregation name in Excel file
### Apostolic Christian Church Nazarene conferences combined and 
### Nazarene -> Nazarean
newnames2020 = {}
for column in data2020.keys():
    colsplit = column.split("--")
    
    if len(colsplit) > 1:
        key = colsplit[1].title()
        key = key.replace(".", "")
        key = key.replace(",", "")
        key = key.replace("-", "")
        key = key.replace("(", "")
        key = key.replace(")", "")
        key = key.replace("Usa", "USA")
        key = key.replace("\'", "")        
        key = key.strip()
        newnames2020[column] = key + colsplit[0]
        
    else:
        newnames2020[column] = column

data2020.rename(columns = newnames2020, inplace = True)

### Add years to all dataframe data!
# Create a column dataframe with the year for concatenation
# Not sure how to do it in one line so here's a bodge job
# Usual setting method causes Dataframe fragmentation error,
#e.g. directly using data52["Year"] = 1952 -> fragmented dataframe
year52 = data52[['stcode']].copy()
year52.columns = ["Year"]
year71 = data71[['name']].copy()
year71.columns = ["Year"]
year80 = data80[['state']].copy()
year80.columns = ["Year"]
year90 = data90[['state']].copy()
year90.columns = ["Year"]
year2000 = data2000[['totcg']].copy()
year2000.columns = ["Year"]
year2010 = data2010[['totcng']].copy()
year2010.columns = ["Year"]
year2020 = data2020[['State Name']].copy()
year2020.columns = ["Year"]

year52["Year"] = 1952
year71["Year"] = 1971
year80["Year"] = 1980
year90["Year"] = 1990
year2000["Year"] = 2000
year2010["Year"] = 2010
year2020["Year"] = 2020

data52 = pd.concat((data52,year52),axis=1)
data71 = pd.concat((data71,year71),axis=1)
data80 = pd.concat((data80,year80),axis=1)
data90 = pd.concat((data90,year90),axis=1)
data2000 = pd.concat((data2000,year2000),axis=1)
data2010 = pd.concat((data2010,year2010),axis=1)
data2020 = pd.concat((data2020,year2020),axis=1)


### 1971 - 1990 data are missing state name and only have state code! We make a new
### state name column based on the state code
statecodeconversion = {
    1 : "Alabama",
    2 : "Alaska",
    4 : "Arizona",
    5 : "Arkansas",
    6 : "California",
    8 : "Colorado",
    9 : "Connecticut",
    10 : "Delaware",
    11 : "District of Columbia",
    12 : "Florida",
    13 : "Georgia",
    15 : "Hawaii",
    16 : "Idaho",
    17 : "Illinois",
    18 : "Indiana",
    19 : "Iowa",
    20 : "Kansas",
    21 : "Kentucky",
    22 : "Louisiana",
    23 : "Maine",
    24 : "Maryland",
    25 : "Massachusetts",
    26 : "Michigan",
    27 : "Minnesota",
    28 : "Mississippi",
    29 : "Missouri",
    30 : "Montana",
    31 : "Nebraska",
    32 : "Nevada",
    33 : "New Hampshire",
    34 : "New Jersey",
    35 : "New Mexico",
    36 : "New York",
    37 : "North Carolina",
    38 : "North Dakota",
    39 : "Ohio",
    40 : "Oklahoma",
    41 : "Oregon",
    42 : "Pennslyvania",
    44 : "Rhode Island",
    45 : "South Carolina",
    46 : "South Dakota",
    47 : "Tennessee",
    48 : "Texas",
    49 : "Utah",
    50 : "Vermont",
    51 : "Virginia",
    53 : "Washington",
    54 : "West Virginia",
    55 : "Wisconsin",
    56 : "Wyoming"
    }

data71.state.replace(to_replace = statecodeconversion, inplace = True)
data71.rename(columns={ 'state':'State Name'}, inplace = True)
del labels71['state']

data80.state.replace(to_replace = statecodeconversion, inplace = True)
data80.rename(columns={ 'state':'State Name'}, inplace = True)
del labels80['state']

data90.state.replace(to_replace = statecodeconversion, inplace = True)
data90.rename(columns={ 'state':'State Name'}, inplace = True)
del labels90['state']


#### List of all dataframes we'll be using!
dataframes = [data71, data80, data90, data2000, data2010, data2020] #, data52]

#### key will be the label description (all uppercase), values will be the various names used,
#### e.g. {"STATE NAME" : [name, statena]} etc.
#set would be better than list for cleanedvariables, but we want to verify
#that nothing went missing
cleanedlabels = defaultdict(list)

for column in data2020.keys():
    cleanedlabels[column].append(column)
 
### Hand replace errors - labels only go to 80 characters so some need manual fixing
### takes out of dictionary, then appends it separately to cleanedlabels and replacement

## 1971
del labels71["totpop"]
cleanedlabels["Total Population"].append("totpop")
del labels71["totmem"]
cleanedlabels["Total Members"].append("totmem")
del labels71["totadh"]
cleanedlabels["Total Adherents"].append("totadh")
del labels71["chtotal"]
cleanedlabels["Total Number of Churches"].append("chtotal")
del labels71["county"]
cleanedlabels["County Code"].append("county")
del labels71["name"]
cleanedlabels["County Name"].append("name")



## 1980
del labels80["totpop"]
cleanedlabels["Total Population"].append("totpop")
del labels80["NOCTOT80"]
cleanedlabels["Total Number of Churches"].append("NOCTOT80")
del labels80["MEMTOT80"]
cleanedlabels["Total Members"].append("MEMTOT80")
del labels80["ADHTOT80"]
cleanedlabels["Total Adherents"].append("ADHTOT80")
del labels80["county"]
cleanedlabels["County Code"].append("county")
del labels80["name"]
cleanedlabels["County Name"].append("name")

## 1990
del labels90["totpop"]
cleanedlabels["Total Population"].append("totpop")
del labels90["chtotal"]
cleanedlabels["Total Number of Churches"].append("chtotal")
del labels90["totmem"]
cleanedlabels["Total Members"].append("totmem")
del labels90["totadh"]
cleanedlabels["Total Adherents"].append("totadh")
del labels90["county"]
cleanedlabels["County Code"].append("county")
del labels90["name"]
cleanedlabels["County Name"].append("name")

## 2000
#label is "Total Popolation (2000)", code is "POP200", what is happening?
del labels2000["POP200"]
cleanedlabels["Total Population"].append("POP200")
del labels2000["totcg"]
cleanedlabels["Total Number of Churches"].append("totcg")
del labels2000["totad"]
cleanedlabels["Total Adherents"].append("totad")
del labels2000["totrt"]
cleanedlabels["Total Rate of Adherence"].append("totrt")
del labels2000["ctycod"]
cleanedlabels["County Code"].append("ctycod")
del labels2000["county"]
#county name manually changed in dataframe at bottom,
#since County was County Name in 2000 but County Code in all other years



## 2010
del labels2010["POP2010"]
cleanedlabels["Total Population"].append("POP2010")
del labels2010["totcng"]
cleanedlabels["Total Number of Churches"].append("totcng")
del labels2010["totadh"]
cleanedlabels["Total Adherents"].append("totadh")
del labels2010["totrate"]
cleanedlabels["Total Rate of Adherence"].append("totrate")
del labels2010["cntycode"]
cleanedlabels["County Code"].append("cntycode")
del labels2010["cntyname"]
cleanedlabels["County Name"].append("cntyname")

# Note: 2020 cleaned in Excel

#other labels
#label entered with a typo, only 1 dash :(
del labels2000["frlutcg"]
cleanedlabels["Association of Free Lutheran Congregations_c"].append("frlutcg")

del labels2000["frlutad"]
cleanedlabels["Association of Free Lutheran Congregations_a"].append("frlutad")


# in 1980, BMAA_A = BAPTIST GENERAL CONFERENCE Number of Adherents
# and BMA_A = BAPTIST MISSIONARY ASSOCIATION OF AMERICA  Number of Adherents
# but in 1990,BMAA_A = BAPTIST MISSIONARY ASSOCIATION OF AMERICA Number of Adherents
# and BAPTGC_A = BAPTIST GENERAL CONFERENCE Number of Adherents
# Not sure why this was done...
#will have to be manuall added back in later
del labels90["BAPTGC_A"]
del labels90["BAPTGC_C"]
del labels90["BAPTGC_M"]
del labels90["BMAA_A"]
del labels90["BMAA_C"]
del labels90["BMAA_M"]

# same with CGGC between 1980 and 1990
del labels90["CGGC_M"]
del labels90["CGGC_C"]
del labels90["CGGC_A"]

# same with ROMORT between 1980 and 1990
del labels90["ROMORT_M"]
del labels90["ROMORT_C"]
del labels90["ROMORT_A"]


# del labels2000["cccadrt"]
# cleanedlabels["Congregational Christian Churches appenditional Not In Any Ccc Body_roa"].append("cccadrt")

# del labels2000["cccadcg"]
# cleanedlabels["Congregational Christian Churches appenditional Not In Any Ccc Body_c"].append("cccadcg")

# del labels2000["cccadad"]
# cleanedlabels["Congregational Christian Churches appenditional Not In Any Ccc Body_a"].append("cccadad")

del labels2000["gsixbcg"]
cleanedlabels["General Six Principle Baptists_c"].append("gsixbcg")

del labels2000["gsixbad"]
cleanedlabels["General Six Principle Baptists_a"].append("gsixbad")

# del labels2000["gsixbrt"]
# cleanedlabels["General Six Principle Baptists_roa"].append("gsixbrt")

# del labels2000["groracg"]
# cleanedlabels["Greek Orthodox Archdiocese Of America_c"].append("groracg")

# del labels2000["intfbrt"]
# cleanedlabels["Interstate And Foreign Landmark Missionary Baptist Association_roa"].append("intfbrt")


#### Known documented issues here

#Metropolitan community Churches, Universal Fellowship - p is cut off due to 
#label max limit of 80 characters, from 1980
#Number of Adherents (1980)--METROPOLITAN COMMUNITY CHURCHES, UNIVERSAL FELLOWSHI

#Moravian Church northern and southern provinces kept apart

#Some are renamed but not caught, in the format of The A of the B C vs 
# B C, The A of the
# -- Mostly fixed

# Presbyterian church merges between 1980 and 1990 - should we merge its
# 2 components in 1972 also?
# Presbyterian chruch in the United States merged with Presbyterian Church in the U.S.A.

#Mennonite church merged in 2002 with General Conference Mennonite Church to make
#Mennonite Church USA


todo_list1 = [labels71, labels80, labels90] #, labels52]
###append from 1971, 1980, 1990
for data in todo_list1:
    for varname in data:
        label = data[varname]
        
        label_list = label.split("--")
        #identify if it is church or adherents or member
        temp = label_list[0].split(" ")
        identifier = ""
        
        if len(temp) == 4:
            if temp[2].lower() == "members":
                identifier = "_m"
            
            elif temp[2].lower() == "adherents":
                identifier = "_a"
            
            elif temp[2].lower() == "churches":
                identifier = "_c"
            
            else:
                print("Warning! Unidentified pattern below:")
                print(label)
            
        else:
            #print("Caution! Below should not be a congregation:")
            #print(label_list)
            pass
        
        #format key
        key = ""
        if len(label_list) == 1:
            key = label_list[0].title()
        
        else:   
            key = label_list[1].title()
            
        key += identifier
        
        #gets rid of things like U.S.A. vs USA,
        #Church of God, Memmonite vs Church of God (Memmonite)
        key = key.replace(".", "")
        key = key.replace(",", "")
        key = key.replace("-", "")
        key = key.replace("(", "")
        key = key.replace(")", "")
        key = key.replace("Usa", "USA")
        key = key.replace("\'", "")        
        key = key.strip() 
        
        cleanedlabels[key].append(varname)


        
todo_list2 = [labels2000, labels2010]
###append from 2000, 2010

for data in todo_list2:
    for varname in data:
        label = data[varname]
        
        label_list = label.split("--")
        #identify if it is church or adherents or member
        identifier = ""              
        
        temp = ""

        #this case for most congregations; if label_list is len 1 it is not a 
        #church
        if len(label_list) == 2:
            temp = label_list[1].split(" ")
        
        #this case is only for Moravian Church
        elif len(label_list) == 3:
            temp = label_list[2].split(" ")
            
        if len(temp) >= 2:
            #for Evangelical Denominations in 2000
            if temp[1] == "Adherents":
                identifier = "_a"
        
        if len(temp) >= 3:
            if temp[2] == "adherence":
                identifier = "_roa"
            
            elif temp[2] == "Adherents":
                identifier = "_a"
            
            elif temp[2] == "adherents":
                identifier = "_a"
                
            #typo for Muslim Estimate in 2000
            elif temp[2] == "aherence":
                identifier = "_roa"
                
            #typo for Duck River and Kindred Baptists Associations in 2000
            elif temp[2] == "populations":
                identifier = "_roa"
            
            elif temp[2] == "Congregations":
                identifier = "_c"
            
            #typo for Armenian Apostolic Church in 2000
            elif temp[2] == "Congregatoins":
                identifier = "_c"
        
        if len(temp) >= 4:
            if temp[3] == "adherence":
                identifier = "_roa"
            
            elif temp[3] == "Adherents":
                identifier = "_a"
            
            elif temp[3] == "adherents":
                identifier = "_a"
            
            elif temp[3] == "congregations":
                identifier = "_c"

            elif temp[3] == "Congregations":
                identifier = "_c"
                
            elif temp[3].lower()[:2] == "co":
                identifier = "_c"
                
            elif temp[3].lower()[:2] == "ad":
                identifier = "_a"

        # if identifier == "":
        #     print("Caution! Below should not be a congregation:")
        #     print(label_list)
                    
        else:
            #print("Caution! Below should not be a congregation:")
            #print(label_list)
            pass
        
        #format key
        key = label_list[0].title()
                  
        ## Moravian Church needs special attention since it is formatted with two --
        ## Note : Moravian Church also hand-cleaned in Excel file!
        if len(label_list) == 3:
            moravian = label_list[0] + label_list[1]
            
            if moravian == "Moravian Church in AmericaAlaska Province":
                key = "Moravian Church in America Alaska Province"
            elif moravian == "Moravian Church in AmericaNorthern Province":
                key = "Moravian Church In Amer Unitas Fratrum No Prov"
            elif moravian == "Moravian Church in AmericaSouthern Province":
                key = "Moravian Church In Amer Unitas Fratrum So Prov"
                
        key += identifier
        
        #gets rid of things like U.S.A. vs USA,
        #Church of God, Memmonite vs Church of God (Memmonite)
        key = key.replace(".", "")
        key = key.replace(",", "")
        key = key.replace("-", "")
        key = key.replace("(", "")
        key = key.replace(")", "")
        key = key.replace("Usa", "USA")
        key = key.replace("\'", "")        
        key = key.strip() 
        
        cleanedlabels[key].append(varname)
    
        
for l in cleanedlabels:
    if Counter(cleanedlabels[l])["2020placeholder"] > 1:
        print(l, cleanedlabels[l])
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")   
    
    
#### Sometimes the data had only 1 dash separating, i.e.  
#### Association Of Free Lutheran Congregations-Number Of Adherents (2000)  
#### rather than Association Of Free Lutheran Congregations--Number Of Adherents (2000)
#### The above code wouldn't detect this so we take care of it now.
#### Needed to carefully check this didn't delete any good data before executing,
#### hence the two exceptions for adjrate and adjad from 2000.

#helper function
def findIndexOfSubstring(word : str, substring : str) -> int:
    #O(n^2) time, returns -1 if substring is not in word
    #finds first occurence
    n = len(word)
    k = len(substring)
    for i in range(n - k + 1):
        if word[i : i + k] == substring:
            return i
    
    return -1

#tests the above function
# print(findIndexOfSubstring("alabama", "bama"))
# print(findIndexOfSubstring("alabama", "ala"))
# print(findIndexOfSubstring("alabama", "a"))


badphrases = set()
badphrases.add("Rates Of Adh")
badphrases.add("Number Of")


#if a bad phrase is in label, then delete the rest of the label starting at 
#the beginning of the phrase. For example, 
#Albanian Orthodox Diocese Of AmericaRates Of Adherence Per 1000 Population 200
#becomes Albanian Orthodox Diocese Of America
for label in cleanedlabels.copy():
    for word in badphrases:
        if word in label:
            i = findIndexOfSubstring(label, word)
            cleanedlabels[label[:i].strip()] = cleanedlabels[label]
            del cleanedlabels[label]
            
#adding back 2 things that were unintentionally cleaned            
cleanedlabels["Adjusted Total Number of Adherents (2000)"].append("adjad")
cleanedlabels["Adjusted Rates of Adherence Per 1000 Population (2000)"].append("adjrate")
del cleanedlabels["Adjusted"] 
del cleanedlabels["Adjusted Total"]       

#### Corrects cleanedlabels that still have a ";" - these are to separate notes
#### Most are from 1980
trackednotes = set()
for label in cleanedlabels.copy():
    if ";" in label:
        trackednotes.add(label)
        ind = findIndexOfSubstring(label, ";")
        cleanedlabels[label[:ind]] += cleanedlabels[label]
        del cleanedlabels[label]

#### Some names of congregations are too long, cutting off part of the label
#### This part tries to fix it; if label ends in:
#### "adh", "ad" = adherents
#### "rate", "rt" = rate of adherence
#### "cng", "cg" = congregations     
todelete = set()
toappend = []
identifiercols = set()
identifiercols.add("Total Adherents")
identifiercols.add("Total Number of Churches")
identifiercols.add("Total Members")
identifiercols.add("Year")
identifiercols.add("Total Rate of Adherence")
identifiercols.add("Total Population")
identifiercols.add("State Name")
#identifiercols.add("State Census Code")
identifiercols.add("State Abbreviation")
identifiercols.add("State Code")
identifiercols.add("County Name")
identifiercols.add("Fips Code")
identifiercols.add("County Code")

for label in cleanedlabels:
    x = label[-len("_a"):]
    y = label[-len("_roa"):]
    roap = label[-len("_roap"):]
    roata = label[-len("_roata"):]
    
    if label not in identifiercols and \
        x != "_c" and x != "_a" and x != "_m" and y != "_roa"\
        and roap != "_roap" and roata != "_roata":
            
        remaining = len(cleanedlabels[label])
        done = 0
        
        for varname in cleanedlabels[label]:
            
            #adherents
            if varname[-3:] == "adh" or varname[-2:] == "ad":
                toappend.append((label + "_a",varname))
                done += 1
            
            elif varname[-4:] == "rate" or varname[-2:] == "rt":
                toappend.append((label + "_roa",varname))
                done += 1
                
            elif varname[-3:] == "cng" or varname[-2:] == "cg":
                toappend.append((label + "_c",varname))
                done += 1
        
        if done == remaining:
            todelete.add(label)

for label in todelete:
    del cleanedlabels[label]

for label, varname in toappend:
    cleanedlabels[label].append(varname)
        

##### MANUAL CORRECTION INTO CLEANEDLABELS HERE #########

#### manually correct some basic aggregate labels from cleanedlabels
cleanedlabels["Catholic (2010 label)_a"] += cleanedlabels["Catholic_a"]
del cleanedlabels["Catholic_a"]

cleanedlabels["Catholic (2010 label)_c"] += cleanedlabels["Catholic_c"]
del cleanedlabels["Catholic_c"]

cleanedlabels["Catholic (2010 label)_roa"] += cleanedlabels["Catholic_roa"]
del cleanedlabels["Catholic_roa"]

cleanedlabels["Other Denominations_a"] += cleanedlabels["Other_a"]
del cleanedlabels["Other_a"]

cleanedlabels["Other Denominations_c"] += cleanedlabels["Other_c"]
del cleanedlabels["Other_c"]

cleanedlabels["Other Denominations_roa"] += cleanedlabels["Other_roa"]
del cleanedlabels["Other_roa"]

cleanedlabels["Orthodox Denominations_a"] += cleanedlabels["Orthodox_a"]
del cleanedlabels["Orthodox_a"]

cleanedlabels["Orthodox Denominations_c"] += cleanedlabels["Orthodox_c"]
del cleanedlabels["Orthodox_c"]

cleanedlabels["Orthodox Denominations_roa"] += cleanedlabels["Orthodox_roa"]
del cleanedlabels["Orthodox_roa"]

cleanedlabels["Mainline Protestant_roa"] += cleanedlabels["Mainline Denominations_roa"]
del cleanedlabels["Mainline Denominations_roa"]

cleanedlabels["Mainline Protestant_a"] += cleanedlabels["Mainline Denominations_a"]
del cleanedlabels["Mainline Denominations_a"]

cleanedlabels["Mainline Protestant_c"] += cleanedlabels["Mainline Denominations_c"]
del cleanedlabels["Mainline Denominations_c"]

cleanedlabels["Evangelical Protestant_c"] += cleanedlabels["Evangelical Denominations_c"]
del cleanedlabels["Evangelical Denominations_c"]

cleanedlabels["Evangelical Protestant_a"] += cleanedlabels["Evangelical Denominations_a"]
del cleanedlabels["Evangelical Denominations_a"]

cleanedlabels["Evangelical Protestant_roa"] += cleanedlabels["Evangelical Denominations_roa"]
del cleanedlabels["Evangelical Denominations_roa"]

#Other labels to correct

cleanedlabels["Evangelical Lutheran Church In America_a"].append("ELCA_A")
cleanedlabels["Evangelical Lutheran Church In America_c"].append("ELCA_C")
cleanedlabels["Evangelical Lutheran Church In America_m"].append("ELCA_M")
del cleanedlabels["Evangelical Lutheran Church In America"]

cleanedlabels["Presbyterian Church USA_a"].append("PCUSA_A")
cleanedlabels["Presbyterian Church USA_c"].append("PCUSA_C")
cleanedlabels["Presbyterian Church USA_m"].append("PCUSA_M")
del cleanedlabels["Presbyterian Church USA"]

cleanedlabels["Jewish Estimate_m"].append("JEWISH_M")
cleanedlabels["Jewish Estimate_c"].append("JEWISH_C")
cleanedlabels["Jewish Estimate_a"].append("JEWISH_A")
del cleanedlabels["Jewish Estimate"]


##### We will consider congregations that are within 4 edit distance (Levenshtein distance)
##### away from each other to be to be the same congregation, just typed into
##### the STATA file labels incorrectly. Within 4 was chosen since it doesn't appear
##### to combine anything incorrectly, and catches things like 
##### "Church Of  God Anderson Indiana_a" vs "Church Of God Anderson Indiana_a",
##### "Church Of Jesus Christ Of LatterDay Saints The_a" vs "Church Of Jesus Christ Of LatterDay Saints_a",
##### "Evangelical Mennonite Church Inc_a" vs "Evangelical Mennonite Church_a",
##### etc.


#Below function is from official Leetcode solution:
#https://leetcode.com/problems/edit-distance/solutions/197003/edit-distance/
#Known as "Levenshtein distance"             
def levDistance(word1 : str, word2 : str) -> int:
        """
        :type word1: str
        :type word2: str
        :rtype: int
        """
        n = len(word1)
        m = len(word2)
        
        # if one of the strings is empty
        if n * m == 0:
            return n + m
        
        # array to store the convertion history
        d = [ [0] * (m + 1) for _ in range(n + 1)]
        
        # init boundaries
        for i in range(n + 1):
            d[i][0] = i
        for j in range(m + 1):
            d[0][j] = j
        
        # DP compute 
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                left = d[i - 1][j] + 1
                down = d[i][j - 1] + 1
                left_down = d[i - 1][j - 1] 
                if word1[i - 1] != word2[j - 1]:
                    left_down += 1
                d[i][j] = min(left, down, left_down)
        
        return d[n][m]


def elimEnding(word : str) -> str:
    """ strips out the _m, _a, _roa, _c ending """
    end = findIndexOfSubstring(word, "_")
    return word[:end] if end != -1 else word 

todelete = set()
toadd = defaultdict(list)
seen = set()
changed = {}
oldgarbage = set()
newgarbage = set()

## sets how far away autocorrect will be done; 
## a good balance seems to be 4 for auto, manual can do a little higher
DISTANCE = 4
endings = ["_m", "_a", "_roa", "_c", "_roap", "_roata"]
knownerrors = set()
knownerrors.add("Churches Of Christ")
knownerrors.add("Church Of Christ")
knownerrors.add("Moravian Church In Amer Unitas Fratrum So Prov")
knownerrors.add("Moravian Church In Amer Unitas Fratrum No Prov" )
knownerrors.add("Independent NonCharismatic Churches")
knownerrors.add( "Independent Charismatic Churches")
knownerrors.add("Buddhism Vajrayana")
knownerrors.add("Buddhism Mahayana")
knownerrors.add("Christian Catholic Church")
knownerrors.add("Christ Catholic Church")
knownerrors.add("Churches Of God General Conference")
knownerrors.add("Church Of God General Conference")
knownerrors.add("Schmiedeleut Hutterite Group 2")
knownerrors.add("Schmiedeleut Hutterite Group 1")
knownerrors.add("Mennonite Church")
knownerrors.add("Mennonite Church USA")


def autocorrect(dist : int, manualcheck = False):
    """This function will autocombine any labels that are within dist"""
    """Levenshtein distance away from each other"""
    for label in cleanedlabels:
        if label in seen:
            continue 
        
        seen.add(label)
        
        for other in cleanedlabels:
            if other in seen:
                continue
            
            #makes sure they are the same category, e.g. _a, _m, _roa (it will only check
            #the 'oa' portion of _roa but should be ok)
            if label[-2:] == other[-2:] and label[:3] == other[:3] and\
                elimEnding(label) not in knownerrors \
                and elimEnding(other) not in knownerrors\
                    and levDistance(label, other) <= dist:
                
                seen.add(other)
                combinedlabel = label
                deletedlabel = other
                
                #picks shortest label as combinedlabel
                if (len(other) < len(label)):
                    combinedlabel = other
                    deletedlabel = label
                    
                #levenshtein distance should be transitive,
                #or kind of like adding things to an equivalence class
                todelete.add((deletedlabel,combinedlabel))
                    
                #takes out the end, e.g. _a, _m, _roa, _c
                #and adds it to the changed dictionary to standardize everything
                #later; this is necessary because say "Evangelical Mennonite Church Inc_a"
                #becomes "Evangelical Mennonite Church_a" (and same for _c, _roa),
                #we would still have "Evangelical Mennonite Church Inc_m" as there was no
                #_m file with the other name from 2000 data and later
                if changed.get(elimEnding(deletedlabel)) and \
                    changed[elimEnding(deletedlabel)] != elimEnding(combinedlabel):
                        ###debugging statements below
                        #print("MULTIPLE NAMES ADDED TO SAME DELETION IN CHANGED:")
                        #print("Old label:", elimEnding(deletedlabel))
                        #print("New Label 1:",elimEnding(changed[elimEnding(deletedlabel)]))
                        #print("New Label 2:",elimEnding(combinedlabel))
                        #print("--------------------------------------------------------")
                        
                        #keep this
                        changed[changed[elimEnding(deletedlabel)]] = elimEnding(combinedlabel)
                changed[elimEnding(deletedlabel)] = elimEnding(combinedlabel)
                    
                toadd[combinedlabel] += cleanedlabels[label]
                toadd[combinedlabel] += cleanedlabels[other]
    
    #DEBUG = changed.copy()
    #print(DEBUG)
    
    ## manually approve each entry if manual check option
    if manualcheck:
        for oldlabel in changed:
            print("Do you want to combine \"",oldlabel,"\" WITH \"",\
                  changed[oldlabel],"\" ?", sep = "")
            ans = input("(y/n)")
            while(ans != "y" and ans != "n"):
                print("Invalid input. Press y/n and then enter.")
                ans = input("(y/n)")
            if ans == "n":
                oldgarbage.add(oldlabel)
                newgarbage.add(changed[oldlabel])
                
        #take out things user doesn't want combined 
        #this function would ideally be refactored later as below section is unwieldy
        for label in todelete.copy():
            label1 = label[0]
            label2 = label[1]
            if elimEnding(label1) in oldgarbage or elimEnding(label2) in oldgarbage:
                todelete.remove(label)
             
        for label in toadd.copy():
            if elimEnding(label) in newgarbage or elimEnding(label) in oldgarbage:
                del toadd[label]
                
        for label in oldgarbage:
            del changed[label]
    
    ##finally, modify    
        
    for label, _ in todelete:
        if label in cleanedlabels:
            del cleanedlabels[label]
        else:
            for ending in endings:
                if label + ending in cleanedlabels:
                    del cleanedlabels[label + ending]
    
    for label in toadd:
        cleanedlabels[label] = toadd[label].copy()
        
    for oldlabel in changed:
        for ending in endings:
            if oldlabel + ending in cleanedlabels:
                newlabel = changed[oldlabel] + ending
                cleanedlabels[newlabel] = cleanedlabels[oldlabel + ending].copy()
                del cleanedlabels[oldlabel + ending]

###Can manually check or not
autocorrect(DISTANCE,manualcheck = False)

for l in cleanedlabels:
    if Counter(cleanedlabels[l])["2020placeholder"] > 1:
        print(l, cleanedlabels[l])
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")



### Direct Changes to cleanedlabels ###
def manualchange(d : dict):
    """Manually replaces things in cleanedlabels. Dict should have the old label as its key"""
    for label in d:
        for ending in endings:
            if label in cleanedlabels:
                cleanedlabels[d[label]] += cleanedlabels[label]
                del cleanedlabels[label]
            elif label+ending in cleanedlabels:
                cleanedlabels[d[label]+ending] += cleanedlabels[label + ending]
                del cleanedlabels[label + ending]
            
##### Manual Section to add to changed #######
tochange = {}

##national association of free will baptists: code 223 in 1971 and 1990
tochange["Free Will Baptist National Association Of Inc"] = "National Association Of Free Will Baptists"

tochange["Free Will Baptists"] = "National Association Of Free Will Baptists"

tochange["General Baptists General Association Of"] = "General Association Of General Baptists"

tochange["Malankara Archdiocese Syrian Orthodox Church In North America"] = "Malankara Archdiocese Of The Syrian Orthodox Church In North America"

tochange["Malankara Orthodox Syrian Church American Diocese"] = "Malankara Orthodox Syrian Church"

tochange["Malankara Orthodox Syrian Church American Diocese"] = "Malankara Orthodox Syrian Church"

tochange["Primitive Methodist Church In The USA"] = "Primitive Methodist Church USA"

tochange["Unitarian Universalist Association Of Congregations"] = "Unitarian Universalist Association"

tochange["Ukrainian Orthodox Church Of Amer Ecum Patr"] = "Ukrainian Orthodox Church Of The USA"

tochange["Ukrainian Orthodox Church Of Amer Ecumenical Patriar"] = "Ukrainian Orthodox Church Of The USA"

tochange["Ukrainian Orthodox Church Of Amer Ecumenical Patria"] = "Ukrainian Orthodox Church Of The USA"

tochange["Ukrainian Orthodox Church Of Amer Ecumenical Patriarc"] = "Ukrainian Orthodox Church Of The USA"

tochange["Ukranian Orthodox Church Of The USA"] = "Ukrainian Orthodox Church Of The USA"

tochange["Full Fips Code"] = "Fips Code"

manualchange(tochange)
    
    

#### Checking section!
#### Check that the number in the sets appends up
#s = 0
#for item in cleanedlabels:
#    s += len(cleanedlabels[item])
#print("Number of labels in the sets of 'cleanedlabels:'")
#print(s)
#print("Number of labels in the labels variables:")
#print(sum([len(x) for x in todo_list1]) + sum([len(x) for x in todo_list2]))
#print("NOTE: If the above 2 numbers are NOT the same, double-check! Something is wrong.")
print("-------------------------------------------------------------")
print("Number of labels in \"cleanedlabels\" that have more entries than number of years of data (should be 0):")
print(len([x for x in cleanedlabels if len(cleanedlabels[x]) > len(dataframes)]))
print("They are:")
print([x for x in cleanedlabels if len(cleanedlabels[x]) > len(dataframes)])
print("-------------------------------------------------------------")
baselabels = set()
## This set will have most datapoints at index 0, least datapoints at last index
## If a congregation has "multiple" datapoints from one year, this will be thrown off
## i.e. for moravian church
## but this is an edge case
datapoints = []
print("Number of labels that have", len(dataframes),
      "entries (has a datapoint from every piece of data entered):")
appearances = set([elimEnding(x) for x in cleanedlabels \
                   if len(cleanedlabels[x]) == len(dataframes)])
datapoints.append(set([x for x in cleanedlabels if len(cleanedlabels[x]) == len(dataframes)]))
print(len(appearances))
print("They are:")
print(appearances)
baselabels = baselabels.union(appearances)
print("-------------------------------------------------------------")
for i in range(len(dataframes)-1, 0, -1):
    print("Number of labels that have", i, "entries:" )
    appearances = set([elimEnding(x) for x in cleanedlabels \
                       if len(cleanedlabels[x]) == i]) - baselabels
    datapoints.append(set([x for x in cleanedlabels if len(cleanedlabels[x]) == i]))
    print(len(appearances))
    print("They are:")
    print(appearances)
    baselabels = baselabels.union(appearances)
    print("-------------------------------------------------------------")
print("The", len(changed),"congregations that had their names auto-changed using Levenshtein distance"
      + "(format is 'Old Name': 'New Name'):")
print(changed)
print("-------------------------------------------------------------")
    
### Check for potential errors
print("Entries in 'cleanedlabels' without a '_c', '_a', '_m', '_roa',"+
      "'_roata', '_roap' ending, that are not an identifier column (should be 0):")
for label in cleanedlabels:
    x = label[-len("_a"):]
    y = label[-len("_roa"):]
    roap = label[-len("_roap"):]
    roata = label[-len("_roata"):]
    
    if label not in identifiercols and \
        x != "_c" and x != "_a" and x != "_m" and y != "_roa"\
        and roap != "_roap" and roata != "_roata":
        print(label + ":")
        for item in cleanedlabels[label]:
            print(item)
        print("+++++++++++++++++++++++++++++++++++++++++++++++")
        

countdups = 0
### make replacement dictionary
replacement = {}
for label in cleanedlabels:
    for varname in cleanedlabels[label]:
        if varname != "2020placeholder" and \
        replacement.get(varname):
            if replacement[varname] != label:
                if ";" in label:
                    replacement[varname] = "1990n_" + replacement[varname]
                
                elif ";" in replacement[varname]:
                    replacement[varname] = "1990n_"+label
                    
                else:
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    print("Error: a variable name has more than 1 label!")
                    print("varname:",varname)
                    print("oldlabel:", replacement[varname])
                    print("newlabel:",label)
            else:
                countdups += 1
                
        if varname == "2020placeholder":
            countdups += 1
            
        replacement[varname] = label


print("-------------------------------------------------------------")
print("Number of labels in the sets of 'replacement:'")
print(len(replacement))
print("-------------------------------------------------------------")


#### Manual replacement section
data90.rename(columns={ 'BAPTGC_C':'Baptist General Conference_c'}, inplace = True)
data90.rename(columns={ 'BAPTGC_A':'Baptist General Conference_a'}, inplace = True)
data90.rename(columns={ 'BAPTGC_M':'Baptist General Conference_m'}, inplace = True)
data90.rename(columns={ 'BMAA_C':'Baptist Missionary Association Of America_c'}, inplace = True)
data90.rename(columns={ 'BMAA_A':'Baptist Missionary Association Of America_a'}, inplace = True)
data90.rename(columns={ 'BMAA_M':'Baptist Missionary Association Of America_m'}, inplace = True)
data90.rename(columns={ 'CGGC_A':'Churches Of God General Conference_a'}, inplace = True)
data90.rename(columns={ 'CGGC_M':'Churches Of God General Conference_m'}, inplace = True)
data90.rename(columns={ 'CGGC_C':'Churches Of God General Conference_c'}, inplace = True)
data90.rename(columns={ 'ROMORT_C':'Romanian Orthodox Episcopate Of America_c'}, inplace = True)
data90.rename(columns={ 'ROMORT_M':'Romanian Orthodox Episcopate Of America_m'}, inplace = True)
data90.rename(columns={ 'ROMORT_A':'Romanian Orthodox Episcopate Of America_a'}, inplace = True)
data2000.rename(columns={ 'county':'County Name'}, inplace = True)

#### Auto-replace others!
print("Column headers for a congregation that don't end in one of the endings:")
for df in dataframes:
    newcolnames = {}
    for column in df.keys():

        ### checks to make sure we haven't forgotten to replace anything
        checkcol = column
        if column in replacement:
            checkcol = replacement[column]
            
        flag = False
        for ending in endings:
            if ending in checkcol:
                flag = True
        if checkcol not in identifiercols and not flag:
            print(checkcol)
               
        ### does the replacement for the stata dataframes with variable codes
        if column in replacement:
            newcolnames[column] = replacement[column]

        ### does replacement for 2020 Excel datasheet
        # actually doesn't
#        elif column in changed:
#            newcolnames[column] = changed[column]
        else:
            newcolnames[column] = column
        
    df.rename(columns = newcolnames, inplace = True)

print("-------------------------------------------------------------")
print("Notes to keep in mind (most are found in 1980 data codebook):")
for note in trackednotes:
    print(note)
print("-------------------------------------------------------------")


#### Make main dataframe

#add numbering to columns for debugging
# # for df in dataframes:
# #     newcolnames = {}
# #     c = 0
# #     for column in df.keys():              
# #         newcolnames[column] = str(c)+"_"+column
# #         c += 1
        
# #     #part of debug
# #     newcolnames["Year"] = "Year"
# #     df.rename(columns = newcolnames, inplace = True)


# # #use below for debugging along with column numbering
# # for df in dataframes:
# # #    print(df.Year[0])
# #     seen = {}
# #     num = 0
# #     for c in df.keys():           
# #         if c[findIndexOfSubstring(c, "_") + 1:] in seen:
# #             print(c)
# #             print(seen[c[findIndexOfSubstring(c, "_") + 1:]])
# #             print(num)
# #         seen[c[findIndexOfSubstring(c, "_") + 1:]] = num
# #         num += 1
        
# #     df.reset_index(inplace=True, drop=True)

print("Repeated columns in a dataframe:")
c = 0
for df in dataframes:
    seen = set()
    for col in df.columns:
        if col in seen:
            print("DF: " + str(c))
            print(col)
        else:
            seen.add(col)
    c += 1
print("-------------------------------------------------------------")

#concat all clean dataframes to make the main dataframe    
main = pd.concat(dataframes, axis = 0, ignore_index = True)

#Converts all states to capital case
main["State Name"] = main["State Name"].str.title()
main["Year"] = main["Year"].astype(int)
main["Fips Code"] = main["Fips Code"].astype(str)

### Standardize County Names

#from python library geonamescache, function get_us_counties(), modified by me into a dict
standardcountytuples = {'1001': ('Autauga County', 'AL'),
 '1003': ('Baldwin County', 'AL'),
 '1005': ('Barbour County', 'AL'),
 '1007': ('Bibb County', 'AL'),
 '1009': ('Blount County', 'AL'),
 '1011': ('Bullock County', 'AL'),
 '1013': ('Butler County', 'AL'),
 '1015': ('Calhoun County', 'AL'),
 '1017': ('Chambers County', 'AL'),
 '1019': ('Cherokee County', 'AL'),
 '1021': ('Chilton County', 'AL'),
 '1023': ('Choctaw County', 'AL'),
 '1025': ('Clarke County', 'AL'),
 '1027': ('Clay County', 'AL'),
 '1029': ('Cleburne County', 'AL'),
 '1031': ('Coffee County', 'AL'),
 '1033': ('Colbert County', 'AL'),
 '1035': ('Conecuh County', 'AL'),
 '1037': ('Coosa County', 'AL'),
 '1039': ('Covington County', 'AL'),
 '1041': ('Crenshaw County', 'AL'),
 '1043': ('Cullman County', 'AL'),
 '1045': ('Dale County', 'AL'),
 '1047': ('Dallas County', 'AL'),
 '1049': ('DeKalb County', 'AL'),
 '1051': ('Elmore County', 'AL'),
 '1053': ('Escambia County', 'AL'),
 '1055': ('Etowah County', 'AL'),
 '1057': ('Fayette County', 'AL'),
 '1059': ('Franklin County', 'AL'),
 '1061': ('Geneva County', 'AL'),
 '1063': ('Greene County', 'AL'),
 '1065': ('Hale County', 'AL'),
 '1067': ('Henry County', 'AL'),
 '1069': ('Houston County', 'AL'),
 '1071': ('Jackson County', 'AL'),
 '1073': ('Jefferson County', 'AL'),
 '1075': ('Lamar County', 'AL'),
 '1077': ('Lauderdale County', 'AL'),
 '1079': ('Lawrence County', 'AL'),
 '1081': ('Lee County', 'AL'),
 '1083': ('Limestone County', 'AL'),
 '1085': ('Lowndes County', 'AL'),
 '1087': ('Macon County', 'AL'),
 '1089': ('Madison County', 'AL'),
 '1091': ('Marengo County', 'AL'),
 '1093': ('Marion County', 'AL'),
 '1095': ('Marshall County', 'AL'),
 '1097': ('Mobile County', 'AL'),
 '1099': ('Monroe County', 'AL'),
 '1101': ('Montgomery County', 'AL'),
 '1103': ('Morgan County', 'AL'),
 '1105': ('Perry County', 'AL'),
 '1107': ('Pickens County', 'AL'),
 '1109': ('Pike County', 'AL'),
 '1111': ('Randolph County', 'AL'),
 '1113': ('Russell County', 'AL'),
 '1115': ('St. Clair County', 'AL'),
 '1117': ('Shelby County', 'AL'),
 '1119': ('Sumter County', 'AL'),
 '1121': ('Talladega County', 'AL'),
 '1123': ('Tallapoosa County', 'AL'),
 '1125': ('Tuscaloosa County', 'AL'),
 '1127': ('Walker County', 'AL'),
 '1129': ('Washington County', 'AL'),
 '1131': ('Wilcox County', 'AL'),
 '1133': ('Winston County', 'AL'),
 '2013': ('Aleutians East Borough', 'AK'),
 '2016': ('Aleutians West Census Area', 'AK'),
 '2020': ('Anchorage Municipality', 'AK'),
 '2050': ('Bethel Census Area', 'AK'),
 '2060': ('Bristol Bay Borough', 'AK'),
 '2068': ('Denali Borough', 'AK'),
 '2070': ('Dillingham Census Area', 'AK'),
 '2090': ('Fairbanks North Star Borough', 'AK'),
 '2100': ('Haines Borough', 'AK'),
 '2105': ('Hoonah-Angoon Census Area', 'AK'),
 '2110': ('Juneau City and Borough', 'AK'),
 '2122': ('Kenai Peninsula Borough', 'AK'),
 '2130': ('Ketchikan Gateway Borough', 'AK'),
 '2150': ('Kodiak Island Borough', 'AK'),
 '2164': ('Lake and Peninsula Borough', 'AK'),
 '2170': ('Matanuska-Susitna Borough', 'AK'),
 '2180': ('Nome Census Area', 'AK'),
 '2185': ('North Slope Borough', 'AK'),
 '2188': ('Northwest Arctic Borough', 'AK'),
 '2195': ('Petersburg Census Area', 'AK'),
 '2198': ('Prince of Wales-Hyder Census Area', 'AK'),
 '2220': ('Sitka City and Borough', 'AK'),
 '2230': ('Skagway Municipality', 'AK'),
 '2240': ('Southeast Fairbanks Census Area', 'AK'),
 '2261': ('Valdez-Cordova Census Area', 'AK'),
 '2270': ('Wade Hampton Census Area', 'AK'),
 '2275': ('Wrangell City and Borough', 'AK'),
 '2282': ('Yakutat City and Borough', 'AK'),
 '2290': ('Yukon-Koyukuk Census Area', 'AK'),
 '4001': ('Apache County', 'AZ'),
 '4003': ('Cochise County', 'AZ'),
 '4005': ('Coconino County', 'AZ'),
 '4007': ('Gila County', 'AZ'),
 '4009': ('Graham County', 'AZ'),
 '4011': ('Greenlee County', 'AZ'),
 '4012': ('La Paz County', 'AZ'),
 '4013': ('Maricopa County', 'AZ'),
 '4015': ('Mohave County', 'AZ'),
 '4017': ('Navajo County', 'AZ'),
 '4019': ('Pima County', 'AZ'),
 '4021': ('Pinal County', 'AZ'),
 '4023': ('Santa Cruz County', 'AZ'),
 '4025': ('Yavapai County', 'AZ'),
 '4027': ('Yuma County', 'AZ'),
 '5001': ('Arkansas County', 'AR'),
 '5003': ('Ashley County', 'AR'),
 '5005': ('Baxter County', 'AR'),
 '5007': ('Benton County', 'AR'),
 '5009': ('Boone County', 'AR'),
 '5011': ('Bradley County', 'AR'),
 '5013': ('Calhoun County', 'AR'),
 '5015': ('Carroll County', 'AR'),
 '5017': ('Chicot County', 'AR'),
 '5019': ('Clark County', 'AR'),
 '5021': ('Clay County', 'AR'),
 '5023': ('Cleburne County', 'AR'),
 '5025': ('Cleveland County', 'AR'),
 '5027': ('Columbia County', 'AR'),
 '5029': ('Conway County', 'AR'),
 '5031': ('Craighead County', 'AR'),
 '5033': ('Crawford County', 'AR'),
 '5035': ('Crittenden County', 'AR'),
 '5037': ('Cross County', 'AR'),
 '5039': ('Dallas County', 'AR'),
 '5041': ('Desha County', 'AR'),
 '5043': ('Drew County', 'AR'),
 '5045': ('Faulkner County', 'AR'),
 '5047': ('Franklin County', 'AR'),
 '5049': ('Fulton County', 'AR'),
 '5051': ('Garland County', 'AR'),
 '5053': ('Grant County', 'AR'),
 '5055': ('Greene County', 'AR'),
 '5057': ('Hempstead County', 'AR'),
 '5059': ('Hot Spring County', 'AR'),
 '5061': ('Howard County', 'AR'),
 '5063': ('Independence County', 'AR'),
 '5065': ('Izard County', 'AR'),
 '5067': ('Jackson County', 'AR'),
 '5069': ('Jefferson County', 'AR'),
 '5071': ('Johnson County', 'AR'),
 '5073': ('Lafayette County', 'AR'),
 '5075': ('Lawrence County', 'AR'),
 '5077': ('Lee County', 'AR'),
 '5079': ('Lincoln County', 'AR'),
 '5081': ('Little River County', 'AR'),
 '5083': ('Logan County', 'AR'),
 '5085': ('Lonoke County', 'AR'),
 '5087': ('Madison County', 'AR'),
 '5089': ('Marion County', 'AR'),
 '5091': ('Miller County', 'AR'),
 '5093': ('Mississippi County', 'AR'),
 '5095': ('Monroe County', 'AR'),
 '5097': ('Montgomery County', 'AR'),
 '5099': ('Nevada County', 'AR'),
 '5101': ('Newton County', 'AR'),
 '5103': ('Ouachita County', 'AR'),
 '5105': ('Perry County', 'AR'),
 '5107': ('Phillips County', 'AR'),
 '5109': ('Pike County', 'AR'),
 '5111': ('Poinsett County', 'AR'),
 '5113': ('Polk County', 'AR'),
 '5115': ('Pope County', 'AR'),
 '5117': ('Prairie County', 'AR'),
 '5119': ('Pulaski County', 'AR'),
 '5121': ('Randolph County', 'AR'),
 '5123': ('St. Francis County', 'AR'),
 '5125': ('Saline County', 'AR'),
 '5127': ('Scott County', 'AR'),
 '5129': ('Searcy County', 'AR'),
 '5131': ('Sebastian County', 'AR'),
 '5133': ('Sevier County', 'AR'),
 '5135': ('Sharp County', 'AR'),
 '5137': ('Stone County', 'AR'),
 '5139': ('Union County', 'AR'),
 '5141': ('Van Buren County', 'AR'),
 '5143': ('Washington County', 'AR'),
 '5145': ('White County', 'AR'),
 '5147': ('Woodruff County', 'AR'),
 '5149': ('Yell County', 'AR'),
 '6001': ('Alameda County', 'CA'),
 '6003': ('Alpine County', 'CA'),
 '6005': ('Amador County', 'CA'),
 '6007': ('Butte County', 'CA'),
 '6009': ('Calaveras County', 'CA'),
 '6011': ('Colusa County', 'CA'),
 '6013': ('Contra Costa County', 'CA'),
 '6015': ('Del Norte County', 'CA'),
 '6017': ('El Dorado County', 'CA'),
 '6019': ('Fresno County', 'CA'),
 '6021': ('Glenn County', 'CA'),
 '6023': ('Humboldt County', 'CA'),
 '6025': ('Imperial County', 'CA'),
 '6027': ('Inyo County', 'CA'),
 '6029': ('Kern County', 'CA'),
 '6031': ('Kings County', 'CA'),
 '6033': ('Lake County', 'CA'),
 '6035': ('Lassen County', 'CA'),
 '6037': ('Los Angeles County', 'CA'),
 '6039': ('Madera County', 'CA'),
 '6041': ('Marin County', 'CA'),
 '6043': ('Mariposa County', 'CA'),
 '6045': ('Mendocino County', 'CA'),
 '6047': ('Merced County', 'CA'),
 '6049': ('Modoc County', 'CA'),
 '6051': ('Mono County', 'CA'),
 '6053': ('Monterey County', 'CA'),
 '6055': ('Napa County', 'CA'),
 '6057': ('Nevada County', 'CA'),
 '6059': ('Orange County', 'CA'),
 '6061': ('Placer County', 'CA'),
 '6063': ('Plumas County', 'CA'),
 '6065': ('Riverside County', 'CA'),
 '6067': ('Sacramento County', 'CA'),
 '6069': ('San Benito County', 'CA'),
 '6071': ('San Bernardino County', 'CA'),
 '6073': ('San Diego County', 'CA'),
 '6075': ('San Francisco County', 'CA'),
 '6077': ('San Joaquin County', 'CA'),
 '6079': ('San Luis Obispo County', 'CA'),
 '6081': ('San Mateo County', 'CA'),
 '6083': ('Santa Barbara County', 'CA'),
 '6085': ('Santa Clara County', 'CA'),
 '6087': ('Santa Cruz County', 'CA'),
 '6089': ('Shasta County', 'CA'),
 '6091': ('Sierra County', 'CA'),
 '6093': ('Siskiyou County', 'CA'),
 '6095': ('Solano County', 'CA'),
 '6097': ('Sonoma County', 'CA'),
 '6099': ('Stanislaus County', 'CA'),
 '6101': ('Sutter County', 'CA'),
 '6103': ('Tehama County', 'CA'),
 '6105': ('Trinity County', 'CA'),
 '6107': ('Tulare County', 'CA'),
 '6109': ('Tuolumne County', 'CA'),
 '6111': ('Ventura County', 'CA'),
 '6113': ('Yolo County', 'CA'),
 '6115': ('Yuba County', 'CA'),
 '8001': ('Adams County', 'CO'),
 '8003': ('Alamosa County', 'CO'),
 '8005': ('Arapahoe County', 'CO'),
 '8007': ('Archuleta County', 'CO'),
 '8009': ('Baca County', 'CO'),
 '8011': ('Bent County', 'CO'),
 '8013': ('Boulder County', 'CO'),
 '8014': ('Broomfield County', 'CO'),
 '8015': ('Chaffee County', 'CO'),
 '8017': ('Cheyenne County', 'CO'),
 '8019': ('Clear Creek County', 'CO'),
 '8021': ('Conejos County', 'CO'),
 '8023': ('Costilla County', 'CO'),
 '8025': ('Crowley County', 'CO'),
 '8027': ('Custer County', 'CO'),
 '8029': ('Delta County', 'CO'),
 '8031': ('Denver County', 'CO'),
 '8033': ('Dolores County', 'CO'),
 '8035': ('Douglas County', 'CO'),
 '8037': ('Eagle County', 'CO'),
 '8039': ('Elbert County', 'CO'),
 '8041': ('El Paso County', 'CO'),
 '8043': ('Fremont County', 'CO'),
 '8045': ('Garfield County', 'CO'),
 '8047': ('Gilpin County', 'CO'),
 '8049': ('Grand County', 'CO'),
 '8051': ('Gunnison County', 'CO'),
 '8053': ('Hinsdale County', 'CO'),
 '8055': ('Huerfano County', 'CO'),
 '8057': ('Jackson County', 'CO'),
 '8059': ('Jefferson County', 'CO'),
 '8061': ('Kiowa County', 'CO'),
 '8063': ('Kit Carson County', 'CO'),
 '8065': ('Lake County', 'CO'),
 '8067': ('La Plata County', 'CO'),
 '8069': ('Larimer County', 'CO'),
 '8071': ('Las Animas County', 'CO'),
 '8073': ('Lincoln County', 'CO'),
 '8075': ('Logan County', 'CO'),
 '8077': ('Mesa County', 'CO'),
 '8079': ('Mineral County', 'CO'),
 '8081': ('Moffat County', 'CO'),
 '8083': ('Montezuma County', 'CO'),
 '8085': ('Montrose County', 'CO'),
 '8087': ('Morgan County', 'CO'),
 '8089': ('Otero County', 'CO'),
 '8091': ('Ouray County', 'CO'),
 '8093': ('Park County', 'CO'),
 '8095': ('Phillips County', 'CO'),
 '8097': ('Pitkin County', 'CO'),
 '8099': ('Prowers County', 'CO'),
 '8101': ('Pueblo County', 'CO'),
 '8103': ('Rio Blanco County', 'CO'),
 '8105': ('Rio Grande County', 'CO'),
 '8107': ('Routt County', 'CO'),
 '8109': ('Saguache County', 'CO'),
 '8111': ('San Juan County', 'CO'),
 '8113': ('San Miguel County', 'CO'),
 '8115': ('Sedgwick County', 'CO'),
 '8117': ('Summit County', 'CO'),
 '8119': ('Teller County', 'CO'),
 '8121': ('Washington County', 'CO'),
 '8123': ('Weld County', 'CO'),
 '8125': ('Yuma County', 'CO'),
 '9001': ('Fairfield County', 'CT'),
 '9003': ('Hartford County', 'CT'),
 '9005': ('Litchfield County', 'CT'),
 '9007': ('Middlesex County', 'CT'),
 '9009': ('New Haven County', 'CT'),
 '9011': ('New London County', 'CT'),
 '9013': ('Tolland County', 'CT'),
 '9015': ('Windham County', 'CT'),
 '10001': ('Kent County', 'DE'),
 '10003': ('New Castle County', 'DE'),
 '10005': ('Sussex County', 'DE'),
 '11001': ('District of Columbia', 'DC'),
 '12001': ('Alachua County', 'FL'),
 '12003': ('Baker County', 'FL'),
 '12005': ('Bay County', 'FL'),
 '12007': ('Bradford County', 'FL'),
 '12009': ('Brevard County', 'FL'),
 '12011': ('Broward County', 'FL'),
 '12013': ('Calhoun County', 'FL'),
 '12015': ('Charlotte County', 'FL'),
 '12017': ('Citrus County', 'FL'),
 '12019': ('Clay County', 'FL'),
 '12021': ('Collier County', 'FL'),
 '12023': ('Columbia County', 'FL'),
 '12027': ('DeSoto County', 'FL'),
 '12029': ('Dixie County', 'FL'),
 '12031': ('Duval County', 'FL'),
 '12033': ('Escambia County', 'FL'),
 '12035': ('Flagler County', 'FL'),
 '12037': ('Franklin County', 'FL'),
 '12039': ('Gadsden County', 'FL'),
 '12041': ('Gilchrist County', 'FL'),
 '12043': ('Glades County', 'FL'),
 '12045': ('Gulf County', 'FL'),
 '12047': ('Hamilton County', 'FL'),
 '12049': ('Hardee County', 'FL'),
 '12051': ('Hendry County', 'FL'),
 '12053': ('Hernando County', 'FL'),
 '12055': ('Highlands County', 'FL'),
 '12057': ('Hillsborough County', 'FL'),
 '12059': ('Holmes County', 'FL'),
 '12061': ('Indian River County', 'FL'),
 '12063': ('Jackson County', 'FL'),
 '12065': ('Jefferson County', 'FL'),
 '12067': ('Lafayette County', 'FL'),
 '12069': ('Lake County', 'FL'),
 '12071': ('Lee County', 'FL'),
 '12073': ('Leon County', 'FL'),
 '12075': ('Levy County', 'FL'),
 '12077': ('Liberty County', 'FL'),
 '12079': ('Madison County', 'FL'),
 '12081': ('Manatee County', 'FL'),
 '12083': ('Marion County', 'FL'),
 '12085': ('Martin County', 'FL'),
 '12086': ('Miami-Dade County', 'FL'),
 '12087': ('Monroe County', 'FL'),
 '12089': ('Nassau County', 'FL'),
 '12091': ('Okaloosa County', 'FL'),
 '12093': ('Okeechobee County', 'FL'),
 '12095': ('Orange County', 'FL'),
 '12097': ('Osceola County', 'FL'),
 '12099': ('Palm Beach County', 'FL'),
 '12101': ('Pasco County', 'FL'),
 '12103': ('Pinellas County', 'FL'),
 '12105': ('Polk County', 'FL'),
 '12107': ('Putnam County', 'FL'),
 '12109': ('St. Johns County', 'FL'),
 '12111': ('St. Lucie County', 'FL'),
 '12113': ('Santa Rosa County', 'FL'),
 '12115': ('Sarasota County', 'FL'),
 '12117': ('Seminole County', 'FL'),
 '12119': ('Sumter County', 'FL'),
 '12121': ('Suwannee County', 'FL'),
 '12123': ('Taylor County', 'FL'),
 '12125': ('Union County', 'FL'),
 '12127': ('Volusia County', 'FL'),
 '12129': ('Wakulla County', 'FL'),
 '12131': ('Walton County', 'FL'),
 '12133': ('Washington County', 'FL'),
 '13001': ('Appling County', 'GA'),
 '13003': ('Atkinson County', 'GA'),
 '13005': ('Bacon County', 'GA'),
 '13007': ('Baker County', 'GA'),
 '13009': ('Baldwin County', 'GA'),
 '13011': ('Banks County', 'GA'),
 '13013': ('Barrow County', 'GA'),
 '13015': ('Bartow County', 'GA'),
 '13017': ('Ben Hill County', 'GA'),
 '13019': ('Berrien County', 'GA'),
 '13021': ('Bibb County', 'GA'),
 '13023': ('Bleckley County', 'GA'),
 '13025': ('Brantley County', 'GA'),
 '13027': ('Brooks County', 'GA'),
 '13029': ('Bryan County', 'GA'),
 '13031': ('Bulloch County', 'GA'),
 '13033': ('Burke County', 'GA'),
 '13035': ('Butts County', 'GA'),
 '13037': ('Calhoun County', 'GA'),
 '13039': ('Camden County', 'GA'),
 '13043': ('Candler County', 'GA'),
 '13045': ('Carroll County', 'GA'),
 '13047': ('Catoosa County', 'GA'),
 '13049': ('Charlton County', 'GA'),
 '13051': ('Chatham County', 'GA'),
 '13053': ('Chattahoochee County', 'GA'),
 '13055': ('Chattooga County', 'GA'),
 '13057': ('Cherokee County', 'GA'),
 '13059': ('Clarke County', 'GA'),
 '13061': ('Clay County', 'GA'),
 '13063': ('Clayton County', 'GA'),
 '13065': ('Clinch County', 'GA'),
 '13067': ('Cobb County', 'GA'),
 '13069': ('Coffee County', 'GA'),
 '13071': ('Colquitt County', 'GA'),
 '13073': ('Columbia County', 'GA'),
 '13075': ('Cook County', 'GA'),
 '13077': ('Coweta County', 'GA'),
 '13079': ('Crawford County', 'GA'),
 '13081': ('Crisp County', 'GA'),
 '13083': ('Dade County', 'GA'),
 '13085': ('Dawson County', 'GA'),
 '13087': ('Decatur County', 'GA'),
 '13089': ('DeKalb County', 'GA'),
 '13091': ('Dodge County', 'GA'),
 '13093': ('Dooly County', 'GA'),
 '13095': ('Dougherty County', 'GA'),
 '13097': ('Douglas County', 'GA'),
 '13099': ('Early County', 'GA'),
 '13101': ('Echols County', 'GA'),
 '13103': ('Effingham County', 'GA'),
 '13105': ('Elbert County', 'GA'),
 '13107': ('Emanuel County', 'GA'),
 '13109': ('Evans County', 'GA'),
 '13111': ('Fannin County', 'GA'),
 '13113': ('Fayette County', 'GA'),
 '13115': ('Floyd County', 'GA'),
 '13117': ('Forsyth County', 'GA'),
 '13119': ('Franklin County', 'GA'),
 '13121': ('Fulton County', 'GA'),
 '13123': ('Gilmer County', 'GA'),
 '13125': ('Glascock County', 'GA'),
 '13127': ('Glynn County', 'GA'),
 '13129': ('Gordon County', 'GA'),
 '13131': ('Grady County', 'GA'),
 '13133': ('Greene County', 'GA'),
 '13135': ('Gwinnett County', 'GA'),
 '13137': ('Habersham County', 'GA'),
 '13139': ('Hall County', 'GA'),
 '13141': ('Hancock County', 'GA'),
 '13143': ('Haralson County', 'GA'),
 '13145': ('Harris County', 'GA'),
 '13147': ('Hart County', 'GA'),
 '13149': ('Heard County', 'GA'),
 '13151': ('Henry County', 'GA'),
 '13153': ('Houston County', 'GA'),
 '13155': ('Irwin County', 'GA'),
 '13157': ('Jackson County', 'GA'),
 '13159': ('Jasper County', 'GA'),
 '13161': ('Jeff Davis County', 'GA'),
 '13163': ('Jefferson County', 'GA'),
 '13165': ('Jenkins County', 'GA'),
 '13167': ('Johnson County', 'GA'),
 '13169': ('Jones County', 'GA'),
 '13171': ('Lamar County', 'GA'),
 '13173': ('Lanier County', 'GA'),
 '13175': ('Laurens County', 'GA'),
 '13177': ('Lee County', 'GA'),
 '13179': ('Liberty County', 'GA'),
 '13181': ('Lincoln County', 'GA'),
 '13183': ('Long County', 'GA'),
 '13185': ('Lowndes County', 'GA'),
 '13187': ('Lumpkin County', 'GA'),
 '13189': ('McDuffie County', 'GA'),
 '13191': ('McIntosh County', 'GA'),
 '13193': ('Macon County', 'GA'),
 '13195': ('Madison County', 'GA'),
 '13197': ('Marion County', 'GA'),
 '13199': ('Meriwether County', 'GA'),
 '13201': ('Miller County', 'GA'),
 '13205': ('Mitchell County', 'GA'),
 '13207': ('Monroe County', 'GA'),
 '13209': ('Montgomery County', 'GA'),
 '13211': ('Morgan County', 'GA'),
 '13213': ('Murray County', 'GA'),
 '13215': ('Muscogee County', 'GA'),
 '13217': ('Newton County', 'GA'),
 '13219': ('Oconee County', 'GA'),
 '13221': ('Oglethorpe County', 'GA'),
 '13223': ('Paulding County', 'GA'),
 '13225': ('Peach County', 'GA'),
 '13227': ('Pickens County', 'GA'),
 '13229': ('Pierce County', 'GA'),
 '13231': ('Pike County', 'GA'),
 '13233': ('Polk County', 'GA'),
 '13235': ('Pulaski County', 'GA'),
 '13237': ('Putnam County', 'GA'),
 '13239': ('Quitman County', 'GA'),
 '13241': ('Rabun County', 'GA'),
 '13243': ('Randolph County', 'GA'),
 '13245': ('Richmond County', 'GA'),
 '13247': ('Rockdale County', 'GA'),
 '13249': ('Schley County', 'GA'),
 '13251': ('Screven County', 'GA'),
 '13253': ('Seminole County', 'GA'),
 '13255': ('Spalding County', 'GA'),
 '13257': ('Stephens County', 'GA'),
 '13259': ('Stewart County', 'GA'),
 '13261': ('Sumter County', 'GA'),
 '13263': ('Talbot County', 'GA'),
 '13265': ('Taliaferro County', 'GA'),
 '13267': ('Tattnall County', 'GA'),
 '13269': ('Taylor County', 'GA'),
 '13271': ('Telfair County', 'GA'),
 '13273': ('Terrell County', 'GA'),
 '13275': ('Thomas County', 'GA'),
 '13277': ('Tift County', 'GA'),
 '13279': ('Toombs County', 'GA'),
 '13281': ('Towns County', 'GA'),
 '13283': ('Treutlen County', 'GA'),
 '13285': ('Troup County', 'GA'),
 '13287': ('Turner County', 'GA'),
 '13289': ('Twiggs County', 'GA'),
 '13291': ('Union County', 'GA'),
 '13293': ('Upson County', 'GA'),
 '13295': ('Walker County', 'GA'),
 '13297': ('Walton County', 'GA'),
 '13299': ('Ware County', 'GA'),
 '13301': ('Warren County', 'GA'),
 '13303': ('Washington County', 'GA'),
 '13305': ('Wayne County', 'GA'),
 '13307': ('Webster County', 'GA'),
 '13309': ('Wheeler County', 'GA'),
 '13311': ('White County', 'GA'),
 '13313': ('Whitfield County', 'GA'),
 '13315': ('Wilcox County', 'GA'),
 '13317': ('Wilkes County', 'GA'),
 '13319': ('Wilkinson County', 'GA'),
 '13321': ('Worth County', 'GA'),
 '15001': ('Hawaii County', 'HI'),
 '15003': ('Honolulu County', 'HI'),
 '15005': ('Kalawao County', 'HI'),
 '15007': ('Kauai County', 'HI'),
 '15009': ('Maui County', 'HI'),
 '16001': ('Ada County', 'ID'),
 '16003': ('Adams County', 'ID'),
 '16005': ('Bannock County', 'ID'),
 '16007': ('Bear Lake County', 'ID'),
 '16009': ('Benewah County', 'ID'),
 '16011': ('Bingham County', 'ID'),
 '16013': ('Blaine County', 'ID'),
 '16015': ('Boise County', 'ID'),
 '16017': ('Bonner County', 'ID'),
 '16019': ('Bonneville County', 'ID'),
 '16021': ('Boundary County', 'ID'),
 '16023': ('Butte County', 'ID'),
 '16025': ('Camas County', 'ID'),
 '16027': ('Canyon County', 'ID'),
 '16029': ('Caribou County', 'ID'),
 '16031': ('Cassia County', 'ID'),
 '16033': ('Clark County', 'ID'),
 '16035': ('Clearwater County', 'ID'),
 '16037': ('Custer County', 'ID'),
 '16039': ('Elmore County', 'ID'),
 '16041': ('Franklin County', 'ID'),
 '16043': ('Fremont County', 'ID'),
 '16045': ('Gem County', 'ID'),
 '16047': ('Gooding County', 'ID'),
 '16049': ('Idaho County', 'ID'),
 '16051': ('Jefferson County', 'ID'),
 '16053': ('Jerome County', 'ID'),
 '16055': ('Kootenai County', 'ID'),
 '16057': ('Latah County', 'ID'),
 '16059': ('Lemhi County', 'ID'),
 '16061': ('Lewis County', 'ID'),
 '16063': ('Lincoln County', 'ID'),
 '16065': ('Madison County', 'ID'),
 '16067': ('Minidoka County', 'ID'),
 '16069': ('Nez Perce County', 'ID'),
 '16071': ('Oneida County', 'ID'),
 '16073': ('Owyhee County', 'ID'),
 '16075': ('Payette County', 'ID'),
 '16077': ('Power County', 'ID'),
 '16079': ('Shoshone County', 'ID'),
 '16081': ('Teton County', 'ID'),
 '16083': ('Twin Falls County', 'ID'),
 '16085': ('Valley County', 'ID'),
 '16087': ('Washington County', 'ID'),
 '17001': ('Adams County', 'IL'),
 '17003': ('Alexander County', 'IL'),
 '17005': ('Bond County', 'IL'),
 '17007': ('Boone County', 'IL'),
 '17009': ('Brown County', 'IL'),
 '17011': ('Bureau County', 'IL'),
 '17013': ('Calhoun County', 'IL'),
 '17015': ('Carroll County', 'IL'),
 '17017': ('Cass County', 'IL'),
 '17019': ('Champaign County', 'IL'),
 '17021': ('Christian County', 'IL'),
 '17023': ('Clark County', 'IL'),
 '17025': ('Clay County', 'IL'),
 '17027': ('Clinton County', 'IL'),
 '17029': ('Coles County', 'IL'),
 '17031': ('Cook County', 'IL'),
 '17033': ('Crawford County', 'IL'),
 '17035': ('Cumberland County', 'IL'),
 '17037': ('DeKalb County', 'IL'),
 '17039': ('De Witt County', 'IL'),
 '17041': ('Douglas County', 'IL'),
 '17043': ('DuPage County', 'IL'),
 '17045': ('Edgar County', 'IL'),
 '17047': ('Edwards County', 'IL'),
 '17049': ('Effingham County', 'IL'),
 '17051': ('Fayette County', 'IL'),
 '17053': ('Ford County', 'IL'),
 '17055': ('Franklin County', 'IL'),
 '17057': ('Fulton County', 'IL'),
 '17059': ('Gallatin County', 'IL'),
 '17061': ('Greene County', 'IL'),
 '17063': ('Grundy County', 'IL'),
 '17065': ('Hamilton County', 'IL'),
 '17067': ('Hancock County', 'IL'),
 '17069': ('Hardin County', 'IL'),
 '17071': ('Henderson County', 'IL'),
 '17073': ('Henry County', 'IL'),
 '17075': ('Iroquois County', 'IL'),
 '17077': ('Jackson County', 'IL'),
 '17079': ('Jasper County', 'IL'),
 '17081': ('Jefferson County', 'IL'),
 '17083': ('Jersey County', 'IL'),
 '17085': ('Jo Daviess County', 'IL'),
 '17087': ('Johnson County', 'IL'),
 '17089': ('Kane County', 'IL'),
 '17091': ('Kankakee County', 'IL'),
 '17093': ('Kendall County', 'IL'),
 '17095': ('Knox County', 'IL'),
 '17097': ('Lake County', 'IL'),
 '17099': ('LaSalle County', 'IL'),
 '17101': ('Lawrence County', 'IL'),
 '17103': ('Lee County', 'IL'),
 '17105': ('Livingston County', 'IL'),
 '17107': ('Logan County', 'IL'),
 '17109': ('McDonough County', 'IL'),
 '17111': ('McHenry County', 'IL'),
 '17113': ('McLean County', 'IL'),
 '17115': ('Macon County', 'IL'),
 '17117': ('Macoupin County', 'IL'),
 '17119': ('Madison County', 'IL'),
 '17121': ('Marion County', 'IL'),
 '17123': ('Marshall County', 'IL'),
 '17125': ('Mason County', 'IL'),
 '17127': ('Massac County', 'IL'),
 '17129': ('Menard County', 'IL'),
 '17131': ('Mercer County', 'IL'),
 '17133': ('Monroe County', 'IL'),
 '17135': ('Montgomery County', 'IL'),
 '17137': ('Morgan County', 'IL'),
 '17139': ('Moultrie County', 'IL'),
 '17141': ('Ogle County', 'IL'),
 '17143': ('Peoria County', 'IL'),
 '17145': ('Perry County', 'IL'),
 '17147': ('Piatt County', 'IL'),
 '17149': ('Pike County', 'IL'),
 '17151': ('Pope County', 'IL'),
 '17153': ('Pulaski County', 'IL'),
 '17155': ('Putnam County', 'IL'),
 '17157': ('Randolph County', 'IL'),
 '17159': ('Richland County', 'IL'),
 '17161': ('Rock Island County', 'IL'),
 '17163': ('St. Clair County', 'IL'),
 '17165': ('Saline County', 'IL'),
 '17167': ('Sangamon County', 'IL'),
 '17169': ('Schuyler County', 'IL'),
 '17171': ('Scott County', 'IL'),
 '17173': ('Shelby County', 'IL'),
 '17175': ('Stark County', 'IL'),
 '17177': ('Stephenson County', 'IL'),
 '17179': ('Tazewell County', 'IL'),
 '17181': ('Union County', 'IL'),
 '17183': ('Vermilion County', 'IL'),
 '17185': ('Wabash County', 'IL'),
 '17187': ('Warren County', 'IL'),
 '17189': ('Washington County', 'IL'),
 '17191': ('Wayne County', 'IL'),
 '17193': ('White County', 'IL'),
 '17195': ('Whiteside County', 'IL'),
 '17197': ('Will County', 'IL'),
 '17199': ('Williamson County', 'IL'),
 '17201': ('Winnebago County', 'IL'),
 '17203': ('Woodford County', 'IL'),
 '18001': ('Adams County', 'IN'),
 '18003': ('Allen County', 'IN'),
 '18005': ('Bartholomew County', 'IN'),
 '18007': ('Benton County', 'IN'),
 '18009': ('Blackford County', 'IN'),
 '18011': ('Boone County', 'IN'),
 '18013': ('Brown County', 'IN'),
 '18015': ('Carroll County', 'IN'),
 '18017': ('Cass County', 'IN'),
 '18019': ('Clark County', 'IN'),
 '18021': ('Clay County', 'IN'),
 '18023': ('Clinton County', 'IN'),
 '18025': ('Crawford County', 'IN'),
 '18027': ('Daviess County', 'IN'),
 '18029': ('Dearborn County', 'IN'),
 '18031': ('Decatur County', 'IN'),
 '18033': ('DeKalb County', 'IN'),
 '18035': ('Delaware County', 'IN'),
 '18037': ('Dubois County', 'IN'),
 '18039': ('Elkhart County', 'IN'),
 '18041': ('Fayette County', 'IN'),
 '18043': ('Floyd County', 'IN'),
 '18045': ('Fountain County', 'IN'),
 '18047': ('Franklin County', 'IN'),
 '18049': ('Fulton County', 'IN'),
 '18051': ('Gibson County', 'IN'),
 '18053': ('Grant County', 'IN'),
 '18055': ('Greene County', 'IN'),
 '18057': ('Hamilton County', 'IN'),
 '18059': ('Hancock County', 'IN'),
 '18061': ('Harrison County', 'IN'),
 '18063': ('Hendricks County', 'IN'),
 '18065': ('Henry County', 'IN'),
 '18067': ('Howard County', 'IN'),
 '18069': ('Huntington County', 'IN'),
 '18071': ('Jackson County', 'IN'),
 '18073': ('Jasper County', 'IN'),
 '18075': ('Jay County', 'IN'),
 '18077': ('Jefferson County', 'IN'),
 '18079': ('Jennings County', 'IN'),
 '18081': ('Johnson County', 'IN'),
 '18083': ('Knox County', 'IN'),
 '18085': ('Kosciusko County', 'IN'),
 '18087': ('LaGrange County', 'IN'),
 '18089': ('Lake County', 'IN'),
 '18091': ('LaPorte County', 'IN'),
 '18093': ('Lawrence County', 'IN'),
 '18095': ('Madison County', 'IN'),
 '18097': ('Marion County', 'IN'),
 '18099': ('Marshall County', 'IN'),
 '18101': ('Martin County', 'IN'),
 '18103': ('Miami County', 'IN'),
 '18105': ('Monroe County', 'IN'),
 '18107': ('Montgomery County', 'IN'),
 '18109': ('Morgan County', 'IN'),
 '18111': ('Newton County', 'IN'),
 '18113': ('Noble County', 'IN'),
 '18115': ('Ohio County', 'IN'),
 '18117': ('Orange County', 'IN'),
 '18119': ('Owen County', 'IN'),
 '18121': ('Parke County', 'IN'),
 '18123': ('Perry County', 'IN'),
 '18125': ('Pike County', 'IN'),
 '18127': ('Porter County', 'IN'),
 '18129': ('Posey County', 'IN'),
 '18131': ('Pulaski County', 'IN'),
 '18133': ('Putnam County', 'IN'),
 '18135': ('Randolph County', 'IN'),
 '18137': ('Ripley County', 'IN'),
 '18139': ('Rush County', 'IN'),
 '18141': ('St. Joseph County', 'IN'),
 '18143': ('Scott County', 'IN'),
 '18145': ('Shelby County', 'IN'),
 '18147': ('Spencer County', 'IN'),
 '18149': ('Starke County', 'IN'),
 '18151': ('Steuben County', 'IN'),
 '18153': ('Sullivan County', 'IN'),
 '18155': ('Switzerland County', 'IN'),
 '18157': ('Tippecanoe County', 'IN'),
 '18159': ('Tipton County', 'IN'),
 '18161': ('Union County', 'IN'),
 '18163': ('Vanderburgh County', 'IN'),
 '18165': ('Vermillion County', 'IN'),
 '18167': ('Vigo County', 'IN'),
 '18169': ('Wabash County', 'IN'),
 '18171': ('Warren County', 'IN'),
 '18173': ('Warrick County', 'IN'),
 '18175': ('Washington County', 'IN'),
 '18177': ('Wayne County', 'IN'),
 '18179': ('Wells County', 'IN'),
 '18181': ('White County', 'IN'),
 '18183': ('Whitley County', 'IN'),
 '19001': ('Adair County', 'IA'),
 '19003': ('Adams County', 'IA'),
 '19005': ('Allamakee County', 'IA'),
 '19007': ('Appanoose County', 'IA'),
 '19009': ('Audubon County', 'IA'),
 '19011': ('Benton County', 'IA'),
 '19013': ('Black Hawk County', 'IA'),
 '19015': ('Boone County', 'IA'),
 '19017': ('Bremer County', 'IA'),
 '19019': ('Buchanan County', 'IA'),
 '19021': ('Buena Vista County', 'IA'),
 '19023': ('Butler County', 'IA'),
 '19025': ('Calhoun County', 'IA'),
 '19027': ('Carroll County', 'IA'),
 '19029': ('Cass County', 'IA'),
 '19031': ('Cedar County', 'IA'),
 '19033': ('Cerro Gordo County', 'IA'),
 '19035': ('Cherokee County', 'IA'),
 '19037': ('Chickasaw County', 'IA'),
 '19039': ('Clarke County', 'IA'),
 '19041': ('Clay County', 'IA'),
 '19043': ('Clayton County', 'IA'),
 '19045': ('Clinton County', 'IA'),
 '19047': ('Crawford County', 'IA'),
 '19049': ('Dallas County', 'IA'),
 '19051': ('Davis County', 'IA'),
 '19053': ('Decatur County', 'IA'),
 '19055': ('Delaware County', 'IA'),
 '19057': ('Des Moines County', 'IA'),
 '19059': ('Dickinson County', 'IA'),
 '19061': ('Dubuque County', 'IA'),
 '19063': ('Emmet County', 'IA'),
 '19065': ('Fayette County', 'IA'),
 '19067': ('Floyd County', 'IA'),
 '19069': ('Franklin County', 'IA'),
 '19071': ('Fremont County', 'IA'),
 '19073': ('Greene County', 'IA'),
 '19075': ('Grundy County', 'IA'),
 '19077': ('Guthrie County', 'IA'),
 '19079': ('Hamilton County', 'IA'),
 '19081': ('Hancock County', 'IA'),
 '19083': ('Hardin County', 'IA'),
 '19085': ('Harrison County', 'IA'),
 '19087': ('Henry County', 'IA'),
 '19089': ('Howard County', 'IA'),
 '19091': ('Humboldt County', 'IA'),
 '19093': ('Ida County', 'IA'),
 '19095': ('Iowa County', 'IA'),
 '19097': ('Jackson County', 'IA'),
 '19099': ('Jasper County', 'IA'),
 '19101': ('Jefferson County', 'IA'),
 '19103': ('Johnson County', 'IA'),
 '19105': ('Jones County', 'IA'),
 '19107': ('Keokuk County', 'IA'),
 '19109': ('Kossuth County', 'IA'),
 '19111': ('Lee County', 'IA'),
 '19113': ('Linn County', 'IA'),
 '19115': ('Louisa County', 'IA'),
 '19117': ('Lucas County', 'IA'),
 '19119': ('Lyon County', 'IA'),
 '19121': ('Madison County', 'IA'),
 '19123': ('Mahaska County', 'IA'),
 '19125': ('Marion County', 'IA'),
 '19127': ('Marshall County', 'IA'),
 '19129': ('Mills County', 'IA'),
 '19131': ('Mitchell County', 'IA'),
 '19133': ('Monona County', 'IA'),
 '19135': ('Monroe County', 'IA'),
 '19137': ('Montgomery County', 'IA'),
 '19139': ('Muscatine County', 'IA'),
 '19141': ("O'Brien County", 'IA'),
 '19143': ('Osceola County', 'IA'),
 '19145': ('Page County', 'IA'),
 '19147': ('Palo Alto County', 'IA'),
 '19149': ('Plymouth County', 'IA'),
 '19151': ('Pocahontas County', 'IA'),
 '19153': ('Polk County', 'IA'),
 '19155': ('Pottawattamie County', 'IA'),
 '19157': ('Poweshiek County', 'IA'),
 '19159': ('Ringgold County', 'IA'),
 '19161': ('Sac County', 'IA'),
 '19163': ('Scott County', 'IA'),
 '19165': ('Shelby County', 'IA'),
 '19167': ('Sioux County', 'IA'),
 '19169': ('Story County', 'IA'),
 '19171': ('Tama County', 'IA'),
 '19173': ('Taylor County', 'IA'),
 '19175': ('Union County', 'IA'),
 '19177': ('Van Buren County', 'IA'),
 '19179': ('Wapello County', 'IA'),
 '19181': ('Warren County', 'IA'),
 '19183': ('Washington County', 'IA'),
 '19185': ('Wayne County', 'IA'),
 '19187': ('Webster County', 'IA'),
 '19189': ('Winnebago County', 'IA'),
 '19191': ('Winneshiek County', 'IA'),
 '19193': ('Woodbury County', 'IA'),
 '19195': ('Worth County', 'IA'),
 '19197': ('Wright County', 'IA'),
 '20001': ('Allen County', 'KS'),
 '20003': ('Anderson County', 'KS'),
 '20005': ('Atchison County', 'KS'),
 '20007': ('Barber County', 'KS'),
 '20009': ('Barton County', 'KS'),
 '20011': ('Bourbon County', 'KS'),
 '20013': ('Brown County', 'KS'),
 '20015': ('Butler County', 'KS'),
 '20017': ('Chase County', 'KS'),
 '20019': ('Chautauqua County', 'KS'),
 '20021': ('Cherokee County', 'KS'),
 '20023': ('Cheyenne County', 'KS'),
 '20025': ('Clark County', 'KS'),
 '20027': ('Clay County', 'KS'),
 '20029': ('Cloud County', 'KS'),
 '20031': ('Coffey County', 'KS'),
 '20033': ('Comanche County', 'KS'),
 '20035': ('Cowley County', 'KS'),
 '20037': ('Crawford County', 'KS'),
 '20039': ('Decatur County', 'KS'),
 '20041': ('Dickinson County', 'KS'),
 '20043': ('Doniphan County', 'KS'),
 '20045': ('Douglas County', 'KS'),
 '20047': ('Edwards County', 'KS'),
 '20049': ('Elk County', 'KS'),
 '20051': ('Ellis County', 'KS'),
 '20053': ('Ellsworth County', 'KS'),
 '20055': ('Finney County', 'KS'),
 '20057': ('Ford County', 'KS'),
 '20059': ('Franklin County', 'KS'),
 '20061': ('Geary County', 'KS'),
 '20063': ('Gove County', 'KS'),
 '20065': ('Graham County', 'KS'),
 '20067': ('Grant County', 'KS'),
 '20069': ('Gray County', 'KS'),
 '20071': ('Greeley County', 'KS'),
 '20073': ('Greenwood County', 'KS'),
 '20075': ('Hamilton County', 'KS'),
 '20077': ('Harper County', 'KS'),
 '20079': ('Harvey County', 'KS'),
 '20081': ('Haskell County', 'KS'),
 '20083': ('Hodgeman County', 'KS'),
 '20085': ('Jackson County', 'KS'),
 '20087': ('Jefferson County', 'KS'),
 '20089': ('Jewell County', 'KS'),
 '20091': ('Johnson County', 'KS'),
 '20093': ('Kearny County', 'KS'),
 '20095': ('Kingman County', 'KS'),
 '20097': ('Kiowa County', 'KS'),
 '20099': ('Labette County', 'KS'),
 '20101': ('Lane County', 'KS'),
 '20103': ('Leavenworth County', 'KS'),
 '20105': ('Lincoln County', 'KS'),
 '20107': ('Linn County', 'KS'),
 '20109': ('Logan County', 'KS'),
 '20111': ('Lyon County', 'KS'),
 '20113': ('McPherson County', 'KS'),
 '20115': ('Marion County', 'KS'),
 '20117': ('Marshall County', 'KS'),
 '20119': ('Meade County', 'KS'),
 '20121': ('Miami County', 'KS'),
 '20123': ('Mitchell County', 'KS'),
 '20125': ('Montgomery County', 'KS'),
 '20127': ('Morris County', 'KS'),
 '20129': ('Morton County', 'KS'),
 '20131': ('Nemaha County', 'KS'),
 '20133': ('Neosho County', 'KS'),
 '20135': ('Ness County', 'KS'),
 '20137': ('Norton County', 'KS'),
 '20139': ('Osage County', 'KS'),
 '20141': ('Osborne County', 'KS'),
 '20143': ('Ottawa County', 'KS'),
 '20145': ('Pawnee County', 'KS'),
 '20147': ('Phillips County', 'KS'),
 '20149': ('Pottawatomie County', 'KS'),
 '20151': ('Pratt County', 'KS'),
 '20153': ('Rawlins County', 'KS'),
 '20155': ('Reno County', 'KS'),
 '20157': ('Republic County', 'KS'),
 '20159': ('Rice County', 'KS'),
 '20161': ('Riley County', 'KS'),
 '20163': ('Rooks County', 'KS'),
 '20165': ('Rush County', 'KS'),
 '20167': ('Russell County', 'KS'),
 '20169': ('Saline County', 'KS'),
 '20171': ('Scott County', 'KS'),
 '20173': ('Sedgwick County', 'KS'),
 '20175': ('Seward County', 'KS'),
 '20177': ('Shawnee County', 'KS'),
 '20179': ('Sheridan County', 'KS'),
 '20181': ('Sherman County', 'KS'),
 '20183': ('Smith County', 'KS'),
 '20185': ('Stafford County', 'KS'),
 '20187': ('Stanton County', 'KS'),
 '20189': ('Stevens County', 'KS'),
 '20191': ('Sumner County', 'KS'),
 '20193': ('Thomas County', 'KS'),
 '20195': ('Trego County', 'KS'),
 '20197': ('Wabaunsee County', 'KS'),
 '20199': ('Wallace County', 'KS'),
 '20201': ('Washington County', 'KS'),
 '20203': ('Wichita County', 'KS'),
 '20205': ('Wilson County', 'KS'),
 '20207': ('Woodson County', 'KS'),
 '20209': ('Wyandotte County', 'KS'),
 '21001': ('Adair County', 'KY'),
 '21003': ('Allen County', 'KY'),
 '21005': ('Anderson County', 'KY'),
 '21007': ('Ballard County', 'KY'),
 '21009': ('Barren County', 'KY'),
 '21011': ('Bath County', 'KY'),
 '21013': ('Bell County', 'KY'),
 '21015': ('Boone County', 'KY'),
 '21017': ('Bourbon County', 'KY'),
 '21019': ('Boyd County', 'KY'),
 '21021': ('Boyle County', 'KY'),
 '21023': ('Bracken County', 'KY'),
 '21025': ('Breathitt County', 'KY'),
 '21027': ('Breckinridge County', 'KY'),
 '21029': ('Bullitt County', 'KY'),
 '21031': ('Butler County', 'KY'),
 '21033': ('Caldwell County', 'KY'),
 '21035': ('Calloway County', 'KY'),
 '21037': ('Campbell County', 'KY'),
 '21039': ('Carlisle County', 'KY'),
 '21041': ('Carroll County', 'KY'),
 '21043': ('Carter County', 'KY'),
 '21045': ('Casey County', 'KY'),
 '21047': ('Christian County', 'KY'),
 '21049': ('Clark County', 'KY'),
 '21051': ('Clay County', 'KY'),
 '21053': ('Clinton County', 'KY'),
 '21055': ('Crittenden County', 'KY'),
 '21057': ('Cumberland County', 'KY'),
 '21059': ('Daviess County', 'KY'),
 '21061': ('Edmonson County', 'KY'),
 '21063': ('Elliott County', 'KY'),
 '21065': ('Estill County', 'KY'),
 '21067': ('Fayette County', 'KY'),
 '21069': ('Fleming County', 'KY'),
 '21071': ('Floyd County', 'KY'),
 '21073': ('Franklin County', 'KY'),
 '21075': ('Fulton County', 'KY'),
 '21077': ('Gallatin County', 'KY'),
 '21079': ('Garrard County', 'KY'),
 '21081': ('Grant County', 'KY'),
 '21083': ('Graves County', 'KY'),
 '21085': ('Grayson County', 'KY'),
 '21087': ('Green County', 'KY'),
 '21089': ('Greenup County', 'KY'),
 '21091': ('Hancock County', 'KY'),
 '21093': ('Hardin County', 'KY'),
 '21095': ('Harlan County', 'KY'),
 '21097': ('Harrison County', 'KY'),
 '21099': ('Hart County', 'KY'),
 '21101': ('Henderson County', 'KY'),
 '21103': ('Henry County', 'KY'),
 '21105': ('Hickman County', 'KY'),
 '21107': ('Hopkins County', 'KY'),
 '21109': ('Jackson County', 'KY'),
 '21111': ('Jefferson County', 'KY'),
 '21113': ('Jessamine County', 'KY'),
 '21115': ('Johnson County', 'KY'),
 '21117': ('Kenton County', 'KY'),
 '21119': ('Knott County', 'KY'),
 '21121': ('Knox County', 'KY'),
 '21123': ('Larue County', 'KY'),
 '21125': ('Laurel County', 'KY'),
 '21127': ('Lawrence County', 'KY'),
 '21129': ('Lee County', 'KY'),
 '21131': ('Leslie County', 'KY'),
 '21133': ('Letcher County', 'KY'),
 '21135': ('Lewis County', 'KY'),
 '21137': ('Lincoln County', 'KY'),
 '21139': ('Livingston County', 'KY'),
 '21141': ('Logan County', 'KY'),
 '21143': ('Lyon County', 'KY'),
 '21145': ('McCracken County', 'KY'),
 '21147': ('McCreary County', 'KY'),
 '21149': ('McLean County', 'KY'),
 '21151': ('Madison County', 'KY'),
 '21153': ('Magoffin County', 'KY'),
 '21155': ('Marion County', 'KY'),
 '21157': ('Marshall County', 'KY'),
 '21159': ('Martin County', 'KY'),
 '21161': ('Mason County', 'KY'),
 '21163': ('Meade County', 'KY'),
 '21165': ('Menifee County', 'KY'),
 '21167': ('Mercer County', 'KY'),
 '21169': ('Metcalfe County', 'KY'),
 '21171': ('Monroe County', 'KY'),
 '21173': ('Montgomery County', 'KY'),
 '21175': ('Morgan County', 'KY'),
 '21177': ('Muhlenberg County', 'KY'),
 '21179': ('Nelson County', 'KY'),
 '21181': ('Nicholas County', 'KY'),
 '21183': ('Ohio County', 'KY'),
 '21185': ('Oldham County', 'KY'),
 '21187': ('Owen County', 'KY'),
 '21189': ('Owsley County', 'KY'),
 '21191': ('Pendleton County', 'KY'),
 '21193': ('Perry County', 'KY'),
 '21195': ('Pike County', 'KY'),
 '21197': ('Powell County', 'KY'),
 '21199': ('Pulaski County', 'KY'),
 '21201': ('Robertson County', 'KY'),
 '21203': ('Rockcastle County', 'KY'),
 '21205': ('Rowan County', 'KY'),
 '21207': ('Russell County', 'KY'),
 '21209': ('Scott County', 'KY'),
 '21211': ('Shelby County', 'KY'),
 '21213': ('Simpson County', 'KY'),
 '21215': ('Spencer County', 'KY'),
 '21217': ('Taylor County', 'KY'),
 '21219': ('Todd County', 'KY'),
 '21221': ('Trigg County', 'KY'),
 '21223': ('Trimble County', 'KY'),
 '21225': ('Union County', 'KY'),
 '21227': ('Warren County', 'KY'),
 '21229': ('Washington County', 'KY'),
 '21231': ('Wayne County', 'KY'),
 '21233': ('Webster County', 'KY'),
 '21235': ('Whitley County', 'KY'),
 '21237': ('Wolfe County', 'KY'),
 '21239': ('Woodford County', 'KY'),
 '22001': ('Acadia Parish', 'LA'),
 '22003': ('Allen Parish', 'LA'),
 '22005': ('Ascension Parish', 'LA'),
 '22007': ('Assumption Parish', 'LA'),
 '22009': ('Avoyelles Parish', 'LA'),
 '22011': ('Beauregard Parish', 'LA'),
 '22013': ('Bienville Parish', 'LA'),
 '22015': ('Bossier Parish', 'LA'),
 '22017': ('Caddo Parish', 'LA'),
 '22019': ('Calcasieu Parish', 'LA'),
 '22021': ('Caldwell Parish', 'LA'),
 '22023': ('Cameron Parish', 'LA'),
 '22025': ('Catahoula Parish', 'LA'),
 '22027': ('Claiborne Parish', 'LA'),
 '22029': ('Concordia Parish', 'LA'),
 '22031': ('De Soto Parish', 'LA'),
 '22033': ('East Baton Rouge Parish', 'LA'),
 '22035': ('East Carroll Parish', 'LA'),
 '22037': ('East Feliciana Parish', 'LA'),
 '22039': ('Evangeline Parish', 'LA'),
 '22041': ('Franklin Parish', 'LA'),
 '22043': ('Grant Parish', 'LA'),
 '22045': ('Iberia Parish', 'LA'),
 '22047': ('Iberville Parish', 'LA'),
 '22049': ('Jackson Parish', 'LA'),
 '22051': ('Jefferson Parish', 'LA'),
 '22053': ('Jefferson Davis Parish', 'LA'),
 '22055': ('Lafayette Parish', 'LA'),
 '22057': ('Lafourche Parish', 'LA'),
 '22059': ('La Salle Parish', 'LA'),
 '22061': ('Lincoln Parish', 'LA'),
 '22063': ('Livingston Parish', 'LA'),
 '22065': ('Madison Parish', 'LA'),
 '22067': ('Morehouse Parish', 'LA'),
 '22069': ('Natchitoches Parish', 'LA'),
 '22071': ('Orleans Parish', 'LA'),
 '22073': ('Ouachita Parish', 'LA'),
 '22075': ('Plaquemines Parish', 'LA'),
 '22077': ('Pointe Coupee Parish', 'LA'),
 '22079': ('Rapides Parish', 'LA'),
 '22081': ('Red River Parish', 'LA'),
 '22083': ('Richland Parish', 'LA'),
 '22085': ('Sabine Parish', 'LA'),
 '22087': ('St. Bernard Parish', 'LA'),
 '22089': ('St. Charles Parish', 'LA'),
 '22091': ('St. Helena Parish', 'LA'),
 '22093': ('St. James Parish', 'LA'),
 '22095': ('St. John the Baptist Parish', 'LA'),
 '22097': ('St. Landry Parish', 'LA'),
 '22099': ('St. Martin Parish', 'LA'),
 '22101': ('St. Mary Parish', 'LA'),
 '22103': ('St. Tammany Parish', 'LA'),
 '22105': ('Tangipahoa Parish', 'LA'),
 '22107': ('Tensas Parish', 'LA'),
 '22109': ('Terrebonne Parish', 'LA'),
 '22111': ('Union Parish', 'LA'),
 '22113': ('Vermilion Parish', 'LA'),
 '22115': ('Vernon Parish', 'LA'),
 '22117': ('Washington Parish', 'LA'),
 '22119': ('Webster Parish', 'LA'),
 '22121': ('West Baton Rouge Parish', 'LA'),
 '22123': ('West Carroll Parish', 'LA'),
 '22125': ('West Feliciana Parish', 'LA'),
 '22127': ('Winn Parish', 'LA'),
 '23001': ('Androscoggin County', 'ME'),
 '23003': ('Aroostook County', 'ME'),
 '23005': ('Cumberland County', 'ME'),
 '23007': ('Franklin County', 'ME'),
 '23009': ('Hancock County', 'ME'),
 '23011': ('Kennebec County', 'ME'),
 '23013': ('Knox County', 'ME'),
 '23015': ('Lincoln County', 'ME'),
 '23017': ('Oxford County', 'ME'),
 '23019': ('Penobscot County', 'ME'),
 '23021': ('Piscataquis County', 'ME'),
 '23023': ('Sagadahoc County', 'ME'),
 '23025': ('Somerset County', 'ME'),
 '23027': ('Waldo County', 'ME'),
 '23029': ('Washington County', 'ME'),
 '23031': ('York County', 'ME'),
 '24001': ('Allegany County', 'MD'),
 '24003': ('Anne Arundel County', 'MD'),
 '24005': ('Baltimore County', 'MD'),
 '24009': ('Calvert County', 'MD'),
 '24011': ('Caroline County', 'MD'),
 '24013': ('Carroll County', 'MD'),
 '24015': ('Cecil County', 'MD'),
 '24017': ('Charles County', 'MD'),
 '24019': ('Dorchester County', 'MD'),
 '24021': ('Frederick County', 'MD'),
 '24023': ('Garrett County', 'MD'),
 '24025': ('Harford County', 'MD'),
 '24027': ('Howard County', 'MD'),
 '24029': ('Kent County', 'MD'),
 '24031': ('Montgomery County', 'MD'),
 '24033': ("Prince George's County", 'MD'),
 '24035': ("Queen Anne's County", 'MD'),
 '24037': ("St. Mary's County", 'MD'),
 '24039': ('Somerset County', 'MD'),
 '24041': ('Talbot County', 'MD'),
 '24043': ('Washington County', 'MD'),
 '24045': ('Wicomico County', 'MD'),
 '24047': ('Worcester County', 'MD'),
 '24510': ('Baltimore city', 'MD'),
 '25001': ('Barnstable County', 'MA'),
 '25003': ('Berkshire County', 'MA'),
 '25005': ('Bristol County', 'MA'),
 '25007': ('Dukes County', 'MA'),
 '25009': ('Essex County', 'MA'),
 '25011': ('Franklin County', 'MA'),
 '25013': ('Hampden County', 'MA'),
 '25015': ('Hampshire County', 'MA'),
 '25017': ('Middlesex County', 'MA'),
 '25019': ('Nantucket County', 'MA'),
 '25021': ('Norfolk County', 'MA'),
 '25023': ('Plymouth County', 'MA'),
 '25025': ('Suffolk County', 'MA'),
 '25027': ('Worcester County', 'MA'),
 '26001': ('Alcona County', 'MI'),
 '26003': ('Alger County', 'MI'),
 '26005': ('Allegan County', 'MI'),
 '26007': ('Alpena County', 'MI'),
 '26009': ('Antrim County', 'MI'),
 '26011': ('Arenac County', 'MI'),
 '26013': ('Baraga County', 'MI'),
 '26015': ('Barry County', 'MI'),
 '26017': ('Bay County', 'MI'),
 '26019': ('Benzie County', 'MI'),
 '26021': ('Berrien County', 'MI'),
 '26023': ('Branch County', 'MI'),
 '26025': ('Calhoun County', 'MI'),
 '26027': ('Cass County', 'MI'),
 '26029': ('Charlevoix County', 'MI'),
 '26031': ('Cheboygan County', 'MI'),
 '26033': ('Chippewa County', 'MI'),
 '26035': ('Clare County', 'MI'),
 '26037': ('Clinton County', 'MI'),
 '26039': ('Crawford County', 'MI'),
 '26041': ('Delta County', 'MI'),
 '26043': ('Dickinson County', 'MI'),
 '26045': ('Eaton County', 'MI'),
 '26047': ('Emmet County', 'MI'),
 '26049': ('Genesee County', 'MI'),
 '26051': ('Gladwin County', 'MI'),
 '26053': ('Gogebic County', 'MI'),
 '26055': ('Grand Traverse County', 'MI'),
 '26057': ('Gratiot County', 'MI'),
 '26059': ('Hillsdale County', 'MI'),
 '26061': ('Houghton County', 'MI'),
 '26063': ('Huron County', 'MI'),
 '26065': ('Ingham County', 'MI'),
 '26067': ('Ionia County', 'MI'),
 '26069': ('Iosco County', 'MI'),
 '26071': ('Iron County', 'MI'),
 '26073': ('Isabella County', 'MI'),
 '26075': ('Jackson County', 'MI'),
 '26077': ('Kalamazoo County', 'MI'),
 '26079': ('Kalkaska County', 'MI'),
 '26081': ('Kent County', 'MI'),
 '26083': ('Keweenaw County', 'MI'),
 '26085': ('Lake County', 'MI'),
 '26087': ('Lapeer County', 'MI'),
 '26089': ('Leelanau County', 'MI'),
 '26091': ('Lenawee County', 'MI'),
 '26093': ('Livingston County', 'MI'),
 '26095': ('Luce County', 'MI'),
 '26097': ('Mackinac County', 'MI'),
 '26099': ('Macomb County', 'MI'),
 '26101': ('Manistee County', 'MI'),
 '26103': ('Marquette County', 'MI'),
 '26105': ('Mason County', 'MI'),
 '26107': ('Mecosta County', 'MI'),
 '26109': ('Menominee County', 'MI'),
 '26111': ('Midland County', 'MI'),
 '26113': ('Missaukee County', 'MI'),
 '26115': ('Monroe County', 'MI'),
 '26117': ('Montcalm County', 'MI'),
 '26119': ('Montmorency County', 'MI'),
 '26121': ('Muskegon County', 'MI'),
 '26123': ('Newaygo County', 'MI'),
 '26125': ('Oakland County', 'MI'),
 '26127': ('Oceana County', 'MI'),
 '26129': ('Ogemaw County', 'MI'),
 '26131': ('Ontonagon County', 'MI'),
 '26133': ('Osceola County', 'MI'),
 '26135': ('Oscoda County', 'MI'),
 '26137': ('Otsego County', 'MI'),
 '26139': ('Ottawa County', 'MI'),
 '26141': ('Presque Isle County', 'MI'),
 '26143': ('Roscommon County', 'MI'),
 '26145': ('Saginaw County', 'MI'),
 '26147': ('St. Clair County', 'MI'),
 '26149': ('St. Joseph County', 'MI'),
 '26151': ('Sanilac County', 'MI'),
 '26153': ('Schoolcraft County', 'MI'),
 '26155': ('Shiawassee County', 'MI'),
 '26157': ('Tuscola County', 'MI'),
 '26159': ('Van Buren County', 'MI'),
 '26161': ('Washtenaw County', 'MI'),
 '26163': ('Wayne County', 'MI'),
 '26165': ('Wexford County', 'MI'),
 '27001': ('Aitkin County', 'MN'),
 '27003': ('Anoka County', 'MN'),
 '27005': ('Becker County', 'MN'),
 '27007': ('Beltrami County', 'MN'),
 '27009': ('Benton County', 'MN'),
 '27011': ('Big Stone County', 'MN'),
 '27013': ('Blue Earth County', 'MN'),
 '27015': ('Brown County', 'MN'),
 '27017': ('Carlton County', 'MN'),
 '27019': ('Carver County', 'MN'),
 '27021': ('Cass County', 'MN'),
 '27023': ('Chippewa County', 'MN'),
 '27025': ('Chisago County', 'MN'),
 '27027': ('Clay County', 'MN'),
 '27029': ('Clearwater County', 'MN'),
 '27031': ('Cook County', 'MN'),
 '27033': ('Cottonwood County', 'MN'),
 '27035': ('Crow Wing County', 'MN'),
 '27037': ('Dakota County', 'MN'),
 '27039': ('Dodge County', 'MN'),
 '27041': ('Douglas County', 'MN'),
 '27043': ('Faribault County', 'MN'),
 '27045': ('Fillmore County', 'MN'),
 '27047': ('Freeborn County', 'MN'),
 '27049': ('Goodhue County', 'MN'),
 '27051': ('Grant County', 'MN'),
 '27053': ('Hennepin County', 'MN'),
 '27055': ('Houston County', 'MN'),
 '27057': ('Hubbard County', 'MN'),
 '27059': ('Isanti County', 'MN'),
 '27061': ('Itasca County', 'MN'),
 '27063': ('Jackson County', 'MN'),
 '27065': ('Kanabec County', 'MN'),
 '27067': ('Kandiyohi County', 'MN'),
 '27069': ('Kittson County', 'MN'),
 '27071': ('Koochiching County', 'MN'),
 '27073': ('Lac qui Parle County', 'MN'),
 '27075': ('Lake County', 'MN'),
 '27077': ('Lake of the Woods County', 'MN'),
 '27079': ('Le Sueur County', 'MN'),
 '27081': ('Lincoln County', 'MN'),
 '27083': ('Lyon County', 'MN'),
 '27085': ('McLeod County', 'MN'),
 '27087': ('Mahnomen County', 'MN'),
 '27089': ('Marshall County', 'MN'),
 '27091': ('Martin County', 'MN'),
 '27093': ('Meeker County', 'MN'),
 '27095': ('Mille Lacs County', 'MN'),
 '27097': ('Morrison County', 'MN'),
 '27099': ('Mower County', 'MN'),
 '27101': ('Murray County', 'MN'),
 '27103': ('Nicollet County', 'MN'),
 '27105': ('Nobles County', 'MN'),
 '27107': ('Norman County', 'MN'),
 '27109': ('Olmsted County', 'MN'),
 '27111': ('Otter Tail County', 'MN'),
 '27113': ('Pennington County', 'MN'),
 '27115': ('Pine County', 'MN'),
 '27117': ('Pipestone County', 'MN'),
 '27119': ('Polk County', 'MN'),
 '27121': ('Pope County', 'MN'),
 '27123': ('Ramsey County', 'MN'),
 '27125': ('Red Lake County', 'MN'),
 '27127': ('Redwood County', 'MN'),
 '27129': ('Renville County', 'MN'),
 '27131': ('Rice County', 'MN'),
 '27133': ('Rock County', 'MN'),
 '27135': ('Roseau County', 'MN'),
 '27137': ('St. Louis County', 'MN'),
 '27139': ('Scott County', 'MN'),
 '27141': ('Sherburne County', 'MN'),
 '27143': ('Sibley County', 'MN'),
 '27145': ('Stearns County', 'MN'),
 '27147': ('Steele County', 'MN'),
 '27149': ('Stevens County', 'MN'),
 '27151': ('Swift County', 'MN'),
 '27153': ('Todd County', 'MN'),
 '27155': ('Traverse County', 'MN'),
 '27157': ('Wabasha County', 'MN'),
 '27159': ('Wadena County', 'MN'),
 '27161': ('Waseca County', 'MN'),
 '27163': ('Washington County', 'MN'),
 '27165': ('Watonwan County', 'MN'),
 '27167': ('Wilkin County', 'MN'),
 '27169': ('Winona County', 'MN'),
 '27171': ('Wright County', 'MN'),
 '27173': ('Yellow Medicine County', 'MN'),
 '28001': ('Adams County', 'MS'),
 '28003': ('Alcorn County', 'MS'),
 '28005': ('Amite County', 'MS'),
 '28007': ('Attala County', 'MS'),
 '28009': ('Benton County', 'MS'),
 '28011': ('Bolivar County', 'MS'),
 '28013': ('Calhoun County', 'MS'),
 '28015': ('Carroll County', 'MS'),
 '28017': ('Chickasaw County', 'MS'),
 '28019': ('Choctaw County', 'MS'),
 '28021': ('Claiborne County', 'MS'),
 '28023': ('Clarke County', 'MS'),
 '28025': ('Clay County', 'MS'),
 '28027': ('Coahoma County', 'MS'),
 '28029': ('Copiah County', 'MS'),
 '28031': ('Covington County', 'MS'),
 '28033': ('DeSoto County', 'MS'),
 '28035': ('Forrest County', 'MS'),
 '28037': ('Franklin County', 'MS'),
 '28039': ('George County', 'MS'),
 '28041': ('Greene County', 'MS'),
 '28043': ('Grenada County', 'MS'),
 '28045': ('Hancock County', 'MS'),
 '28047': ('Harrison County', 'MS'),
 '28049': ('Hinds County', 'MS'),
 '28051': ('Holmes County', 'MS'),
 '28053': ('Humphreys County', 'MS'),
 '28055': ('Issaquena County', 'MS'),
 '28057': ('Itawamba County', 'MS'),
 '28059': ('Jackson County', 'MS'),
 '28061': ('Jasper County', 'MS'),
 '28063': ('Jefferson County', 'MS'),
 '28065': ('Jefferson Davis County', 'MS'),
 '28067': ('Jones County', 'MS'),
 '28069': ('Kemper County', 'MS'),
 '28071': ('Lafayette County', 'MS'),
 '28073': ('Lamar County', 'MS'),
 '28075': ('Lauderdale County', 'MS'),
 '28077': ('Lawrence County', 'MS'),
 '28079': ('Leake County', 'MS'),
 '28081': ('Lee County', 'MS'),
 '28083': ('Leflore County', 'MS'),
 '28085': ('Lincoln County', 'MS'),
 '28087': ('Lowndes County', 'MS'),
 '28089': ('Madison County', 'MS'),
 '28091': ('Marion County', 'MS'),
 '28093': ('Marshall County', 'MS'),
 '28095': ('Monroe County', 'MS'),
 '28097': ('Montgomery County', 'MS'),
 '28099': ('Neshoba County', 'MS'),
 '28101': ('Newton County', 'MS'),
 '28103': ('Noxubee County', 'MS'),
 '28105': ('Oktibbeha County', 'MS'),
 '28107': ('Panola County', 'MS'),
 '28109': ('Pearl River County', 'MS'),
 '28111': ('Perry County', 'MS'),
 '28113': ('Pike County', 'MS'),
 '28115': ('Pontotoc County', 'MS'),
 '28117': ('Prentiss County', 'MS'),
 '28119': ('Quitman County', 'MS'),
 '28121': ('Rankin County', 'MS'),
 '28123': ('Scott County', 'MS'),
 '28125': ('Sharkey County', 'MS'),
 '28127': ('Simpson County', 'MS'),
 '28129': ('Smith County', 'MS'),
 '28131': ('Stone County', 'MS'),
 '28133': ('Sunflower County', 'MS'),
 '28135': ('Tallahatchie County', 'MS'),
 '28137': ('Tate County', 'MS'),
 '28139': ('Tippah County', 'MS'),
 '28141': ('Tishomingo County', 'MS'),
 '28143': ('Tunica County', 'MS'),
 '28145': ('Union County', 'MS'),
 '28147': ('Walthall County', 'MS'),
 '28149': ('Warren County', 'MS'),
 '28151': ('Washington County', 'MS'),
 '28153': ('Wayne County', 'MS'),
 '28155': ('Webster County', 'MS'),
 '28157': ('Wilkinson County', 'MS'),
 '28159': ('Winston County', 'MS'),
 '28161': ('Yalobusha County', 'MS'),
 '28163': ('Yazoo County', 'MS'),
 '29001': ('Adair County', 'MO'),
 '29003': ('Andrew County', 'MO'),
 '29005': ('Atchison County', 'MO'),
 '29007': ('Audrain County', 'MO'),
 '29009': ('Barry County', 'MO'),
 '29011': ('Barton County', 'MO'),
 '29013': ('Bates County', 'MO'),
 '29015': ('Benton County', 'MO'),
 '29017': ('Bollinger County', 'MO'),
 '29019': ('Boone County', 'MO'),
 '29021': ('Buchanan County', 'MO'),
 '29023': ('Butler County', 'MO'),
 '29025': ('Caldwell County', 'MO'),
 '29027': ('Callaway County', 'MO'),
 '29029': ('Camden County', 'MO'),
 '29031': ('Cape Girardeau County', 'MO'),
 '29033': ('Carroll County', 'MO'),
 '29035': ('Carter County', 'MO'),
 '29037': ('Cass County', 'MO'),
 '29039': ('Cedar County', 'MO'),
 '29041': ('Chariton County', 'MO'),
 '29043': ('Christian County', 'MO'),
 '29045': ('Clark County', 'MO'),
 '29047': ('Clay County', 'MO'),
 '29049': ('Clinton County', 'MO'),
 '29051': ('Cole County', 'MO'),
 '29053': ('Cooper County', 'MO'),
 '29055': ('Crawford County', 'MO'),
 '29057': ('Dade County', 'MO'),
 '29059': ('Dallas County', 'MO'),
 '29061': ('Daviess County', 'MO'),
 '29063': ('DeKalb County', 'MO'),
 '29065': ('Dent County', 'MO'),
 '29067': ('Douglas County', 'MO'),
 '29069': ('Dunklin County', 'MO'),
 '29071': ('Franklin County', 'MO'),
 '29073': ('Gasconade County', 'MO'),
 '29075': ('Gentry County', 'MO'),
 '29077': ('Greene County', 'MO'),
 '29079': ('Grundy County', 'MO'),
 '29081': ('Harrison County', 'MO'),
 '29083': ('Henry County', 'MO'),
 '29085': ('Hickory County', 'MO'),
 '29087': ('Holt County', 'MO'),
 '29089': ('Howard County', 'MO'),
 '29091': ('Howell County', 'MO'),
 '29093': ('Iron County', 'MO'),
 '29095': ('Jackson County', 'MO'),
 '29097': ('Jasper County', 'MO'),
 '29099': ('Jefferson County', 'MO'),
 '29101': ('Johnson County', 'MO'),
 '29103': ('Knox County', 'MO'),
 '29105': ('Laclede County', 'MO'),
 '29107': ('Lafayette County', 'MO'),
 '29109': ('Lawrence County', 'MO'),
 '29111': ('Lewis County', 'MO'),
 '29113': ('Lincoln County', 'MO'),
 '29115': ('Linn County', 'MO'),
 '29117': ('Livingston County', 'MO'),
 '29119': ('McDonald County', 'MO'),
 '29121': ('Macon County', 'MO'),
 '29123': ('Madison County', 'MO'),
 '29125': ('Maries County', 'MO'),
 '29127': ('Marion County', 'MO'),
 '29129': ('Mercer County', 'MO'),
 '29131': ('Miller County', 'MO'),
 '29133': ('Mississippi County', 'MO'),
 '29135': ('Moniteau County', 'MO'),
 '29137': ('Monroe County', 'MO'),
 '29139': ('Montgomery County', 'MO'),
 '29141': ('Morgan County', 'MO'),
 '29143': ('New Madrid County', 'MO'),
 '29145': ('Newton County', 'MO'),
 '29147': ('Nodaway County', 'MO'),
 '29149': ('Oregon County', 'MO'),
 '29151': ('Osage County', 'MO'),
 '29153': ('Ozark County', 'MO'),
 '29155': ('Pemiscot County', 'MO'),
 '29157': ('Perry County', 'MO'),
 '29159': ('Pettis County', 'MO'),
 '29161': ('Phelps County', 'MO'),
 '29163': ('Pike County', 'MO'),
 '29165': ('Platte County', 'MO'),
 '29167': ('Polk County', 'MO'),
 '29169': ('Pulaski County', 'MO'),
 '29171': ('Putnam County', 'MO'),
 '29173': ('Ralls County', 'MO'),
 '29175': ('Randolph County', 'MO'),
 '29177': ('Ray County', 'MO'),
 '29179': ('Reynolds County', 'MO'),
 '29181': ('Ripley County', 'MO'),
 '29183': ('St. Charles County', 'MO'),
 '29185': ('St. Clair County', 'MO'),
 '29186': ('Ste. Genevieve County', 'MO'),
 '29187': ('St. Francois County', 'MO'),
 '29189': ('St. Louis County', 'MO'),
 '29195': ('Saline County', 'MO'),
 '29197': ('Schuyler County', 'MO'),
 '29199': ('Scotland County', 'MO'),
 '29201': ('Scott County', 'MO'),
 '29203': ('Shannon County', 'MO'),
 '29205': ('Shelby County', 'MO'),
 '29207': ('Stoddard County', 'MO'),
 '29209': ('Stone County', 'MO'),
 '29211': ('Sullivan County', 'MO'),
 '29213': ('Taney County', 'MO'),
 '29215': ('Texas County', 'MO'),
 '29217': ('Vernon County', 'MO'),
 '29219': ('Warren County', 'MO'),
 '29221': ('Washington County', 'MO'),
 '29223': ('Wayne County', 'MO'),
 '29225': ('Webster County', 'MO'),
 '29227': ('Worth County', 'MO'),
 '29229': ('Wright County', 'MO'),
 '29510': ('St. Louis city', 'MO'),
 '30001': ('Beaverhead County', 'MT'),
 '30003': ('Big Horn County', 'MT'),
 '30005': ('Blaine County', 'MT'),
 '30007': ('Broadwater County', 'MT'),
 '30009': ('Carbon County', 'MT'),
 '30011': ('Carter County', 'MT'),
 '30013': ('Cascade County', 'MT'),
 '30015': ('Chouteau County', 'MT'),
 '30017': ('Custer County', 'MT'),
 '30019': ('Daniels County', 'MT'),
 '30021': ('Dawson County', 'MT'),
 '30023': ('Deer Lodge County', 'MT'),
 '30025': ('Fallon County', 'MT'),
 '30027': ('Fergus County', 'MT'),
 '30029': ('Flathead County', 'MT'),
 '30031': ('Gallatin County', 'MT'),
 '30033': ('Garfield County', 'MT'),
 '30035': ('Glacier County', 'MT'),
 '30037': ('Golden Valley County', 'MT'),
 '30039': ('Granite County', 'MT'),
 '30041': ('Hill County', 'MT'),
 '30043': ('Jefferson County', 'MT'),
 '30045': ('Judith Basin County', 'MT'),
 '30047': ('Lake County', 'MT'),
 '30049': ('Lewis and Clark County', 'MT'),
 '30051': ('Liberty County', 'MT'),
 '30053': ('Lincoln County', 'MT'),
 '30055': ('McCone County', 'MT'),
 '30057': ('Madison County', 'MT'),
 '30059': ('Meagher County', 'MT'),
 '30061': ('Mineral County', 'MT'),
 '30063': ('Missoula County', 'MT'),
 '30065': ('Musselshell County', 'MT'),
 '30067': ('Park County', 'MT'),
 '30069': ('Petroleum County', 'MT'),
 '30071': ('Phillips County', 'MT'),
 '30073': ('Pondera County', 'MT'),
 '30075': ('Powder River County', 'MT'),
 '30077': ('Powell County', 'MT'),
 '30079': ('Prairie County', 'MT'),
 '30081': ('Ravalli County', 'MT'),
 '30083': ('Richland County', 'MT'),
 '30085': ('Roosevelt County', 'MT'),
 '30087': ('Rosebud County', 'MT'),
 '30089': ('Sanders County', 'MT'),
 '30091': ('Sheridan County', 'MT'),
 '30093': ('Silver Bow County', 'MT'),
 '30095': ('Stillwater County', 'MT'),
 '30097': ('Sweet Grass County', 'MT'),
 '30099': ('Teton County', 'MT'),
 '30101': ('Toole County', 'MT'),
 '30103': ('Treasure County', 'MT'),
 '30105': ('Valley County', 'MT'),
 '30107': ('Wheatland County', 'MT'),
 '30109': ('Wibaux County', 'MT'),
 '30111': ('Yellowstone County', 'MT'),
 '31001': ('Adams County', 'NE'),
 '31003': ('Antelope County', 'NE'),
 '31005': ('Arthur County', 'NE'),
 '31007': ('Banner County', 'NE'),
 '31009': ('Blaine County', 'NE'),
 '31011': ('Boone County', 'NE'),
 '31013': ('Box Butte County', 'NE'),
 '31015': ('Boyd County', 'NE'),
 '31017': ('Brown County', 'NE'),
 '31019': ('Buffalo County', 'NE'),
 '31021': ('Burt County', 'NE'),
 '31023': ('Butler County', 'NE'),
 '31025': ('Cass County', 'NE'),
 '31027': ('Cedar County', 'NE'),
 '31029': ('Chase County', 'NE'),
 '31031': ('Cherry County', 'NE'),
 '31033': ('Cheyenne County', 'NE'),
 '31035': ('Clay County', 'NE'),
 '31037': ('Colfax County', 'NE'),
 '31039': ('Cuming County', 'NE'),
 '31041': ('Custer County', 'NE'),
 '31043': ('Dakota County', 'NE'),
 '31045': ('Dawes County', 'NE'),
 '31047': ('Dawson County', 'NE'),
 '31049': ('Deuel County', 'NE'),
 '31051': ('Dixon County', 'NE'),
 '31053': ('Dodge County', 'NE'),
 '31055': ('Douglas County', 'NE'),
 '31057': ('Dundy County', 'NE'),
 '31059': ('Fillmore County', 'NE'),
 '31061': ('Franklin County', 'NE'),
 '31063': ('Frontier County', 'NE'),
 '31065': ('Furnas County', 'NE'),
 '31067': ('Gage County', 'NE'),
 '31069': ('Garden County', 'NE'),
 '31071': ('Garfield County', 'NE'),
 '31073': ('Gosper County', 'NE'),
 '31075': ('Grant County', 'NE'),
 '31077': ('Greeley County', 'NE'),
 '31079': ('Hall County', 'NE'),
 '31081': ('Hamilton County', 'NE'),
 '31083': ('Harlan County', 'NE'),
 '31085': ('Hayes County', 'NE'),
 '31087': ('Hitchcock County', 'NE'),
 '31089': ('Holt County', 'NE'),
 '31091': ('Hooker County', 'NE'),
 '31093': ('Howard County', 'NE'),
 '31095': ('Jefferson County', 'NE'),
 '31097': ('Johnson County', 'NE'),
 '31099': ('Kearney County', 'NE'),
 '31101': ('Keith County', 'NE'),
 '31103': ('Keya Paha County', 'NE'),
 '31105': ('Kimball County', 'NE'),
 '31107': ('Knox County', 'NE'),
 '31109': ('Lancaster County', 'NE'),
 '31111': ('Lincoln County', 'NE'),
 '31113': ('Logan County', 'NE'),
 '31115': ('Loup County', 'NE'),
 '31117': ('McPherson County', 'NE'),
 '31119': ('Madison County', 'NE'),
 '31121': ('Merrick County', 'NE'),
 '31123': ('Morrill County', 'NE'),
 '31125': ('Nance County', 'NE'),
 '31127': ('Nemaha County', 'NE'),
 '31129': ('Nuckolls County', 'NE'),
 '31131': ('Otoe County', 'NE'),
 '31133': ('Pawnee County', 'NE'),
 '31135': ('Perkins County', 'NE'),
 '31137': ('Phelps County', 'NE'),
 '31139': ('Pierce County', 'NE'),
 '31141': ('Platte County', 'NE'),
 '31143': ('Polk County', 'NE'),
 '31145': ('Red Willow County', 'NE'),
 '31147': ('Richardson County', 'NE'),
 '31149': ('Rock County', 'NE'),
 '31151': ('Saline County', 'NE'),
 '31153': ('Sarpy County', 'NE'),
 '31155': ('Saunders County', 'NE'),
 '31157': ('Scotts Bluff County', 'NE'),
 '31159': ('Seward County', 'NE'),
 '31161': ('Sheridan County', 'NE'),
 '31163': ('Sherman County', 'NE'),
 '31165': ('Sioux County', 'NE'),
 '31167': ('Stanton County', 'NE'),
 '31169': ('Thayer County', 'NE'),
 '31171': ('Thomas County', 'NE'),
 '31173': ('Thurston County', 'NE'),
 '31175': ('Valley County', 'NE'),
 '31177': ('Washington County', 'NE'),
 '31179': ('Wayne County', 'NE'),
 '31181': ('Webster County', 'NE'),
 '31183': ('Wheeler County', 'NE'),
 '31185': ('York County', 'NE'),
 '32001': ('Churchill County', 'NV'),
 '32003': ('Clark County', 'NV'),
 '32005': ('Douglas County', 'NV'),
 '32007': ('Elko County', 'NV'),
 '32009': ('Esmeralda County', 'NV'),
 '32011': ('Eureka County', 'NV'),
 '32013': ('Humboldt County', 'NV'),
 '32015': ('Lander County', 'NV'),
 '32017': ('Lincoln County', 'NV'),
 '32019': ('Lyon County', 'NV'),
 '32021': ('Mineral County', 'NV'),
 '32023': ('Nye County', 'NV'),
 '32027': ('Pershing County', 'NV'),
 '32029': ('Storey County', 'NV'),
 '32031': ('Washoe County', 'NV'),
 '32033': ('White Pine County', 'NV'),
 '32510': ('Carson City', 'NV'),
 '33001': ('Belknap County', 'NH'),
 '33003': ('Carroll County', 'NH'),
 '33005': ('Cheshire County', 'NH'),
 '33007': ('Coos County', 'NH'),
 '33009': ('Grafton County', 'NH'),
 '33011': ('Hillsborough County', 'NH'),
 '33013': ('Merrimack County', 'NH'),
 '33015': ('Rockingham County', 'NH'),
 '33017': ('Strafford County', 'NH'),
 '33019': ('Sullivan County', 'NH'),
 '34001': ('Atlantic County', 'NJ'),
 '34003': ('Bergen County', 'NJ'),
 '34005': ('Burlington County', 'NJ'),
 '34007': ('Camden County', 'NJ'),
 '34009': ('Cape May County', 'NJ'),
 '34011': ('Cumberland County', 'NJ'),
 '34013': ('Essex County', 'NJ'),
 '34015': ('Gloucester County', 'NJ'),
 '34017': ('Hudson County', 'NJ'),
 '34019': ('Hunterdon County', 'NJ'),
 '34021': ('Mercer County', 'NJ'),
 '34023': ('Middlesex County', 'NJ'),
 '34025': ('Monmouth County', 'NJ'),
 '34027': ('Morris County', 'NJ'),
 '34029': ('Ocean County', 'NJ'),
 '34031': ('Passaic County', 'NJ'),
 '34033': ('Salem County', 'NJ'),
 '34035': ('Somerset County', 'NJ'),
 '34037': ('Sussex County', 'NJ'),
 '34039': ('Union County', 'NJ'),
 '34041': ('Warren County', 'NJ'),
 '35001': ('Bernalillo County', 'NM'),
 '35003': ('Catron County', 'NM'),
 '35005': ('Chaves County', 'NM'),
 '35006': ('Cibola County', 'NM'),
 '35007': ('Colfax County', 'NM'),
 '35009': ('Curry County', 'NM'),
 '35011': ('De Baca County', 'NM'),
 '35013': ('Dona Ana County', 'NM'),
 '35015': ('Eddy County', 'NM'),
 '35017': ('Grant County', 'NM'),
 '35019': ('Guadalupe County', 'NM'),
 '35021': ('Harding County', 'NM'),
 '35023': ('Hidalgo County', 'NM'),
 '35025': ('Lea County', 'NM'),
 '35027': ('Lincoln County', 'NM'),
 '35028': ('Los Alamos County', 'NM'),
 '35029': ('Luna County', 'NM'),
 '35031': ('McKinley County', 'NM'),
 '35033': ('Mora County', 'NM'),
 '35035': ('Otero County', 'NM'),
 '35037': ('Quay County', 'NM'),
 '35039': ('Rio Arriba County', 'NM'),
 '35041': ('Roosevelt County', 'NM'),
 '35043': ('Sandoval County', 'NM'),
 '35045': ('San Juan County', 'NM'),
 '35047': ('San Miguel County', 'NM'),
 '35049': ('Santa Fe County', 'NM'),
 '35051': ('Sierra County', 'NM'),
 '35053': ('Socorro County', 'NM'),
 '35055': ('Taos County', 'NM'),
 '35057': ('Torrance County', 'NM'),
 '35059': ('Union County', 'NM'),
 '35061': ('Valencia County', 'NM'),
 '36001': ('Albany County', 'NY'),
 '36003': ('Allegany County', 'NY'),
 '36005': ('Bronx County', 'NY'),
 '36007': ('Broome County', 'NY'),
 '36009': ('Cattaraugus County', 'NY'),
 '36011': ('Cayuga County', 'NY'),
 '36013': ('Chautauqua County', 'NY'),
 '36015': ('Chemung County', 'NY'),
 '36017': ('Chenango County', 'NY'),
 '36019': ('Clinton County', 'NY'),
 '36021': ('Columbia County', 'NY'),
 '36023': ('Cortland County', 'NY'),
 '36025': ('Delaware County', 'NY'),
 '36027': ('Dutchess County', 'NY'),
 '36029': ('Erie County', 'NY'),
 '36031': ('Essex County', 'NY'),
 '36033': ('Franklin County', 'NY'),
 '36035': ('Fulton County', 'NY'),
 '36037': ('Genesee County', 'NY'),
 '36039': ('Greene County', 'NY'),
 '36041': ('Hamilton County', 'NY'),
 '36043': ('Herkimer County', 'NY'),
 '36045': ('Jefferson County', 'NY'),
 '36047': ('Kings County', 'NY'),
 '36049': ('Lewis County', 'NY'),
 '36051': ('Livingston County', 'NY'),
 '36053': ('Madison County', 'NY'),
 '36055': ('Monroe County', 'NY'),
 '36057': ('Montgomery County', 'NY'),
 '36059': ('Nassau County', 'NY'),
 '36061': ('New York County', 'NY'),
 '36063': ('Niagara County', 'NY'),
 '36065': ('Oneida County', 'NY'),
 '36067': ('Onondaga County', 'NY'),
 '36069': ('Ontario County', 'NY'),
 '36071': ('Orange County', 'NY'),
 '36073': ('Orleans County', 'NY'),
 '36075': ('Oswego County', 'NY'),
 '36077': ('Otsego County', 'NY'),
 '36079': ('Putnam County', 'NY'),
 '36081': ('Queens County', 'NY'),
 '36083': ('Rensselaer County', 'NY'),
 '36085': ('Richmond County', 'NY'),
 '36087': ('Rockland County', 'NY'),
 '36089': ('St. Lawrence County', 'NY'),
 '36091': ('Saratoga County', 'NY'),
 '36093': ('Schenectady County', 'NY'),
 '36095': ('Schoharie County', 'NY'),
 '36097': ('Schuyler County', 'NY'),
 '36099': ('Seneca County', 'NY'),
 '36101': ('Steuben County', 'NY'),
 '36103': ('Suffolk County', 'NY'),
 '36105': ('Sullivan County', 'NY'),
 '36107': ('Tioga County', 'NY'),
 '36109': ('Tompkins County', 'NY'),
 '36111': ('Ulster County', 'NY'),
 '36113': ('Warren County', 'NY'),
 '36115': ('Washington County', 'NY'),
 '36117': ('Wayne County', 'NY'),
 '36119': ('Westchester County', 'NY'),
 '36121': ('Wyoming County', 'NY'),
 '36123': ('Yates County', 'NY'),
 '37001': ('Alamance County', 'NC'),
 '37003': ('Alexander County', 'NC'),
 '37005': ('Alleghany County', 'NC'),
 '37007': ('Anson County', 'NC'),
 '37009': ('Ashe County', 'NC'),
 '37011': ('Avery County', 'NC'),
 '37013': ('Beaufort County', 'NC'),
 '37015': ('Bertie County', 'NC'),
 '37017': ('Bladen County', 'NC'),
 '37019': ('Brunswick County', 'NC'),
 '37021': ('Buncombe County', 'NC'),
 '37023': ('Burke County', 'NC'),
 '37025': ('Cabarrus County', 'NC'),
 '37027': ('Caldwell County', 'NC'),
 '37029': ('Camden County', 'NC'),
 '37031': ('Carteret County', 'NC'),
 '37033': ('Caswell County', 'NC'),
 '37035': ('Catawba County', 'NC'),
 '37037': ('Chatham County', 'NC'),
 '37039': ('Cherokee County', 'NC'),
 '37041': ('Chowan County', 'NC'),
 '37043': ('Clay County', 'NC'),
 '37045': ('Cleveland County', 'NC'),
 '37047': ('Columbus County', 'NC'),
 '37049': ('Craven County', 'NC'),
 '37051': ('Cumberland County', 'NC'),
 '37053': ('Currituck County', 'NC'),
 '37055': ('Dare County', 'NC'),
 '37057': ('Davidson County', 'NC'),
 '37059': ('Davie County', 'NC'),
 '37061': ('Duplin County', 'NC'),
 '37063': ('Durham County', 'NC'),
 '37065': ('Edgecombe County', 'NC'),
 '37067': ('Forsyth County', 'NC'),
 '37069': ('Franklin County', 'NC'),
 '37071': ('Gaston County', 'NC'),
 '37073': ('Gates County', 'NC'),
 '37075': ('Graham County', 'NC'),
 '37077': ('Granville County', 'NC'),
 '37079': ('Greene County', 'NC'),
 '37081': ('Guilford County', 'NC'),
 '37083': ('Halifax County', 'NC'),
 '37085': ('Harnett County', 'NC'),
 '37087': ('Haywood County', 'NC'),
 '37089': ('Henderson County', 'NC'),
 '37091': ('Hertford County', 'NC'),
 '37093': ('Hoke County', 'NC'),
 '37095': ('Hyde County', 'NC'),
 '37097': ('Iredell County', 'NC'),
 '37099': ('Jackson County', 'NC'),
 '37101': ('Johnston County', 'NC'),
 '37103': ('Jones County', 'NC'),
 '37105': ('Lee County', 'NC'),
 '37107': ('Lenoir County', 'NC'),
 '37109': ('Lincoln County', 'NC'),
 '37111': ('McDowell County', 'NC'),
 '37113': ('Macon County', 'NC'),
 '37115': ('Madison County', 'NC'),
 '37117': ('Martin County', 'NC'),
 '37119': ('Mecklenburg County', 'NC'),
 '37121': ('Mitchell County', 'NC'),
 '37123': ('Montgomery County', 'NC'),
 '37125': ('Moore County', 'NC'),
 '37127': ('Nash County', 'NC'),
 '37129': ('New Hanover County', 'NC'),
 '37131': ('Northampton County', 'NC'),
 '37133': ('Onslow County', 'NC'),
 '37135': ('Orange County', 'NC'),
 '37137': ('Pamlico County', 'NC'),
 '37139': ('Pasquotank County', 'NC'),
 '37141': ('Pender County', 'NC'),
 '37143': ('Perquimans County', 'NC'),
 '37145': ('Person County', 'NC'),
 '37147': ('Pitt County', 'NC'),
 '37149': ('Polk County', 'NC'),
 '37151': ('Randolph County', 'NC'),
 '37153': ('Richmond County', 'NC'),
 '37155': ('Robeson County', 'NC'),
 '37157': ('Rockingham County', 'NC'),
 '37159': ('Rowan County', 'NC'),
 '37161': ('Rutherford County', 'NC'),
 '37163': ('Sampson County', 'NC'),
 '37165': ('Scotland County', 'NC'),
 '37167': ('Stanly County', 'NC'),
 '37169': ('Stokes County', 'NC'),
 '37171': ('Surry County', 'NC'),
 '37173': ('Swain County', 'NC'),
 '37175': ('Transylvania County', 'NC'),
 '37177': ('Tyrrell County', 'NC'),
 '37179': ('Union County', 'NC'),
 '37181': ('Vance County', 'NC'),
 '37183': ('Wake County', 'NC'),
 '37185': ('Warren County', 'NC'),
 '37187': ('Washington County', 'NC'),
 '37189': ('Watauga County', 'NC'),
 '37191': ('Wayne County', 'NC'),
 '37193': ('Wilkes County', 'NC'),
 '37195': ('Wilson County', 'NC'),
 '37197': ('Yadkin County', 'NC'),
 '37199': ('Yancey County', 'NC'),
 '38001': ('Adams County', 'ND'),
 '38003': ('Barnes County', 'ND'),
 '38005': ('Benson County', 'ND'),
 '38007': ('Billings County', 'ND'),
 '38009': ('Bottineau County', 'ND'),
 '38011': ('Bowman County', 'ND'),
 '38013': ('Burke County', 'ND'),
 '38015': ('Burleigh County', 'ND'),
 '38017': ('Cass County', 'ND'),
 '38019': ('Cavalier County', 'ND'),
 '38021': ('Dickey County', 'ND'),
 '38023': ('Divide County', 'ND'),
 '38025': ('Dunn County', 'ND'),
 '38027': ('Eddy County', 'ND'),
 '38029': ('Emmons County', 'ND'),
 '38031': ('Foster County', 'ND'),
 '38033': ('Golden Valley County', 'ND'),
 '38035': ('Grand Forks County', 'ND'),
 '38037': ('Grant County', 'ND'),
 '38039': ('Griggs County', 'ND'),
 '38041': ('Hettinger County', 'ND'),
 '38043': ('Kidder County', 'ND'),
 '38045': ('LaMoure County', 'ND'),
 '38047': ('Logan County', 'ND'),
 '38049': ('McHenry County', 'ND'),
 '38051': ('McIntosh County', 'ND'),
 '38053': ('McKenzie County', 'ND'),
 '38055': ('McLean County', 'ND'),
 '38057': ('Mercer County', 'ND'),
 '38059': ('Morton County', 'ND'),
 '38061': ('Mountrail County', 'ND'),
 '38063': ('Nelson County', 'ND'),
 '38065': ('Oliver County', 'ND'),
 '38067': ('Pembina County', 'ND'),
 '38069': ('Pierce County', 'ND'),
 '38071': ('Ramsey County', 'ND'),
 '38073': ('Ransom County', 'ND'),
 '38075': ('Renville County', 'ND'),
 '38077': ('Richland County', 'ND'),
 '38079': ('Rolette County', 'ND'),
 '38081': ('Sargent County', 'ND'),
 '38083': ('Sheridan County', 'ND'),
 '38085': ('Sioux County', 'ND'),
 '38087': ('Slope County', 'ND'),
 '38089': ('Stark County', 'ND'),
 '38091': ('Steele County', 'ND'),
 '38093': ('Stutsman County', 'ND'),
 '38095': ('Towner County', 'ND'),
 '38097': ('Traill County', 'ND'),
 '38099': ('Walsh County', 'ND'),
 '38101': ('Ward County', 'ND'),
 '38103': ('Wells County', 'ND'),
 '38105': ('Williams County', 'ND'),
 '39001': ('Adams County', 'OH'),
 '39003': ('Allen County', 'OH'),
 '39005': ('Ashland County', 'OH'),
 '39007': ('Ashtabula County', 'OH'),
 '39009': ('Athens County', 'OH'),
 '39011': ('Auglaize County', 'OH'),
 '39013': ('Belmont County', 'OH'),
 '39015': ('Brown County', 'OH'),
 '39017': ('Butler County', 'OH'),
 '39019': ('Carroll County', 'OH'),
 '39021': ('Champaign County', 'OH'),
 '39023': ('Clark County', 'OH'),
 '39025': ('Clermont County', 'OH'),
 '39027': ('Clinton County', 'OH'),
 '39029': ('Columbiana County', 'OH'),
 '39031': ('Coshocton County', 'OH'),
 '39033': ('Crawford County', 'OH'),
 '39035': ('Cuyahoga County', 'OH'),
 '39037': ('Darke County', 'OH'),
 '39039': ('Defiance County', 'OH'),
 '39041': ('Delaware County', 'OH'),
 '39043': ('Erie County', 'OH'),
 '39045': ('Fairfield County', 'OH'),
 '39047': ('Fayette County', 'OH'),
 '39049': ('Franklin County', 'OH'),
 '39051': ('Fulton County', 'OH'),
 '39053': ('Gallia County', 'OH'),
 '39055': ('Geauga County', 'OH'),
 '39057': ('Greene County', 'OH'),
 '39059': ('Guernsey County', 'OH'),
 '39061': ('Hamilton County', 'OH'),
 '39063': ('Hancock County', 'OH'),
 '39065': ('Hardin County', 'OH'),
 '39067': ('Harrison County', 'OH'),
 '39069': ('Henry County', 'OH'),
 '39071': ('Highland County', 'OH'),
 '39073': ('Hocking County', 'OH'),
 '39075': ('Holmes County', 'OH'),
 '39077': ('Huron County', 'OH'),
 '39079': ('Jackson County', 'OH'),
 '39081': ('Jefferson County', 'OH'),
 '39083': ('Knox County', 'OH'),
 '39085': ('Lake County', 'OH'),
 '39087': ('Lawrence County', 'OH'),
 '39089': ('Licking County', 'OH'),
 '39091': ('Logan County', 'OH'),
 '39093': ('Lorain County', 'OH'),
 '39095': ('Lucas County', 'OH'),
 '39097': ('Madison County', 'OH'),
 '39099': ('Mahoning County', 'OH'),
 '39101': ('Marion County', 'OH'),
 '39103': ('Medina County', 'OH'),
 '39105': ('Meigs County', 'OH'),
 '39107': ('Mercer County', 'OH'),
 '39109': ('Miami County', 'OH'),
 '39111': ('Monroe County', 'OH'),
 '39113': ('Montgomery County', 'OH'),
 '39115': ('Morgan County', 'OH'),
 '39117': ('Morrow County', 'OH'),
 '39119': ('Muskingum County', 'OH'),
 '39121': ('Noble County', 'OH'),
 '39123': ('Ottawa County', 'OH'),
 '39125': ('Paulding County', 'OH'),
 '39127': ('Perry County', 'OH'),
 '39129': ('Pickaway County', 'OH'),
 '39131': ('Pike County', 'OH'),
 '39133': ('Portage County', 'OH'),
 '39135': ('Preble County', 'OH'),
 '39137': ('Putnam County', 'OH'),
 '39139': ('Richland County', 'OH'),
 '39141': ('Ross County', 'OH'),
 '39143': ('Sandusky County', 'OH'),
 '39145': ('Scioto County', 'OH'),
 '39147': ('Seneca County', 'OH'),
 '39149': ('Shelby County', 'OH'),
 '39151': ('Stark County', 'OH'),
 '39153': ('Summit County', 'OH'),
 '39155': ('Trumbull County', 'OH'),
 '39157': ('Tuscarawas County', 'OH'),
 '39159': ('Union County', 'OH'),
 '39161': ('Van Wert County', 'OH'),
 '39163': ('Vinton County', 'OH'),
 '39165': ('Warren County', 'OH'),
 '39167': ('Washington County', 'OH'),
 '39169': ('Wayne County', 'OH'),
 '39171': ('Williams County', 'OH'),
 '39173': ('Wood County', 'OH'),
 '39175': ('Wyandot County', 'OH'),
 '40001': ('Adair County', 'OK'),
 '40003': ('Alfalfa County', 'OK'),
 '40005': ('Atoka County', 'OK'),
 '40007': ('Beaver County', 'OK'),
 '40009': ('Beckham County', 'OK'),
 '40011': ('Blaine County', 'OK'),
 '40013': ('Bryan County', 'OK'),
 '40015': ('Caddo County', 'OK'),
 '40017': ('Canadian County', 'OK'),
 '40019': ('Carter County', 'OK'),
 '40021': ('Cherokee County', 'OK'),
 '40023': ('Choctaw County', 'OK'),
 '40025': ('Cimarron County', 'OK'),
 '40027': ('Cleveland County', 'OK'),
 '40029': ('Coal County', 'OK'),
 '40031': ('Comanche County', 'OK'),
 '40033': ('Cotton County', 'OK'),
 '40035': ('Craig County', 'OK'),
 '40037': ('Creek County', 'OK'),
 '40039': ('Custer County', 'OK'),
 '40041': ('Delaware County', 'OK'),
 '40043': ('Dewey County', 'OK'),
 '40045': ('Ellis County', 'OK'),
 '40047': ('Garfield County', 'OK'),
 '40049': ('Garvin County', 'OK'),
 '40051': ('Grady County', 'OK'),
 '40053': ('Grant County', 'OK'),
 '40055': ('Greer County', 'OK'),
 '40057': ('Harmon County', 'OK'),
 '40059': ('Harper County', 'OK'),
 '40061': ('Haskell County', 'OK'),
 '40063': ('Hughes County', 'OK'),
 '40065': ('Jackson County', 'OK'),
 '40067': ('Jefferson County', 'OK'),
 '40069': ('Johnston County', 'OK'),
 '40071': ('Kay County', 'OK'),
 '40073': ('Kingfisher County', 'OK'),
 '40075': ('Kiowa County', 'OK'),
 '40077': ('Latimer County', 'OK'),
 '40079': ('Le Flore County', 'OK'),
 '40081': ('Lincoln County', 'OK'),
 '40083': ('Logan County', 'OK'),
 '40085': ('Love County', 'OK'),
 '40087': ('McClain County', 'OK'),
 '40089': ('McCurtain County', 'OK'),
 '40091': ('McIntosh County', 'OK'),
 '40093': ('Major County', 'OK'),
 '40095': ('Marshall County', 'OK'),
 '40097': ('Mayes County', 'OK'),
 '40099': ('Murray County', 'OK'),
 '40101': ('Muskogee County', 'OK'),
 '40103': ('Noble County', 'OK'),
 '40105': ('Nowata County', 'OK'),
 '40107': ('Okfuskee County', 'OK'),
 '40109': ('Oklahoma County', 'OK'),
 '40111': ('Okmulgee County', 'OK'),
 '40113': ('Osage County', 'OK'),
 '40115': ('Ottawa County', 'OK'),
 '40117': ('Pawnee County', 'OK'),
 '40119': ('Payne County', 'OK'),
 '40121': ('Pittsburg County', 'OK'),
 '40123': ('Pontotoc County', 'OK'),
 '40125': ('Pottawatomie County', 'OK'),
 '40127': ('Pushmataha County', 'OK'),
 '40129': ('Roger Mills County', 'OK'),
 '40131': ('Rogers County', 'OK'),
 '40133': ('Seminole County', 'OK'),
 '40135': ('Sequoyah County', 'OK'),
 '40137': ('Stephens County', 'OK'),
 '40139': ('Texas County', 'OK'),
 '40141': ('Tillman County', 'OK'),
 '40143': ('Tulsa County', 'OK'),
 '40145': ('Wagoner County', 'OK'),
 '40147': ('Washington County', 'OK'),
 '40149': ('Washita County', 'OK'),
 '40151': ('Woods County', 'OK'),
 '40153': ('Woodward County', 'OK'),
 '41001': ('Baker County', 'OR'),
 '41003': ('Benton County', 'OR'),
 '41005': ('Clackamas County', 'OR'),
 '41007': ('Clatsop County', 'OR'),
 '41009': ('Columbia County', 'OR'),
 '41011': ('Coos County', 'OR'),
 '41013': ('Crook County', 'OR'),
 '41015': ('Curry County', 'OR'),
 '41017': ('Deschutes County', 'OR'),
 '41019': ('Douglas County', 'OR'),
 '41021': ('Gilliam County', 'OR'),
 '41023': ('Grant County', 'OR'),
 '41025': ('Harney County', 'OR'),
 '41027': ('Hood River County', 'OR'),
 '41029': ('Jackson County', 'OR'),
 '41031': ('Jefferson County', 'OR'),
 '41033': ('Josephine County', 'OR'),
 '41035': ('Klamath County', 'OR'),
 '41037': ('Lake County', 'OR'),
 '41039': ('Lane County', 'OR'),
 '41041': ('Lincoln County', 'OR'),
 '41043': ('Linn County', 'OR'),
 '41045': ('Malheur County', 'OR'),
 '41047': ('Marion County', 'OR'),
 '41049': ('Morrow County', 'OR'),
 '41051': ('Multnomah County', 'OR'),
 '41053': ('Polk County', 'OR'),
 '41055': ('Sherman County', 'OR'),
 '41057': ('Tillamook County', 'OR'),
 '41059': ('Umatilla County', 'OR'),
 '41061': ('Union County', 'OR'),
 '41063': ('Wallowa County', 'OR'),
 '41065': ('Wasco County', 'OR'),
 '41067': ('Washington County', 'OR'),
 '41069': ('Wheeler County', 'OR'),
 '41071': ('Yamhill County', 'OR'),
 '42001': ('Adams County', 'PA'),
 '42003': ('Allegheny County', 'PA'),
 '42005': ('Armstrong County', 'PA'),
 '42007': ('Beaver County', 'PA'),
 '42009': ('Bedford County', 'PA'),
 '42011': ('Berks County', 'PA'),
 '42013': ('Blair County', 'PA'),
 '42015': ('Bradford County', 'PA'),
 '42017': ('Bucks County', 'PA'),
 '42019': ('Butler County', 'PA'),
 '42021': ('Cambria County', 'PA'),
 '42023': ('Cameron County', 'PA'),
 '42025': ('Carbon County', 'PA'),
 '42027': ('Centre County', 'PA'),
 '42029': ('Chester County', 'PA'),
 '42031': ('Clarion County', 'PA'),
 '42033': ('Clearfield County', 'PA'),
 '42035': ('Clinton County', 'PA'),
 '42037': ('Columbia County', 'PA'),
 '42039': ('Crawford County', 'PA'),
 '42041': ('Cumberland County', 'PA'),
 '42043': ('Dauphin County', 'PA'),
 '42045': ('Delaware County', 'PA'),
 '42047': ('Elk County', 'PA'),
 '42049': ('Erie County', 'PA'),
 '42051': ('Fayette County', 'PA'),
 '42053': ('Forest County', 'PA'),
 '42055': ('Franklin County', 'PA'),
 '42057': ('Fulton County', 'PA'),
 '42059': ('Greene County', 'PA'),
 '42061': ('Huntingdon County', 'PA'),
 '42063': ('Indiana County', 'PA'),
 '42065': ('Jefferson County', 'PA'),
 '42067': ('Juniata County', 'PA'),
 '42069': ('Lackawanna County', 'PA'),
 '42071': ('Lancaster County', 'PA'),
 '42073': ('Lawrence County', 'PA'),
 '42075': ('Lebanon County', 'PA'),
 '42077': ('Lehigh County', 'PA'),
 '42079': ('Luzerne County', 'PA'),
 '42081': ('Lycoming County', 'PA'),
 '42083': ('McKean County', 'PA'),
 '42085': ('Mercer County', 'PA'),
 '42087': ('Mifflin County', 'PA'),
 '42089': ('Monroe County', 'PA'),
 '42091': ('Montgomery County', 'PA'),
 '42093': ('Montour County', 'PA'),
 '42095': ('Northampton County', 'PA'),
 '42097': ('Northumberland County', 'PA'),
 '42099': ('Perry County', 'PA'),
 '42101': ('Philadelphia County', 'PA'),
 '42103': ('Pike County', 'PA'),
 '42105': ('Potter County', 'PA'),
 '42107': ('Schuylkill County', 'PA'),
 '42109': ('Snyder County', 'PA'),
 '42111': ('Somerset County', 'PA'),
 '42113': ('Sullivan County', 'PA'),
 '42115': ('Susquehanna County', 'PA'),
 '42117': ('Tioga County', 'PA'),
 '42119': ('Union County', 'PA'),
 '42121': ('Venango County', 'PA'),
 '42123': ('Warren County', 'PA'),
 '42125': ('Washington County', 'PA'),
 '42127': ('Wayne County', 'PA'),
 '42129': ('Westmoreland County', 'PA'),
 '42131': ('Wyoming County', 'PA'),
 '42133': ('York County', 'PA'),
 '44001': ('Bristol County', 'RI'),
 '44003': ('Kent County', 'RI'),
 '44005': ('Newport County', 'RI'),
 '44007': ('Providence County', 'RI'),
 '44009': ('Washington County', 'RI'),
 '45001': ('Abbeville County', 'SC'),
 '45003': ('Aiken County', 'SC'),
 '45005': ('Allendale County', 'SC'),
 '45007': ('Anderson County', 'SC'),
 '45009': ('Bamberg County', 'SC'),
 '45011': ('Barnwell County', 'SC'),
 '45013': ('Beaufort County', 'SC'),
 '45015': ('Berkeley County', 'SC'),
 '45017': ('Calhoun County', 'SC'),
 '45019': ('Charleston County', 'SC'),
 '45021': ('Cherokee County', 'SC'),
 '45023': ('Chester County', 'SC'),
 '45025': ('Chesterfield County', 'SC'),
 '45027': ('Clarendon County', 'SC'),
 '45029': ('Colleton County', 'SC'),
 '45031': ('Darlington County', 'SC'),
 '45033': ('Dillon County', 'SC'),
 '45035': ('Dorchester County', 'SC'),
 '45037': ('Edgefield County', 'SC'),
 '45039': ('Fairfield County', 'SC'),
 '45041': ('Florence County', 'SC'),
 '45043': ('Georgetown County', 'SC'),
 '45045': ('Greenville County', 'SC'),
 '45047': ('Greenwood County', 'SC'),
 '45049': ('Hampton County', 'SC'),
 '45051': ('Horry County', 'SC'),
 '45053': ('Jasper County', 'SC'),
 '45055': ('Kershaw County', 'SC'),
 '45057': ('Lancaster County', 'SC'),
 '45059': ('Laurens County', 'SC'),
 '45061': ('Lee County', 'SC'),
 '45063': ('Lexington County', 'SC'),
 '45065': ('McCormick County', 'SC'),
 '45067': ('Marion County', 'SC'),
 '45069': ('Marlboro County', 'SC'),
 '45071': ('Newberry County', 'SC'),
 '45073': ('Oconee County', 'SC'),
 '45075': ('Orangeburg County', 'SC'),
 '45077': ('Pickens County', 'SC'),
 '45079': ('Richland County', 'SC'),
 '45081': ('Saluda County', 'SC'),
 '45083': ('Spartanburg County', 'SC'),
 '45085': ('Sumter County', 'SC'),
 '45087': ('Union County', 'SC'),
 '45089': ('Williamsburg County', 'SC'),
 '45091': ('York County', 'SC'),
 '46003': ('Aurora County', 'SD'),
 '46005': ('Beadle County', 'SD'),
 '46007': ('Bennett County', 'SD'),
 '46009': ('Bon Homme County', 'SD'),
 '46011': ('Brookings County', 'SD'),
 '46013': ('Brown County', 'SD'),
 '46015': ('Brule County', 'SD'),
 '46017': ('Buffalo County', 'SD'),
 '46019': ('Butte County', 'SD'),
 '46021': ('Campbell County', 'SD'),
 '46023': ('Charles Mix County', 'SD'),
 '46025': ('Clark County', 'SD'),
 '46027': ('Clay County', 'SD'),
 '46029': ('Codington County', 'SD'),
 '46031': ('Corson County', 'SD'),
 '46033': ('Custer County', 'SD'),
 '46035': ('Davison County', 'SD'),
 '46037': ('Day County', 'SD'),
 '46039': ('Deuel County', 'SD'),
 '46041': ('Dewey County', 'SD'),
 '46043': ('Douglas County', 'SD'),
 '46045': ('Edmunds County', 'SD'),
 '46047': ('Fall River County', 'SD'),
 '46049': ('Faulk County', 'SD'),
 '46051': ('Grant County', 'SD'),
 '46053': ('Gregory County', 'SD'),
 '46055': ('Haakon County', 'SD'),
 '46057': ('Hamlin County', 'SD'),
 '46059': ('Hand County', 'SD'),
 '46061': ('Hanson County', 'SD'),
 '46063': ('Harding County', 'SD'),
 '46065': ('Hughes County', 'SD'),
 '46067': ('Hutchinson County', 'SD'),
 '46069': ('Hyde County', 'SD'),
 '46071': ('Jackson County', 'SD'),
 '46073': ('Jerauld County', 'SD'),
 '46075': ('Jones County', 'SD'),
 '46077': ('Kingsbury County', 'SD'),
 '46079': ('Lake County', 'SD'),
 '46081': ('Lawrence County', 'SD'),
 '46083': ('Lincoln County', 'SD'),
 '46085': ('Lyman County', 'SD'),
 '46087': ('McCook County', 'SD'),
 '46089': ('McPherson County', 'SD'),
 '46091': ('Marshall County', 'SD'),
 '46093': ('Meade County', 'SD'),
 '46095': ('Mellette County', 'SD'),
 '46097': ('Miner County', 'SD'),
 '46099': ('Minnehaha County', 'SD'),
 '46101': ('Moody County', 'SD'),
 '46103': ('Pennington County', 'SD'),
 '46105': ('Perkins County', 'SD'),
 '46107': ('Potter County', 'SD'),
 '46109': ('Roberts County', 'SD'),
 '46111': ('Sanborn County', 'SD'),
 '46113': ('Shannon County', 'SD'),
 '46115': ('Spink County', 'SD'),
 '46117': ('Stanley County', 'SD'),
 '46119': ('Sully County', 'SD'),
 '46121': ('Todd County', 'SD'),
 '46123': ('Tripp County', 'SD'),
 '46125': ('Turner County', 'SD'),
 '46127': ('Union County', 'SD'),
 '46129': ('Walworth County', 'SD'),
 '46135': ('Yankton County', 'SD'),
 '46137': ('Ziebach County', 'SD'),
 '47001': ('Anderson County', 'TN'),
 '47003': ('Bedford County', 'TN'),
 '47005': ('Benton County', 'TN'),
 '47007': ('Bledsoe County', 'TN'),
 '47009': ('Blount County', 'TN'),
 '47011': ('Bradley County', 'TN'),
 '47013': ('Campbell County', 'TN'),
 '47015': ('Cannon County', 'TN'),
 '47017': ('Carroll County', 'TN'),
 '47019': ('Carter County', 'TN'),
 '47021': ('Cheatham County', 'TN'),
 '47023': ('Chester County', 'TN'),
 '47025': ('Claiborne County', 'TN'),
 '47027': ('Clay County', 'TN'),
 '47029': ('Cocke County', 'TN'),
 '47031': ('Coffee County', 'TN'),
 '47033': ('Crockett County', 'TN'),
 '47035': ('Cumberland County', 'TN'),
 '47037': ('Davidson County', 'TN'),
 '47039': ('Decatur County', 'TN'),
 '47041': ('DeKalb County', 'TN'),
 '47043': ('Dickson County', 'TN'),
 '47045': ('Dyer County', 'TN'),
 '47047': ('Fayette County', 'TN'),
 '47049': ('Fentress County', 'TN'),
 '47051': ('Franklin County', 'TN'),
 '47053': ('Gibson County', 'TN'),
 '47055': ('Giles County', 'TN'),
 '47057': ('Grainger County', 'TN'),
 '47059': ('Greene County', 'TN'),
 '47061': ('Grundy County', 'TN'),
 '47063': ('Hamblen County', 'TN'),
 '47065': ('Hamilton County', 'TN'),
 '47067': ('Hancock County', 'TN'),
 '47069': ('Hardeman County', 'TN'),
 '47071': ('Hardin County', 'TN'),
 '47073': ('Hawkins County', 'TN'),
 '47075': ('Haywood County', 'TN'),
 '47077': ('Henderson County', 'TN'),
 '47079': ('Henry County', 'TN'),
 '47081': ('Hickman County', 'TN'),
 '47083': ('Houston County', 'TN'),
 '47085': ('Humphreys County', 'TN'),
 '47087': ('Jackson County', 'TN'),
 '47089': ('Jefferson County', 'TN'),
 '47091': ('Johnson County', 'TN'),
 '47093': ('Knox County', 'TN'),
 '47095': ('Lake County', 'TN'),
 '47097': ('Lauderdale County', 'TN'),
 '47099': ('Lawrence County', 'TN'),
 '47101': ('Lewis County', 'TN'),
 '47103': ('Lincoln County', 'TN'),
 '47105': ('Loudon County', 'TN'),
 '47107': ('McMinn County', 'TN'),
 '47109': ('McNairy County', 'TN'),
 '47111': ('Macon County', 'TN'),
 '47113': ('Madison County', 'TN'),
 '47115': ('Marion County', 'TN'),
 '47117': ('Marshall County', 'TN'),
 '47119': ('Maury County', 'TN'),
 '47121': ('Meigs County', 'TN'),
 '47123': ('Monroe County', 'TN'),
 '47125': ('Montgomery County', 'TN'),
 '47127': ('Moore County', 'TN'),
 '47129': ('Morgan County', 'TN'),
 '47131': ('Obion County', 'TN'),
 '47133': ('Overton County', 'TN'),
 '47135': ('Perry County', 'TN'),
 '47137': ('Pickett County', 'TN'),
 '47139': ('Polk County', 'TN'),
 '47141': ('Putnam County', 'TN'),
 '47143': ('Rhea County', 'TN'),
 '47145': ('Roane County', 'TN'),
 '47147': ('Robertson County', 'TN'),
 '47149': ('Rutherford County', 'TN'),
 '47151': ('Scott County', 'TN'),
 '47153': ('Sequatchie County', 'TN'),
 '47155': ('Sevier County', 'TN'),
 '47157': ('Shelby County', 'TN'),
 '47159': ('Smith County', 'TN'),
 '47161': ('Stewart County', 'TN'),
 '47163': ('Sullivan County', 'TN'),
 '47165': ('Sumner County', 'TN'),
 '47167': ('Tipton County', 'TN'),
 '47169': ('Trousdale County', 'TN'),
 '47171': ('Unicoi County', 'TN'),
 '47173': ('Union County', 'TN'),
 '47175': ('Van Buren County', 'TN'),
 '47177': ('Warren County', 'TN'),
 '47179': ('Washington County', 'TN'),
 '47181': ('Wayne County', 'TN'),
 '47183': ('Weakley County', 'TN'),
 '47185': ('White County', 'TN'),
 '47187': ('Williamson County', 'TN'),
 '47189': ('Wilson County', 'TN'),
 '48001': ('Anderson County', 'TX'),
 '48003': ('Andrews County', 'TX'),
 '48005': ('Angelina County', 'TX'),
 '48007': ('Aransas County', 'TX'),
 '48009': ('Archer County', 'TX'),
 '48011': ('Armstrong County', 'TX'),
 '48013': ('Atascosa County', 'TX'),
 '48015': ('Austin County', 'TX'),
 '48017': ('Bailey County', 'TX'),
 '48019': ('Bandera County', 'TX'),
 '48021': ('Bastrop County', 'TX'),
 '48023': ('Baylor County', 'TX'),
 '48025': ('Bee County', 'TX'),
 '48027': ('Bell County', 'TX'),
 '48029': ('Bexar County', 'TX'),
 '48031': ('Blanco County', 'TX'),
 '48033': ('Borden County', 'TX'),
 '48035': ('Bosque County', 'TX'),
 '48037': ('Bowie County', 'TX'),
 '48039': ('Brazoria County', 'TX'),
 '48041': ('Brazos County', 'TX'),
 '48043': ('Brewster County', 'TX'),
 '48045': ('Briscoe County', 'TX'),
 '48047': ('Brooks County', 'TX'),
 '48049': ('Brown County', 'TX'),
 '48051': ('Burleson County', 'TX'),
 '48053': ('Burnet County', 'TX'),
 '48055': ('Caldwell County', 'TX'),
 '48057': ('Calhoun County', 'TX'),
 '48059': ('Callahan County', 'TX'),
 '48061': ('Cameron County', 'TX'),
 '48063': ('Camp County', 'TX'),
 '48065': ('Carson County', 'TX'),
 '48067': ('Cass County', 'TX'),
 '48069': ('Castro County', 'TX'),
 '48071': ('Chambers County', 'TX'),
 '48073': ('Cherokee County', 'TX'),
 '48075': ('Childress County', 'TX'),
 '48077': ('Clay County', 'TX'),
 '48079': ('Cochran County', 'TX'),
 '48081': ('Coke County', 'TX'),
 '48083': ('Coleman County', 'TX'),
 '48085': ('Collin County', 'TX'),
 '48087': ('Collingsworth County', 'TX'),
 '48089': ('Colorado County', 'TX'),
 '48091': ('Comal County', 'TX'),
 '48093': ('Comanche County', 'TX'),
 '48095': ('Concho County', 'TX'),
 '48097': ('Cooke County', 'TX'),
 '48099': ('Coryell County', 'TX'),
 '48101': ('Cottle County', 'TX'),
 '48103': ('Crane County', 'TX'),
 '48105': ('Crockett County', 'TX'),
 '48107': ('Crosby County', 'TX'),
 '48109': ('Culberson County', 'TX'),
 '48111': ('Dallam County', 'TX'),
 '48113': ('Dallas County', 'TX'),
 '48115': ('Dawson County', 'TX'),
 '48117': ('Deaf Smith County', 'TX'),
 '48119': ('Delta County', 'TX'),
 '48121': ('Denton County', 'TX'),
 '48123': ('DeWitt County', 'TX'),
 '48125': ('Dickens County', 'TX'),
 '48127': ('Dimmit County', 'TX'),
 '48129': ('Donley County', 'TX'),
 '48131': ('Duval County', 'TX'),
 '48133': ('Eastland County', 'TX'),
 '48135': ('Ector County', 'TX'),
 '48137': ('Edwards County', 'TX'),
 '48139': ('Ellis County', 'TX'),
 '48141': ('El Paso County', 'TX'),
 '48143': ('Erath County', 'TX'),
 '48145': ('Falls County', 'TX'),
 '48147': ('Fannin County', 'TX'),
 '48149': ('Fayette County', 'TX'),
 '48151': ('Fisher County', 'TX'),
 '48153': ('Floyd County', 'TX'),
 '48155': ('Foard County', 'TX'),
 '48157': ('Fort Bend County', 'TX'),
 '48159': ('Franklin County', 'TX'),
 '48161': ('Freestone County', 'TX'),
 '48163': ('Frio County', 'TX'),
 '48165': ('Gaines County', 'TX'),
 '48167': ('Galveston County', 'TX'),
 '48169': ('Garza County', 'TX'),
 '48171': ('Gillespie County', 'TX'),
 '48173': ('Glasscock County', 'TX'),
 '48175': ('Goliad County', 'TX'),
 '48177': ('Gonzales County', 'TX'),
 '48179': ('Gray County', 'TX'),
 '48181': ('Grayson County', 'TX'),
 '48183': ('Gregg County', 'TX'),
 '48185': ('Grimes County', 'TX'),
 '48187': ('Guadalupe County', 'TX'),
 '48189': ('Hale County', 'TX'),
 '48191': ('Hall County', 'TX'),
 '48193': ('Hamilton County', 'TX'),
 '48195': ('Hansford County', 'TX'),
 '48197': ('Hardeman County', 'TX'),
 '48199': ('Hardin County', 'TX'),
 '48201': ('Harris County', 'TX'),
 '48203': ('Harrison County', 'TX'),
 '48205': ('Hartley County', 'TX'),
 '48207': ('Haskell County', 'TX'),
 '48209': ('Hays County', 'TX'),
 '48211': ('Hemphill County', 'TX'),
 '48213': ('Henderson County', 'TX'),
 '48215': ('Hidalgo County', 'TX'),
 '48217': ('Hill County', 'TX'),
 '48219': ('Hockley County', 'TX'),
 '48221': ('Hood County', 'TX'),
 '48223': ('Hopkins County', 'TX'),
 '48225': ('Houston County', 'TX'),
 '48227': ('Howard County', 'TX'),
 '48229': ('Hudspeth County', 'TX'),
 '48231': ('Hunt County', 'TX'),
 '48233': ('Hutchinson County', 'TX'),
 '48235': ('Irion County', 'TX'),
 '48237': ('Jack County', 'TX'),
 '48239': ('Jackson County', 'TX'),
 '48241': ('Jasper County', 'TX'),
 '48243': ('Jeff Davis County', 'TX'),
 '48245': ('Jefferson County', 'TX'),
 '48247': ('Jim Hogg County', 'TX'),
 '48249': ('Jim Wells County', 'TX'),
 '48251': ('Johnson County', 'TX'),
 '48253': ('Jones County', 'TX'),
 '48255': ('Karnes County', 'TX'),
 '48257': ('Kaufman County', 'TX'),
 '48259': ('Kendall County', 'TX'),
 '48261': ('Kenedy County', 'TX'),
 '48263': ('Kent County', 'TX'),
 '48265': ('Kerr County', 'TX'),
 '48267': ('Kimble County', 'TX'),
 '48269': ('King County', 'TX'),
 '48271': ('Kinney County', 'TX'),
 '48273': ('Kleberg County', 'TX'),
 '48275': ('Knox County', 'TX'),
 '48277': ('Lamar County', 'TX'),
 '48279': ('Lamb County', 'TX'),
 '48281': ('Lampasas County', 'TX'),
 '48283': ('La Salle County', 'TX'),
 '48285': ('Lavaca County', 'TX'),
 '48287': ('Lee County', 'TX'),
 '48289': ('Leon County', 'TX'),
 '48291': ('Liberty County', 'TX'),
 '48293': ('Limestone County', 'TX'),
 '48295': ('Lipscomb County', 'TX'),
 '48297': ('Live Oak County', 'TX'),
 '48299': ('Llano County', 'TX'),
 '48301': ('Loving County', 'TX'),
 '48303': ('Lubbock County', 'TX'),
 '48305': ('Lynn County', 'TX'),
 '48307': ('McCulloch County', 'TX'),
 '48309': ('McLennan County', 'TX'),
 '48311': ('McMullen County', 'TX'),
 '48313': ('Madison County', 'TX'),
 '48315': ('Marion County', 'TX'),
 '48317': ('Martin County', 'TX'),
 '48319': ('Mason County', 'TX'),
 '48321': ('Matagorda County', 'TX'),
 '48323': ('Maverick County', 'TX'),
 '48325': ('Medina County', 'TX'),
 '48327': ('Menard County', 'TX'),
 '48329': ('Midland County', 'TX'),
 '48331': ('Milam County', 'TX'),
 '48333': ('Mills County', 'TX'),
 '48335': ('Mitchell County', 'TX'),
 '48337': ('Montague County', 'TX'),
 '48339': ('Montgomery County', 'TX'),
 '48341': ('Moore County', 'TX'),
 '48343': ('Morris County', 'TX'),
 '48345': ('Motley County', 'TX'),
 '48347': ('Nacogdoches County', 'TX'),
 '48349': ('Navarro County', 'TX'),
 '48351': ('Newton County', 'TX'),
 '48353': ('Nolan County', 'TX'),
 '48355': ('Nueces County', 'TX'),
 '48357': ('Ochiltree County', 'TX'),
 '48359': ('Oldham County', 'TX'),
 '48361': ('Orange County', 'TX'),
 '48363': ('Palo Pinto County', 'TX'),
 '48365': ('Panola County', 'TX'),
 '48367': ('Parker County', 'TX'),
 '48369': ('Parmer County', 'TX'),
 '48371': ('Pecos County', 'TX'),
 '48373': ('Polk County', 'TX'),
 '48375': ('Potter County', 'TX'),
 '48377': ('Presidio County', 'TX'),
 '48379': ('Rains County', 'TX'),
 '48381': ('Randall County', 'TX'),
 '48383': ('Reagan County', 'TX'),
 '48385': ('Real County', 'TX'),
 '48387': ('Red River County', 'TX'),
 '48389': ('Reeves County', 'TX'),
 '48391': ('Refugio County', 'TX'),
 '48393': ('Roberts County', 'TX'),
 '48395': ('Robertson County', 'TX'),
 '48397': ('Rockwall County', 'TX'),
 '48399': ('Runnels County', 'TX'),
 '48401': ('Rusk County', 'TX'),
 '48403': ('Sabine County', 'TX'),
 '48405': ('San Augustine County', 'TX'),
 '48407': ('San Jacinto County', 'TX'),
 '48409': ('San Patricio County', 'TX'),
 '48411': ('San Saba County', 'TX'),
 '48413': ('Schleicher County', 'TX'),
 '48415': ('Scurry County', 'TX'),
 '48417': ('Shackelford County', 'TX'),
 '48419': ('Shelby County', 'TX'),
 '48421': ('Sherman County', 'TX'),
 '48423': ('Smith County', 'TX'),
 '48425': ('Somervell County', 'TX'),
 '48427': ('Starr County', 'TX'),
 '48429': ('Stephens County', 'TX'),
 '48431': ('Sterling County', 'TX'),
 '48433': ('Stonewall County', 'TX'),
 '48435': ('Sutton County', 'TX'),
 '48437': ('Swisher County', 'TX'),
 '48439': ('Tarrant County', 'TX'),
 '48441': ('Taylor County', 'TX'),
 '48443': ('Terrell County', 'TX'),
 '48445': ('Terry County', 'TX'),
 '48447': ('Throckmorton County', 'TX'),
 '48449': ('Titus County', 'TX'),
 '48451': ('Tom Green County', 'TX'),
 '48453': ('Travis County', 'TX'),
 '48455': ('Trinity County', 'TX'),
 '48457': ('Tyler County', 'TX'),
 '48459': ('Upshur County', 'TX'),
 '48461': ('Upton County', 'TX'),
 '48463': ('Uvalde County', 'TX'),
 '48465': ('Val Verde County', 'TX'),
 '48467': ('Van Zandt County', 'TX'),
 '48469': ('Victoria County', 'TX'),
 '48471': ('Walker County', 'TX'),
 '48473': ('Waller County', 'TX'),
 '48475': ('Ward County', 'TX'),
 '48477': ('Washington County', 'TX'),
 '48479': ('Webb County', 'TX'),
 '48481': ('Wharton County', 'TX'),
 '48483': ('Wheeler County', 'TX'),
 '48485': ('Wichita County', 'TX'),
 '48487': ('Wilbarger County', 'TX'),
 '48489': ('Willacy County', 'TX'),
 '48491': ('Williamson County', 'TX'),
 '48493': ('Wilson County', 'TX'),
 '48495': ('Winkler County', 'TX'),
 '48497': ('Wise County', 'TX'),
 '48499': ('Wood County', 'TX'),
 '48501': ('Yoakum County', 'TX'),
 '48503': ('Young County', 'TX'),
 '48505': ('Zapata County', 'TX'),
 '48507': ('Zavala County', 'TX'),
 '49001': ('Beaver County', 'UT'),
 '49003': ('Box Elder County', 'UT'),
 '49005': ('Cache County', 'UT'),
 '49007': ('Carbon County', 'UT'),
 '49009': ('Daggett County', 'UT'),
 '49011': ('Davis County', 'UT'),
 '49013': ('Duchesne County', 'UT'),
 '49015': ('Emery County', 'UT'),
 '49017': ('Garfield County', 'UT'),
 '49019': ('Grand County', 'UT'),
 '49021': ('Iron County', 'UT'),
 '49023': ('Juab County', 'UT'),
 '49025': ('Kane County', 'UT'),
 '49027': ('Millard County', 'UT'),
 '49029': ('Morgan County', 'UT'),
 '49031': ('Piute County', 'UT'),
 '49033': ('Rich County', 'UT'),
 '49035': ('Salt Lake County', 'UT'),
 '49037': ('San Juan County', 'UT'),
 '49039': ('Sanpete County', 'UT'),
 '49041': ('Sevier County', 'UT'),
 '49043': ('Summit County', 'UT'),
 '49045': ('Tooele County', 'UT'),
 '49047': ('Uintah County', 'UT'),
 '49049': ('Utah County', 'UT'),
 '49051': ('Wasatch County', 'UT'),
 '49053': ('Washington County', 'UT'),
 '49055': ('Wayne County', 'UT'),
 '49057': ('Weber County', 'UT'),
 '50001': ('Addison County', 'VT'),
 '50003': ('Bennington County', 'VT'),
 '50005': ('Caledonia County', 'VT'),
 '50007': ('Chittenden County', 'VT'),
 '50009': ('Essex County', 'VT'),
 '50011': ('Franklin County', 'VT'),
 '50013': ('Grand Isle County', 'VT'),
 '50015': ('Lamoille County', 'VT'),
 '50017': ('Orange County', 'VT'),
 '50019': ('Orleans County', 'VT'),
 '50021': ('Rutland County', 'VT'),
 '50023': ('Washington County', 'VT'),
 '50025': ('Windham County', 'VT'),
 '50027': ('Windsor County', 'VT'),
 '51001': ('Accomack County', 'VA'),
 '51003': ('Albemarle County', 'VA'),
 '51005': ('Alleghany County', 'VA'),
 '51007': ('Amelia County', 'VA'),
 '51009': ('Amherst County', 'VA'),
 '51011': ('Appomattox County', 'VA'),
 '51013': ('Arlington County', 'VA'),
 '51015': ('Augusta County', 'VA'),
 '51017': ('Bath County', 'VA'),
 '51019': ('Bedford County', 'VA'),
 '51021': ('Bland County', 'VA'),
 '51023': ('Botetourt County', 'VA'),
 '51025': ('Brunswick County', 'VA'),
 '51027': ('Buchanan County', 'VA'),
 '51029': ('Buckingham County', 'VA'),
 '51031': ('Campbell County', 'VA'),
 '51033': ('Caroline County', 'VA'),
 '51035': ('Carroll County', 'VA'),
 '51036': ('Charles City County', 'VA'),
 '51037': ('Charlotte County', 'VA'),
 '51041': ('Chesterfield County', 'VA'),
 '51043': ('Clarke County', 'VA'),
 '51045': ('Craig County', 'VA'),
 '51047': ('Culpeper County', 'VA'),
 '51049': ('Cumberland County', 'VA'),
 '51051': ('Dickenson County', 'VA'),
 '51053': ('Dinwiddie County', 'VA'),
 '51057': ('Essex County', 'VA'),
 '51059': ('Fairfax County', 'VA'),
 '51061': ('Fauquier County', 'VA'),
 '51063': ('Floyd County', 'VA'),
 '51065': ('Fluvanna County', 'VA'),
 '51067': ('Franklin County', 'VA'),
 '51069': ('Frederick County', 'VA'),
 '51071': ('Giles County', 'VA'),
 '51073': ('Gloucester County', 'VA'),
 '51075': ('Goochland County', 'VA'),
 '51077': ('Grayson County', 'VA'),
 '51079': ('Greene County', 'VA'),
 '51081': ('Greensville County', 'VA'),
 '51083': ('Halifax County', 'VA'),
 '51085': ('Hanover County', 'VA'),
 '51087': ('Henrico County', 'VA'),
 '51089': ('Henry County', 'VA'),
 '51091': ('Highland County', 'VA'),
 '51093': ('Isle of Wight County', 'VA'),
 '51095': ('James City County', 'VA'),
 '51097': ('King and Queen County', 'VA'),
 '51099': ('King George County', 'VA'),
 '51101': ('King William County', 'VA'),
 '51103': ('Lancaster County', 'VA'),
 '51105': ('Lee County', 'VA'),
 '51107': ('Loudoun County', 'VA'),
 '51109': ('Louisa County', 'VA'),
 '51111': ('Lunenburg County', 'VA'),
 '51113': ('Madison County', 'VA'),
 '51115': ('Mathews County', 'VA'),
 '51117': ('Mecklenburg County', 'VA'),
 '51119': ('Middlesex County', 'VA'),
 '51121': ('Montgomery County', 'VA'),
 '51125': ('Nelson County', 'VA'),
 '51127': ('New Kent County', 'VA'),
 '51131': ('Northampton County', 'VA'),
 '51133': ('Northumberland County', 'VA'),
 '51135': ('Nottoway County', 'VA'),
 '51137': ('Orange County', 'VA'),
 '51139': ('Page County', 'VA'),
 '51141': ('Patrick County', 'VA'),
 '51143': ('Pittsylvania County', 'VA'),
 '51145': ('Powhatan County', 'VA'),
 '51147': ('Prince Edward County', 'VA'),
 '51149': ('Prince George County', 'VA'),
 '51153': ('Prince William County', 'VA'),
 '51155': ('Pulaski County', 'VA'),
 '51157': ('Rappahannock County', 'VA'),
 '51159': ('Richmond County', 'VA'),
 '51161': ('Roanoke County', 'VA'),
 '51163': ('Rockbridge County', 'VA'),
 '51165': ('Rockingham County', 'VA'),
 '51167': ('Russell County', 'VA'),
 '51169': ('Scott County', 'VA'),
 '51171': ('Shenandoah County', 'VA'),
 '51173': ('Smyth County', 'VA'),
 '51175': ('Southampton County', 'VA'),
 '51177': ('Spotsylvania County', 'VA'),
 '51179': ('Stafford County', 'VA'),
 '51181': ('Surry County', 'VA'),
 '51183': ('Sussex County', 'VA'),
 '51185': ('Tazewell County', 'VA'),
 '51187': ('Warren County', 'VA'),
 '51191': ('Washington County', 'VA'),
 '51193': ('Westmoreland County', 'VA'),
 '51195': ('Wise County', 'VA'),
 '51197': ('Wythe County', 'VA'),
 '51199': ('York County', 'VA'),
 '51510': ('Alexandria city', 'VA'),
 '51515': ('Bedford city', 'VA'),
 '51520': ('Bristol city', 'VA'),
 '51530': ('Buena Vista city', 'VA'),
 '51540': ('Charlottesville city', 'VA'),
 '51550': ('Chesapeake city', 'VA'),
 '51570': ('Colonial Heights city', 'VA'),
 '51580': ('Covington city', 'VA'),
 '51590': ('Danville city', 'VA'),
 '51595': ('Emporia city', 'VA'),
 '51600': ('Fairfax city', 'VA'),
 '51610': ('Falls Church city', 'VA'),
 '51620': ('Franklin city', 'VA'),
 '51630': ('Fredericksburg city', 'VA'),
 '51640': ('Galax city', 'VA'),
 '51650': ('Hampton city', 'VA'),
 '51660': ('Harrisonburg city', 'VA'),
 '51670': ('Hopewell city', 'VA'),
 '51678': ('Lexington city', 'VA'),
 '51680': ('Lynchburg city', 'VA'),
 '51683': ('Manassas city', 'VA'),
 '51685': ('Manassas Park city', 'VA'),
 '51690': ('Martinsville city', 'VA'),
 '51700': ('Newport News city', 'VA'),
 '51710': ('Norfolk city', 'VA'),
 '51720': ('Norton city', 'VA'),
 '51730': ('Petersburg city', 'VA'),
 '51735': ('Poquoson city', 'VA'),
 '51740': ('Portsmouth city', 'VA'),
 '51750': ('Radford city', 'VA'),
 '51760': ('Richmond city', 'VA'),
 '51770': ('Roanoke city', 'VA'),
 '51775': ('Salem city', 'VA'),
 '51790': ('Staunton city', 'VA'),
 '51800': ('Suffolk city', 'VA'),
 '51810': ('Virginia Beach city', 'VA'),
 '51820': ('Waynesboro city', 'VA'),
 '51830': ('Williamsburg city', 'VA'),
 '51840': ('Winchester city', 'VA'),
 '53001': ('Adams County', 'WA'),
 '53003': ('Asotin County', 'WA'),
 '53005': ('Benton County', 'WA'),
 '53007': ('Chelan County', 'WA'),
 '53009': ('Clallam County', 'WA'),
 '53011': ('Clark County', 'WA'),
 '53013': ('Columbia County', 'WA'),
 '53015': ('Cowlitz County', 'WA'),
 '53017': ('Douglas County', 'WA'),
 '53019': ('Ferry County', 'WA'),
 '53021': ('Franklin County', 'WA'),
 '53023': ('Garfield County', 'WA'),
 '53025': ('Grant County', 'WA'),
 '53027': ('Grays Harbor County', 'WA'),
 '53029': ('Island County', 'WA'),
 '53031': ('Jefferson County', 'WA'),
 '53033': ('King County', 'WA'),
 '53035': ('Kitsap County', 'WA'),
 '53037': ('Kittitas County', 'WA'),
 '53039': ('Klickitat County', 'WA'),
 '53041': ('Lewis County', 'WA'),
 '53043': ('Lincoln County', 'WA'),
 '53045': ('Mason County', 'WA'),
 '53047': ('Okanogan County', 'WA'),
 '53049': ('Pacific County', 'WA'),
 '53051': ('Pend Oreille County', 'WA'),
 '53053': ('Pierce County', 'WA'),
 '53055': ('San Juan County', 'WA'),
 '53057': ('Skagit County', 'WA'),
 '53059': ('Skamania County', 'WA'),
 '53061': ('Snohomish County', 'WA'),
 '53063': ('Spokane County', 'WA'),
 '53065': ('Stevens County', 'WA'),
 '53067': ('Thurston County', 'WA'),
 '53069': ('Wahkiakum County', 'WA'),
 '53071': ('Walla Walla County', 'WA'),
 '53073': ('Whatcom County', 'WA'),
 '53075': ('Whitman County', 'WA'),
 '53077': ('Yakima County', 'WA'),
 '54001': ('Barbour County', 'WV'),
 '54003': ('Berkeley County', 'WV'),
 '54005': ('Boone County', 'WV'),
 '54007': ('Braxton County', 'WV'),
 '54009': ('Brooke County', 'WV'),
 '54011': ('Cabell County', 'WV'),
 '54013': ('Calhoun County', 'WV'),
 '54015': ('Clay County', 'WV'),
 '54017': ('Doddridge County', 'WV'),
 '54019': ('Fayette County', 'WV'),
 '54021': ('Gilmer County', 'WV'),
 '54023': ('Grant County', 'WV'),
 '54025': ('Greenbrier County', 'WV'),
 '54027': ('Hampshire County', 'WV'),
 '54029': ('Hancock County', 'WV'),
 '54031': ('Hardy County', 'WV'),
 '54033': ('Harrison County', 'WV'),
 '54035': ('Jackson County', 'WV'),
 '54037': ('Jefferson County', 'WV'),
 '54039': ('Kanawha County', 'WV'),
 '54041': ('Lewis County', 'WV'),
 '54043': ('Lincoln County', 'WV'),
 '54045': ('Logan County', 'WV'),
 '54047': ('McDowell County', 'WV'),
 '54049': ('Marion County', 'WV'),
 '54051': ('Marshall County', 'WV'),
 '54053': ('Mason County', 'WV'),
 '54055': ('Mercer County', 'WV'),
 '54057': ('Mineral County', 'WV'),
 '54059': ('Mingo County', 'WV'),
 '54061': ('Monongalia County', 'WV'),
 '54063': ('Monroe County', 'WV'),
 '54065': ('Morgan County', 'WV'),
 '54067': ('Nicholas County', 'WV'),
 '54069': ('Ohio County', 'WV'),
 '54071': ('Pendleton County', 'WV'),
 '54073': ('Pleasants County', 'WV'),
 '54075': ('Pocahontas County', 'WV'),
 '54077': ('Preston County', 'WV'),
 '54079': ('Putnam County', 'WV'),
 '54081': ('Raleigh County', 'WV'),
 '54083': ('Randolph County', 'WV'),
 '54085': ('Ritchie County', 'WV'),
 '54087': ('Roane County', 'WV'),
 '54089': ('Summers County', 'WV'),
 '54091': ('Taylor County', 'WV'),
 '54093': ('Tucker County', 'WV'),
 '54095': ('Tyler County', 'WV'),
 '54097': ('Upshur County', 'WV'),
 '54099': ('Wayne County', 'WV'),
 '54101': ('Webster County', 'WV'),
 '54103': ('Wetzel County', 'WV'),
 '54105': ('Wirt County', 'WV'),
 '54107': ('Wood County', 'WV'),
 '54109': ('Wyoming County', 'WV'),
 '55001': ('Adams County', 'WI'),
 '55003': ('Ashland County', 'WI'),
 '55005': ('Barron County', 'WI'),
 '55007': ('Bayfield County', 'WI'),
 '55009': ('Brown County', 'WI'),
 '55011': ('Buffalo County', 'WI'),
 '55013': ('Burnett County', 'WI'),
 '55015': ('Calumet County', 'WI'),
 '55017': ('Chippewa County', 'WI'),
 '55019': ('Clark County', 'WI'),
 '55021': ('Columbia County', 'WI'),
 '55023': ('Crawford County', 'WI'),
 '55025': ('Dane County', 'WI'),
 '55027': ('Dodge County', 'WI'),
 '55029': ('Door County', 'WI'),
 '55031': ('Douglas County', 'WI'),
 '55033': ('Dunn County', 'WI'),
 '55035': ('Eau Claire County', 'WI'),
 '55037': ('Florence County', 'WI'),
 '55039': ('Fond du Lac County', 'WI'),
 '55041': ('Forest County', 'WI'),
 '55043': ('Grant County', 'WI'),
 '55045': ('Green County', 'WI'),
 '55047': ('Green Lake County', 'WI'),
 '55049': ('Iowa County', 'WI'),
 '55051': ('Iron County', 'WI'),
 '55053': ('Jackson County', 'WI'),
 '55055': ('Jefferson County', 'WI'),
 '55057': ('Juneau County', 'WI'),
 '55059': ('Kenosha County', 'WI'),
 '55061': ('Kewaunee County', 'WI'),
 '55063': ('La Crosse County', 'WI'),
 '55065': ('Lafayette County', 'WI'),
 '55067': ('Langlade County', 'WI'),
 '55069': ('Lincoln County', 'WI'),
 '55071': ('Manitowoc County', 'WI'),
 '55073': ('Marathon County', 'WI'),
 '55075': ('Marinette County', 'WI'),
 '55077': ('Marquette County', 'WI'),
 '55078': ('Menominee County', 'WI'),
 '55079': ('Milwaukee County', 'WI'),
 '55081': ('Monroe County', 'WI'),
 '55083': ('Oconto County', 'WI'),
 '55085': ('Oneida County', 'WI'),
 '55087': ('Outagamie County', 'WI'),
 '55089': ('Ozaukee County', 'WI'),
 '55091': ('Pepin County', 'WI'),
 '55093': ('Pierce County', 'WI'),
 '55095': ('Polk County', 'WI'),
 '55097': ('Portage County', 'WI'),
 '55099': ('Price County', 'WI'),
 '55101': ('Racine County', 'WI'),
 '55103': ('Richland County', 'WI'),
 '55105': ('Rock County', 'WI'),
 '55107': ('Rusk County', 'WI'),
 '55109': ('St. Croix County', 'WI'),
 '55111': ('Sauk County', 'WI'),
 '55113': ('Sawyer County', 'WI'),
 '55115': ('Shawano County', 'WI'),
 '55117': ('Sheboygan County', 'WI'),
 '55119': ('Taylor County', 'WI'),
 '55121': ('Trempealeau County', 'WI'),
 '55123': ('Vernon County', 'WI'),
 '55125': ('Vilas County', 'WI'),
 '55127': ('Walworth County', 'WI'),
 '55129': ('Washburn County', 'WI'),
 '55131': ('Washington County', 'WI'),
 '55133': ('Waukesha County', 'WI'),
 '55135': ('Waupaca County', 'WI'),
 '55137': ('Waushara County', 'WI'),
 '55139': ('Winnebago County', 'WI'),
 '55141': ('Wood County', 'WI'),
 '56001': ('Albany County', 'WY'),
 '56003': ('Big Horn County', 'WY'),
 '56005': ('Campbell County', 'WY'),
 '56007': ('Carbon County', 'WY'),
 '56009': ('Converse County', 'WY'),
 '56011': ('Crook County', 'WY'),
 '56013': ('Fremont County', 'WY'),
 '56015': ('Goshen County', 'WY'),
 '56017': ('Hot Springs County', 'WY'),
 '56019': ('Johnson County', 'WY'),
 '56021': ('Laramie County', 'WY'),
 '56023': ('Lincoln County', 'WY'),
 '56025': ('Natrona County', 'WY'),
 '56027': ('Niobrara County', 'WY'),
 '56029': ('Park County', 'WY'),
 '56031': ('Platte County', 'WY'),
 '56033': ('Sheridan County', 'WY'),
 '56035': ('Sublette County', 'WY'),
 '56037': ('Sweetwater County', 'WY'),
 '56039': ('Teton County', 'WY'),
 '56041': ('Uinta County', 'WY'),
 '56043': ('Washakie County', 'WY'),
 '56045': ('Weston County', 'WY')}

statecodes = {'AK': {'code': 'AK', 'name': 'Alaska', 'fips': '02', 'geonameid': 5879092},
 'AL': {'code': 'AL', 'name': 'Alabama', 'fips': '01', 'geonameid': 4829764},
 'AR': {'code': 'AR', 'name': 'Arkansas', 'fips': '05', 'geonameid': 4099753},
 'AZ': {'code': 'AZ', 'name': 'Arizona', 'fips': '04', 'geonameid': 5551752},
 'CA': {'code': 'CA', 'name': 'California', 'fips': '06', 'geonameid': 5332921},
 'CO': {'code': 'CO', 'name': 'Colorado', 'fips': '08', 'geonameid': 5417618},
 'CT': {'code': 'CT', 'name': 'Connecticut', 'fips': '09', 'geonameid': 4831725},
 'DC': {'code': 'DC', 'name': 'District of Columbia', 'fips': '11', 'geonameid': 4138106},
 'DE': {'code': 'DE', 'name': 'Delaware', 'fips': '10', 'geonameid': 4142224},
 'FL': {'code': 'FL', 'name': 'Florida', 'fips': '12', 'geonameid': 4155751},
 'GA': {'code': 'GA', 'name': 'Georgia', 'fips': '13', 'geonameid': 4197000},
 'HI': {'code': 'HI', 'name': 'Hawaii', 'fips': '15', 'geonameid': 5855797},
 'IA': {'code': 'IA', 'name': 'Iowa', 'fips': '19', 'geonameid': 4862182},
 'ID': {'code': 'ID', 'name': 'Idaho', 'fips': '16', 'geonameid': 5596512},
 'IL': {'code': 'IL', 'name': 'Illinois', 'fips': '17', 'geonameid': 4896861},
 'IN': {'code': 'IN', 'name': 'Indiana', 'fips': '18', 'geonameid': 4921868},
 'KS': {'code': 'KS', 'name': 'Kansas', 'fips': '20', 'geonameid': 4273857},
 'KY': {'code': 'KY', 'name': 'Kentucky', 'fips': '21', 'geonameid': 6254925},
 'LA': {'code': 'LA', 'name': 'Louisiana', 'fips': '22', 'geonameid': 4331987},
 'MA': {'code': 'MA', 'name': 'Massachusetts', 'fips': '25', 'geonameid': 6254926},
 'MD': {'code': 'MD', 'name': 'Maryland', 'fips': '24', 'geonameid': 4361885},
 'ME': {'code': 'ME', 'name': 'Maine', 'fips': '23', 'geonameid': 4971068},
 'MI': {'code': 'MI', 'name': 'Michigan', 'fips': '26', 'geonameid': 5001836},
 'MN': {'code': 'MN', 'name': 'Minnesota', 'fips': '27', 'geonameid': 5037779},
 'MO': {'code': 'MO', 'name': 'Missouri', 'fips': '29', 'geonameid': 4398678},
 'MS': {'code': 'MS', 'name': 'Mississippi', 'fips': '28', 'geonameid': 4436296},
 'MT': {'code': 'MT', 'name': 'Montana', 'fips': '30', 'geonameid': 5667009},
 'NC': {'code': 'NC', 'name': 'North Carolina', 'fips': '37', 'geonameid': 4482348},
 'ND': {'code': 'ND', 'name': 'North Dakota', 'fips': '38', 'geonameid': 5690763},
 'NE': {'code': 'NE', 'name': 'Nebraska', 'fips': '31', 'geonameid': 5073708},
 'NH': {'code': 'NH', 'name': 'New Hampshire', 'fips': '33', 'geonameid': 5090174},
 'NJ': {'code': 'NJ', 'name': 'New Jersey', 'fips': '34', 'geonameid': 5101760},
 'NM': {'code': 'NM', 'name': 'New Mexico', 'fips': '35', 'geonameid': 5481136},
 'NV': {'code': 'NV', 'name': 'Nevada', 'fips': '32', 'geonameid': 5509151},
 'NY': {'code': 'NY', 'name': 'New York', 'fips': '36', 'geonameid': 5128638},
 'OH': {'code': 'OH', 'name': 'Ohio', 'fips': '39', 'geonameid': 5165418},
 'OK': {'code': 'OK', 'name': 'Oklahoma', 'fips': '40', 'geonameid': 4544379},
 'OR': {'code': 'OR', 'name': 'Oregon', 'fips': '41', 'geonameid': 5744337},
 'PA': {'code': 'PA', 'name': 'Pennsylvania', 'fips': '42', 'geonameid': 6254927},
 'RI': {'code': 'RI', 'name': 'Rhode Island', 'fips': '44', 'geonameid': 5224323},
 'SC': {'code': 'SC', 'name': 'South Carolina', 'fips': '45', 'geonameid': 4597040},
 'SD': {'code': 'SD', 'name': 'South Dakota', 'fips': '46', 'geonameid': 5769223},
 'TN': {'code': 'TN', 'name': 'Tennessee', 'fips': '47', 'geonameid': 4662168},
 'TX': {'code': 'TX', 'name': 'Texas', 'fips': '48', 'geonameid': 4736286},
 'UT': {'code': 'UT', 'name': 'Utah', 'fips': '49', 'geonameid': 5549030},
 'VA': {'code': 'VA', 'name': 'Virginia', 'fips': '51', 'geonameid': 6254928},
 'VT': {'code': 'VT', 'name': 'Vermont', 'fips': '50', 'geonameid': 5242283},
 'WA': {'code': 'WA', 'name': 'Washington', 'fips': '53', 'geonameid': 5815135},
 'WI': {'code': 'WI', 'name': 'Wisconsin', 'fips': '55', 'geonameid': 5279468},
 'WV': {'code': 'WV', 'name': 'West Virginia', 'fips': '54', 'geonameid': 4826850},
 'WY': {'code': 'WY', 'name': 'Wyoming', 'fips': '56', 'geonameid': 5843591}}

#changes state abbreviation to non-abbreviation for ease of use
for code in standardcountytuples:
    county, stateabr = standardcountytuples[code]
    standardcountytuples[code] = (county, statecodes[stateabr]["name"])

standardcountynames = {}
for code in standardcountytuples:
    standardcountynames[code] = standardcountytuples[code][0]

copy = pd.DataFrame().assign(StandardCountyName = main['Fips Code'])
copy.StandardCountyName.replace(to_replace = standardcountynames, inplace = True)
main = pd.concat([copy, main], axis = 0, ignore_index = True)


# #outputs cleaned data to Excel
#main.to_excel("COUNTYcleanedstatedata_1971_to_2020.xlsx")

years = [1971, 1980, 1990, 2000, 2010, 2020]

USstates = set()
#get states
for i in range(len(main)):
    USstates.add(main.loc[i,"State Name"])
    
adherents = set()
members = set()
churches = set()
for col in main.columns:
    if col not in identifiercols:
        if "_a" in col:
            adherents.add(col)
        if "_m" in col:
            members.add(col)
        if "_c" in col:
            churches.add(col)


majordenominations = set()
majordenominations.add("Catholic Church_a")
majordenominations.add("Other Denominations_a")
majordenominations.add("Mainline Protestant_a")
majordenominations.add("Evangelical Protestant_a")
majordenominations.add("Catholic (2010 label)_a")
majordenominations.add("Orthodox Denominations_a")
majordenominations.add("Muslim Estimate_a")
majordenominations.add("Jewish Estimate_a")



adherents = adherents - majordenominations
#only in 2000 data
adherents.remove("Adjusted Total Number of Adherents (2000)_a")
#only in 1980 data
adherents.remove("Black Baptists Estimate_a")
adherents.add("Catholic Church_a")
adherents.add("Muslim Estimate_a")
adherents.add("Jewish Estimate_a")

MINCONGREGATIONSIZE = 10000
PERCENTAGEGROWTH = .5
###Filter out so only denominations of certain size in 2020


filteredcolumns = [col for col in identifiercols]
main2020 = main.loc[main["Year"] == 2020]
for col in main2020.columns:
    tempcol = main2020[col]
    if col in adherents and tempcol.sum() > MINCONGREGATIONSIZE:
        filteredcolumns.append(col)

#uncomment here, and comment out code in the note, if only want 2020
# filteredmain_adherents = main[filteredcolumns]

## NOTE: This may filter out a large denomination if their data is missing from
## 2020, but present in all other years. Check for that here
otherbigdenoms = set()
for year in years[:-1]:
    temp = main.loc[main["Year"] == year]
    for col in temp.columns:
        tempcol = temp[col]
        if col in adherents and tempcol.sum() > MINCONGREGATIONSIZE:
            otherbigdenoms.add(col)

leftout = otherbigdenoms - set(filteredcolumns)

filteredmain_adherents = main[[x for x in leftout.union(set(filteredcolumns))]]

#fgc = fast growing counties
fgc_statekey = defaultdict(list)
fgc_countystatetuplekey = defaultdict(list)
for code in standardcountynames:
    thiscounty = main.loc[main["Fips Code"] == code]
    countyname = standardcountynames[code]
    for col in thiscounty.columns:
        if col not in identifiercols:
            for val in thiscounty[col].pct_change():
                if val >= PERCENTAGEGROWTH:
                    state = standardcountytuples[code][1]
                    congregname = col
                    county = countyname
                    fgc_statekey[state].append((congregname, county))
                    fgc_countystatetuplekey[(state, county)].append(congregname)
                    break


################## GRAPHS ################

# for state in USstates:
#     ### State with County Names
#     statesubframe = main.loc[main["State Name"] == state]
#     tograph = []
        
#     for congreg, county in fgc_statekey[state]:
#         statesubframe.rename(columns = {congreg : elimEnding(congreg) +", " + county},\
#                              inplace = True)
#         tograph.append(elimEnding(congreg) +", " + county)

    
#     ## normal plot
#     ax = statesubframe.plot(x = "Year", y = tograph, title = "Denominations in " +\
#                             state + "That Saw an Increase of At Least 50% Between "+\
#                                 "Two Datapoints"
#                             , grid = True, ylabel = "Adherents", figsize = (20,8),\
#                             marker = ".", table = True)
#     ax.xaxis.set_label_position('top') 
#     ax.xaxis.tick_top()
#     ax.legend(loc="upper left",  bbox_to_anchor=(1,1))
#     plt.ticklabel_format(style='plain')  
#     #from https://queirozf.com/entries/matplotlib-examples-number-formatting-for-axes-labels#:~:text=Comma%20as%20thousands%20separator%20Formatting%20labels%20must%20only,with.set_yticklabels%20%28%29%20%28similar%20methods%20exist%20for%20X-axis%20too%29%3A
#     current_values = plt.gca().get_yticks()
#     plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
#     #plt.legend(loc = "center left")
#     #table(ax, np.round(statesubframe[tograph].describe(), 2),loc='upper right')
#     plt.savefig("countyoutputs/by_each_state/" + state + '_IncreaseOf' +\
#                 str(PERCENTAGEGROWTH * 100) + 'percent.png',\
#                 bbox_inches='tight', dpi=150)
#     plt.show()
    
#     ## percentage plot
#     tograph.append("Year")
#     tograph.append("Total Population")
#     ssf_pct = statesubframe[tograph]
    
#     pct_tograph = []
#     for col in ssf_pct.columns:
#         ssf_pct[col + "_pct"] = ssf_pct[col] / ssf_pct["Total Population"]
#         pct_tograph.append(col + "_pct")
#     pct_tograph.remove("Total Population_pct")
#     pct_tograph.remove("Year_pct")
#     ax = ssf_pct.plot(x = "Year", y = pct_tograph, title = "Denominations in " +\
#                             state + "That Saw an Increase of At Least 50% Between "+\
#                                 "Two Datapoints, as a Percentage"+\
#                                     " of Total Population of Thier County"\
#                             , grid = True, ylabel = "Adherents as % of County's Population",\
#                                 figsize = (20,8),\
#                             marker = ".", table = True)
#     ax.xaxis.set_label_position('top') 
#     ax.xaxis.tick_top()
#     ax.legend(loc="upper left",  bbox_to_anchor=(1,1))
#     plt.ticklabel_format(style='plain')  
#     #from https://queirozf.com/entries/matplotlib-examples-number-formatting-for-axes-labels#:~:text=Comma%20as%20thousands%20separator%20Formatting%20labels%20must%20only,with.set_yticklabels%20%28%29%20%28similar%20methods%20exist%20for%20X-axis%20too%29%3A
#     current_values = plt.gca().get_yticks()
#     plt.gca().set_yticklabels(['{:,.0%}'.format(x) for x in current_values])
#     #table(ax, np.round(statesubframe[tograph].describe(), 2),loc='upper right')
#     plt.savefig("countyoutputs/by_each_state/" + state + '_IncreaseOf' +\
#                 str(PERCENTAGEGROWTH * 100) + 'percent_pct.png',\
#                 bbox_inches='tight', dpi=150)
#     plt.show()

#     # # ### By County
    
#     for code in standardcountynames:
#         countysubframe = statesubframe.loc[main["Fips Code"] == code]
#         tograph = []
            
#         for congreg in fgc_countystatetuplekey[(state, standardcountynames[code])]:
#             countysubframe.rename(columns = {congreg : elimEnding(congreg) +", " + county},\
#                                   inplace = True)
#             tograph.append(elimEnding(congreg))
    
        
#         ## normal plot
#         ax = statesubframe.plot(x = "Year", y = tograph, title = "Denominations in " +\
#                                 county + ", " + state +\
#                                     "That Saw an Increase of At Least 50% Between "+\
#                                     "Two Datapoints"
#                                 , grid = True, ylabel = "Adherents", figsize = (20,8),\
#                                 marker = ".", table = True)
#         ax.xaxis.set_label_position('top') 
#         ax.xaxis.tick_top()
#         ax.legend(loc="upper left",  bbox_to_anchor=(1,1))
#         plt.ticklabel_format(style='plain')  
#         #from https://queirozf.com/entries/matplotlib-examples-number-formatting-for-axes-labels#:~:text=Comma%20as%20thousands%20separator%20Formatting%20labels%20must%20only,with.set_yticklabels%20%28%29%20%28similar%20methods%20exist%20for%20X-axis%20too%29%3A
#         current_values = plt.gca().get_yticks()
#         plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
#         #plt.legend(loc = "center left")
#         #table(ax, np.round(statesubframe[tograph].describe(), 2),loc='upper right')
#         plt.savefig("countyoutputs/by_each_county/" + county+"_"+state + '_IncreaseOf' +\
#                     str(PERCENTAGEGROWTH * 100) + 'percent.png',\
#                     bbox_inches='tight', dpi=150)
#         plt.show()
        
#         ## percentage plot
#         tograph.append("Year")
#         tograph.append("Total Population")
#         ssf_pct = statesubframe[tograph]
        
#         pct_tograph = []
#         for col in ssf_pct.columns:
#             ssf_pct[col + "_pct"] = ssf_pct[col] / ssf_pct["Total Population"]
#             pct_tograph.append(col + "_pct")
#         pct_tograph.remove("Total Population_pct")
#         pct_tograph.remove("Year_pct")
#         ax = ssf_pct.plot(x = "Year", y = pct_tograph, title = "Denominations in " +\
#                                 state + "That Saw an Increase of At Least 50% Between "+\
#                                     "Two Datapoints, as a Percentage"+\
#                                         " of Total Population of County"\
#                                 , grid = True, ylabel = "Adherents as % of County's Population",\
#                                     figsize = (20,8),\
#                                 marker = ".", table = True)
#         ax.xaxis.set_label_position('top') 
#         ax.xaxis.tick_top()
#         ax.legend(loc="upper left",  bbox_to_anchor=(1,1))
#         plt.ticklabel_format(style='plain')  
#         #from https://queirozf.com/entries/matplotlib-examples-number-formatting-for-axes-labels#:~:text=Comma%20as%20thousands%20separator%20Formatting%20labels%20must%20only,with.set_yticklabels%20%28%29%20%28similar%20methods%20exist%20for%20X-axis%20too%29%3A
#         current_values = plt.gca().get_yticks()
#         plt.gca().set_yticklabels(['{:,.0%}'.format(x) for x in current_values])
#         #table(ax, np.round(statesubframe[tograph].describe(), 2),loc='upper right')
#         plt.savefig("countyoutputs/by_each_county/" + county + "_"+state + '_IncreaseOf' +\
#                     str(PERCENTAGEGROWTH * 100) + 'percent_pct.png',\
#                     bbox_inches='tight', dpi=150)
#         plt.show()

# ---------------------------- extra code



# NUMBERTOSHOW = 20

# FILTERNUM = 500000

# years = [1971, 1980, 1990, 2000, 2010, 2020]

# ###Filter out so only denominations of certain size in 2020


# filteredcolumns = [col for col in identifiercols]
# main2020 = main.loc[main["Year"] == 2020]
# for col in main2020.columns:
#     tempcol = main2020[col]
#     if col in adherents and tempcol.sum() > FILTERNUM:
#         filteredcolumns.append(col)

# #uncomment here, and comment out code in the note, if only want 2020
# # filteredmain_adherents = main[filteredcolumns]

# ## NOTE: This may filter out a large denomination if their data is missing from
# ## 2020, but present in all other years. Check for that here
# otherbigdenoms = set()
# for year in years[:-1]:
#     temp = main.loc[main["Year"] == year]
#     for col in temp.columns:
#         tempcol = temp[col]
#         if col in adherents and tempcol.sum() > FILTERNUM:
#             otherbigdenoms.add(col)

# leftout = otherbigdenoms - set(filteredcolumns)

# filteredmain_adherents = main[[x for x in leftout.union(set(filteredcolumns))]]
    

# #### Entire US

# years = [1971, 1980, 1990, 2000, 2010, 2020]
# summed = defaultdict(list)
# summed["Year"] = years
# for year in years:
#     for col in filteredmain_adherents.columns:
#         if col not in identifiercols or col == "Total Population":
#             summed[col].append(\
#                                 filteredmain_adherents.loc[filteredmain_adherents["Year"] == year][col].sum())

# summed_df = pd.DataFrame(summed)
# summed_y = [x for x in summed]
# summed_y.remove("Year")
# summed_y.remove("Total Population")

# ### Normal Plot
# ax = summed_df.plot(x = "Year", y = summed_y, title = "Denominations in USA " + \
#                 "with over " + str(format(FILTERNUM, ',d')) + " Adherents in Any Year"\
#                         , grid = True, ylabel = "Adherents", figsize = (20,8),\
#                         marker = ".", table = True)
# ax.xaxis.set_label_position('top') 
# ax.xaxis.tick_top()
# ax.legend(loc="upper left",  bbox_to_anchor=(1,1))
# plt.ticklabel_format(style='plain')  
# #from https://queirozf.com/entries/matplotlib-examples-number-formatting-for-axes-labels#:~:text=Comma%20as%20thousands%20separator%20Formatting%20labels%20must%20only,with.set_yticklabels%20%28%29%20%28similar%20methods%20exist%20for%20X-axis%20too%29%3A
# current_values = plt.gca().get_yticks()
# plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
# #table(ax, np.round(statesubframe[tograph].describe(), 2),loc='upper right')
# plt.savefig("stateoutputs/US/" + "USA" + '_Over' +\
#             str(FILTERNUM) +'_inAnyYear_Religions_total.png',\
#             bbox_inches='tight', dpi=150)
# plt.show()


# # ## percentage plot
# pct_tograph = []
# for col in summed_df.columns:
#     summed_df[col + "_pct"] = summed_df[col] / summed_df["Total Population"]
#     pct_tograph.append(col + "_pct")
# pct_tograph.remove("Total Population_pct")
# pct_tograph.remove("Year_pct")
# ax = summed_df.plot(x = "Year", y = pct_tograph, title = " Denominations in " \
#                     + "USA" + " with over " + str(format(FILTERNUM, ',d')) +\
#                         " Adherents in Any Year,"+\
#                         " as a Percentage of Total Population of " + "USA"\
#                         , grid = True, ylabel = "Adherents as % of USA Population",\
#                             figsize = (20,8),\
#                         marker = ".", table = True)
# ax.xaxis.set_label_position('top') 
# ax.xaxis.tick_top()
# ax.legend(loc="upper left",  bbox_to_anchor=(1,1))
# plt.ticklabel_format(style='plain')  
# #from https://queirozf.com/entries/matplotlib-examples-number-formatting-for-axes-labels#:~:text=Comma%20as%20thousands%20separator%20Formatting%20labels%20must%20only,with.set_yticklabels%20%28%29%20%28similar%20methods%20exist%20for%20X-axis%20too%29%3A
# current_values = plt.gca().get_yticks()
# plt.gca().set_yticklabels(['{:,.0%}'.format(x) for x in current_values])
# #table(ax, np.round(statesubframe[tograph].describe(), 2),loc='upper right')
# plt.savefig("stateoutputs/US/" + "USA" + '_Over' + str(FILTERNUM) \
#             +'_inAnyYear_Religions_total_pct.png',\
#             bbox_inches='tight', dpi=150)
# plt.show()
    
    




# # # ### By state

# # for state in USstates:
# #     statesubframe = main.loc[main["State Name"] == state]
    
    
# #     ### by average
# #     heapavg = []
    
# #     for col in statesubframe.columns:
# #         if col in adherents:
            
# #             #note: heap is minheap by default in python,
# #             #so we take negative of each element for maxheap
# #             #python automatically compares by first element of tuple
# #             if len(heapavg) >= NUMBERTOSHOW:
# #                 heapq.heappushpop(heapavg, (statesubframe[col].mean(), col))
            
# #             else:
# #                 heapq.heappush(heapavg, (statesubframe[col].mean(), col))
    
# #     ## normal plot
# #     tograph = [col for _, col in heapavg]
# #     ax = statesubframe.plot(x = "Year", y = tograph, title = "Top " + str(NUMBERTOSHOW)\
# #                         +" Denominations in " + state + " by Average Number of Adherents"\
# #                             , grid = True, ylabel = "Adherents", figsize = (20,8),\
# #                             marker = ".", table = True)
# #     ax.xaxis.set_label_position('top') 
# #     ax.xaxis.tick_top()
# #     ax.legend(loc="upper left",  bbox_to_anchor=(1,1))
# #     plt.ticklabel_format(style='plain')  
# #     #from https://queirozf.com/entries/matplotlib-examples-number-formatting-for-axes-labels#:~:text=Comma%20as%20thousands%20separator%20Formatting%20labels%20must%20only,with.set_yticklabels%20%28%29%20%28similar%20methods%20exist%20for%20X-axis%20too%29%3A
# #     current_values = plt.gca().get_yticks()
# #     plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
# #     #plt.legend(loc = "center left")
# #     #table(ax, np.round(statesubframe[tograph].describe(), 2),loc='upper right')
# #     plt.savefig("stateoutputs/avg/" + state + '_Top' + str(NUMBERTOSHOW) +'Religions_avg.png',\
# #                 bbox_inches='tight', dpi=150)
# #     plt.show()
    
# #     ## percentage plot
# #     tograph = [col for _, col in heapavg]
# #     tograph.append("Year")
# #     tograph.append("Total Population")
# #     ssf_pct = statesubframe[tograph]
    
# #     pct_tograph = []
# #     for col in ssf_pct.columns:
# #         ssf_pct[col + "_pct"] = ssf_pct[col] / ssf_pct["Total Population"]
# #         pct_tograph.append(col + "_pct")
# #     pct_tograph.remove("Total Population_pct")
# #     pct_tograph.remove("Year_pct")
# #     ax = ssf_pct.plot(x = "Year", y = pct_tograph, title = "Top " + str(NUMBERTOSHOW)\
# #                         +" Denominations in " + state + " by Average Number of Adherents,"+\
# #                             " as a Percentage of Total Population of " + state\
# #                             , grid = True, ylabel = "Adherents as % of State Population",\
# #                                 figsize = (20,8),\
# #                             marker = ".", table = True)
# #     ax.xaxis.set_label_position('top') 
# #     ax.xaxis.tick_top()
# #     ax.legend(loc="upper left",  bbox_to_anchor=(1,1))
# #     plt.ticklabel_format(style='plain')  
# #     #from https://queirozf.com/entries/matplotlib-examples-number-formatting-for-axes-labels#:~:text=Comma%20as%20thousands%20separator%20Formatting%20labels%20must%20only,with.set_yticklabels%20%28%29%20%28similar%20methods%20exist%20for%20X-axis%20too%29%3A
# #     current_values = plt.gca().get_yticks()
# #     plt.gca().set_yticklabels(['{:,.0%}'.format(x) for x in current_values])
# #     #table(ax, np.round(statesubframe[tograph].describe(), 2),loc='upper right')
# #     plt.savefig("stateoutputs/avg_pct/" + state + '_Top' + str(NUMBERTOSHOW) +\
# #                 'Religions_avg_pct.png',\
# #                 bbox_inches='tight', dpi=150)
# #     plt.show()
    
    
# #     ## by sum
# #     heapsum = []
    
# #     for col in statesubframe.columns:
# #         if col in adherents:
            
# #             #note: heap is minheap by default in python,
# #             #so we take negative of each element for maxheap
# #             #python automatically compares by first element of tuple
# #             if len(heapsum) >= NUMBERTOSHOW:
# #                 heapq.heappushpop(heapsum, (statesubframe[col].sum(), col))
            
# #             else:
# #                 heapq.heappush(heapsum, (statesubframe[col].sum(), col))
    
# #     ## normal plot
# #     tograph = [col for _, col in heapsum]
# #     ax = statesubframe.plot(x = "Year", y = tograph, title = "Top " + str(NUMBERTOSHOW)\
# #                         +" Denominations in " + state + " by Sum of Number of Adherents"\
# #                             , grid = True, ylabel = "Adherents", figsize = (20,8),\
# #                             marker = ".", table = True)
# #     ax.xaxis.set_label_position('top') 
# #     ax.xaxis.tick_top()
# #     ax.legend(loc="upper left",  bbox_to_anchor=(1,1))
# #     plt.ticklabel_format(style='plain')  
# #     #from https://queirozf.com/entries/matplotlib-examples-number-formatting-for-axes-labels#:~:text=Comma%20as%20thousands%20separator%20Formatting%20labels%20must%20only,with.set_yticklabels%20%28%29%20%28similar%20methods%20exist%20for%20X-axis%20too%29%3A
# #     current_values = plt.gca().get_yticks()
# #     plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
# #     #table(ax, np.round(statesubframe[tograph].describe(), 2),loc='upper right')
# #     plt.savefig("stateoutputs/sum/" + state + '_Top' + str(NUMBERTOSHOW) +'Religions_sum.png',\
# #                 bbox_inches='tight', dpi=150)
# #     plt.show()
    
# #     ## percentage plot
# #     tograph = [col for _, col in heapsum]
# #     tograph.append("Year")
# #     tograph.append("Total Population")
# #     ssf_pct = statesubframe[tograph]
    
# #     pct_tograph = []
# #     for col in ssf_pct.columns:
# #         ssf_pct[col + "_pct"] = ssf_pct[col] / ssf_pct["Total Population"]
# #         pct_tograph.append(col + "_pct")
# #     pct_tograph.remove("Total Population_pct")
# #     pct_tograph.remove("Year_pct")
# #     ax = ssf_pct.plot(x = "Year", y = pct_tograph, title = "Top " + str(NUMBERTOSHOW)\
# #                         +" Denominations in " + state + " by Sum of Number of Adherents,"+\
# #                             " as a Percentage of Total Population of " + state\
# #                             , grid = True, ylabel = "Adherents as % of State Population",\
# #                                 figsize = (20,8),\
# #                             marker = ".", table = True)
# #     ax.xaxis.set_label_position('top') 
# #     ax.xaxis.tick_top()
# #     ax.legend(loc="upper left",  bbox_to_anchor=(1,1))
# #     plt.ticklabel_format(style='plain')  
# #     #from https://queirozf.com/entries/matplotlib-examples-number-formatting-for-axes-labels#:~:text=Comma%20as%20thousands%20separator%20Formatting%20labels%20must%20only,with.set_yticklabels%20%28%29%20%28similar%20methods%20exist%20for%20X-axis%20too%29%3A
# #     current_values = plt.gca().get_yticks()
# #     plt.gca().set_yticklabels(['{:,.0%}'.format(x) for x in current_values])
# #     #table(ax, np.round(statesubframe[tograph].describe(), 2),loc='upper right')
# #     plt.savefig("stateoutputs/sum_pct/" + state + '_Top' + str(NUMBERTOSHOW) +\
# #                 'Religions_sum_pct.png',\
# #                 bbox_inches='tight', dpi=150)
# #     plt.show()
    
    
    
# #     ### Finding greatest amount of change!
# #     # by sum
# #     heapsum = []
    
# #     for col in statesubframe.columns:
# #         if col in adherents:
            
# #             #note: heap is minheap by default in python,
# #             #so we take negative of each element for maxheap
# #             #python automatically compares by first element of tuple
# #             if len(heapsum) >= NUMBERTOSHOW:
# #                 heapq.heappushpop(heapsum, (statesubframe[col].sum(), col))
            
# #             else:
# #                 heapq.heappush(heapsum, (statesubframe[col].sum(), col))
    
# #     ## normal plot
# #     tograph = [col for _, col in heapsum]
# #     ax = statesubframe.plot(x = "Year", y = tograph, title = "Top " + str(NUMBERTOSHOW)\
# #                         +" Denominations in " + state + " by Sum of Number of Adherents"\
# #                             , grid = True, ylabel = "Adherents", figsize = (20,8),\
# #                             marker = ".", table = True)
# #     ax.xaxis.set_label_position('top') 
# #     ax.xaxis.tick_top()
# #     ax.legend(loc="upper left",  bbox_to_anchor=(1,1))
# #     plt.ticklabel_format(style='plain')  
# #     #from https://queirozf.com/entries/matplotlib-examples-number-formatting-for-axes-labels#:~:text=Comma%20as%20thousands%20separator%20Formatting%20labels%20must%20only,with.set_yticklabels%20%28%29%20%28similar%20methods%20exist%20for%20X-axis%20too%29%3A
# #     current_values = plt.gca().get_yticks()
# #     plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
# #     #table(ax, np.round(statesubframe[tograph].describe(), 2),loc='upper right')
# #     plt.savefig("stateoutputs/sum/" + state + '_Top' + str(NUMBERTOSHOW) +'Religions_sum.png',\
# #                 bbox_inches='tight', dpi=150)
# #     plt.show()
    
# #     ## percentage plot
# #     tograph = [col for _, col in heapsum]
# #     tograph.append("Year")
# #     tograph.append("Total Population")
# #     ssf_pct = statesubframe[tograph]
    
# #     pct_tograph = []
# #     for col in ssf_pct.columns:
# #         ssf_pct[col + "_pct"] = ssf_pct[col] / ssf_pct["Total Population"]
# #         pct_tograph.append(col + "_pct")
# #     pct_tograph.remove("Total Population_pct")
# #     pct_tograph.remove("Year_pct")
# #     ax = ssf_pct.plot(x = "Year", y = pct_tograph, title = "Top " + str(NUMBERTOSHOW)\
# #                         +" Denominations in " + state + " by Sum of Number of Adherents,"+\
# #                             " as a Percentage of Total Population of " + state\
# #                             , grid = True, ylabel = "Adherents as % of State Population",\
# #                                 figsize = (20,8),\
# #                             marker = ".", table = True)
# #     ax.xaxis.set_label_position('top') 
# #     ax.xaxis.tick_top()
# #     ax.legend(loc="upper left",  bbox_to_anchor=(1,1))
# #     plt.ticklabel_format(style='plain')  
# #     #from https://queirozf.com/entries/matplotlib-examples-number-formatting-for-axes-labels#:~:text=Comma%20as%20thousands%20separator%20Formatting%20labels%20must%20only,with.set_yticklabels%20%28%29%20%28similar%20methods%20exist%20for%20X-axis%20too%29%3A
# #     current_values = plt.gca().get_yticks()
# #     plt.gca().set_yticklabels(['{:,.0%}'.format(x) for x in current_values])
# #     #table(ax, np.round(statesubframe[tograph].describe(), 2),loc='upper right')
# #     plt.savefig("stateoutputs/sum_pct/" + state + '_Top' + str(NUMBERTOSHOW) +\
# #                 'Religions_sum_pct.png',\
# #                 bbox_inches='tight', dpi=150)
# #     plt.show()


    
    
    
            
   
    
            
            

