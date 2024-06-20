from functions import *

# Read in the data file
data = pd.read_csv('csv_files/all-rule-data.csv',index_col=False)
# isolate the rows with passed rules
data = data[data['Status']=='passed']
# isolate the description column and make all lowercase
data = data['Description'].str.lower()
data = pd.read_csv("language_csv_files/germanCleaned.csv")['Description']


# list of phrases to remove involving "characters"
characterRemovalList = ["all characters with ","only characters with ","characters with ",
"all characters consisting of ","characters composed of ","characters made out of ","characters of ",
"characters containing ","characters including ",
"this character has ","character has ","characters have a ","all characters have ","characters have "
"characters that are ","characters that contain ", "characters that ",
" as part of the character"," of the character","in this character ", 
"characters consist of ","characters contain s ","characters are formed by ","all characters contain ",
"all characters are ","all characters where ","all characters that ","all characters made up of ",
"all characters created by ","characters which consist of ","characters consisting of ","characters made of ",
"the characters are all look like ","any character that ","any character with ", "the character ",
"character contains ","character includes ","all characters incorporating ","all characters ","characters made with ",
"characters drawn with ","characters made with ","characters constructed with ","characters are ",
"characters made up of ","characters contain ","characters made up by ","characters made from ",
"characters where ","characters have ","character with ","characters having ","characters comprising ","characters whose ","all of these characters ","all these characters ",
"characters comprising ","these characters ","character whose ","characters","character"]

# a few more things to remove
otherRemovalList = ["testedrule","retestedrule",'"',"'","“","‘","”","’"]

# things to remove involving "letter"
letterRemovalList = ["all letters with ","letters with ","letters that are ","letters that ","letters made up of ","all of these letters ",
                     "all letters are ","these letters ","letters have ","letters made of ","letters containing ","letter with ","letter having ","letter containing "]


# goes through every description and removes the above phrases

for row in range(len(data)):
    words = data.iloc[row]
    if("character" in words):
        for line in characterRemovalList:
            if line in words:
                data.iloc[row] = words.replace(line,"")
                break
    if("letter" in words):
        for line in letterRemovalList:
            if line in words:
                data.iloc[row] = words.replace(line,"")
                break
    words = data.iloc[row]
    for line in otherRemovalList:
        if line in words:
            data.iloc[row] = words.replace(line,"")
    

# saves the cleaned rule list in a csv file
#data.to_csv("csv_files/cleanedData.csv",index=False)
data.to_csv("language_csv_files/germanCleaned2.csv",index=False)