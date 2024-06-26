import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np

data = pd.read_csv("crowdSourcing/admissionsData.csv")
languages = list(data["Language 1"])
total = len(languages)
uniqueLangs = []
counts = []
for lang in languages:
    if lang not in uniqueLangs:
        uniqueLangs.append(lang)
        counts.append(1)
    else:
        counts[uniqueLangs.index(lang)]+=1
#plt.pie(counts,labels=uniqueLangs)
#plt.show()


homeLangs1 = data[data["Language 1 Proficiency"].str.contains(r"Spoken at Home",na=False)][["Language 1","Language 1 Proficiency"]]
homeLangs2 = data[data["Language 2 Proficiency"].str.contains(r"Spoken at Home",na=False)][["Language 2","Language 2 Proficiency"]]
homeLangs3 = data[data["Language 3 Proficiency"].str.contains(r"Spoken at Home",na=False)][["Language 3","Language 3 Proficiency"]]
homeLangs4 = data[data["Language 4 Proficiency"].str.contains(r"Spoken at Home",na=False)][["Language 4","Language 4 Proficiency"]]
homeLangs5 = data[data["Language 5 Proficiency"].str.contains(r"Spoken at Home",na=False)][["Language 5","Language 5 Proficiency"]]
totalHomeLangs = float(len(homeLangs1)+len(homeLangs2)+len(homeLangs3)+len(homeLangs4)+len(homeLangs5))

homeCounts = []
for lang in range(len(uniqueLangs)):
    homeCounts.append(0)
    homeCounts[lang]+= len(homeLangs1[homeLangs1["Language 1"]==uniqueLangs[lang]])
    homeCounts[lang]+= len(homeLangs2[homeLangs2["Language 2"]==uniqueLangs[lang]])
    homeCounts[lang]+= len(homeLangs3[homeLangs3["Language 3"]==uniqueLangs[lang]])
    homeCounts[lang]+= len(homeLangs4[homeLangs4["Language 4"]==uniqueLangs[lang]])
    homeCounts[lang]+= len(homeLangs5[homeLangs5["Language 5"]==uniqueLangs[lang]])

homePercents = []
for x in homeCounts:
    homePercents.append(float(x)/totalHomeLangs)

#plt.pie(homePercents,labels=uniqueLangs)
#plt.show()

ourHome = pd.read_csv("crowdSourcing/percentData.csv")
ourHome = ourHome[ourHome["LANGUAGE"]=="What language do you speak at home?"]

ourHomeLangs = ourHome.columns[1:]
allLangs = list(uniqueLangs)
for lang in ourHomeLangs:
    if(ourHome[lang].values[0]!=0):
        print(ourHome[lang])
        if lang not in allLangs:
            allLangs.append(lang)

for i in range(len(allLangs)-len(uniqueLangs)):
    homePercents.append(0)
ourHomePercents = []
for lang in allLangs:
    try:
        ourHomePercents.append(float(ourHome[lang]))
    except:
        ourHomePercents.append(0)

x_axis = np.arange(len(allLangs))
plt.bar(x_axis-0.25,homePercents,label="Admissions",width=0.5)
plt.bar(x_axis+0.25,ourHomePercents,label="Ours",width=0.5)
plt.xticks(x_axis,allLangs,rotation=90,fontsize=5)
plt.subplots_adjust(bottom=0.5)
plt.legend()
plt.show()