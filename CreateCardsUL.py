

import CardTemplatesT1qqqqVV as CT


#create a directory to store cards for genproductions script
import os
import sys

#path = "testPath2/testDir2"
path = str(sys.argv[1])
pathExists = os.path.exists(path)

if not pathExists:
        print("creating path", path)
        os.makedirs(path)



#create each card in path
#define masses and lifetime
#GridPackPath='gridpathtest'
#mGo='1500'
mGo=str(sys.argv[2])
#mN2='500'
mN2=str(sys.argv[3])
#mN1='100'
mN1=str(sys.argv[4])
#N2ctau=0.1 #METERS
N2ctau=float(sys.argv[5])
#N2ctauStr='0p1'
N2ctauStr=str(sys.argv[6])
#mode='23'
#mode='22'
mode=str(sys.argv[7])
def ConstructOutputName(mGo, mN2, mN1, N2ctau, mode, N2ctauStr):
    modename = ''
    if(mode =='23'):
        modename = 'Zff'
    if(mode=='22'):
        modename = 'gam'
    name = 'SMS-GlGl_mGl-'+mGo+'_mN2-'+mN2+'_mN1-'+mN1+'_'+modename+'_N2ctau-'+N2ctauStr
    return name

#ProcCard needs outputName
outputName = ConstructOutputName(mGo, mN2, mN1, N2ctau, mode,N2ctauStr)
#fragment needs gp path 
GridPackPath='root://cmseos.fnal.gov//store/user/janguian/gridpacks/'+outputName+'_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz'
#CMSSW_10_6_17_patch1
print("Writing Proc Card with outputName=",outputName)
procCard = CT.getProcCard(outputName)
f = open(path+"/"+outputName+'_proc_card.dat', "w")
f.write(procCard)
f.close()

print("Writing Run Card")
runCard = CT.getRunCardUL()
f = open(path+"/"+outputName+'_run_card.dat', "w")
f.write(runCard)
f.close()

print("Writing Param Card with options:")
print("mgo=",mGo," mN2=",mN2," mN1=",mN1," N2ctau=",N2ctau, " N2decayMode=",mode)
N2Width=1.973270521762532e-16/N2ctau
paramCard = CT.getParamCard(mGo, mN1, mN2, N2Width, mode)
f = open(path+"/"+outputName+'_param_card.dat', "w")
f.write(paramCard)
f.close()

print("Creating Fragment")
print("Linking EOS gridpack: ", GridPackPath)
#ctau = N2ctauStr
fragment = CT.getFragmentUL(GridPackPath, mGo, N2ctau)
f = open(path+"/"+outputName+'-fragment.py', "w")
f.write(fragment)
f.close()


