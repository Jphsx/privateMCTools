import csv
import os

#input csv of masses
gridcsv='photonGrid1.csv'

#global parameters for the overall grid
n2ctaustr='0p1'
nevent=2000
njob=100
configpath='Configuration/GenProduction/python'
cmsswbase='/uscms/home/janguian/nobackup/CMSSW_12_4_14_patch3/src'
pdname='gogoG'


gridpointNum=0
with open(gridcsv, 'r') as file:
    reader = csv.reader(file, delimiter=' ')
    next(reader) #skip header
    for gridpoint in reader:
        mGo=gridpoint[0]
        mn2=gridpoint[1]
        mn1=gridpoint[2]
        n2ctau=float(gridpoint[3])/100. #csv is in cm! input needs m!
        mode=gridpoint[4]
        dirname='gp'+str(gridpointNum)+'_'+str(mGo)+'_'+str(mn2)+'_'+str(mn1)+'_'+n2ctaustr+'_'+str(mode)
        carddir='gp'+str(gridpointNum)+'_cards'
        packpath = dirname+'/'+carddir
        
        cmd = 'python3 CreateCards.py '+packpath+' '+str(mGo)+' '+str(mn2)+' '+str(mn1)+' '+str(n2ctau)+' '+n2ctaustr+' '+str(mode)
        print('launching cmd:',cmd)
        os.system(cmd)
   
        cmd2 = 'python3 CreateScripts.py '+str(mGo)+' '+str(mn2)+' '+str(mn1)+' '+str(n2ctau)+' '+n2ctaustr+' '+str(mode)+' '+str(nevent)+' '+str(njob)+' '+str(configpath)+' '+str(cmsswbase)+' '+dirname+' '+carddir+' '+pdname
        print('launching cmd2:',cmd2)
        os.system(cmd2)

        
        gridpointNum=gridpointNum+1
       # if gridpointNum > 2 :
        #    break
        
 
