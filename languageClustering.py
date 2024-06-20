from functions import *
import os.path


'''# only using english, french, and german bc other languages do not have enough data
langs = ["English","French","German"]
allRules = []

print("Loading Rules")
for lang in langs: 
    f = open("languageDividedRules/"+lang+"Rules.txt","r")
    allRules.append(pd.DataFrame(f.read().splitlines(),columns=['Description'])['Description'])
    f.close()'''




print("Fetching Embeddings")
'''for i in range(len(allRules)):
    if not os.path.isfile("language_csv_files/"+langs[i]+"Embeddings.csv"):
        e = makeEmbeddings(allRules[i], multi=False)
        e.to_csv("language_csv_files/"+langs[i]+"Embeddings.csv",index=False)
        e2d = pd.DataFrame(make2D(e.drop(['Description'],axis=1)))
        e2d.to_csv("language_csv_files/"+langs[i]+"Embeddings2d.csv",index=False)'''
'''freRules = pd.read_csv('language_csv_files/frenchCleaned2.csv')
df = pd.DataFrame()
df['Description']=freRules['Description']
frenchTranslatedEmbeddings = makeEmbeddings(df['Description'],multi=False)
frenchTranslatedEmbeddings.to_csv('language_csv_files/FrenchTranslatedEmbeddings.csv')

gerRules = pd.read_csv('language_csv_files/germanCleaned2.csv')
df = pd.DataFrame()
df['Description']=gerRules['Description']
germanTranslatedEmbeddings = makeEmbeddings(df['Description'],multi=False)
germanTranslatedEmbeddings.to_csv('language_csv_files/GermanTranslatedEmbeddings.csv')'''


print("Starting Clustering")
'''allEmbeddings = []
for i in langs:
    allEmbeddings.append(pd.read_csv("language_csv_files/"+i+"Embeddings.csv",index_col=False))'''
kmeansToTest = range(17,35)
'''for i in range(len(allEmbeddings)):
    if not os.path.isfile("language_csv_files/"+langs[i]+"Clusters.csv"):
        embeddings = allEmbeddings[i]
        clusterDf = doKmeans(embeddings,kmeansToTest)
        clusterDf.to_csv("language_csv_files/"+langs[i]+"Clusters.csv",index=False)'''


#french = pd.read_csv("language_csv_files/FrenchTranslatedEmbeddings.csv")
#german = pd.read_csv("language_csv_files/GermanTranslatedEmbeddings.csv")




'''freClusters = doKmeans(frenchTranslatedEmbeddings,kmeansToTest)
freClusters.to_csv('language_csv_files/FrenchTranslatedClusters.csv')
gerClusters = doKmeans(germanTranslatedEmbeddings,kmeansToTest)
gerClusters.to_csv('language_csv_files/GermanTranslatedClusters.csv')'''
gerClusters = pd.read_csv('language_csv_files/GermanTranslatedClusters.csv',index_col=False)
freClusters = pd.read_csv('language_csv_files/FrenchTranslatedClusters.csv',index_col=False)
engClusters = pd.read_csv('language_csv_files/EnglishClusters.csv',index_col=False)

printClusterSet(engClusters,17)
printClusterSet(freClusters,17)
printClusterSet(gerClusters,17)


#printClusterSet(pd.read_csv("language_csv_files/"+langs[0]+"Clusters.csv"),30)

'''engClusterDf = pd.read_csv("language_csv_files/EnglishClusters.csv",index_col=False)
freClusterDf = pd.read_csv("language_csv_files/FrenchClusters.csv",index_col=False)
gerClusterDf = pd.read_csv("language_csv_files/GermanClusters.csv",index_col=False)'''

'''eng2d = pd.read_csv("language_csv_files/EnglishEmbeddings2d.csv",index_col=False)
fre2d = pd.read_csv("language_csv_files/FrenchEmbeddings2d.csv",index_col=False)
ger2d = pd.read_csv("language_csv_files/GermanEmbeddings2d.csv",index_col=False)

plt.scatter(x=eng2d['0'].tolist(),y=eng2d['1'].tolist(),c=engClusterDf['Kmeans 25'].tolist())
plt.show()'''


# 31 clusters lets go
#printClusterSet(engClusterDf,31)

#printClusterSet(freClusterDf,31)
#printClusterSet(gerClusterDf,31)
