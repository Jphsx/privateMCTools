

#ARGS NEEDED FOR CREATECARDS, IN THIS ORDER
#path = "testPath2/testDir2"
#mGo='1500'
#mN2='500'
#mN1='100'
#N2ctau=0.1 #METERS
#N2ctauStr='0p1'
#mode='23'
#mode='22'


#config for Zff testing create cards
dirname=testPath3
carddir=testDir3
PACKPATH=${dirname}/${carddir}
mGo=1500
mN2=500
mN1=100
N2ctau=0.1
N2ctauStr=0p1
mode=23

python3 CreateCards.py ${PACKPATH} ${mGo} ${mN2} ${mN1} ${N2ctau} ${N2ctauStr} ${mode} 


#config for Zff testing create scripts
nevent=1000
njob=200
configpath=Configuration/GenProduction/python
cmsswbase=/uscms/home/janguian/nobackup/CMSSW_12_4_14_patch3/src
#dirname=testPath
#carddir=testDir
#pdname="gogoG"
pdname=gogoZ

python3 CreateScripts.py ${mGo} ${mN2} ${mN1} ${N2ctau} ${N2ctauStr} ${mode} ${nevent} ${njob} ${configpath} ${cmsswbase} ${dirname} ${carddir} ${pdname}
