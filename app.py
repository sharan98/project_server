from data import *
from defaults import URI, DB_NAME, COLLECTION
import matplotlib.pyplot as plt
from statistics import mean
import numpy as np
import seaborn as sns
import pandas as pd
import io
from sklearn.cluster import KMeans


class Project():
    def __init__(self, uri = URI, dbName = DB_NAME, collection = COLLECTION):
        print('uri: {0}, db: {1}, coll: {2}'.format(uri, dbName, collection))
        self.db = connectToDb(uri, dbName)
        self.data = readToDataFrame(self.db, collection)
        self.analytics()
        """
            area_list = list(df['Area'].unique())
            year_list = list(df.iloc[:,10:].columns)
            
            year_list = year_list[:-2]
            new_df_dict = {}
            for ar in area_list:
                yearly_produce = []
                for yr in year_list:
                    yearly_produce.append(self.data[yr][self.data['Area']==ar].sum())
                new_df_dict[ar] = yearly_produce
            new_df = pd.DataFrame(new_df_dict)
            new_df = pd.DataFrame.transpose(new_df) 
            new_df.columns = year_list
        """
    
    def getData(self):
        return self.data

    def analytics(self):
        df = self.data
        df.replace('', 0)
        area_list = list(df['Area'].unique())
        year_list = list(df.iloc[:,10:].columns)
        year_list = year_list[:-2]
        print(year_list)

        #to create the plot of production per year for every country
        print("---------------------------")        
        print("first plot")
        plt.figure(figsize=(24,12))
        for ar in area_list:
            yearly_produce = []
            for yr in year_list:
                print('.', end='')
                yearly_produce.append(df[yr][df['Area'] == ar].sum())
            plt.plot(yearly_produce, label=ar)
        plt.xticks(np.arange(53), tuple(year_list), rotation=60)
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=8, mode="expand", borderaxespad=0.)
        plt.savefig("productionPlot.png")
        # self.plo1_bytes_image = io.BytesIO()
        # plt.savefig(self.plo1_bytes_image, format='png')
        # self.plo1_bytes_image.seek(0)
        # print()
        # print(self.plo1_bytes_image)


        # create a new Data Frame with countries as index and years as columns 
        print("---------------------------")
        print("Create new_df")
        new_df_dict = {}
        for ar in area_list:
            yearly_produce = []
            for yr in year_list:
                print('.', end='')
                yearly_produce.append(self.data[yr][self.data['Area']==ar].sum())
            new_df_dict[ar] = yearly_produce
        new_df = pd.DataFrame(new_df_dict)
        new_df = pd.DataFrame.transpose(new_df) 
        new_df.columns = year_list
        print()
        print(new_df.head())

        #First, a new column which indicates mean produce of each state over the given years. Second, a ranking column which ranks countries on the basis of mean produce
        #new_df.head()
        print("---------------------------")
        print("Add mean and crank cols")
        mean_produce = []
        for i in range(174):
            #print(new_df.iloc[i,:].values)
            print('.', end='')
            l = [0 if x=='' else x for x in new_df.iloc[i,:].values]
            mean_produce.append(mean(l))
            #print(mean_produce)
        new_df['Mean_Produce'] = mean_produce
        new_df['Rank'] = new_df['Mean_Produce'].rank(ascending=False)
        print()
        print(new_df.head())

        # create another dataframe with items and their total production each year from 1961 to 2013
        print("---------------------------")
        print("Create item_df")
        item_list = list(df['Item'].unique())
        item_df = pd.DataFrame()
        item_df['Item_Name'] = item_list
        for yr in year_list:
            item_produce = []
            for it in item_list:
                print('.', end='')
                l = [0 if x=='' else x for x in df[yr][df['Item']==it]]
                item_produce.append(sum(l))
            item_df[yr] = item_produce
        print()
        print(item_df.head())
        
        # total amount produced for each commodity rank them in descending order 
        print("---------------------------")
        print("Add sum and rank cols")
        sum_col = []
        for i in range(115):
            #print(item_df.iloc[i,1:].values)    # first element is name of item
            print('.', end='')
            l = [0 if x=='' else x for x in item_df.iloc[i,1:].values]
            sum_col.append(sum(l))
        item_df['Sum'] = sum_col
        item_df['Production_Rank'] = item_df['Sum'].rank(ascending=False)
        print()
        print(item_df.head())
        #plt.close()

        #plt.close('all')
        # heat map showing correlation of Year on year production 
        print("---------------------------")
        print("Heatmap years")
        year_df = df.iloc[:,8:-2]
        print(year_df.head())
        year_df = year_df.apply(pd.to_numeric,errors = 'ignore')
        fig, ax = plt.subplots()
        print("year_df.corr")
        print(year_df.corr())
        sns.heatmap(year_df.corr())
        print("heatmap")
        #plt.show()
        plt.savefig("year_heatmap.png")
        # self.year_heatmap_bytes_image = io.BytesIO()
        # plt.savefig(self.year_heatmap_bytes_image, format='png')
        # self.year_heatmap_bytes_image.seek(0)

        #heatmap for products
        item_df1 = pd.DataFrame.transpose(item_df.iloc[:,1:-2])
        #item_df1.columns = item_list
        item_df1 = item_df1
        print(item_df.head())
        print(item_df1.head())
        item_df1= item_df1.dropna(axis = 1,how = 'any')
        print("\n\n\n\n\n\n\n\n\n\n")
        for item in item_df1:
            print(item)
        item_df1 = item_df1.apply(pd.to_numeric,errors = 'ignore')
        fig, ax = plt.subplots(figsize = (56,56))
        print(item_df1.corr())
        sns.heatmap(item_df1.corr())
        #plt.show()

        #heat map for countries
        area_df1 = pd.DataFrame.transpose(new_df)
        area_df1.columns = area_list
        print (area_df1)
        area_df1 = area_df1.apply(pd.to_numeric,errors = 'ignore')
        area_df1= area_df1.dropna(axis = 1,how = 'any')
        print("\n\n\n\n\n\n\n\n\n\n")
        for are in area_df1:
            print(area_df1[are])
        fig, ax = plt.subplots()
        print(area_df1.corr())
        sns.heatmap(area_df1.corr())
        plt.show()
        #,annot = True,xticklabels=1, yticklabels=1, center= 0.0
        
        

        # heat map for products over the years
        print("---------------------------")
        print("Heatmap items")
        new_item_df = item_df.drop(["Item_Name","Sum","Production_Rank"], axis = 1)
        fig, ax = plt.subplots(figsize=(12,24))
        sns.heatmap(new_item_df,ax=ax)
        ax.set_yticklabels(item_df.Item_Name.values[::-1])
        #plt.show()
        # self.item_heatmap_bytes_image = io.BytesIO()
        # plt.savefig(self.item_heatmap_bytes_image, format='png')
        # self.item_heatmap_bytes_image.seek(0)
        plt.savefig("item_heatmap.png")
        #k-means taking data set
        print("---------------------------")
        print("K means")
        X = new_df.iloc[:,:-2].values
        X = pd.DataFrame(X)
        # X = X.convert_objects(convert_numeric=True)
        for k in list(X):
            print('.', end='')
            X[k]=pd.to_numeric(X[k], errors='ignore')
        X.columns = year_list
        X = pd.DataFrame(X).fillna(0)
        # print(year_list)
        print()
        print(X.head())

        print("---------------------------")
        print("Elbow")
        wcss = []
        plt.close('all')
        for i in range(1,11):
            print('.', end='')
            kmeans = KMeans(n_clusters=i,init='k-means++',max_iter=300,n_init=10,random_state=0)
            kmeans.fit(X)
            wcss.append(kmeans.inertia_)
        plt.plot(range(1,11),wcss)
        plt.title('The Elbow Method')
        plt.xlabel('Number of clusters')
        plt.ylabel('WCSS')
        plt.savefig("elbow.png")
        # plt.show()

        # self.elbow_bytes_image = io.BytesIO()
        # plt.savefig(self.elbow_bytes_image, format='png')
        # self.elbow_bytes_image.seek(0)
        # print()
        # print(self.elbow_bytes_image)
        
        kmeans = KMeans(n_clusters=2,init='k-means++',max_iter=300,n_init=10,random_state=0) 
        y_kmeans = kmeans.fit_predict(X)

        X = X.as_matrix(columns=None)
        plt.close('all')

        plt.scatter(X[y_kmeans == 0, 0], X[y_kmeans == 0,1],s=100,c='red',label='Others')
        plt.scatter(X[y_kmeans == 1, 0], X[y_kmeans == 1,1],s=100,c='blue',label='China(mainland),USA,India')
        plt.scatter(kmeans.cluster_centers_[:,0],kmeans.cluster_centers_[:,1],s=300,c='yellow',label='Centroids')
        plt.title('Clusters of countries by Productivity')
        plt.legend()
        plt.savefig("clusters.png")
        # self.kmeans_bytes_image = io.BytesIO()
        # plt.savefig(self.kmeans_bytes_image, format='png')
        # self.kmeans_bytes_image.seek(0)
        # plt.show()

    def plot_images(self):
        print(self.plo1_bytes_image)
        print(self.year_heatmap_bytes_image)
        
        
    def productionPerYear(self):
        df = self.data
        area_list = list(df['Area'].unique())
        year_list = list(df.iloc[:,10:].columns)
        
        year_list = year_list[:-2]
        print(year_list)
        

        plt.figure(figsize=(24,12))
        for ar in area_list:
            yearly_produce = []
            for yr in year_list:
                yearly_produce.append(df[yr][df['Area'] == ar].sum())
            plt.plot(yearly_produce, label=ar)
        plt.xticks(np.arange(53), tuple(year_list), rotation=60)
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=8, mode="expand", borderaxespad=0.)
        #plt.savefig('p.png')
        #plt.show()

        bytes_image_production = io.BytesIO()
        plt.savefig(bytes_image_production, format='png')
        bytes_image_production.seek(0)
        return bytes_image_production

    def find(self, collection = COLLECTION, filter = {}, projection = None,\
         skip = 0, limit = 0, sort = None):
        try:
            result = self.db[collection].find(filter= filter, \
                projection= projection, skip= skip, limit= limit, sort= sort)
            df = DataFrame(list(result))
            return df.to_html()
        except Exception as e:
            return str(e)

    def updateOne(self, collection = COLLECTION, filter = {}, update = None, upsert = False):
        try:
            assert update != None, "No update modifications passed"
            result = self.db[collection].update_one(filter= filter, update= update, upsert= upsert)
            return result
        except Exception as e:
            return str(e)
    
    def updateMany(self, collection = COLLECTION, filter = {}, update = None, upsert = False):
        try:
            assert update != None, "No update modifications passed"
            result = self.db[collection].update_many(filter= filter, update= update, upsert= upsert)
            return result
        except Exception as e:
            return str(e)

    def insertOne(self, collection = COLLECTION, data = None):
        try:
            assert data != None, "No data passed"
            result = self.db[collection].insert_one(data)
            return result
        except Exception as e:
            return str(e)

    def insertMany(self, collection = COLLECTION, data = None):
        try:
            assert data != None, "No data passed"
            result = self.db[collection].insert_many(data)
            return result
        except Exception as e:
            return str(e)

    def deleteOne(self, collection = COLLECTION, filter = None):
        try:
            assert filter != None, "No filter passed"
            result = self.db[collection].delete_one(filter)
            return result
        except Exception as e:
            return str(e)
    
    def deleteMany(self, collection = COLLECTION, filter = None):
        try:
            assert filter != None, "No filter passed"
            result = self.db[collection].delete_many(filter)
            return result
        except Exception as e:
            return str(e)

    def plot(self):
        plt.figure()
        self.data.plot()
        bytes_image = io.BytesIO()
        plt.savefig(bytes_image, format='png')
        bytes_image.seek(0)
        return self.year_heatmap_bytes_image

    def head(self):
        return (self.data.head().to_html())

if __name__ == '__main__':
    # pass
    plt.close('all')
    p = Project(dbName= 'food', collection="FAO")
    # p.analytics()
    # p.plot_images()
    # print(p.insertOne())
    # print(p.insertOne(data="sdss"))
    # print(list(p.find(limit=3)))
    # print (p.head())
    # df = p.getData()
    # print(p.plot())
