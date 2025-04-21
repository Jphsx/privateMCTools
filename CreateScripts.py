

def ConstructOutputName(mGo, mN2, mN1, N2ctau, mode, N2ctauStr):
    modename = ''
    if(mode =='23'):
        modename = 'Zff'
    if(mode=='22'):
        modename = 'gam'
    name = 'SMS-GlGl_mGl-'+mGo+'_mN2-'+mN2+'_mN1-'+mN1+'_'+modename+'_N2ctau-'+N2ctauStr
    return name


import ScriptTemplates as ST


#create a directory to store cards for genproductions script
import os
import sys
#path = "testPath/testDir"
#path = "testPath"
#if not pathExists:
#        print("creating path", path)
#        os.makedirs(path)



#create each card in path
#define masses and lifetime
#GridPackPath='gridpathtest'

#mGo='1500'
mGo=str(sys.argv[1])
#mN2='500'
mN2=str(sys.argv[2])
#mN1='100'
mN1=str(sys.argv[3])
#N2ctau=0.1 #METERS
N2ctau=float(sys.argv[4])
#N2ctauStr='0p1'
N2ctauStr=str(sys.argv[5])
#mode='23'
#mode='22'
mode=str(sys.argv[6])



name = ConstructOutputName(mGo,mN2,mN1,N2ctau,mode,N2ctauStr)
#nevent = 1000
nevent = int(sys.argv[7])
#njob = 200
njob= int(sys.argv[8])
#configpath="Configuration/GenProduction/python"
configpath=str(sys.argv[9])
#cmsswbase="/uscms/home/janguian/nobackup/CMSSW_12_4_14_patch3/src"
cmsswbase=str(sys.argv[10])
#dirname="testPath"
#dirname="testPath2"
dirname=str(sys.argv[11])
#carddir="testDir"
#carddir="testDir2"
carddir=str(sys.argv[12])
#pdname="gogoG"
#pdname="gogoZ"
pdname=str(sys.argv[13])
DriverScript = ST.DriverScript(name,nevent,dirname,carddir,configpath,cmsswbase)
#print(DriverScript)
f = open(dirname+'/doDriver.sh', "w")
f.write(DriverScript)
f.close()
os.chmod(dirname+'/doDriver.sh', 0o755)


GPScript = ST.CreateGPScript(name,dirname,carddir,cmsswbase)
#print(GPScript)
f = open(dirname+'/doGP.sh', "w")
f.write(GPScript)
f.close()
os.chmod(dirname+'/doGP.sh', 0o755)


genScript = ST.CrabGEN(name,dirname,pdname,nevent,njob)
#print(genScript)
f = open(dirname+'/crab_stepGEN.py', "w")
f.write(genScript)
f.close()

digiScript = ST.CrabDIGI(name,dirname,pdname)
#print(digiScript)
f = open(dirname+'/crab_stepDIGI.py', "w")
f.write(digiScript)
f.close()

aodScript = ST.CrabAOD(name,dirname,pdname)
#print(aodScript)
f = open(dirname+'/crab_stepAOD.py', "w")
f.write(aodScript)
f.close()

crablauncher = ST.CrabLauncher(name)
#print(crablauncher)
f = open(dirname+'/runCrab.sh', "w")
f.write(crablauncher)
f.close()
os.chmod(dirname+'/runCrab.sh', 0o755)

listmaker = ST.MakeList(name,pdname)
f = open(dirname+'/MakeList.sh', "w")
f.write(listmaker)
os.chmod(dirname+'/MakeList.sh', 0o755)

