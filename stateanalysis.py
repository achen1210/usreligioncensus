<<<<<<< HEAD
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


subfoldername = "statedata"

##Note: 1952 data does not have adherents! Have commented out, but
##can add back in by putting it back in "todo_list1" below
data52 = pd.read_stata(subfoldername + '/'+ '1952.dta')
#labels52iterator = pd.read_stata('1952.dta', iterator = True)
#labels52 = labels52iterator.variable_labels()

data71 = pd.read_stata(subfoldername + '/'+ '1971.dta')
labels71iterator = pd.read_stata(subfoldername + '/'+ '1971.dta', iterator = True)
labels71 = labels71iterator.variable_labels()

data80 = pd.read_stata(subfoldername + '/'+ '1980.dta')
labels80iterator = pd.read_stata(subfoldername + '/'+ '1980.dta', iterator = True)
labels80 = labels80iterator.variable_labels()

data90 = pd.read_stata(subfoldername + '/'+ '1990.dta')
labels90iterator = pd.read_stata(subfoldername + '/'+ '1990.dta', iterator = True)
labels90 = labels90iterator.variable_labels()

data2000 = pd.read_stata(subfoldername + '/'+ '2000.dta')
labels2000iterator = pd.read_stata(subfoldername + '/'+ '2000.dta', iterator = True)
labels2000 = labels2000iterator.variable_labels()

data2010 = pd.read_stata(subfoldername + '/' + '2010.dta')
labels2010iterator = pd.read_stata(subfoldername + '/'+ '2010.dta', iterator = True)
labels2010 = labels2010iterator.variable_labels()

data2020 = pd.read_excel('statedata/2020USRCStateData.xlsx')
#### 2020 data cleaned separately
#### pre-cleaned and 
#### formatted in the form of identifier--congregation name in Excel file
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
year80 = data80[['statena']].copy()
year80.columns = ["Year"]
year90 = data90[['statena']].copy()
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

## 1980
del labels80["totpop"]
cleanedlabels["Total Population"].append("totpop")
del labels80["NOCTOT80"]
cleanedlabels["Total Number of Churches"].append("NOCTOT80")
del labels80["MEMTOT80"]
cleanedlabels["Total Members"].append("MEMTOT80")
del labels80["ADHTOT80"]
cleanedlabels["Total Adherents"].append("ADHTOT80")

## 1990
del labels90["totpop"]
cleanedlabels["Total Population"].append("totpop")
del labels90["totch"]
cleanedlabels["Total Number of Churches"].append("totch")
del labels90["totmem"]
cleanedlabels["Total Members"].append("totmem")
del labels90["totadh"]
cleanedlabels["Total Adherents"].append("totadh")


## 2000
del labels2000["POP2000"]
cleanedlabels["Total Population"].append("POP2000")
del labels2000["totcg"]
cleanedlabels["Total Number of Churches"].append("totcg")
del labels2000["totad"]
cleanedlabels["Total Adherents"].append("totad")
del labels2000["totrt"]
cleanedlabels["Total Rate of Adherence"].append("totrt")
#del labels2000["adjad"]
#cleanedlabels["Adjusted Total Adherents"].append("adjad")
#del labels2000["adjrate"]
#cleanedlabels["Adjusted Total Rate of Adherence"].append("adjrate")

## 2010
del labels2010["POP2010"]
cleanedlabels["Total Population"].append("POP2010")
del labels2010["totcng"]
cleanedlabels["Total Number of Churches"].append("totcng")
del labels2010["totadh"]
cleanedlabels["Total Adherents"].append("totadh")
del labels2010["totrate"]
cleanedlabels["Total Rate of Adherence"].append("totrate")

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
identifiercols.add("State Census Code")
identifiercols.add("State Abbreviation")
identifiercols.add("State Code")

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
        del cleanedlabels[label]
    
    for label in toadd:
        cleanedlabels[label] = toadd[label].copy()
        
    endings = ["_m", "_a", "_roa", "_c", "_roap", "_roata"]
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
data90.rename(columns={ 'BMAA_C':'Baptist Missionary Association of America_c'}, inplace = True)
data90.rename(columns={ 'BMAA_A':'Baptist Missionary Association of America_a'}, inplace = True)
data90.rename(columns={ 'BMAA_M':'Baptist Missionary Association of America_m'}, inplace = True)
data90.rename(columns={ 'CGGC_A':'Churches Of God General Conference_a'}, inplace = True)
data90.rename(columns={ 'CGGC_M':'Churches Of God General Conference_m'}, inplace = True)
data90.rename(columns={ 'CGGC_C':'Churches Of God General Conference_c'}, inplace = True)
data90.rename(columns={ 'ROMORT_C':'Romanian Orthodox Episcopate Of America_c'}, inplace = True)
data90.rename(columns={ 'ROMORT_M':'Romanian Orthodox Episcopate Of America_m'}, inplace = True)
data90.rename(columns={ 'ROMORT_A':'Romanian Orthodox Episcopate Of America_a'}, inplace = True)

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
# for df in dataframes:
#     newcolnames = {}
#     c = 0
#     for column in df.keys():              
#         newcolnames[column] = str(c)+"_"+column
#         c += 1
        
#     #part of debug
#     newcolnames["Year"] = "Year"
#     df.rename(columns = newcolnames, inplace = True)


#use below for debugging along with column numbering
# for df in dataframes:
# #    print(df.Year[0])
#     seen = {}
#     num = 0
#     for c in df.keys():           
#         if c[findIndexOfSubstring(c, "_") + 1:] in seen:
#             print(c)
#             print(seen[c[findIndexOfSubstring(c, "_") + 1:]])
#             print(num)
#         seen[c[findIndexOfSubstring(c, "_") + 1:]] = num
#         num += 1
        
    #df.reset_index(inplace=True, drop=True)

#concat all clean dataframes to make the main dataframe    
main = pd.concat(dataframes, axis = 0, ignore_index = True)

#Converts all states to capital case
main["State Name"] = main["State Name"].str.title()
main["Year"] = main["Year"].astype(int)

#outputs cleaned data to Excel
#main.to_excel("cleanedstatedata_1971_to_2020.xlsx")

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



NUMBERTOSHOW = 20

FILTERNUM = 500000
###Filter out so only denominations of certain size
filteredcolumns = []
main2020 = main.loc[main["Year"] == 2020]
for col in main2020.columns:
    tempcol = main2020[col]
    if col in adherents and tempcol.sum() > FILTERNUM:
        filteredcolumns.append(col)

filteredmain_adherents = main[filteredcolumns]

#### Entire US
# ### by average
# heapsum = []

# for col in main.columns:
#     if col in adherents:
        
#         #note: heap is minheap by default in python,
#         #so we take negative of each element for maxheap
#         #python automatically compares by first element of tuple
#         if len(heapsum) >= NUMBERTOSHOW:
#             heapq.heappushpop(heapsum, (main[col].mean(), col))
        
#         else:
#             heapq.heappush(heapsum, (main[col].mean(), col))

# ## normal plot
# tograph = [col for _, col in heapsum]
# ax = main.plot(x = "Year", y = tograph, title = "Top " + str(NUMBERTOSHOW)\
#                     +" Denominations in USA by Average Number of Adherents"\
#                         , grid = True, ylabel = "Adherents", figsize = (20,8),\
#                         marker = ".", table = True)
# ax.xaxis.set_label_position('top') 
# ax.xaxis.tick_top()
# plt.ticklabel_format(style='plain') 
# #from https://queirozf.com/entries/matplotlib-examples-number-formatting-for-axes-labels#:~:text=Comma%20as%20thousands%20separator%20Formatting%20labels%20must%20only,with.set_yticklabels%20%28%29%20%28similar%20methods%20exist%20for%20X-axis%20too%29%3A
# current_values = plt.gca().get_yticks()
# plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
# #table(ax, np.round(statesubframe[tograph].describe(), 2),loc='upper right')
# plt.savefig("stateoutputs/US/" + "USA" + '_Top' + str(NUMBERTOSHOW) +'Religions_avg.png',\
#             bbox_inches='tight', dpi=150)
# plt.show()

# ## percentage plot
# tograph = [col for _, col in heapsum]
# tograph.append("Year")
# tograph.append("Total Population")
# ssf_pct = main[tograph]

# pct_tograph = []
# for col in ssf_pct.columns:
#     ssf_pct[col + "_pct"] = ssf_pct[col] / ssf_pct["Total Population"]
#     pct_tograph.append(col + "_pct")
# pct_tograph.remove("Total Population_pct")
# pct_tograph.remove("Year_pct")
# ax = ssf_pct.plot(x = "Year", y = pct_tograph, title = "Top " + str(NUMBERTOSHOW)\
#                     +" Denominations in " + "USA" + " by Average Number of Adherents,"+\
#                         " as a Percentage of Total Population of " + "USA"\
#                         , grid = True, ylabel = "Adherents as % of State Population",\
#                             figsize = (20,8),\
#                         marker = ".", table = True)
# ax.xaxis.set_label_position('top') 
# ax.xaxis.tick_top()
# plt.ticklabel_format(style='plain') 
# #from https://queirozf.com/entries/matplotlib-examples-number-formatting-for-axes-labels#:~:text=Comma%20as%20thousands%20separator%20Formatting%20labels%20must%20only,with.set_yticklabels%20%28%29%20%28similar%20methods%20exist%20for%20X-axis%20too%29%3A
# current_values = plt.gca().get_yticks()
# plt.gca().set_yticklabels(['{:,.0%}'.format(x) for x in current_values])
# #table(ax, np.round(statesubframe[tograph].describe(), 2),loc='upper right')
# plt.savefig("stateoutputs/US/" + "USA" + '_Top' + str(NUMBERTOSHOW) +\
#             'Religions_acg_pct.png',\
#             bbox_inches='tight', dpi=150)
# plt.show()
    
    




#### By state

# for state in USstates:
#     statesubframe = main.loc[main["State Name"] == state]
    
    
#     ### by average
#     heapavg = []
    
#     for col in statesubframe.columns:
#         if col in adherents:
            
#             #note: heap is minheap by default in python,
#             #so we take negative of each element for maxheap
#             #python automatically compares by first element of tuple
#             if len(heapavg) >= NUMBERTOSHOW:
#                 heapq.heappushpop(heapavg, (statesubframe[col].mean(), col))
            
#             else:
#                 heapq.heappush(heapavg, (statesubframe[col].mean(), col))
    
#     ## normal plot
#     tograph = [col for _, col in heapavg]
#     ax = statesubframe.plot(x = "Year", y = tograph, title = "Top " + str(NUMBERTOSHOW)\
#                         +" Denominations in " + state + " by Average Number of Adherents"\
#                             , grid = True, ylabel = "Adherents", figsize = (20,8),\
#                             marker = ".", table = True)
#     ax.xaxis.set_label_position('top') 
#     ax.xaxis.tick_top()
#     plt.ticklabel_format(style='plain') 
#     #from https://queirozf.com/entries/matplotlib-examples-number-formatting-for-axes-labels#:~:text=Comma%20as%20thousands%20separator%20Formatting%20labels%20must%20only,with.set_yticklabels%20%28%29%20%28similar%20methods%20exist%20for%20X-axis%20too%29%3A
#     current_values = plt.gca().get_yticks()
#     plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
#     #plt.legend(loc = "center left")
#     #table(ax, np.round(statesubframe[tograph].describe(), 2),loc='upper right')
#     plt.savefig("stateoutputs/avg/" + state + '_Top' + str(NUMBERTOSHOW) +'Religions_avg.png',\
#                 bbox_inches='tight', dpi=150)
#     plt.show()
    
    # ## percentage plot
    # tograph = [col for _, col in heapavg]
    # tograph.append("Year")
    # tograph.append("Total Population")
    # ssf_pct = statesubframe[tograph]
    
    # pct_tograph = []
    # for col in ssf_pct.columns:
    #     ssf_pct[col + "_pct"] = ssf_pct[col] / ssf_pct["Total Population"]
    #     pct_tograph.append(col + "_pct")
    # pct_tograph.remove("Total Population_pct")
    # pct_tograph.remove("Year_pct")
    # ax = ssf_pct.plot(x = "Year", y = pct_tograph, title = "Top " + str(NUMBERTOSHOW)\
    #                     +" Denominations in " + state + " by Average Number of Adherents,"+\
    #                         " as a Percentage of Total Population of " + state\
    #                         , grid = True, ylabel = "Adherents as % of State Population",\
    #                             figsize = (20,8),\
    #                         marker = ".", table = True)
    # ax.xaxis.set_label_position('top') 
    # ax.xaxis.tick_top()
    # plt.ticklabel_format(style='plain') 
    # #from https://queirozf.com/entries/matplotlib-examples-number-formatting-for-axes-labels#:~:text=Comma%20as%20thousands%20separator%20Formatting%20labels%20must%20only,with.set_yticklabels%20%28%29%20%28similar%20methods%20exist%20for%20X-axis%20too%29%3A
    # current_values = plt.gca().get_yticks()
    # plt.gca().set_yticklabels(['{:,.0%}'.format(x) for x in current_values])
    # #table(ax, np.round(statesubframe[tograph].describe(), 2),loc='upper right')
    # plt.savefig("stateoutputs/avg_pct/" + state + '_Top' + str(NUMBERTOSHOW) +\
    #             'Religions_avg_pct.png',\
    #             bbox_inches='tight', dpi=150)
    # plt.show()
    
    
    ### by sum
    # heapsum = []
    
    # for col in statesubframe.columns:
    #     if col in adherents:
            
    #         #note: heap is minheap by default in python,
    #         #so we take negative of each element for maxheap
    #         #python automatically compares by first element of tuple
    #         if len(heapsum) >= NUMBERTOSHOW:
    #             heapq.heappushpop(heapsum, (statesubframe[col].sum(), col))
            
    #         else:
    #             heapq.heappush(heapsum, (statesubframe[col].sum(), col))
    
    # ## normal plot
    # tograph = [col for _, col in heapsum]
    # ax = statesubframe.plot(x = "Year", y = tograph, title = "Top " + str(NUMBERTOSHOW)\
    #                     +" Denominations in " + state + " by Sum of Number of Adherents"\
    #                         , grid = True, ylabel = "Adherents", figsize = (20,8),\
    #                         marker = ".", table = True)
    # ax.xaxis.set_label_position('top') 
    # ax.xaxis.tick_top()
    # plt.ticklabel_format(style='plain') 
    # #from https://queirozf.com/entries/matplotlib-examples-number-formatting-for-axes-labels#:~:text=Comma%20as%20thousands%20separator%20Formatting%20labels%20must%20only,with.set_yticklabels%20%28%29%20%28similar%20methods%20exist%20for%20X-axis%20too%29%3A
    # current_values = plt.gca().get_yticks()
    # plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
    # #table(ax, np.round(statesubframe[tograph].describe(), 2),loc='upper right')
    # plt.savefig("stateoutputs/sum/" + state + '_Top' + str(NUMBERTOSHOW) +'Religions_sum.png',\
    #             bbox_inches='tight', dpi=150)
    # plt.show()
    
    # ## percentage plot
    # tograph = [col for _, col in heapsum]
    # tograph.append("Year")
    # tograph.append("Total Population")
    # ssf_pct = statesubframe[tograph]
    
    # pct_tograph = []
    # for col in ssf_pct.columns:
    #     ssf_pct[col + "_pct"] = ssf_pct[col] / ssf_pct["Total Population"]
    #     pct_tograph.append(col + "_pct")
    # pct_tograph.remove("Total Population_pct")
    # pct_tograph.remove("Year_pct")
    # ax = ssf_pct.plot(x = "Year", y = pct_tograph, title = "Top " + str(NUMBERTOSHOW)\
    #                     +" Denominations in " + state + " by Sum of Number of Adherents,"+\
    #                         " as a Percentage of Total Population of " + state\
    #                         , grid = True, ylabel = "Adherents as % of State Population",\
    #                             figsize = (20,8),\
    #                         marker = ".", table = True)
    # ax.xaxis.set_label_position('top') 
    # ax.xaxis.tick_top()
    # plt.ticklabel_format(style='plain') 
    # #from https://queirozf.com/entries/matplotlib-examples-number-formatting-for-axes-labels#:~:text=Comma%20as%20thousands%20separator%20Formatting%20labels%20must%20only,with.set_yticklabels%20%28%29%20%28similar%20methods%20exist%20for%20X-axis%20too%29%3A
    # current_values = plt.gca().get_yticks()
    # plt.gca().set_yticklabels(['{:,.0%}'.format(x) for x in current_values])
    # #table(ax, np.round(statesubframe[tograph].describe(), 2),loc='upper right')
    # plt.savefig("stateoutputs/sum_pct/" + state + '_Top' + str(NUMBERTOSHOW) +\
    #             'Religions_sum_pct.png',\
    #             bbox_inches='tight', dpi=150)
    # plt.show()
    
    
    
    #### Finding greatest amount of change!
    ## by sum
    # heapsum = []
    
    # for col in statesubframe.columns:
    #     if col in adherents:
            
    #         #note: heap is minheap by default in python,
    #         #so we take negative of each element for maxheap
    #         #python automatically compares by first element of tuple
    #         if len(heapsum) >= NUMBERTOSHOW:
    #             heapq.heappushpop(heapsum, (statesubframe[col].sum(), col))
            
    #         else:
    #             heapq.heappush(heapsum, (statesubframe[col].sum(), col))
    
    # ## normal plot
    # tograph = [col for _, col in heapsum]
    # ax = statesubframe.plot(x = "Year", y = tograph, title = "Top " + str(NUMBERTOSHOW)\
    #                     +" Denominations in " + state + " by Sum of Number of Adherents"\
    #                         , grid = True, ylabel = "Adherents", figsize = (20,8),\
    #                         marker = ".", table = True)
    # ax.xaxis.set_label_position('top') 
    # ax.xaxis.tick_top()
    # plt.ticklabel_format(style='plain') 
    # #from https://queirozf.com/entries/matplotlib-examples-number-formatting-for-axes-labels#:~:text=Comma%20as%20thousands%20separator%20Formatting%20labels%20must%20only,with.set_yticklabels%20%28%29%20%28similar%20methods%20exist%20for%20X-axis%20too%29%3A
    # current_values = plt.gca().get_yticks()
    # plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
    # #table(ax, np.round(statesubframe[tograph].describe(), 2),loc='upper right')
    # plt.savefig("stateoutputs/sum/" + state + '_Top' + str(NUMBERTOSHOW) +'Religions_sum.png',\
    #             bbox_inches='tight', dpi=150)
    # plt.show()
    
    # ## percentage plot
    # tograph = [col for _, col in heapsum]
    # tograph.append("Year")
    # tograph.append("Total Population")
    # ssf_pct = statesubframe[tograph]
    
    # pct_tograph = []
    # for col in ssf_pct.columns:
    #     ssf_pct[col + "_pct"] = ssf_pct[col] / ssf_pct["Total Population"]
    #     pct_tograph.append(col + "_pct")
    # pct_tograph.remove("Total Population_pct")
    # pct_tograph.remove("Year_pct")
    # ax = ssf_pct.plot(x = "Year", y = pct_tograph, title = "Top " + str(NUMBERTOSHOW)\
    #                     +" Denominations in " + state + " by Sum of Number of Adherents,"+\
    #                         " as a Percentage of Total Population of " + state\
    #                         , grid = True, ylabel = "Adherents as % of State Population",\
    #                             figsize = (20,8),\
    #                         marker = ".", table = True)
    # ax.xaxis.set_label_position('top') 
    # ax.xaxis.tick_top()
    # plt.ticklabel_format(style='plain') 
    # #from https://queirozf.com/entries/matplotlib-examples-number-formatting-for-axes-labels#:~:text=Comma%20as%20thousands%20separator%20Formatting%20labels%20must%20only,with.set_yticklabels%20%28%29%20%28similar%20methods%20exist%20for%20X-axis%20too%29%3A
    # current_values = plt.gca().get_yticks()
    # plt.gca().set_yticklabels(['{:,.0%}'.format(x) for x in current_values])
    # #table(ax, np.round(statesubframe[tograph].describe(), 2),loc='upper right')
    # plt.savefig("stateoutputs/sum_pct/" + state + '_Top' + str(NUMBERTOSHOW) +\
    #             'Religions_sum_pct.png',\
    #             bbox_inches='tight', dpi=150)
    # plt.show()


    
    
    
            
            

=======
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


subfoldername = "statedata"

##Note: 1952 data does not have adherents! Have commented out, but
##can add back in by putting it back in "todo_list1" below
data52 = pd.read_stata(subfoldername + '/'+ '1952.dta')
#labels52iterator = pd.read_stata('1952.dta', iterator = True)
#labels52 = labels52iterator.variable_labels()

data71 = pd.read_stata(subfoldername + '/'+ '1971.dta')
labels71iterator = pd.read_stata(subfoldername + '/'+ '1971.dta', iterator = True)
labels71 = labels71iterator.variable_labels()

data80 = pd.read_stata(subfoldername + '/'+ '1980.dta')
labels80iterator = pd.read_stata(subfoldername + '/'+ '1980.dta', iterator = True)
labels80 = labels80iterator.variable_labels()

data90 = pd.read_stata(subfoldername + '/'+ '1990.dta')
labels90iterator = pd.read_stata(subfoldername + '/'+ '1990.dta', iterator = True)
labels90 = labels90iterator.variable_labels()

data2000 = pd.read_stata(subfoldername + '/'+ '2000.dta')
labels2000iterator = pd.read_stata(subfoldername + '/'+ '2000.dta', iterator = True)
labels2000 = labels2000iterator.variable_labels()

data2010 = pd.read_stata(subfoldername + '/' + '2010.dta')
labels2010iterator = pd.read_stata(subfoldername + '/'+ '2010.dta', iterator = True)
labels2010 = labels2010iterator.variable_labels()

data2020 = pd.read_excel('statedata/2020USRCStateData.xlsx')
#### 2020 data cleaned separately
#### pre-cleaned and 
#### formatted in the form of identifier--congregation name in Excel file
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
year80 = data80[['statena']].copy()
year80.columns = ["Year"]
year90 = data90[['statena']].copy()
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

## 1980
del labels80["totpop"]
cleanedlabels["Total Population"].append("totpop")
del labels80["NOCTOT80"]
cleanedlabels["Total Number of Churches"].append("NOCTOT80")
del labels80["MEMTOT80"]
cleanedlabels["Total Members"].append("MEMTOT80")
del labels80["ADHTOT80"]
cleanedlabels["Total Adherents"].append("ADHTOT80")

## 1990
del labels90["totpop"]
cleanedlabels["Total Population"].append("totpop")
del labels90["totch"]
cleanedlabels["Total Number of Churches"].append("totch")
del labels90["totmem"]
cleanedlabels["Total Members"].append("totmem")
del labels90["totadh"]
cleanedlabels["Total Adherents"].append("totadh")


## 2000
del labels2000["POP2000"]
cleanedlabels["Total Population"].append("POP2000")
del labels2000["totcg"]
cleanedlabels["Total Number of Churches"].append("totcg")
del labels2000["totad"]
cleanedlabels["Total Adherents"].append("totad")
del labels2000["totrt"]
cleanedlabels["Total Rate of Adherence"].append("totrt")
#del labels2000["adjad"]
#cleanedlabels["Adjusted Total Adherents"].append("adjad")
#del labels2000["adjrate"]
#cleanedlabels["Adjusted Total Rate of Adherence"].append("adjrate")

## 2010
del labels2010["POP2010"]
cleanedlabels["Total Population"].append("POP2010")
del labels2010["totcng"]
cleanedlabels["Total Number of Churches"].append("totcng")
del labels2010["totadh"]
cleanedlabels["Total Adherents"].append("totadh")
del labels2010["totrate"]
cleanedlabels["Total Rate of Adherence"].append("totrate")

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
identifiercols.add("State Census Code")
identifiercols.add("State Abbreviation")
identifiercols.add("State Code")

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
        del cleanedlabels[label]
    
    for label in toadd:
        cleanedlabels[label] = toadd[label].copy()
        
    endings = ["_m", "_a", "_roa", "_c", "_roap", "_roata"]
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
data90.rename(columns={ 'BMAA_C':'Baptist Missionary Association of America_c'}, inplace = True)
data90.rename(columns={ 'BMAA_A':'Baptist Missionary Association of America_a'}, inplace = True)
data90.rename(columns={ 'BMAA_M':'Baptist Missionary Association of America_m'}, inplace = True)
data90.rename(columns={ 'CGGC_A':'Churches Of God General Conference_a'}, inplace = True)
data90.rename(columns={ 'CGGC_M':'Churches Of God General Conference_m'}, inplace = True)
data90.rename(columns={ 'CGGC_C':'Churches Of God General Conference_c'}, inplace = True)
data90.rename(columns={ 'ROMORT_C':'Romanian Orthodox Episcopate Of America_c'}, inplace = True)
data90.rename(columns={ 'ROMORT_M':'Romanian Orthodox Episcopate Of America_m'}, inplace = True)
data90.rename(columns={ 'ROMORT_A':'Romanian Orthodox Episcopate Of America_a'}, inplace = True)

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
# for df in dataframes:
#     newcolnames = {}
#     c = 0
#     for column in df.keys():              
#         newcolnames[column] = str(c)+"_"+column
#         c += 1
        
#     #part of debug
#     newcolnames["Year"] = "Year"
#     df.rename(columns = newcolnames, inplace = True)


#use below for debugging along with column numbering
# for df in dataframes:
# #    print(df.Year[0])
#     seen = {}
#     num = 0
#     for c in df.keys():           
#         if c[findIndexOfSubstring(c, "_") + 1:] in seen:
#             print(c)
#             print(seen[c[findIndexOfSubstring(c, "_") + 1:]])
#             print(num)
#         seen[c[findIndexOfSubstring(c, "_") + 1:]] = num
#         num += 1
        
    #df.reset_index(inplace=True, drop=True)

#concat all clean dataframes to make the main dataframe    
main = pd.concat(dataframes, axis = 0, ignore_index = True)

#Converts all states to capital case
main["State Name"] = main["State Name"].str.title()
main["Year"] = main["Year"].astype(int)

main.to_excel("cleanedstatedata_1971_to_2020.xlsx")

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



NUMBERTOSHOW = 20

# for state in USstates:
#     statesubframe = main.loc[main["State Name"] == state]
    
    
#     ### by average
#     heapavg = []
    
#     for col in statesubframe.columns:
#         if col in adherents:
            
#             #note: heap is minheap by default in python,
#             #so we take negative of each element for maxheap
#             #python automatically compares by first element of tuple
#             if len(heapavg) >= NUMBERTOSHOW:
#                 heapq.heappushpop(heapavg, (statesubframe[col].mean(), col))
            
#             else:
#                 heapq.heappush(heapavg, (statesubframe[col].mean(), col))
    
#     ## normal plot
#     tograph = [col for _, col in heapavg]
#     ax = statesubframe.plot(x = "Year", y = tograph, title = "Top " + str(NUMBERTOSHOW)\
#                         +" Denominations in " + state + " by Average Number of Adherents"\
#                             , grid = True, ylabel = "Adherents", figsize = (20,8),\
#                             marker = ".", table = True)
#     ax.xaxis.set_label_position('top') 
#     ax.xaxis.tick_top()
#     plt.ticklabel_format(style='plain') 
#     #from https://queirozf.com/entries/matplotlib-examples-number-formatting-for-axes-labels#:~:text=Comma%20as%20thousands%20separator%20Formatting%20labels%20must%20only,with.set_yticklabels%20%28%29%20%28similar%20methods%20exist%20for%20X-axis%20too%29%3A
#     current_values = plt.gca().get_yticks()
#     plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
#     #table(ax, np.round(statesubframe[tograph].describe(), 2),loc='upper right')
#     plt.savefig("stateoutputs/avg/" + state + '_Top' + str(NUMBERTOSHOW) +'Religions_avg.png',\
#                 bbox_inches='tight', dpi=150)
#     plt.show()
    
#     ## percentage plot
#     tograph = [col for _, col in heapavg]
#     tograph.append("Year")
#     tograph.append("Total Population")
#     ssf_pct = statesubframe[tograph]
    
#     pct_tograph = []
#     for col in ssf_pct.columns:
#         ssf_pct[col + "_pct"] = ssf_pct[col] / ssf_pct["Total Population"]
#         pct_tograph.append(col + "_pct")
#     pct_tograph.remove("Total Population_pct")
#     pct_tograph.remove("Year_pct")
#     ax = ssf_pct.plot(x = "Year", y = pct_tograph, title = "Top " + str(NUMBERTOSHOW)\
#                         +" Denominations in " + state + " by Average Number of Adherents,"+\
#                             " as a Percentage of Total Population of " + state\
#                             , grid = True, ylabel = "Adherents as % of State Population",\
#                                 figsize = (20,8),\
#                             marker = ".", table = True)
#     ax.xaxis.set_label_position('top') 
#     ax.xaxis.tick_top()
#     plt.ticklabel_format(style='plain') 
#     #from https://queirozf.com/entries/matplotlib-examples-number-formatting-for-axes-labels#:~:text=Comma%20as%20thousands%20separator%20Formatting%20labels%20must%20only,with.set_yticklabels%20%28%29%20%28similar%20methods%20exist%20for%20X-axis%20too%29%3A
#     current_values = plt.gca().get_yticks()
#     plt.gca().set_yticklabels(['{:,.0%}'.format(x) for x in current_values])
#     #table(ax, np.round(statesubframe[tograph].describe(), 2),loc='upper right')
#     plt.savefig("stateoutputs/avg_pct/" + state + '_Top' + str(NUMBERTOSHOW) +\
#                 'Religions_avg_pct.png',\
#                 bbox_inches='tight', dpi=150)
#     plt.show()
    
    
#     ### by sum
#     heapsum = []
    
#     for col in statesubframe.columns:
#         if col in adherents:
            
#             #note: heap is minheap by default in python,
#             #so we take negative of each element for maxheap
#             #python automatically compares by first element of tuple
#             if len(heapsum) >= NUMBERTOSHOW:
#                 heapq.heappushpop(heapsum, (statesubframe[col].sum(), col))
            
#             else:
#                 heapq.heappush(heapsum, (statesubframe[col].mean(), col))
    
#     ## normal plot
#     tograph = [col for _, col in heapsum]
#     ax = statesubframe.plot(x = "Year", y = tograph, title = "Top " + str(NUMBERTOSHOW)\
#                         +" Denominations in " + state + " by Sum of Number of Adherents"\
#                             , grid = True, ylabel = "Adherents", figsize = (20,8),\
#                             marker = ".", table = True)
#     ax.xaxis.set_label_position('top') 
#     ax.xaxis.tick_top()
#     plt.ticklabel_format(style='plain') 
#     #from https://queirozf.com/entries/matplotlib-examples-number-formatting-for-axes-labels#:~:text=Comma%20as%20thousands%20separator%20Formatting%20labels%20must%20only,with.set_yticklabels%20%28%29%20%28similar%20methods%20exist%20for%20X-axis%20too%29%3A
#     current_values = plt.gca().get_yticks()
#     plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
#     #table(ax, np.round(statesubframe[tograph].describe(), 2),loc='upper right')
#     plt.savefig("stateoutputs/sum/" + state + '_Top' + str(NUMBERTOSHOW) +'Religions_sum.png',\
#                 bbox_inches='tight', dpi=150)
#     plt.show()
    
#     ## percentage plot
#     tograph = [col for _, col in heapsum]
#     tograph.append("Year")
#     tograph.append("Total Population")
#     ssf_pct = statesubframe[tograph]
    
#     pct_tograph = []
#     for col in ssf_pct.columns:
#         ssf_pct[col + "_pct"] = ssf_pct[col] / ssf_pct["Total Population"]
#         pct_tograph.append(col + "_pct")
#     pct_tograph.remove("Total Population_pct")
#     pct_tograph.remove("Year_pct")
#     ax = ssf_pct.plot(x = "Year", y = pct_tograph, title = "Top " + str(NUMBERTOSHOW)\
#                         +" Denominations in " + state + " by Sum of Number of Adherents,"+\
#                             " as a Percentage of Total Population of " + state\
#                             , grid = True, ylabel = "Adherents as % of State Population",\
#                                 figsize = (20,8),\
#                             marker = ".", table = True)
#     ax.xaxis.set_label_position('top') 
#     ax.xaxis.tick_top()
#     plt.ticklabel_format(style='plain') 
#     #from https://queirozf.com/entries/matplotlib-examples-number-formatting-for-axes-labels#:~:text=Comma%20as%20thousands%20separator%20Formatting%20labels%20must%20only,with.set_yticklabels%20%28%29%20%28similar%20methods%20exist%20for%20X-axis%20too%29%3A
#     current_values = plt.gca().get_yticks()
#     plt.gca().set_yticklabels(['{:,.0%}'.format(x) for x in current_values])
#     #table(ax, np.round(statesubframe[tograph].describe(), 2),loc='upper right')
#     plt.savefig("stateoutputs/sum_pct/" + state + '_Top' + str(NUMBERTOSHOW) +\
#                 'Religions_sum_pct.png',\
#                 bbox_inches='tight', dpi=150)
#     plt.show()
    
    
    
            
            

>>>>>>> 5a46eb1b49468cb7637e965a10f6fb620da9e0f1
