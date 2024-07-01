from functions import *
import os.path

# place to find data csv files
data_folder_path = 'csv_files/'
# specific data csv file to read
data_path = "csv_files/cleanedData.csv"

# checks if the data path exists
if not os.path.isfile(data_path):
    raise Exception("The data file could not be found")

# creates or loads embeddings
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

# path for the kmeans csv file
kmeansClusterPath = data_folder_path+"kmeansClusters.csv"
# kmeans cluster numbers to test
clusterRange = range(17,35)

# checks if there is already a kmeans cluster datafile
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


