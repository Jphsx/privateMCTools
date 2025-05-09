import csv
import os

#input csv of masses
gridcsv='ultest.csv'
#gridcsv='photonGrid2.csv'

year='UL18'
#global parameters for the overall grid
n2ctaustr='0p1'
nevent=2000
njob=100
configpath='Configuration/GenProduction/python'
cmsswbase='/uscms/home/janguian/nobackup/CMSSW_10_6_17_patch1/src'
pdname='gogoG_UL18'

year='UL18'

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
        #select correct ctau str
        if int(gridpoint[3]) == 30:
            n2ctaustr='0p3'

        dirname='gp'+year+str(gridpointNum)+'_'+str(mGo)+'_'+str(mn2)+'_'+str(mn1)+'_'+n2ctaustr+'_'+str(mode)
        carddir='gp'+year+str(gridpointNum)+'_cards'
        packpath = dirname+'/'+carddir
        
        cmd = 'python3 CreateCardsUL.py '+packpath+' '+str(mGo)+' '+str(mn2)+' '+str(mn1)+' '+str(n2ctau)+' '+n2ctaustr+' '+str(mode)
        print('launching cmd:',cmd)
        os.system(cmd)
   
        cmd2 = 'python3 CreateScriptsUL.py '+str(mGo)+' '+str(mn2)+' '+str(mn1)+' '+str(n2ctau)+' '+n2ctaustr+' '+str(mode)+' '+str(nevent)+' '+str(njob)+' '+str(configpath)+' '+str(cmsswbase)+' '+dirname+' '+carddir+' '+pdname
        print('launching cmd2:',cmd2)
        os.system(cmd2)

        
        gridpointNum=gridpointNum+1
       # if gridpointNum > 2 :
        #    break
        
 
