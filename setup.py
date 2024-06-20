from functions import *
import os.path


data_folder_path = 'csv_files/'
data_path = "csv_files/cleanedData.csv"

if not os.path.isfile(data_path):
    raise Exception("The data file could not be found")

if os.path.isfile(data_folder_path+'embeddings.csv'):
    # load embeddings from csv
    embeddings = pd.read_csv(data_folder_path+'embeddings.csv',index_col=False)
    # load 2D version from csv
    embeddings2D = pd.read_csv(data_folder_path+'embeddings2D.csv',index_col=False)
else:
    # load the data file
    col = pd.read_csv(data_path,index_col=False)['Description']
    # make embeddings from scratch
    embeddings = makeEmbeddings(col)
    # makes 2D version of sentences from scratch (for graphical representations)
    embeddings2D = make2D(embeddings.drop(["Description"],axis=1))
    # saves embeddings to csv files
    embeddings.to_csv(data_folder_path+"embeddings.csv",index=False)
    pd.DataFrame(embeddings2D).to_csv(data_folder_path+"embeddings2D.csv",index=False)

print("Done embeddings")




kmeansClusterPath = data_folder_path+"kmeansClusters.csv"
clusterRange = range(17,35)
print(len(embeddings))
print(len(embeddings2D))

if(os.path.isfile(kmeansClusterPath)):
    # if kmeans clusters have already been computed, get data
    clusterDf = pd.read_csv(kmeansClusterPath,index_col=False)

else:
    # compute clusters from scratch
    clusterDf = doKmeans(embeddings,clusterRange,showIntertias=False)
    print(len(clusterDf))
    # saves to csv
    clusterDf.to_csv(kmeansClusterPath,index=False)

print("Done Kmeans")


#clusterDf = doKmeans(embeddings,range(1,100),showIntertias=True)
'''plt.scatter(embeddings2D['0'],embeddings2D['1'],c=clusterDf['Kmeans 25'])
plt.title("2D Cluster Representation")
legend = []
for i in range(25):
    legend.append("Cluster "+ str(i))
plt.legend(range(25),legend)
plt.show()'''
# retrieve specific cluster data from a cluster number
# printClusterSet(clusterDf,25)