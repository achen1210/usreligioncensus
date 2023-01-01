library(readxl)
library(dplyr)


#read in data; note Excel sheets are already cleaned for state names, so STATENAME
#is the standard column header for state names, TOTALPOP is that state's population,
#etc.
data52 <- read_excel("Churches and Church Membership in the United States, 1952 (States).XLS")
data71 <- read_excel("Churches and Church Membership in the United States, 1971 (States).XLS")
data80 <- read_excel("Churches and Church Membership in the United States, 1980 (States).XLSX")
data90 <- read_excel("Churches and Church Membership in the United States, 1990 (States).XLSX")
data2000 <- read_excel("Religious Congregations and Membership Study, 2000 (State File).XLSX")
data2010 <- read_excel("U.S. Religion Census Religious Congregations and Membership Study, 2010 (State File).XLSX")

#add year the data was from
data52$Year <- 1952
data71$Year <- 1971
data80$Year <- 1980
data90$Year <- 1990
data2000$Year <- 2000
data2010$Year <- 2010

#full outer join all files
merged <- merge(data52, data71, all = TRUE)
merged <- merge(merged, data80, all = TRUE)
merged <- merge(merged, data90, all = TRUE)
merged <- merge(merged, data2000, all = TRUE)
merged <- merge(merged, data2010, all = TRUE)
merged <- merged %>% select(Year, everything()) 
merged <- merged %>% select(STATENAME, everything()) 
