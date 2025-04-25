

def DriverScript(name,nevent,dirname,carddir,configpath,cmsswbase):
    
    BS='\\'
    DRIVERSCRIPT=f''' NEVENT={nevent}
NAME={name}
CONFIGPATH={configpath}
BASE={cmsswbase}
DIRNAME={dirname}
CARDDIR={carddir}
COPYANDBUILD=$1 GENSIM=$2 SIM=$3 RAW2DIGI=$4 HLT=$5 AOD=$6
echo "modes" ${{COPYANDBUILD}} ${{GENSIM}} ${{SIM}} ${{RAW2DIGI}} ${{HLT}} ${{AOD}}


if [ ${{COPYANDBUILD}} -eq 1 ]
then
cp ${{CARDDIR}}/${{NAME}}-fragment.py ${{BASE}}/${{CONFIGPATH}}/${{NAME}}-fragment.py
pushd ${{BASE}}
scram b -j 8
popd
fi




if [ ${{GENSIM}} -eq 1 ]
then
pushd ../../
cmsDriver.py Configuration/GenProduction/python/${{NAME}}-fragment.py {BS}
    --python_filename ${{NAME}}_1_cfg.py {BS}
    --eventcontent RAWSIM,LHE {BS}
    --customise Configuration/DataProcessing/Utils.addMonitoring {BS}
    --datatier RAWSIM,LHE {BS}
    --fileout file:${{NAME}}_1.root {BS}
    --conditions 106X_upgrade2018_realistic_v4 {BS}
    --beamspot Realistic25ns13TeVEarly2018Collision {BS}
    --step LHE,GEN {BS}
    --nThreads 8 {BS}
    --geometry DB:Extended {BS}
    --era Run2_2018 {BS}
    --no_exec {BS}
    --mc {BS}
    -n ${{NEVENT}}

mv ${{NAME}}_1_cfg.py ./privateMCTools/${{DIRNAME}}/
popd

fi


if [ ${{SIM}} -eq 1 ]
then
pushd ../../
        --python_filename ${{NAME}}_2_cfg.py {BS}
        --eventcontent RAWSIM {BS}
        --customise Configuration/DataProcessing/Utils.addMonitoring {BS}
        --datatier GEN-SIM {BS}
        --fileout file:${NAME}}_2.root {BS}
        --conditions 106X_upgrade2018_realistic_v11_L1v1 {BS}
        --beamspot Realistic25ns13TeVEarly2018Collision {BS}
        --step SIM {BS}
        --nThreads 8 {BS}
        --geometry DB:Extended {BS}
        --filein file:${{NAME}}_1.root {BS} {BS}
        --era Run2_2018 {BS}
        --runUnscheduled {BS}
        --no_exec {BS}
        --mc {BS}
        -n ${{NEVENT}}

mv ${{NAME}}_2_cfg.py ./privateMCTools/${{DIRNAME}}/
popd



if [ ${{RAW2DIGI}} -eq 1 ]
then
pushd ../../
cmsDriver.py {BS}
    --python_filename ${{NAME}}_3_cfg.py {BS}
    --eventcontent PREMIXRAW {BS}
    --customise Configuration/DataProcessing/Utils.addMonitoring {BS}
    --datatier GEN-SIM-DIGI {BS}
    --fileout file:${{NAME}}_3.root {BS}
    --pileup_input dbs:/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL18_106X_upgrade2018_realistic_v11_L1v1-v2/PREMIX {BS}
    --conditions 106X_upgrade2018_realistic_v11_L1v1 {BS}
    --step DIGI,DATAMIX,L1,DIGI2RAW {BS}
    --procModifiers premix_stage2 {BS}
    --geometry DB:Extended {BS}
    --filein file:${{NAME}}_2.root {BS}
    --datamix PreMix {BS}
    --era Run2_2018 {BS}
    --runUnscheduled {BS}
    --no_exec {BS}
    --mc {BS}
    -n ${{NEVENT}}


#cmsRun ${{NAME}}_3_cfg.py
mv ${{NAME}}_3_cfg.py ./privateMCTools/${{DIRNAME}}/
popd
fi


if [ ${{HLT}} -eq 1 ]
then
pushd ../../
cmsDriver.py {BS}
    --python_filename ${{NAME}}_4_cfg.py {BS}
    --eventcontent RAWSIM {BS}
    --customise Configuration/DataProcessing/Utils.addMonitoring {BS}
    --datatier GEN-SIM-RAW {BS}
    --fileout file:${{NAME}}_4.root {BS}
    --conditions 102X_upgrade2018_realistic_v15 {BS}
    --customise_commands 'process.source.bypassVersionCheck = cms.untracked.bool(True)' {BS}
    --step HLT:2018v32 {BS}
    --nThreads 8 {BS}
    --geometry DB:Extended {BS}
    --filein file:${{NAME}}_3.root {BS}
    --era Run2_2018 {BS}
    --no_exec {BS}
    --mc {BS}
    -n ${{NEVENT}}

#cmsRun ${{NAME}}_4_cfg.py
mv ${{NAME}}_4_cfg.py ./privateMCTools/${{DIRNAME}}/
popd
fi



if [ ${{AOD}} -eq 1 ]
then
pushd ../../
cmsDriver.py {BS}
    --python_filename ${{NAME}}_5_cfg.py {BS}
    --eventcontent AODSIM {BS}
    --customise Configuration/DataProcessing/Utils.addMonitoring {BS}
    --datatier AODSIM {BS}
    --fileout file:${{NAME}}_AOD.root {BS}
    --conditions 106X_upgrade2018_realistic_v11_L1v1 {BS}
    --step RAW2DIGI,L1Reco,RECO,RECOSIM,EI {BS}
    --nThreads 8 {BS}
    --geometry DB:Extended {BS}
    --filein file:${{NAME}}_4.root {BS}
    --era Run2_2018 {BS}
    --runUnscheduled {BS}
    --no_exec {BS}
    --mc {BS}
    -n ${{NEVENT}}


#cmsRun ${{NAME}}_3_cfg.py
mv ${{NAME}}_5_cfg.py ./privateMCTools/${{DIRNAME}}/
popd
fi
'''
    return DRIVERSCRIPT

def CreateGPScript(gpname,dirname,carddir,cmsswbase):
    GPMAKESCRIPT=f'''CARDPATH={dirname}/{carddir}
CARDDIR={carddir}
RELPATH=../../../privateMCTools
MG5PATH=genproductions/bin/MadGraph5_aMCatNLO/
GPNAME={gpname}
CMSSWBASE={cmsswbase}
EOSPATH=root://cmseos.fnal.gov//store/user/janguian/gridpacks

#make gp
pushd ${{CMSSWBASE}}/${{MG5PATH}}
./gridpack_generation.sh ${{GPNAME}} ../../../privateMCTools/${{CARDPATH}}
# andmove it to private mc space
mv ${{GPNAME}}_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz ${{RELPATH}}/${{CARDPATH}}/${{GPNAME}}_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz
mv ${{GPNAME}}.log ${{RELPATH}}/${{CARDPATH}}.log

#thencopy to eos
popd
pushd ${{CARDDIR}}
xrdcp ${{GPNAME}}_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz ${{EOSPATH}}/${{GPNAME}}_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz
'''
    return GPMAKESCRIPT


def CrabLauncher(name):
    CRABLAUNCH=f'''GENSTEP=$1
SIMSTEP=$2
DIGISTEP=$3
HLTSTEP=$4
AODSTEP=$5

NAME={name}
echo "modes" ${{GENSTEP}} ${{SIMSTEP}} ${{DIGISTEP}} ${{HLTSTEP}} ${{AODSTEP}}

if [ ${{GENSTEP}} -eq 1 ]
then
cp crab_stepGEN.py ../../crab_stepGEN_TEMP.py
cp {name}_1_cfg.py ../../{name}_1_cfg.py
pushd ../../
crab submit crab_stepGEN_TEMP.py
rm crab_stepGEN_TEMP.py
rm {name}_1_cfg.py
popd
fi

if [ ${{SIMSTEP}} -eq 1 ]
then
cp crab_stepSIM.py ../../crab_stepSIM_TEMP.py
cp {name}_2_cfg.py ../../{name}_2_cfg.py
pushd ../../
crab submit crab_stepSIM_TEMP.py
rm crab_stepSIM_TEMP.py
rm {name}_2_cfg.py
popd
fi


if [ ${{DIGISTEP}} -eq 1 ]
then
cp crab_stepDIGI.py ../../crab_stepDIGI_TEMP.py
cp {name}_3_cfg.py ../../{name}_3_cfg.py
pushd ../../
crab submit crab_stepDIGI_TEMP.py
rm crab_stepDIGI_TEMP.py
rm {name}_3_cfg.py
popd
fi

if [ ${{HLTSTEP}} -eq 1 ]
then
cp crab_stepHLT.py ../../../CMSSW_10_2_16_UL/src/crab_stepDIGI_HLT.py
cp {name}_4_cfg.py ../../../CMSSW_10_2_16_UL/src/{name}_4_cfg.py
pushd ../../../CMSSW_10_2_16_UL/src
eval `scramv1 runtime -sh`
crab submit crab_stepHLT_TEMP.py
rm crab_stepHLT_TEMP.py
rm {name}_4_cfg.py
popd
fi


if [ ${{AODSTEP}} -eq 1 ]
then
cp crab_stepAOD.py ../../crab_stepAOD_TEMP.py
cp {name}_5_cfg.py ../../{name}_5_cfg.py
pushd ../../
crab submit crab_stepAOD_TEMP.py
rm crab_stepAOD_TEMP.py
rm {name}_5_cfg.py
popd
fi
'''
    return CRABLAUNCH


def CrabGEN(name,dirname,pdname,unitsperjob,njobs):
    CRABGEN=f'''from WMCore.Configuration import Configuration
config = Configuration()

NAME='{name}'


config.section_("General")
config.General.requestName = NAME+"_GEN"
config.General.workArea = 'crabsubmit'

config.section_("JobType")
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = NAME+'_1_cfg.py'
config.JobType.allowUndistributedCMSSW = True
config.JobType.maxMemoryMB = 2300

config.section_("Data")
config.Data.outputPrimaryDataset = '{pdname}'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = {unitsperjob}
NJOBS = {njobs}  # This is not a configuration parameter, but an auxiliary variable that we use in the next line.
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = False
config.Data.outputDatasetTag = NAME+'_GEN'

config.section_("Site")
config.Site.storageSite = 'T3_US_FNALLPC'
'''
    return CRABGEN

def CrabSIM(name,dirname,pdname):
    CRABSIM=f'''from WMCore.Configuration import Configuration
config = Configuration()

NAME='{name}'


config.section_("General")
config.General.requestName = NAME+"_SIM"
config.General.workArea = 'crabsubmit'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = NAME+'_2_cfg.py'
config.JobType.allowUndistributedCMSSW = True
config.JobType.maxMemoryMB = 2300

config.section_("Data")
config.Data.outputPrimaryDataset = '{pdname}'
config.Data.userInputFiles = open('./privateMCTools/{dirname}/crab_gen4sim_list.txt').readlines()
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.publication = False
config.Data.outputDatasetTag = NAME+'_SIM'

config.section_("Site")
config.Site.storageSite = 'T3_US_FNALLPC'
'''
    return CRABSIM





def CrabDIGI(name,dirname,pdname):
    CRABDIGI=f'''from WMCore.Configuration import Configuration
config = Configuration()

NAME='{name}'
config.section_("General")
config.General.requestName = NAME+'_digi'
config.General.workArea = 'crabsubmit'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = NAME+'_3_cfg.py'
config.JobType.allowUndistributedCMSSW = True
config.JobType.maxMemoryMB = 3300


config.section_("Data")
config.Data.outputPrimaryDataset = '{pdname}'
config.Data.userInputFiles = open('./privateMCTools/{dirname}/crab_sim4digi_list.txt').readlines()
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 2
config.Data.publication = False
config.Data.outputDatasetTag = NAME+'_digi'

config.section_("Site")
config.Site.storageSite = 'T3_US_FNALLPC'
'''
    return CRABDIGI


def CrabHLT(name,dirname,pdname):
    CRABHLT=f'''from WMCore.Configuration import Configuration
config = Configuration()

NAME='{name}'


config.section_("General")
config.General.requestName = NAME+"_HLT"
config.General.workArea = 'crabsubmit'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = NAME+'_4_cfg.py'
config.JobType.allowUndistributedCMSSW = True
config.JobType.maxMemoryMB = 2300

config.section_("Data")
config.Data.outputPrimaryDataset = '{pdname}'
config.Data.userInputFiles = open('./privateMCTools/{dirname}/crab_digi4hlt_list.txt').readlines()
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.publication = False
config.Data.outputDatasetTag = NAME+'_HLT'

config.section_("Site")
config.Site.storageSite = 'T3_US_FNALLPC'
'''
    return CRABHLT




def CrabAOD(name,dirname,pdname):
    CRABAOD=f'''from WMCore.Configuration import Configuration
config = Configuration()

NAME='{name}'

config.section_("General")
config.General.requestName = NAME+'_AOD'
config.General.workArea = 'crabsubmit'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = NAME+'_5_cfg.py'
config.JobType.allowUndistributedCMSSW = True
config.JobType.maxMemoryMB = 2800



config.section_("Data")
config.Data.outputPrimaryDataset = '{pdname}'
config.Data.userInputFiles = open('./privateMCTools/{dirname}/crab_hlt4aod_list.txt').readlines()
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.publication = False
config.Data.outputDatasetTag = NAME+'_AOD'

config.section_("Site")
config.Site.storageSite = 'T3_US_FNALLPC'
'''
    return CRABAOD


def MakeList(name,pdname):
    MAKELIST=f'''STAMP4SIM=$1
    STAMP4DIGI=$2
    STAMP4HLT=$3
    STAMP4AOD=$4
    
    GEN4SIM=$5
    SIM4DIGI=$6
    DIGI4HLT=$7
    HLT4AOD=$8
    
DIRNAME=testPath
NAME={name}_GEN
outfile=crab_gen4digi_list.txt
PD={pdname}

PREFIX=root://cmseos.fnal.gov/

if [ ${{STAMP4SIM}} -eq 1 ]
then
NAME={name}_GEN
xrdfs ${{PREFIX}} ls /store/user/janguian/${{PD}}/${{NAME}}/
fi

if [ ${{STAMP4DIGI}} -eq 1 ]
then
NAME={name}_SIM
xrdfs ${{PREFIX}} ls /store/user/janguian/${{PD}}/${{NAME}}/
fi

if [ ${{STAMP4HLT}} -eq 1 ]
then
NAME={name}_digi
xrdfs ${{PREFIX}} ls /store/user/janguian/${{PD}}/${{NAME}}/
fi


if [ ${{STAMP4AOD}} -eq 1 ]
then
NAME={name}_HLT
xrdfs ${{PREFIX}} ls /store/user/janguian/${{PD}}/${{NAME}}/
fi

if [ ${{GEN4SIM}} -eq 1 ]
then
NAME={name}_GEN
outfile=crab_gen4sim_list.txt
STAMP=?
xrdfs ${{PREFIX}} ls /store/user/janguian/${{PD}}/${{NAME}}/${{STAMP}}/0000/ > ${{outfile}}
sed -i 's/^/root:\/\/cmseos.fnal.gov\//' ${{outfile}}
fi

if [ ${{SIM4DIGI}} -eq 1 ]
then
NAME={name}_SIM
outfile=crab_sim4digi_list.txt
STAMP=?
xrdfs ${{PREFIX}} ls /store/user/janguian/${{PD}}/${{NAME}}/${{STAMP}}/0000/ > ${{outfile}}
sed -i 's/^/root:\/\/cmseos.fnal.gov\//' ${{outfile}}
fi


if [ ${{DIGI4HLT}} -eq 1 ]
then
NAME={name}_digi
outfile=crab_digi4hlt_list.txt
STAMP=?
xrdfs ${{PREFIX}} ls /store/user/janguian/${{PD}}/${{NAME}}/${{STAMP}}/0000/ > ${{outfile}}
sed -i 's/^/root:\/\/cmseos.fnal.gov\//' ${{outfile}}
fi

if [ ${{HLT4AOD}} -eq 1 ]
then
NAME={name}_HLT
outfile=crab_hlt4aod_list.txt
STAMP=?
xrdfs ${{PREFIX}} ls /store/user/janguian/${{PD}}/${{NAME}}/${{STAMP}}/0000/ > ${{outfile}}
sed -i 's/^/root:\/\/cmseos.fnal.gov\//' ${{outfile}}
fi

'''
    return MAKELIST
