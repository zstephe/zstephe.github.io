import pandas as pd
import matplotlib.pyplot as plt
data = pd.read_csv("crowdSourcing/allData.csv",index_col=False)
percentData = pd.read_csv("crowdSourcing/percentData.csv")
#plt.pie(data['What language do you speak to your Wellesley friends in?'],labels=data['LANGUAGE'])
#plt.show()



percentEnglish = []
for col in data.drop("LANGUAGE",axis=1).columns:
    percentEnglish.append(data[col].iloc[0]/data[col].iloc[-1])
#print(percentEnglish)


categories = data.drop("LANGUAGE",axis=1).columns
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(categories, percentEnglish)

# Set the labels with a rotation
ax.set_xticklabels(categories, rotation=30, ha='right')
plt.subplots_adjust(bottom=0.5)
plt.show()

percentData.plot(x='LANGUAGE',kind="bar",stacked=True)

# Put a legend to the right of the current axis
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()