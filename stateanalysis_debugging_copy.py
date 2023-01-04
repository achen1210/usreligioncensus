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
from collections import defaultdict
from collections import Counter
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
        key = key.strip()
        newnames2020[column] = key + colsplit[0]
        
    else:
        newnames2020[column] = column

data2020.rename(columns = newnames2020, inplace = True)

### Add years to all dataframe data!
# Create a column dataframe with the year for concatenation
# Not sure how to do it in one line so here's a bodge job
# Normal setting causes Dataframe fragmentation error,
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
#dataframes = [data80, data90]
dataframes = [data71, data80, data90, data2000, data2010, data2020] #, data52]

#### key will be the label description (all uppercase), values will be the various names used,
#### e.g. {"STATE NAME" : [name, statena]} etc.
#### maps to set because we don't want duplicates

#set would be better than list for cleanedvariables, but we want to verify
#that nothing went missing
cleanedlabels = defaultdict(list)

for column in data2020.keys():
    cleanedlabels[column].append("2020placeholder")
 
### Hand replace errors - labels only go to 80 characters so some need manual fixing
### takes out of dictionary, then appends it separately to cleanedlabels and replacement
# del labels2000["alorart"]
# cleanedlabels["Albanian Orthodox Diocese of America_roa"].append("alorart")

# del labels2000["eaorcg"]
# cleanedlabels["American CarpathoRussian Orthodox Greek Catholic Church_c"].append("eaorcg")

# del labels2000["antamcg"]
# cleanedlabels["Antiochian Orthodox Christian Archdiocese Of North America_c"].append("antamcg")

# del labels2000["apcatad"]
# cleanedlabels["Apostolic Catholic Assyrian Church Of The East North America_a"].append("apcatad")

# del labels2000["apcatcg"]
# cleanedlabels["Apostolic Catholic Assyrian Church Of The East North America_c"].append("apcatcg")

# del labels2000["apcatrt"]
# cleanedlabels["Apostolic Catholic Assyrian Church Of The East North America_roa"].append("apcatrt")

# del labels2000["frlutcg"]
# cleanedlabels["Association of Free Lutheran Congregations_c"].append("frlutcg")

# del labels2000["frlutad"]
# cleanedlabels["Association of Free Lutheran Congregations_a"].append("frlutad")

# del labels2000["frlutrt"]
# cleanedlabels["Association of Free Lutheran Congregations_roa"].append("frlutrt")

# del labels2000["cccadrt"]
# cleanedlabels["Congregational Christian Churches appenditional Not In Any Ccc Body_roa"].append("cccadrt")

# del labels2000["cccadcg"]
# cleanedlabels["Congregational Christian Churches appenditional Not In Any Ccc Body_c"].append("cccadcg")

# del labels2000["cccadad"]
# cleanedlabels["Congregational Christian Churches appenditional Not In Any Ccc Body_a"].append("cccadad")

# del labels2000["gsixbcg"]
# cleanedlabels["General Six Principle Baptists_c"].append("gsixbcg")

# del labels2000["gsixbad"]
# cleanedlabels["General Six Principle Baptists_a"].append("gsixbad")

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
            key = label_list[0].title().strip()
        
        else:   
            key = label_list[1].title().strip()
            
        key += identifier
        
        #gets rid of things like U.S.A. vs USA,
        #Church of God, Memmonite vs Church of God (Memmonite)
        key = key.replace(".", "")
        key = key.replace(",", "")
        key = key.replace("-", "")
        key = key.replace("(", "")
        key = key.replace(")", "")
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

        if len(label_list) > 1:
            temp = label_list[1].split(" ")
            
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
                    
        key += identifier
        
        #gets rid of things like U.S.A. vs USA,
        #Church of God, Memmonite vs Church of God (Memmonite)
        key = key.replace(".", "")
        key = key.replace(",", "")
        key = key.replace("-", "")
        key = key.replace("(", "")
        key = key.replace(")", "")
        key = key.replace("Usa", "USA")
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

#### Some names of congregations are too long, cutting off part of the label
#### This part tries to fix it; if label ends in:
#### "adh", "ad" = adherents
#### "rate", "rt" = rate of adherence
#### "cng", "cg" = congregations     
todelete = set()
toappend = []
for label in cleanedlabels:
    x = label[-len("_a"):]
    y = label[-len("_roa"):]
    roap = label[-len("_roap"):]
    roata = label[-len("_roata"):]
    
    if x != "_c" and x != "_a" and x != "_m" and y != "_roa"\
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
                levDistance(label, other) <= dist:
                
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
print("Note for \"Moravian Church In America\": there is a \"Northern Province\" and \"Southern Province\" in the data,"+
      " here they have been combined.")
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
      "'_roata', '_roap' ending:")
for label in cleanedlabels:
    x = label[-len("_a"):]
    y = label[-len("_roa"):]
    roap = label[-len("_roap"):]
    roata = label[-len("_roata"):]
    
    if x != "_c" and x != "_a" and x != "_m" and y != "_roa"\
        and roap != "_roap" and roata != "_roata":
        print(label + ":")
        for item in cleanedlabels[label]:
            print(item)
        print("+++++++++++++++++++++++++++++++++++++++++++++++")
        

countdups = 0
### make replacement
replacement = {}
for label in cleanedlabels:
    for varname in cleanedlabels[label]:
        if varname != "2020placeholder" and \
        replacement.get(varname):
            if replacement[varname] != label:
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


#### Replace!
print("Column headers that don't end in one of the endings:")
for df in dataframes:
    newcolnames = {}
    for column in df.keys():
        
        flag = False
        for ending in endings:
            if ending in column:
                flag = True
        if not flag:
            print(column)
            
        if column in replacement:
            newcolnames[column] = replacement[column]
        else:
            newcolnames[column] = column

    df.rename(columns = newcolnames, inplace = True)

#### Make main dataframe
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
from collections import defaultdict
from collections import Counter
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
        key = key.strip()
        newnames2020[column] = key + colsplit[0]
        
    else:
        newnames2020[column] = column

data2020.rename(columns = newnames2020, inplace = True)

### Add years to all dataframe data!
# Create a column dataframe with the year for concatenation
# Not sure how to do it in one line so here's a bodge job
# Normal setting causes Dataframe fragmentation error,
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
#dataframes = [data80, data90]
dataframes = [data71, data80, data90, data2000, data2010, data2020] #, data52]

#### key will be the label description (all uppercase), values will be the various names used,
#### e.g. {"STATE NAME" : [name, statena]} etc.
#### maps to set because we don't want duplicates

#set would be better than list for cleanedvariables, but we want to verify
#that nothing went missing
cleanedlabels = defaultdict(list)

for column in data2020.keys():
    cleanedlabels[column].append("2020placeholder")
 
### Hand replace errors - labels only go to 80 characters so some need manual fixing
### takes out of dictionary, then appends it separately to cleanedlabels and replacement
# del labels2000["alorart"]
# cleanedlabels["Albanian Orthodox Diocese of America_roa"].append("alorart")

# del labels2000["eaorcg"]
# cleanedlabels["American CarpathoRussian Orthodox Greek Catholic Church_c"].append("eaorcg")

# del labels2000["antamcg"]
# cleanedlabels["Antiochian Orthodox Christian Archdiocese Of North America_c"].append("antamcg")

# del labels2000["apcatad"]
# cleanedlabels["Apostolic Catholic Assyrian Church Of The East North America_a"].append("apcatad")

# del labels2000["apcatcg"]
# cleanedlabels["Apostolic Catholic Assyrian Church Of The East North America_c"].append("apcatcg")

# del labels2000["apcatrt"]
# cleanedlabels["Apostolic Catholic Assyrian Church Of The East North America_roa"].append("apcatrt")

# del labels2000["frlutcg"]
# cleanedlabels["Association of Free Lutheran Congregations_c"].append("frlutcg")

# del labels2000["frlutad"]
# cleanedlabels["Association of Free Lutheran Congregations_a"].append("frlutad")

# del labels2000["frlutrt"]
# cleanedlabels["Association of Free Lutheran Congregations_roa"].append("frlutrt")

# del labels2000["cccadrt"]
# cleanedlabels["Congregational Christian Churches appenditional Not In Any Ccc Body_roa"].append("cccadrt")

# del labels2000["cccadcg"]
# cleanedlabels["Congregational Christian Churches appenditional Not In Any Ccc Body_c"].append("cccadcg")

# del labels2000["cccadad"]
# cleanedlabels["Congregational Christian Churches appenditional Not In Any Ccc Body_a"].append("cccadad")

# del labels2000["gsixbcg"]
# cleanedlabels["General Six Principle Baptists_c"].append("gsixbcg")

# del labels2000["gsixbad"]
# cleanedlabels["General Six Principle Baptists_a"].append("gsixbad")

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
            key = label_list[0].title().strip()
        
        else:   
            key = label_list[1].title().strip()
            
        key += identifier
        
        #gets rid of things like U.S.A. vs USA,
        #Church of God, Memmonite vs Church of God (Memmonite)
        key = key.replace(".", "")
        key = key.replace(",", "")
        key = key.replace("-", "")
        key = key.replace("(", "")
        key = key.replace(")", "")
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

        if len(label_list) > 1:
            temp = label_list[1].split(" ")
            
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
                    
        key += identifier
        
        #gets rid of things like U.S.A. vs USA,
        #Church of God, Memmonite vs Church of God (Memmonite)
        key = key.replace(".", "")
        key = key.replace(",", "")
        key = key.replace("-", "")
        key = key.replace("(", "")
        key = key.replace(")", "")
        key = key.replace("Usa", "USA")
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

#### Some names of congregations are too long, cutting off part of the label
#### This part tries to fix it; if label ends in:
#### "adh", "ad" = adherents
#### "rate", "rt" = rate of adherence
#### "cng", "cg" = congregations     
todelete = set()
toappend = []
for label in cleanedlabels:
    x = label[-len("_a"):]
    y = label[-len("_roa"):]
    roap = label[-len("_roap"):]
    roata = label[-len("_roata"):]
    
    if x != "_c" and x != "_a" and x != "_m" and y != "_roa"\
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
                levDistance(label, other) <= dist:
                
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
print("Note for \"Moravian Church In America\": there is a \"Northern Province\" and \"Southern Province\" in the data,"+
      " here they have been combined.")
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
      "'_roata', '_roap' ending:")
for label in cleanedlabels:
    x = label[-len("_a"):]
    y = label[-len("_roa"):]
    roap = label[-len("_roap"):]
    roata = label[-len("_roata"):]
    
    if x != "_c" and x != "_a" and x != "_m" and y != "_roa"\
        and roap != "_roap" and roata != "_roata":
        print(label + ":")
        for item in cleanedlabels[label]:
            print(item)
        print("+++++++++++++++++++++++++++++++++++++++++++++++")
        

countdups = 0
### make replacement
replacement = {}
for label in cleanedlabels:
    for varname in cleanedlabels[label]:
        if varname != "2020placeholder" and \
        replacement.get(varname):
            if replacement[varname] != label:
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


#### Replace!
print("Column headers that don't end in one of the endings:")
for df in dataframes:
    newcolnames = {}
    for column in df.keys():
        
        flag = False
        for ending in endings:
            if ending in column:
                flag = True
        if not flag:
            print(column)
            
        if column in replacement:
            newcolnames[column] = replacement[column]
        else:
            newcolnames[column] = column

    df.rename(columns = newcolnames, inplace = True)

#### Make main dataframe
>>>>>>> 5a46eb1b49468cb7637e965a10f6fb620da9e0f1
#main = pd.concat(dataframes, axis = 0, ignore_index = True)