from nltk.tokenize import word_tokenize
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import re
import numpy as np
import matplotlib.cm as cm



'''
Makes a list of all the words in the rules (doesn't work on scripts with no spaces)
@param column = datafram column containing the descriptions
@return vocab list
'''
def makeVocabList(column):
    vocabList = []
    # characters to remove from the descriptions
    regex = re.compile(r'[\[\]%;#\\@`_+/()*:,.!?=0-9><~^&\$\-‘’“”„\'"\|]')
    # goes through each description
    for rule in column:
        rule = str(rule)
        # removes the characters from the descriptions
        rule = re.sub(regex, " ", rule)
        # splits into words (by whitespace)
        rule = rule.split()
        # goes through each word and adds to the vocab list if not already in
        for word in rule:
            if word not in vocabList:
                vocabList.append(word)
    return vocabList

def getTopDict(dict, timesUsed):
    return list(filter(lambda x: dict[x] > timesUsed, dict))


'''
Gets the sentences that have passed
@param df = dataframe to parse
@return column of sentences
'''
def getPassedCol(df):
    # get all the passed rules
    passed = df[df['Status']=='passed']
    # make lowercase
    passed['Description'] = passed['Description'].str.lower()
    # returns the sentence column
    return passed['Description']


def getWordTokens(col):
    tokens=[]
    data = []
    words = []
    for row in col:
        for word in word_tokenize(row):
            tokens.append(word.lower())
            if word not in words:
                words.append(word)
    data.append(tokens)
    return data


# takes in the column with descriptions
# returns dataframe with embeddings and column with sentences called "Description"
def makeEmbeddings(col, multi=True):
    # Load a pretrained Sentence Transformer model
    if(multi):
        # a multilingual model
        model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")
    else:
        # non-multilingual model
        model = SentenceTransformer("all-MiniLM-L6-v2")
    
    # The sentences to encode
    sentences = col.values  
    # Calculate embeddings
    embeddings = model.encode(sentences)
    embedded_df = pd.DataFrame(embeddings)
    embedded_df.insert(0,"Description",sentences,True)
    return embedded_df


def make2D(embeddings):
    # reduce the dimension first before using t-SNE
    X_pca = PCA(n_components=50).fit_transform(embeddings)
    # use t-SNE to get to 2D
    X_embedded = TSNE(n_components=2).fit_transform(X_pca)
    return X_embedded

'''
Takes in the number of clusters and the embeddings data and clusters the responses
@param numClusters = number of clusters to use (kmeans)
@param embeddings = pandas dataframe containing embeddings vectors in each row
@return the kmeans clusters
'''
def fitKmeans(numClusters,embeddings,randomSeed = 5):
    kmeans =KMeans(n_clusters = numClusters,random_state=randomSeed)
    kmeans.fit(embeddings)
    return kmeans

'''
Does Kmeans clustering on a bunch of different numbers of clusters and returns the output
@param embeddings = pandas dataframe containing embeddings vectors in each row
@param kmeansToTest = list of cluster numbers to test
@param showInertias = whether to show the inertias graph (default to showing)
@return dataframe containing the clustering data: each row contains the description,
'''
def doKmeans(embeddings,kmeansToTest,showIntertias=True,saveInertias=False,randomSeed = 5):
    # calculates inertias and kmeans clusters for each kmeans val to test
    inertias = []
    kmeansLabels = []
    for i in kmeansToTest:
        kmeans = fitKmeans(i,embeddings.drop('Description',axis=1),randomSeed=randomSeed)
        inertias.append(kmeans.inertia_)
        kmeansLabels.append(kmeans.labels_)

    # adds the cluster data to a df
    clusterDf = pd.DataFrame(embeddings['Description'])
    for i in kmeansToTest:
        clusterDf['Kmeans '+str(i)] = kmeansLabels[i-kmeansToTest[0]]

    # shows graph of inertias for the user to decide where to make the cutoff
    plt.figure(figsize=(8,6))
    plt.scatter(kmeansToTest,inertias)
    plt.title("Kmeans Inertias")
    plt.xlabel("Number of Clusters")
    plt.ylabel("Inertia")
    
    if(saveInertias):
        plt.savefig("../html_files/inertias.png",bbox_inches="tight")
    if(showIntertias):
        plt.show()
    return clusterDf

'''
Creates plt scatter of the clusters with clusters colored
@param embeddings2d = pandas dataframe with 2 columns containing 2d features of the data
@param clusters = pandas dataframe containing the cluster information
@param clusterNum = number of clusters to use to color the points
@param ignore = clusters to ignore (used to remove noisy clusters from data)
'''
def visualize2D(embeddings2d,clusters,clusterNum,ignore=[],savefig = False):
    # number of clusters to test

    # colors and title
    colors = cm.tab20(np.linspace(0, 1, clusterNum))
    plt.figure(figsize=(7,6))
    plt.title("2D Representation of "+str(clusterNum)+" Clusters")
    plt.xlabel("feature 1")
    plt.ylabel("feature 2")
    # scatter each cluster with the appropriate color
    for cluster in range(clusterNum):
        if cluster not in ignore:
            indexList = clusters.index[clusters['Kmeans '+str(clusterNum)] == cluster].tolist()
            this = embeddings2d.iloc[indexList]
            plt.scatter(this[0],this[1],color = colors[cluster],label="Cluster "+str(cluster))

    # add legend, show graph, and save graph to file
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    if savefig:
        plt.savefig("../html_files/clusters.png",bbox_inches="tight")
    plt.show()



'''
Prints the clusters in the chosen number of clusters from the given dataframe
@param clusterDf = datafram containing the cluster information
@param clusterNum = the number of clusters to look at
'''
def printClusterSet(clusterDf,clusterNum):
    print("\n\nPrinting "+str(clusterNum)+" cluster set:\n")
    kmeans = clusterDf[['Description','Kmeans '+str(clusterNum)]]
    for cluster in range(clusterNum):
        print("Cluster "+str(cluster))
        print(kmeans[kmeans["Kmeans "+str(clusterNum)]==cluster])
        print("\n\n")