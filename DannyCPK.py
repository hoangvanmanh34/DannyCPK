#import warnings
#warnings.filterwarnings("ignore", "(?s).*MATPLOTLIBDATA.*", category=UserWarning)
import os, sys
# Artificially add the MATPLOTLIBDATA environment variable. This is reset
# when you restart your python console.
#os.environ["MATPLOTLIBDATA"] = os.path.join(os.path.split(sys.executable)[0], "Lib/site-packages/matplotlib/mpl-data")

import matplotlib.pyplot as plt
#from matplotlib.artist import Artist
import math
import numpy as np

class DannyCPK():
    def __init__(self, ifilepath=None, idata=None, iUSL=0, iLSL=0, ifigname='My CPK'):
        self.iUSL = iUSL
        self.iLSL = iLSL
        self.data = idata
        self.ifigname = ifigname
        print(ifilepath)
        self.file = open(ifilepath, 'r')
        self.cfile = self.file.read()     

    def AnalysisCPK(self):
        if self.data == None:
            #self.ncfile = list(map(float, self.cfile.split('\n')))
            self.strcfile = list(self.cfile.split('\n'))
            #is_integer = lambda s: s.isdigit() or (s[0] == '-' and s[1:].isdigit())
            #self.ncfile = [int(item) for self.ncfile in a for item in self.ncfile if item.isdigit()]
            self.ncfile = []
            for item in self.strcfile:
                try:
                    float(item)
                    self.ncfile.append(item)
                except ValueError:
                    continue                    
            print(self.ncfile)
            self.ncfile = list(map(float, self.ncfile))
            data = np.array(self.ncfile)
        else:
            data = self.data

        
        #sum = sum(prof, 0)
        mean = data.mean()#sum/len(prof)
        median = np.median(data)#(min(prof)+max(prof))/2
        sigma = data.std()
        '''sigma = 0
        sumsigma = 0
        for i in range(0, len(data)):
            sumsigma = sumsigma + math.pow((data[i]-mean), 2)
        sigma = math.sqrt(sumsigma/(len(data)))'''
        USL = None
        LSL = None
        if self.iUSL != None and self.iLSL != None:
            USL = float(self.iUSL)
            LSL = float(self.iLSL) 
            cpk = min(round((USL - mean)/(3*sigma),2), round((mean - LSL)/(3*sigma),2))
            plt.axvline(x=USL, color='red')
            plt.axvline(x=LSL, color='red')
        else:
            if self.iUSL != None:
                USL = float(self.iUSL)
                plt.axvline(x=USL, color='red')
                cpk = round((USL - mean)/(3*sigma), 2)
            if self.iLSL != None:
                LSL = float(self.iLSL)        
                plt.axvline(x=LSL, color='red')
                cpk =round((mean - LSL)/(3*sigma), 2)
        

        print('USL: '+str(USL))
        print('LSL: ' + str(LSL))
        print('Mean: '+str(mean))
        print('Median: '+str(median))
        print('Sigma: '+str(sigma))
        print(data.std())
        print('Cpk: '+str(cpk))

        col_num = 30
        n, bins, patches = plt.hist(data, col_num, density=True, facecolor='orange', alpha = 0.5, edgecolor='black', linewidth=1.5)
        #plt.annotate(xy=[10,10], s='First Entry')

        y = ((1 / (np.sqrt(2 * np.pi) * sigma)) * np.exp(-0.5 * (1 / sigma * (bins - mean))**2))#norm.pdf(bins, mean, sigma)
        plt.plot(bins, y,'r--')

        #plt.subplots_adjust(left=0.20)

        '''textstr = '\n'.join((
            r'Mean=%.2f' % (mean, ),
            r'Median=%.2f' % (median, ),
            r'Sigma=%.2f' % (sigma, ),
            r'Cpk=%.2f' % (cpk, ),))'''
        try:
            textstr = '\n'.join((
                r'USL=%.2f' % (USL, )+r'                  LSL=%.2f' % (LSL, ),
                r'Mean=%.2f' % (mean, )+r'               Median=%.2f' % (median, ),
                r'Sigma=%.2f' % (sigma, )+r'                Cpk=%.2f' % (cpk, ),))
        except:
            textstr = ''
            textstr1 = 'USL   ='+str(USL)+'                  LSL   =' + str(LSL)
            textstr2 = '\nMean  =' + str(round(mean, 2)) + '                  Median=' + str(round(median, 2))
            textstr3 = '\nSigma =' + str(round(sigma, 2)) + '                Cpk   =' + str(round(cpk, 2))
            textstr = textstr1 + textstr2 + textstr3


        '''props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=12,
                verticalalignment='top', bbox=props)'''
        fondi = dict(fontsize=10)
        plt.xlabel(self.ifigname, fontsize=15)
        plt.title(textstr,loc='left', fontdict=fondi)
        #axes = plt.gca()
        #axes.set_xlim([xmin,xmax])
        #axes.set_ylim([0,10])
        plt.gca().axes.get_yaxis().set_visible(False)
        #plt.yticks([])
        plt.show()

'''numbers = []
for item in a:
    for subitem in item.split():
        if(subitem.isdigit()):
            numbers.append(subitem)
print(numbers)'''
