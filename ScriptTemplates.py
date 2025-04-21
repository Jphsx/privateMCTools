

def DriverScript(name,nevent,dirname,carddir,configpath,cmsswbase):
    
    BS='\\'
    DRIVERSCRIPT=f''' NEVENT={nevent}
NAME={name}
CONFIGPATH={configpath}
BASE={cmsswbase}
DIRNAME={dirname}
CARDDIR={carddir}
COPYANDBUILD=$1 GENSIM=$2 RAW2DIGI=$3 AOD=$4
echo "modes" ${{COPYANDBUILD}} ${{GENSIM}} ${{RAW2DIGI}} ${{AOD}}


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
    --datatier GEN-SIM,LHE {BS}
    --fileout file:${{NAME}}_1.root {BS}
    --conditions 124X_mcRun3_2022_realistic_v12 {BS}
    --beamspot Realistic25ns13p6TeVEarly2022Collision {BS}
    --customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed="int(123456)"{BS}{BS}nprocess.source.numberEventsInLuminosityBlock="cms.untracked.uint32(250)" {BS}
    --step LHE,GEN,SIM {BS}
    --geometry DB:Extended {BS}
    --era Run3 {BS}
    --no_exec {BS}
    --mc {BS}
    -n ${{NEVENT}}

mv ${{NAME}}_1_cfg.py ./privateMCTools/${{DIRNAME}}/
popd

fi



if [ ${{RAW2DIGI}} -eq 1 ]
then
pushd ../../
cmsDriver.py {BS}
    --python_filename ${{NAME}}_2_cfg.py {BS}
    --eventcontent PREMIXRAW {BS}
    --customise Configuration/DataProcessing/Utils.addMonitoring {BS}
    --datatier GEN-SIM-RAW {BS}
    --fileout file:${{NAME}}_2.root {BS}
    --pileup_input "dbs:/Neutrino_E-10_gun/Run3Summer21PrePremix-Summer22_124X_mcRun3_2022_realistic_v11-v2/PREMIX" {BS}
    --conditions 124X_mcRun3_2022_realistic_v12 {BS}
    --step DIGI,DATAMIX,L1,DIGI2RAW,HLT:2022v12 {BS}
    --procModifiers premix_stage2,siPixelQualityRawToDigi {BS}
    --geometry DB:Extended {BS}
    --filein file:${{NAME}}_1.root {BS}
    --datamix PreMix {BS}
    --era Run3 {BS}
    --no_exec {BS}
    --mc {BS}
    -n ${{NEVENT}}

#cmsRun ${{NAME}}_2_cfg.py
mv ${{NAME}}_2_cfg.py ./privateMCTools/${{DIRNAME}}/
popd
fi


if [ ${{AOD}} -eq 1 ]
then
pushd ../../
cmsDriver.py {BS}
    --python_filename ${{NAME}}_3_cfg.py {BS}
    --eventcontent AODSIM {BS}
    --customise Configuration/DataProcessing/Utils.addMonitoring {BS}
    --datatier AODSIM {BS}
    --fileout file:${{NAME}}_AOD.root {BS}
    --conditions 124X_mcRun3_2022_realistic_v12 {BS}
    --step RAW2DIGI,L1Reco,RECO,RECOSIM {BS}
    --procModifiers siPixelQualityRawToDigi {BS}
    --geometry DB:Extended {BS}
    --filein file:${{NAME}}_2.root {BS}
    --era Run3 {BS}
    --no_exec {BS}
    --mc {BS}
    -n ${{NEVENT}}

#cmsRun ${{NAME}}_3_cfg.py
mv ${{NAME}}_3_cfg.py ./privateMCTools/${{DIRNAME}}/
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
DIGISTEP=$2
AODSTEP=$3

NAME={name}
echo "modes" ${{GENSTEP}} ${{DIGISTEP}} ${{AODSTEP}}

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

if [ ${{DIGISTEP}} -eq 1 ]
then
cp crab_stepDIGI.py ../../crab_stepDIGI_TEMP.py
cp {name}_2_cfg.py ../../{name}_2_cfg.py
pushd ../../
crab submit crab_stepDIGI_TEMP.py
rm crab_stepDIGI_TEMP.py
rm {name}_2_cfg.py
popd
fi

if [ ${{AODSTEP}} -eq 1 ]
then
cp crab_stepAOD.py ../../crab_stepAOD_TEMP.py
cp {name}_3_cfg.py ../../{name}_3_cfg.py
pushd ../../
crab submit crab_stepAOD_TEMP.py
rm crab_stepAOD_TEMP.py
rm {name}_3_cfg.py
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

def CrabDIGI(name,dirname,pdname):
    CRABDIGI=f'''from WMCore.Configuration import Configuration
config = Configuration()

NAME='{name}'
config.section_("General")
config.General.requestName = NAME+'_digi'
config.General.workArea = 'crabsubmit'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = NAME+'_2_cfg.py'
config.JobType.allowUndistributedCMSSW = True
config.JobType.maxMemoryMB = 3300


config.section_("Data")
config.Data.outputPrimaryDataset = '{pdname}'
config.Data.userInputFiles = open('./privateMCTools/{dirname}/crab_gen4digi_list.txt').readlines()
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5
config.Data.publication = False
config.Data.outputDatasetTag = NAME+'_digi'

config.section_("Site")
config.Site.storageSite = 'T3_US_FNALLPC'
'''
    return CRABDIGI

def CrabAOD(name,dirname,pdname):
    CRABAOD=f'''from WMCore.Configuration import Configuration
config = Configuration()

NAME='{name}'

config.section_("General")
config.General.requestName = NAME+'_AOD'
config.General.workArea = 'crabsubmit'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = NAME+'_3_cfg.py'
config.JobType.allowUndistributedCMSSW = True
config.JobType.maxMemoryMB = 2800



config.section_("Data")
config.Data.outputPrimaryDataset = '{pdname}'
config.Data.userInputFiles = open('./privateMCTools/{dirname}/crab_digi4aod_list.txt').readlines()
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.publication = False
config.Data.outputDatasetTag = NAME+'_AOD'

config.section_("Site")
config.Site.storageSite = 'T3_US_FNALLPC'
'''
    return CRABAOD


def MakeList(name,pdname):
    MAKELIST=f'''STAMP4DIGI=$1
    STAMP4AOD=$2
    GEN4DIGI=$3
DIGI4AOD=$4
    
DIRNAME=testPath
NAME={name}_GEN
outfile=crab_gen4digi_list.txt
PD={pdname}

PREFIX=root://cmseos.fnal.gov/

if [ ${{STAMP4DIGI}} -eq 1 ]
then
NAME={name}_GEN
xrdfs ${{PREFIX}} ls /store/user/janguian/${{PD}}/${{NAME}}/
fi

if [ ${{STAMP4AOD}} -eq 1 ]
then
NAME={name}_digi
xrdfs ${{PREFIX}} ls /store/user/janguian/${{PD}}/${{NAME}}/
fi

if [ ${{GEN4DIGI}} -eq 1 ]
then
NAME={name}_GEN
outfile=crab_gen4digi_list.txt
STAMP=?
xrdfs ${{PREFIX}} ls /store/user/janguian/${{PD}}/${{NAME}}/${{STAMP}}/0000/ > ${{outfile}}
sed -i 's/^/root:\/\/cmseos.fnal.gov\//' ${{outfile}}
fi

if [ ${{DIGI4AOD}} -eq 1 ]
then
NAME={name}_digi
outfile=crab_digi4aod_list.txt
STAMP=?
xrdfs ${{PREFIX}} ls /store/user/janguian/${{PD}}/${{NAME}}/${{STAMP}}/0000/ > ${{outfile}}
sed -i 's/^/root:\/\/cmseos.fnal.gov\//' ${{outfile}}
fi
'''
    return MAKELIST
