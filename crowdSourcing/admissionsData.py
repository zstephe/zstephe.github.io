import pandas as pd
import matplotlib.pyplot as plt

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
print(uniqueLangs)
print(counts)
print(uniqueLangs[counts.index(23)])
plt.pie(counts,labels=uniqueLangs)
plt.show()