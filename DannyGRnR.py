import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
class DannyGRnR():
    def __init__(self, ifilepath=None, idata=None, iUSL=0, iLSL=0, ivaluelist = None, ifigname='My CPK'):
        self.iUSL = iUSL
        self.iLSL = iLSL
        self.data = idata
        self.ifigname = ifigname
        self.ivaluelist = ivaluelist
        self.df = pd.read_csv(ifilepath, sep="\t")    

    def AnalysisGRnR(self):
        # load data file
        df = self.df
        ivaluelist = self.ivaluelist
        if ivaluelist == None:
            ivaluelist = list(df.columns)
        print(ivaluelist)
        # reshape the d dataframe suitable for statsmodels package 
        df_melt = pd.melt(df.reset_index(), id_vars=['index'], value_vars=ivaluelist)
        # replace column names
        df_melt.columns = ['index', 'treatments', 'value']

        # generate a boxplot to see the data distribution by treatments. Using boxplot, we can 
        # easily detect the differences between different treatments

        ax = sns.boxplot(x='treatments', y='value', data=df_melt, color='#99c2a2')
        ax = sns.swarmplot(x="treatments", y="value", data=df_melt, color='#7d0013')
        #ax.set(ylim=(15, 29))
        #a_plot = sns.lmplot('X','Y', data)
        plt.show()


#DannyGRnR('mdata1.txt').AnalysisGRnR()

'''# importing packages 
import seaborn as sns 
import matplotlib.pyplot as plt
  
# current colot palette
palette = sns.color_palette('Greens', 11)
  
# sequential color palette
sns.palplot(palette)
  
plt.show()'''
