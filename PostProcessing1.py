'''
Visualize trainning and testing models results.
'''

# Input Libraries
from re import sub
from turtle import color
from matplotlib import markers
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import seaborn as sns
import os

# set subplot dimensions
rows = 2
cols = 3

# set data plot
fig1, ax = plt.subplots(rows, cols, sharex=False, sharey=False, figsize = (10,6))
for i in range(0, rows):
    for j in range(0, cols):
        # Read from CSV of Model Topology
        caseID = 'Am5_c12'
        # define Topology
        if i == 0:
            model_top = 'Topology '+ str(j+1)
        else:
            model_top = 'Topology '+ str(i+j+3)
        # read test csv
        TopologyFilename = './vCNN/Topologies/Train/'+caseID+'_'+model_top+'.csv'
        if os.path.exists(TopologyFilename):
            # convert csv to df
            TopologyDataframe = pd.read_csv(TopologyFilename,sep=';')
            # export to txt
            if i == 0 and j == 0:
                mode = 'w'
            else:
                mode = 'a'
            mean = np.mean(TopologyDataframe['Error (%)'])
            std = np.std(TopologyDataframe['Error (%)'])
            max = np.max(TopologyDataframe['Error (%)'])
            f = open('./vCNN/Topologies/Test/Topologies_Data.txt',mode)
            f.write('Batch: %s\t' % caseID)
            f.write('Topology: %s\t' % model_top)
            f.write('Mean_error: %.3g\t' % mean)
            f.write('Max_error: %.3g\t' % max)
            f.write('Standard Deviation: %.3g\n' % std)
            f.close()
            # data visualization
            ax[i, j].set_title(label = model_top + ' Performance', fontsize = 12)
            ax[i, j].scatter(TopologyDataframe['Keq/Kpm_teo'],
                            TopologyDataframe['Keq/Kpm_est'], color='mediumpurple', marker='.', label = 'Train Data')
            ax[i, j].plot(TopologyDataframe['Keq/Kpm_teo'],
                          TopologyDataframe['Keq/Kpm_teo'], color='indigo', linewidth=2.0)
            ax[i,j].set_ylabel(ylabel = 'Estimated Perm. (-)', fontsize = 10)
            ax[i,j].set_xlabel(xlabel = 'Theoretical Perm. (-)', fontsize = 10)
            ax[i,j].set_xlim([1.00, 1.20])
            ax[i,j].set_ylim([0.95, 1.20])
            ax[i,j].xaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
        else:
            break
        # read test csv
        TestTopologyFilename = './vCNN/Topologies/Test/'+caseID+'_'+model_top+'.csv'
        if os.path.exists(TestTopologyFilename):
            # convert csv to df
            TestTopologyDataframe = pd.read_csv(TestTopologyFilename,sep=';')
            # export to txt
            if i == 0 and j == 0:
                mode = 'w'
            else:
                mode = 'a'
            mean = np.mean(TestTopologyDataframe['Error (%)'])
            std = np.std(TestTopologyDataframe['Error (%)'])
            max = np.max(TestTopologyDataframe['Error (%)'])
            f = open('./vCNN/Topologies/Train/Topologies_Data.txt',mode)
            f.write('Batch: %s\t' % caseID)
            f.write('Topology: %s\t' % model_top)
            f.write('Mean_error: %.4g\t' % mean)
            f.write('Max_error: %.4g\t' % max)
            f.write('Standard Deviation: %.4g\n' % std)
            f.close()
            ax[i, j].scatter(TestTopologyDataframe['Keq/Kpm_teo'],
                            TestTopologyDataframe['Keq/Kpm_est'], 
                            color='lightgreen', marker='x', label = 'Test Data')
            ax[i, j].legend(loc = "best", fontsize = 8)
            
fig1.tight_layout()
fig1.savefig('./vCNN/Topologies/'+caseID+'_Topologies.png')
        
# set data distribution
fig2, ax2 = plt.subplots(rows, cols, sharex=False, sharey=False, figsize = (10,6))
for i in range(0, rows):
    for j in range(0, cols):
        # define Topology
        if i == 0:
            model_top = 'Topology '+ str(j+1)
        else:
            model_top = 'Topology '+ str(i+j+3)
        # read csv
        TopologyFilename = './vCNN/Topologies/Test/'+caseID+'_'+model_top+'.csv'
        if os.path.exists(TopologyFilename):
            # convert csv to df
            TopologyDataframe = pd.read_csv(TopologyFilename,sep=';')
            # data visualization
            ax2[i,j].set_title(label = model_top+' Distribution', fontsize = 12)
            ax2[i,j] = sns.histplot(100*(np.array(TopologyDataframe['Keq/Kpm_est'])-np.array(TopologyDataframe['Keq/Kpm_teo']))/np.array(TopologyDataframe['Keq/Kpm_teo']),
                                        color = 'm',
                                        stat = "count", common_norm=False, kde = True,
                                        ax = ax2[i, j])
            ax2[i,j].set_ylabel(ylabel = "Count", fontsize = 10)
            ax2[i,j].set_xlabel(xlabel = 'Error (%)', fontsize = 10)
            ax2[i,j].set_xlim([-6.50, 6.50])
            ax2[i,j].set_ylim([0.00, 115])
            ax2[i,j].xaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f'))
        else:
            break
fig2.tight_layout()
fig2.savefig('./vCNN/Topologies/'+caseID+'_Distribution.png')

# visualize distribution of Error (%) per Perm. Equivalent Estimated
fig3, ax3 = plt.subplots(rows, cols, sharex=False, sharey=False, figsize = (10,6))
for i in range(0, rows):
    for j in range(0, cols):
        # define Topology
        if i == 0:
            model_top = 'Topology '+ str(j+1)
        else:
            model_top = 'Topology '+ str(i+j+3)
        # read csv
        TopologyFilename = './vCNN/Topologies/Test/'+caseID+'_'+model_top+'.csv'
        if os.path.exists(TopologyFilename):
            # convert csv to df
            TopologyDataframe = pd.read_csv(TopologyFilename,sep=';')
            # data visualization
            ax3[i, j].set_title(label = model_top, fontsize = 12)
            ax3[i,j] = sns.scatterplot(x = TopologyDataframe['Keq/Kpm_teo'], y = TopologyDataframe['Error (%)'], 
                                        color = 'lightsalmon',
                                        ax = ax3[i,j])
            ax3[i, j].axhline(y = TopologyDataframe['Error (%)'].mean(), color = 'orangered', linestyle = '--', label = 'Mean')
            ax3[i, j].set_xlabel(xlabel = 'Theoretical Perm. (-)', fontsize = 10)
            ax3[i, j].set_ylabel(ylabel = 'Error (%)', fontsize = 10)
            ax3[i,j].set_xlim([1.00, 1.20])
            ax3[i,j].set_ylim([0.00, 6.00])
            ax3[i, j].xaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
            ax3[i, j].yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f'))
            ax3[i, j].legend(loc = "best", fontsize = 8)
        else:
            break
fig3.tight_layout()
fig3.savefig('./vCNN/Topologies/'+caseID+'_ErrorPerKeq.png')

# switch batch and subsets
groups = ['Am5_c34_Topology 2a', 'Am8_c12_Topology 2', 'Am8_c34_Topology 2'] # remaining groups
fig4, ax4 = plt.subplots(1, len(groups), sharex=False, sharey=False, figsize = (10,5))
for i in range(0, len(groups)):
    # Read from CSV of Model Topology
    caseID = groups[i]
    # define Topology
    model_top = 'Topology 2' # best Topology
    # read test csv
    TopologyFilename = './vCNN/Topologies/Train/'+caseID+'.csv'
    if os.path.exists(TopologyFilename):
        # convert csv to df
        TopologyDataframe = pd.read_csv(TopologyFilename,sep=';')
        
        # export to txt
        mode = 'a'
        mean = np.mean(TopologyDataframe['Error (%)'])
        std = np.std(TopologyDataframe['Error (%)'])
        max = np.max(TopologyDataframe['Error (%)'])
        f = open('./vCNN/Topologies/Test/Topologies_Data.txt',mode)
        f.write('Batch: %s\t' % caseID)
        f.write('Topology: %s\t' % model_top)
        f.write('Mean_error: %.3g\t' % mean)
        f.write('Max_error: %.3g\t' % max)
        f.write('Standard Deviation: %.3g\n' % std)
        f.close()
        
        # data visualization
        if i == 0:
            titulo = 'Am5_c34_Topology 2'
        else:
            titulo = groups[i]
        ax4[i].set_title(label = titulo + ' Performance', fontsize = 10)
        ax4[i].scatter(TopologyDataframe['Keq/Kpm_teo'],
                        TopologyDataframe['Keq/Kpm_est'], 
                        color='mediumpurple', marker='.', label = 'Train Data')
        ax4[i].plot(TopologyDataframe['Keq/Kpm_teo'],
                        TopologyDataframe['Keq/Kpm_teo'], 
                        color='indigo', linewidth=2.0)
    else:
        break
        # read test csv
    TestTopologyFilename = './vCNN/Topologies/Test/'+caseID+'.csv'
    if os.path.exists(TestTopologyFilename):
        # convert csv to df
        TestTopologyDataframe = pd.read_csv(TestTopologyFilename,sep=';')
        
        # export to txt
        mode = 'a'
        mean = np.mean(TestTopologyDataframe['Error (%)'])
        std = np.std(TestTopologyDataframe['Error (%)'])
        max = np.max(TestTopologyDataframe['Error (%)'])
        f = open('./vCNN/Topologies/Train/Topologies_Data.txt',mode)
        f.write('Batch: %s\t' % caseID)
        f.write('Topology: %s\t' % model_top)
        f.write('Mean_error: %.4g\t' % mean)
        f.write('Max_error: %.4g\t' % max)
        f.write('Standard Deviation: %.4g\n' % std)
        f.close()
        
        ax4[i].scatter(TestTopologyDataframe['Keq/Kpm_teo'],
                        TestTopologyDataframe['Keq/Kpm_est'], 
                        color='lightgreen', marker='x', label = 'Test Data')
        ax4[i].legend(loc = "best", fontsize = 12)
        ax4[i].set_xlabel('Theoretical Perm. (-)', fontsize = 10)
        ax4[i].set_ylabel('Estimated Perm. (-)', fontsize = 10)
fig4.tight_layout()
fig4.savefig('./vCNN/Topologies/Topology 2_Results.png')