import pandas as pd
import numpy as np
from kmodes.kmodes import KModes
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy.stats import *
from sklearn.decomposition import PCA



''' 
does a single kmeans run
@param numClusters = number of clusters to divide into
@param embeddings = number version of dataset in terms of dataframe
@param randomSeed = random state constant (for reproduceability)
@return kmeans
'''
def fitKmeans(numClusters,embeddings,randomSeed=5):
    kmeans =KMeans(n_clusters = numClusters,random_state=randomSeed)
    kmeans.fit(embeddings)
    return kmeans


'''
prints the clusters in the df based on the labels in the kmeans column
@param df = dataframe with cluster info
@param num = cluster num to look at
'''
def printClusterSet(df,num):
    for cluster in range(num):
        print("Cluster "+str(cluster))
        print(df[df["Kmeans "+str(num)]==cluster])
        print("\n\n")



'''
Does kmeans for a range of vals
@param df = dataframe containing the number version of data
@param kmeansToTest = list of vals to test as kmeans clusters
@param showInertias = whether to show the inertia plot
@param randomSeed = random state constant (for reproduceability)
return = dataframe containing all the cluster info alongside the input dataframe
'''
def doKmeans(df,kmeansToTest,showIntertias=True,randomSeed=5):
    # calculates inertias and kmeans clusters for each kmeans val to test
    inertias = []
    kmeansLabels = []
    for i in kmeansToTest:
        kmeans = fitKmeans(i,df,randomSeed=randomSeed)
        inertias.append(kmeans.inertia_)
        kmeansLabels.append(kmeans.labels_)

    # adds the cluster data to a df
    clusterDf = pd.DataFrame(df)
    for i in kmeansToTest:
        clusterDf['Kmeans '+str(i)] = kmeansLabels[i-kmeansToTest[0]]

    # shows the plot if wanted
    if(showIntertias):
        plt.figure(figsize=(8,6))
        plt.scatter(kmeansToTest,inertias)
        plt.xlabel("Number of Clusters")
        plt.title('Kmeans Inertias')
        plt.ylabel("Inertia")
        plt.show()
    return clusterDf



'''
prints age stats for each cluster
@param df = dataframe containing the cluster information and the age column
@param num = cluster number to look at
@return 2d list of ages based on cluster num (index in list is the cluster num)
'''
def printClusterSetAge(df,num):
    clusterRows = []
    for cluster in range(num):
        print("Cluster "+str(cluster))
        rows = df[df["Kmeans "+str(num)]==cluster]["Age"]
        print("mean: "+ str(np.mean(rows)))
        #print(rows)
        print("")
        clusterRows.append(rows)
    return clusterRows



'''
prints anova and tukey test (if wanted) on age
@param df = dataframe containing age and number mapped data
@param colName = column to check if answers correlated with age (question cols for this)
@param tukey = whether or not to do tukey test as well (default = false) 
'''
def pValTest(df,colName,tukey=False):
    rows = []
    for val in df[colName].unique():
        rows.append(df[df[colName]==val]["Age"])
    result = f_oneway(*rows,nan_policy="omit")
    if tukey:
        # accounts for if only one datapoint of a value
        new = []
        for row in rows:
            if len(row)>1:
                new.append(row)
            else:
                print("SKIPPING A VALUE DUE TO LACK OF DATA (ONLY 1 POINT AVAILABLE)")

        return result, tukey_hsd(*new)
    return result




# checks if the types of answers in the second column are dependent on the first col value (returns p-vals)
def compareCols(q1,q2):
    q2unique = q2.unique()
    q2counts = list(q2.value_counts())
    q2percents = [x/(len(q2)) for x in q2counts]
    dividedCounts = []
    dividedPercents = []
    dividedPercents.append(q2percents)
    for answer in q1.unique():
        dividedCounts.append([])
        for unique in q2unique:
            dividedCounts[-1].append(list(q2[q1==answer]).count(unique))
        dividedPercents.append([x/sum(dividedCounts[-1]) for x in dividedCounts[-1]])
    p_vals = []
    for i in range(1,len(dividedPercents)):
        p_vals.append(chisquare(dividedPercents[i],q2percents).pvalue)
    return p_vals, dividedPercents


def examineQuestion(q,df,ageCol):
    d = pd.DataFrame(ageCol.dropna())
    d[q]=df[q]
    
    result, tukey = pValTest(d,q,tukey=True)
    print(tukey)

    vals = df[q].unique()
    print("Counts of each Response")
    print(df[q].value_counts())
    print()
    print("Group Means")
    df['Age']=ageCol
    for val in vals:
        print(val+" : ",end='')
        print(df[df[q]==val]['Age'].mean())
        print()