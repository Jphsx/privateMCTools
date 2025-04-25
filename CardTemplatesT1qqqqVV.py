

#script to generate gridpack cards for T1qqqqVV where V=Z,A


Mgo='1.0e3' 
Mneu1='2.5e2'
Mneu2='2.5e2'
N2WIDTH='1.97e-14' 
N2mode='22'
mg5Output='testoutput'



def getProcCard( mg5Output ):
    PROCCARD=f'''#************************************************************
#*                     MadGraph5_aMC@NLO                    *
#*                                                          *
#*                *                       *                 *
#*                  *        * *        *                   *
#*                    * * * * 5 * * * *                     *
#*                  *        * *        *                   *
#*                *                       *                 *
#*                                                          *
#*                                                          *
#*         VERSION 2.9.21                2024-09-26         *
#*                                                          *
#*    The MadGraph5_aMC@NLO Development Team - Find us at   *
#*    https://server06.fynu.ucl.ac.be/projects/madgraph     *
#*                                                          *
#************************************************************
#*                                                          *
#*               Command File for MadGraph5_aMC@NLO         *
#*                                                          *
#*     run as ./bin/mg5_aMC  filename                       *
#*                                                          *
#************************************************************
set group_subprocesses Auto
set ignore_six_quark_processes False
set low_mem_multicore_nlo_generation False
set complex_mass_scheme False
set gauge unitary
set loop_optimized_output True
set loop_color_flows False
set max_npoint_for_channel 0
set default_unset_couplings 99
set max_t_for_channel 99
set zerowidth_tchannel True
import model sm
define p = g u c d s u~ c~ d~ s~
define j = g u c d s u~ c~ d~ s~
define p = p b b~
define j = j b b~
define l+ = e+ mu+
define l- = e- mu-
define vl = ve vm vt
define vl~ = ve~ vm~ vt~
import model MSSM_SLHA2
generate p p > go go @1
add process p p > go go j @2
add process p p > go go j j @3
output {mg5Output}
'''
    return PROCCARD

def getRunCard():
    RUNCARD='''#*********************************************************************
#                       MadGraph5_aMC@NLO                            *
#                                                                    *
#                     run_card.dat MadEvent                          *
#                                                                    *
#  This file is used to set the parameters of the run.               *
#                                                                    *
#  Some notation/conventions:                                        *
#                                                                    *
#   Lines starting with a '# ' are info or comments                  *
#                                                                    *
#   mind the format:   value    = variable     ! comment             *
#                                                                    *
#   To display more options, you can type the command:               *
#      update to_full                                                *
#*********************************************************************
#                                                                    
#*********************************************************************
# Tag name for the run (one word)                                    *
#*********************************************************************
  tag_1     = run_tag ! name of the run 
#*********************************************************************
# Number of events and rnd seed                                      *
# Warning: Do not generate more than 1M events in a single run       *
#*********************************************************************
  10000 = nevents ! Number of unweighted events requested 
  0   = iseed   ! rnd seed (0=assigned automatically=default))
#*********************************************************************
# Collider type and energy                                           *
# lpp: 0=No PDF, 1=proton, -1=antiproton, 2=photon from proton,      *
#                3=photon from electron, 4=photon from muon          *
#*********************************************************************
     1        = lpp1    ! beam 1 type 
     1        = lpp2    ! beam 2 type
     6800.0     = ebeam1  ! beam 1 total energy in GeV
     6800.0     = ebeam2  ! beam 2 total energy in GeV
# To see polarised beam options: type "update beam_pol"

#*********************************************************************
# PDF CHOICE: this automatically fixes also alpha_s and its evol.    *
#*********************************************************************
     lhapdf    = pdlabel     ! PDF set                                     
     $DEFAULT_PDF_SETS    = lhaid     ! if pdlabel=lhapdf, this is the lhapdf number
# To see heavy ion options: type "update ion_pdf"
#*********************************************************************
# Renormalization and factorization scales                           *
#*********************************************************************
 False = fixed_ren_scale  ! if .true. use fixed ren scale
 False        = fixed_fac_scale  ! if .true. use fixed fac scale
 91.188  = scale            ! fixed ren scale
 91.188  = dsqrt_q2fact1    ! fixed fact scale for pdf1
 91.188  = dsqrt_q2fact2    ! fixed fact scale for pdf2
 -1 = dynamical_scale_choice ! Choose one of the preselected dynamical choices
 1.0  = scalefact        ! scale factor for event-by-event scales
#*********************************************************************
# Type and output format
#*********************************************************************
  False     = gridpack  !True = setting up the grid pack
  -1.0 = time_of_flight ! threshold (in mm) below which the invariant livetime is not written (-1 means not written)
  average =  event_norm       ! average/sum. Normalization of the weight in the LHEF
# To see MLM/CKKW  merging options: type "update MLM" or "update CKKW"

#*********************************************************************
#
#*********************************************************************
# Phase-Space Optimization strategy (basic options)
#*********************************************************************
   0  = nhel          ! using helicities importance sampling or not.
                             ! 0: sum over helicity, 1: importance sampling
   1  = sde_strategy  ! default integration strategy (hep-ph/2021.00773)
                             ! 1 is old strategy (using amp square)
                             ! 2 is new strategy (using only the denominator)
# To see advanced option for Phase-Space optimization: type "update psoptim"                         
#*********************************************************************
# Generation bias, check the wiki page below for more information:   *
#  'cp3.irmp.ucl.ac.be/projects/madgraph/wiki/LOEventGenerationBias' *
#*********************************************************************
 None = bias_module  ! Bias type of bias, [None, ptj_bias, -custom_folder-]
 {} = bias_parameters ! Specifies the parameters of the module.
#
#*******************************                                                 
# Parton level cuts definition *
#*******************************                                     
#                                                                    
#
#*********************************************************************
# BW cutoff (M+/-bwcutoff*Gamma) ! Define on/off-shell for "$" and decay  
#*********************************************************************
  15.0  = bwcutoff      ! (M+/-bwcutoff*Gamma)
#*********************************************************************
# Standard Cuts                                                      *
#*********************************************************************
# Minimum and maximum pt's (for max, -1 means no cut)                *
#*********************************************************************
 {} = pt_min_pdg ! pt cut for other particles (use pdg code). Applied on particle and anti-particle
 {}     = pt_max_pdg ! pt cut for other particles (syntax e.g. {6: 100, 25: 50}) 
#
# For display option for energy cut in the partonic center of mass frame type 'update ecut'
#
#*********************************************************************
# Maximum and minimum absolute rapidity (for max, -1 means no cut)   *
#*********************************************************************
 {} = eta_min_pdg ! rap cut for other particles (use pdg code). Applied on particle and anti-particle
 {} = eta_max_pdg ! rap cut for other particles (syntax e.g. {6: 2.5, 23: 5})
#*********************************************************************
# Minimum and maximum DeltaR distance                                *
#*********************************************************************
#*********************************************************************
# Minimum and maximum invariant mass for pairs                       *
#*********************************************************************
 {} = mxx_min_pdg ! min invariant mass of a pair of particles X/X~ (e.g. {6:250})
 {'default': False} = mxx_only_part_antipart ! if True the invariant mass is applied only 
                       ! to pairs of particle/antiparticle and not to pairs of the same pdg codes.  
#*********************************************************************
# Inclusive cuts                                                     *
#*********************************************************************
 0.0  = ptheavy   ! minimum pt for at least one heavy final state
#*********************************************************************
# maximal pdg code for quark to be considered as a light jet         *
# (otherwise b cuts are applied)                                     *
#*********************************************************************
 4 = maxjetflavor    ! Maximum jet pdg code
#*********************************************************************
#
#*********************************************************************
# Store info for systematics studies                                 *
# WARNING: Do not use for interference type of computation           *
#*********************************************************************
   True  = use_syst      ! Enable systematics studies
#
systematics = systematics_program ! none, systematics [python], SysCalc [depreceted, C++]
['--mur=0.5,1,2', '--muf=0.5,1,2', '--pdf=errorset'] = systematics_arguments ! see: https://cp3.irmp.ucl.ac.be/projects/madgraph/wiki/Systematics#Systematicspythonmodule
# Syscalc is deprecated but to see the associate options type'update syscalc'
~
'''
    return RUNCARD


def getRunCardUL():
    RUNCARD='''#*********************************************************************
#                       MadGraph5_aMC@NLO                            *
#                                                                    *
#                     run_card.dat MadEvent                          *
#                                                                    *
#  This file is used to set the parameters of the run.               *
#                                                                    *
#  Some notation/conventions:                                        *
#                                                                    *
#   Lines starting with a '# ' are info or comments                  *
#                                                                    *
#   mind the format:   value    = variable     ! comment             *
#                                                                    *
#   To display more options, you can type the command:               *
#      update to_full                                                *
#*********************************************************************
#                                                                    
#*********************************************************************
# Tag name for the run (one word)                                    *
#*********************************************************************
  tag_1     = run_tag ! name of the run 
#*********************************************************************
# Number of events and rnd seed                                      *
# Warning: Do not generate more than 1M events in a single run       *
#*********************************************************************
  10000 = nevents ! Number of unweighted events requested 
  0   = iseed   ! rnd seed (0=assigned automatically=default))
#*********************************************************************
# Collider type and energy                                           *
# lpp: 0=No PDF, 1=proton, -1=antiproton, 2=photon from proton,      *
#                3=photon from electron, 4=photon from muon          *
#*********************************************************************
     1        = lpp1    ! beam 1 type 
     1        = lpp2    ! beam 2 type
     6500.0     = ebeam1  ! beam 1 total energy in GeV
     6500.0     = ebeam2  ! beam 2 total energy in GeV
# To see polarised beam options: type "update beam_pol"

#*********************************************************************
# PDF CHOICE: this automatically fixes also alpha_s and its evol.    *
#*********************************************************************
     lhapdf    = pdlabel     ! PDF set                                     
     $DEFAULT_PDF_SETS    = lhaid     ! if pdlabel=lhapdf, this is the lhapdf number
# To see heavy ion options: type "update ion_pdf"
#*********************************************************************
# Renormalization and factorization scales                           *
#*********************************************************************
 False = fixed_ren_scale  ! if .true. use fixed ren scale
 False        = fixed_fac_scale  ! if .true. use fixed fac scale
 91.188  = scale            ! fixed ren scale
 91.188  = dsqrt_q2fact1    ! fixed fact scale for pdf1
 91.188  = dsqrt_q2fact2    ! fixed fact scale for pdf2
 -1 = dynamical_scale_choice ! Choose one of the preselected dynamical choices
 1.0  = scalefact        ! scale factor for event-by-event scales
#*********************************************************************
# Type and output format
#*********************************************************************
  False     = gridpack  !True = setting up the grid pack
  -1.0 = time_of_flight ! threshold (in mm) below which the invariant livetime is not written (-1 means not written)
  average =  event_norm       ! average/sum. Normalization of the weight in the LHEF
# To see MLM/CKKW  merging options: type "update MLM" or "update CKKW"

#*********************************************************************
#
#*********************************************************************
# Phase-Space Optimization strategy (basic options)
#*********************************************************************
   0  = nhel          ! using helicities importance sampling or not.
                             ! 0: sum over helicity, 1: importance sampling
   1  = sde_strategy  ! default integration strategy (hep-ph/2021.00773)
                             ! 1 is old strategy (using amp square)
                             ! 2 is new strategy (using only the denominator)
# To see advanced option for Phase-Space optimization: type "update psoptim"                         
#*********************************************************************
# Generation bias, check the wiki page below for more information:   *
#  'cp3.irmp.ucl.ac.be/projects/madgraph/wiki/LOEventGenerationBias' *
#*********************************************************************
 None = bias_module  ! Bias type of bias, [None, ptj_bias, -custom_folder-]
 {} = bias_parameters ! Specifies the parameters of the module.
#
#*******************************                                                 
# Parton level cuts definition *
#*******************************                                     
#                                                                    
#
#*********************************************************************
# BW cutoff (M+/-bwcutoff*Gamma) ! Define on/off-shell for "$" and decay  
#*********************************************************************
  15.0  = bwcutoff      ! (M+/-bwcutoff*Gamma)
#*********************************************************************
# Standard Cuts                                                      *
#*********************************************************************
# Minimum and maximum pt's (for max, -1 means no cut)                *
#*********************************************************************
 {} = pt_min_pdg ! pt cut for other particles (use pdg code). Applied on particle and anti-particle
 {}     = pt_max_pdg ! pt cut for other particles (syntax e.g. {6: 100, 25: 50}) 
#
# For display option for energy cut in the partonic center of mass frame type 'update ecut'
#
#*********************************************************************
# Maximum and minimum absolute rapidity (for max, -1 means no cut)   *
#*********************************************************************
 {} = eta_min_pdg ! rap cut for other particles (use pdg code). Applied on particle and anti-particle
 {} = eta_max_pdg ! rap cut for other particles (syntax e.g. {6: 2.5, 23: 5})
#*********************************************************************
# Minimum and maximum DeltaR distance                                *
#*********************************************************************
#*********************************************************************
# Minimum and maximum invariant mass for pairs                       *
#*********************************************************************
 {} = mxx_min_pdg ! min invariant mass of a pair of particles X/X~ (e.g. {6:250})
 {'default': False} = mxx_only_part_antipart ! if True the invariant mass is applied only 
                       ! to pairs of particle/antiparticle and not to pairs of the same pdg codes.  
#*********************************************************************
# Inclusive cuts                                                     *
#*********************************************************************
 0.0  = ptheavy   ! minimum pt for at least one heavy final state
#*********************************************************************
# maximal pdg code for quark to be considered as a light jet         *
# (otherwise b cuts are applied)                                     *
#*********************************************************************
 4 = maxjetflavor    ! Maximum jet pdg code
#*********************************************************************
#
#*********************************************************************
# Store info for systematics studies                                 *
# WARNING: Do not use for interference type of computation           *
#*********************************************************************
   True  = use_syst      ! Enable systematics studies
#
systematics = systematics_program ! none, systematics [python], SysCalc [depreceted, C++]
['--mur=0.5,1,2', '--muf=0.5,1,2', '--pdf=errorset'] = systematics_arguments ! see: https://cp3.irmp.ucl.ac.be/projects/madgraph/wiki/Systematics#Systematicspythonmodule
# Syscalc is deprecated but to see the associate options type'update syscalc'
~
'''
    return RUNCARD

def getParamCard( Mgo, Mneu1, Mneu2, N2WIDTH, N2mode):


    PARAMCARD=f'''######################################################################
## PARAM_CARD AUTOMATICALLY GENERATED BY MG5 FOLLOWING UFO MODEL   ####
######################################################################
##                                                                  ##
##  Width set on Auto will be computed following the information    ##
##        present in the decay.py files of the model.               ##
##        See  arXiv:1402.1178 for more details.                    ##
##                                                                  ##
######################################################################


#WIDTH = 0.0197e-11 / CTAU
#3.94e-14 for CTAU=5 cm
#1.97e-14 for CTAU=10 cm
###################################
## INFORMATION FOR DSQMIX
###################################
Block dsqmix 
    1   1 1.000000e+00 # RRd1x1 
    2   2 1.000000e+00 # RRd2x2 
    3   3 9.387379e-01 # RRd3x3 
    3   6 3.446319e-01 # RRd3x6 
    4   4 1.000000e+00 # RRd4x4 
    5   5 1.000000e+00 # RRd5x5 
    6   3 -3.446319e-01 # RRd6x3 
    6   6 9.387379e-01 # RRd6x6 

###################################
## INFORMATION FOR FRALPHA
###################################
Block fralpha 
    1 -1.138252e-01 # alp 

###################################
## INFORMATION FOR HMIX
###################################
Block hmix 
    1 3.576810e+02 # RMUH 
    2 9.748624e+00 # tb 
    4 1.664391e+05 # MA2 

###################################
## INFORMATION FOR MASS
###################################
Block mass 
    5 4.889917e+00 # MB 
    6 1.750000e+02 # MT 
   15 1.777000e+00 # Mta 
   23 9.118760e+01 # MZ 
   24 8.037900e+01 # MW 
   25 1.251100e+02 # MH01 
   35 1.000000e+05 # MH02 
   36 1.000000e+05 # MA0 
   37 1.000000e+05 # MH 
  1000001 1.000000e+05 # set of param :1*Msd1, 1*Msd2 
  1000002 1.000000e+05 # set of param :1*Msu1, 1*Msu2 
  1000005 1.000000e+05 # Msd3 
  1000006 1.000000e+05 # Msu3 
  1000011 1.000000e+05 # set of param :1*Msl1, 1*Msl2 
  1000012 1.000000e+05 # set of param :1*Msn1, 1*Msn2 
  1000015 1.000000e+05 # Msl3 
  1000016 1.000000e+05 # Msn3 
  1000021 {Mgo} # Mgo 
  1000022 {Mneu1} # Mneu1 
  1000023 {Mneu2} # Mneu2 
  1000024 1.000000e+05 # Mch1 
  1000025 1.000000e+05 # Mneu3 
  1000035 1.000000e+05 # Mneu4 
  1000037 1.000000e+05 # Mch2 
  2000001 1.000000e+05 # set of param :1*Msd4, 1*Msd5 
  2000002 1.000000e+05 # set of param :1*Msu4, 1*Msu5 
  2000005 1.000000e+05 # Msd6 
  2000006 1.000000e+05 # Msu6 
  2000011 1.000000e+05 # set of param :1*Msl4, 1*Msl5 
  2000015 1.000000e+05 # Msl6 
## Dependent parameters, given by model restrictions.
## Those values should be edited following the 
## analytical expression. MG5 ignores those values 
## but they are important for interfacing the output of MG5
## to external program such as Pythia.
  1 0.000000e+00 # d : 0.0 
  2 0.000000e+00 # u : 0.0 
  3 0.000000e+00 # s : 0.0 
  4 0.000000e+00 # c : 0.0 
  11 0.000000e+00 # e- : 0.0 
  12 0.000000e+00 # ve : 0.0 
  13 0.000000e+00 # mu- : 0.0 
  14 0.000000e+00 # vm : 0.0 
  16 0.000000e+00 # vt : 0.0 
  21 0.000000e+00 # g : 0.0 
  22 0.000000e+00 # a : 0.0 
  1000014 1.852583e+02 # svm : Msn1 
  1000013 2.029157e+02 # mul- : Msl1 
  2000013 1.441028e+02 # mur- : Msl4 
  1000004 5.611190e+02 # cl : Msu1 
  2000004 5.492593e+02 # cr : Msu4 
  1000003 5.684411e+02 # sl : Msd1 
  2000003 5.452285e+02 # sr : Msd4 

###################################
## INFORMATION FOR MSD2
###################################
Block msd2 
    1   1 2.736847e+05 # set of param :1*RmD21x1, 1*RmD22x2 
    2   2 2.736847e+05 # MG5 will not use this value use instead 1*mdl_RmD21x1 
    3   3 2.702620e+05 # RmD23x3 

###################################
## INFORMATION FOR MSE2
###################################
Block mse2 
    1   1 1.863063e+04 # set of param :1*RmE21x1, 1*RmE22x2 
    2   2 1.863063e+04 # MG5 will not use this value use instead 1*mdl_RmE21x1 
    3   3 1.796764e+04 # RmE23x3 

###################################
## INFORMATION FOR MSL2
###################################
Block msl2 
    1   1 3.815567e+04 # set of param :1*RmL21x1, 1*RmL22x2 
    2   2 3.815567e+04 # MG5 will not use this value use instead 1*mdl_RmL21x1 
    3   3 3.782868e+04 # RmL23x3 

###################################
## INFORMATION FOR MSOFT
###################################
Block msoft 
    1 1.013965e+02 # RMx1 
    2 1.915042e+02 # RMx2 
    3 5.882630e+02 # RMx3 
   21 3.233749e+04 # mHd2 
   22 -1.288001e+05 # mHu2 

###################################
## INFORMATION FOR MSQ2
###################################
Block msq2 
    1   1 2.998367e+05 # set of param :1*RmQ21x1, 1*RmQ22x2 
    2   2 2.998367e+05 # MG5 will not use this value use instead 1*mdl_RmQ21x1 
    3   3 2.487654e+05 # RmQ23x3 

###################################
## INFORMATION FOR MSU2
###################################
Block msu2 
    1   1 2.803821e+05 # set of param :1*RmU21x1, 1*RmU22x2 
    2   2 2.803821e+05 # MG5 will not use this value use instead 1*mdl_RmU21x1 
    3   3 1.791371e+05 # RmU23x3 

###################################
## INFORMATION FOR NMIX
###################################
Block nmix 
    1   1 9.863644e-01 # RNN1x1 
    1   2 -5.311036e-02 # RNN1x2 
    1   3 1.464340e-01 # RNN1x3 
    1   4 -5.311861e-02 # RNN1x4 
    2   1 9.935054e-02 # RNN2x1 
    2   2 9.449493e-01 # RNN2x2 
    2   3 -2.698467e-01 # RNN2x3 
    2   4 1.561507e-01 # RNN2x4 
    3   1 -6.033880e-02 # RNN3x1 
    3   2 8.770049e-02 # RNN3x2 
    3   3 6.958775e-01 # RNN3x3 
    3   4 7.102270e-01 # RNN3x4 
    4   1 -1.165071e-01 # RNN4x1 
    4   2 3.107390e-01 # RNN4x2 
    4   3 6.492260e-01 # RNN4x3 
    4   4 -6.843778e-01 # RNN4x4 

###################################
## INFORMATION FOR SELMIX
###################################
Block selmix 
    1   1 1.000000e+00 # RRl1x1 
    2   2 1.000000e+00 # RRl2x2 
    3   3 2.824872e-01 # RRl3x3 
    3   6 9.592711e-01 # RRl3x6 
    4   4 1.000000e+00 # RRl4x4 
    5   5 1.000000e+00 # RRl5x5 
    6   3 9.592711e-01 # RRl6x3 
    6   6 -2.824872e-01 # RRl6x6 

###################################
## INFORMATION FOR SMINPUTS
###################################
Block sminputs 
    1 1.279340e+02 # aEWM1 
    3 1.180000e-01 # aS (Note that Parameter not used if you use a PDF set) 

###################################
## INFORMATION FOR SNUMIX
###################################
Block snumix 
    1   1 1.000000e+00 # RRn1x1 
    2   2 1.000000e+00 # RRn2x2 
    3   3 1.000000e+00 # RRn3x3 

###################################
## INFORMATION FOR TD
###################################
Block td 
    3   3 -1.106937e+02 # Rtd3x3 

###################################
## INFORMATION FOR TE
###################################
Block te 
    3   3 -2.540197e+01 # Rte3x3 

###################################
## INFORMATION FOR TU
###################################
Block tu 
    3   3 -4.447525e+02 # Rtu3x3 

###################################
## INFORMATION FOR UMIX
###################################
Block umix 
    1   1 9.168349e-01 # RUU1x1 
    1   2 -3.992666e-01 # RUU1x2 
    2   1 3.992666e-01 # RUU2x1 
    2   2 9.168349e-01 # RUU2x2 

###################################
## INFORMATION FOR UPMNS
###################################
Block upmns 
    1   1 1.000000e+00 # RMNS1x1 
    2   2 1.000000e+00 # RMNS2x2 
    3   3 1.000000e+00 # RMNS3x3 

###################################
## INFORMATION FOR USQMIX
###################################
Block usqmix 
    1   1 1.000000e+00 # RRu1x1 
    2   2 1.000000e+00 # RRu2x2 
    3   3 5.536450e-01 # RRu3x3 
    3   6 8.327528e-01 # RRu3x6 
    4   4 1.000000e+00 # RRu4x4 
    5   5 1.000000e+00 # RRu5x5 
    6   3 8.327528e-01 # RRu6x3 
    6   6 -5.536450e-01 # RRu6x6 

###################################
## INFORMATION FOR VCKM
###################################
Block vckm 
    1   1 1.000000e+00 # RCKM1x1 
    2   2 1.000000e+00 # RCKM2x2 
    3   3 1.000000e+00 # RCKM3x3 

###################################
## INFORMATION FOR VMIX
###################################
Block vmix 
    1   1 9.725578e-01 # RVV1x1 
    1   2 -2.326612e-01 # RVV1x2 
    2   1 2.326612e-01 # RVV2x1 
    2   2 9.725578e-01 # RVV2x2 

###################################
## INFORMATION FOR YD
###################################
Block yd 
    3   3 1.388402e-01 # Ryd3x3 

###################################
## INFORMATION FOR YE
###################################
Block ye 
    3   3 1.008908e-01 # Rye3x3 

###################################
## INFORMATION FOR YU
###################################
Block yu 
    3   3 8.928445e-01 # Ryu3x3 

###################################
## INFORMATION FOR DECAY
###################################
DECAY   6 1.561950e+00 # WT 
DECAY  23 2.411433e+00 # WZ 
DECAY  24 2.002822e+00 # WW 
DECAY  25 1.986108e-03 # WH01 
DECAY  35 5.748014e-01 # WH02 
DECAY  36 6.321785e-01 # WA0 
DECAY  37 5.469628e-01 # WH 
DECAY 1000001 5.312788e+00 # Wsd1 
DECAY 1000002 5.477195e+00 # Wsu1 
DECAY 1000003 5.312788e+00 # Wsd2 
DECAY 1000004 5.477195e+00 # Wsu2 
DECAY 1000005 3.736276e+00 # Wsd3 
DECAY 1000006 2.021596e+00 # Wsu3 
DECAY 1000011 2.136822e-01 # Wsl1 
DECAY 1000012 1.498816e-01 # Wsn1 
DECAY 1000013 2.136822e-01 # Wsl2 
DECAY 1000014 1.498816e-01 # Wsn2 
DECAY 1000015 1.483273e-01 # Wsl3 
DECAY 1000016 1.475190e-01 # Wsn3 
DECAY 1000021 5.506754e+00 # Wgo
    2.5e-01      3    1000023 	-1	1  # BR(~g -> ~chi_20 sdownL)
    2.5e-01      3    1000023   -2	2  # BR(~g -> ~chi_20 supL)
    2.5e-01      3    1000023   -3	3  # BR(~g -> ~chi_20 sdownR)
    2.5e-01      3    1000023   -4	4  # BR(~g -> ~chi_20 supL)  
DECAY 1000023 {N2WIDTH} # Wneu2 
    1.0E00      2    1000022    {N2mode}   # BR(~chi_20 -> ~chi_10 a)
DECAY 1000024 1.704145e-02 # Wch1 
DECAY 1000025 1.915985e+00 # Wneu3 
DECAY 1000035 2.585851e+00 # Wneu4 
DECAY 1000037 2.486895e+00 # Wch2 
DECAY 2000001 2.858123e-01 # Wsd4 
DECAY 2000002 1.152973e+00 # Wsu4 
DECAY 2000003 2.858123e-01 # Wsd5 
DECAY 2000004 1.152973e+00 # Wsu5 
DECAY 2000005 8.015663e-01 # Wsd6 
DECAY 2000006 7.373133e+00 # Wsu6 
DECAY 2000011 2.161216e-01 # Wsl4 
DECAY 2000013 2.161216e-01 # Wsl5 
DECAY 2000015 2.699061e-01 # Wsl6 
## Dependent parameters, given by model restrictions.
## Those values should be edited following the 
## analytical expression. MG5 ignores those values 
## but they are important for interfacing the output of MG5
## to external program such as Pythia.
DECAY  1 0.000000e+00 # d : 0.0 
DECAY  2 0.000000e+00 # u : 0.0 
DECAY  3 0.000000e+00 # s : 0.0 
DECAY  4 0.000000e+00 # c : 0.0 
DECAY  5 0.000000e+00 # b : 0.0 
DECAY  11 0.000000e+00 # e- : 0.0 
DECAY  12 0.000000e+00 # ve : 0.0 
DECAY  13 0.000000e+00 # mu- : 0.0 
DECAY  14 0.000000e+00 # vm : 0.0 
DECAY  15 0.000000e+00 # ta- : 0.0 
DECAY  16 0.000000e+00 # vt : 0.0 
DECAY  21 0.000000e+00 # g : 0.0 
DECAY  22 0.000000e+00 # a : 0.0 
DECAY  1000022 0.000000e+00 # n1 : 0.0 
#===========================================================
# QUANTUM NUMBERS OF NEW STATE(S) (NON SM PDG CODE)
#===========================================================

Block QNUMBERS 1000022  # n1 
        1 0  # 3 times electric charge
        2 2  # number of spin states (2S+1)
        3 1  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 0  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 1000023  # n2 
        1 0  # 3 times electric charge
        2 2  # number of spin states (2S+1)
        3 1  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 0  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 1000025  # n3 
        1 0  # 3 times electric charge
        2 2  # number of spin states (2S+1)
        3 1  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 0  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 1000035  # n4 
        1 0  # 3 times electric charge
        2 2  # number of spin states (2S+1)
        3 1  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 0  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 1000024  # x1+ 
        1 3  # 3 times electric charge
        2 2  # number of spin states (2S+1)
        3 1  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 1000037  # x2+ 
        1 3  # 3 times electric charge
        2 2  # number of spin states (2S+1)
        3 1  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 1000021  # go 
        1 0  # 3 times electric charge
        2 2  # number of spin states (2S+1)
        3 8  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 0  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 35  # h2 
        1 0  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 1  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 0  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 36  # h3 
        1 0  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 1  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 0  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 37  # h+ 
        1 3  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 1  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 1000012  # sve 
        1 0  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 1  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 1000014  # svm 
        1 0  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 1  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 1000016  # svt 
        1 0  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 1  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 1000011  # el- 
        1 -3  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 1  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 1000013  # mul- 
        1 -3  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 1  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 1000015  # ta1- 
        1 -3  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 1  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 2000011  # er- 
        1 -3  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 1  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 2000013  # mur- 
        1 -3  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 1  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 2000015  # ta2- 
        1 -3  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 1  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 1000002  # ul 
        1 2  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 1000004  # cl 
        1 2  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 1000006  # t1 
        1 2  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 2000002  # ur 
        1 2  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 2000004  # cr 
        1 2  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 2000006  # t2 
        1 2  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 1000001  # dl 
        1 -1  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 1000003  # sl 
        1 -1  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 1000005  # b1 
        1 -1  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 2000001  # dr 
        1 -1  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 2000003  # sr 
        1 -1  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
Block QNUMBERS 2000005  # b2 
        1 -1  # 3 times electric charge
        2 1  # number of spin states (2S+1)
        3 3  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 1  # Particle/Antiparticle distinction (0=own anti)
'''
    return PARAMCARD


def getFragment(EOS_gridpack, mglu, ctau):
    ctau_mm = str(ctau*1000.)
    FRAGMENT=f'''import FWCore.ParameterSet.Config as cms

Nevents = 100
externalLHEProducer = cms.EDProducer('ExternalLHEProducer',
    args = cms.vstring('{EOS_gridpack}'),
    nEvents = cms.untracked.uint32(Nevents),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_xrootd.sh'),
    generateConcurrently = cms.untracked.bool(False)
)


from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *


#params from T1qqqqVV
def matchParams(mass):
    if   mass<799: return 118., 0.235
    elif mass<999: return 128., 0.235
    elif mass<1199: return 140., 0.235
    elif mass<1399: return 143., 0.245
    elif mass<1499: return 147., 0.255
    elif mass<1799: return 150., 0.267
    elif mass<2099: return 156., 0.290 
    elif mass<2301: return 160., 0.315 
    elif mass<2601: return 162., 0.340
    elif mass<2851: return 168, 0.364
    else: return 160., 0.315
model="T1qqqqVV"
#mlsp=1.0
mglu={mglu}
qcut, tru_eff = matchParams(mglu)
mcm_eff = 0.258 #what is this??
wgt = Nevents*(mcm_eff/tru_eff)

generator = cms.EDFilter("Pythia8ConcurrentHadronizerFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13600.),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8PSweightsSettingsBlock,
        processParameters = cms.vstring(                          
            'JetMatching:setMad = off',
            'JetMatching:scheme = 1',
            'JetMatching:merge = on',
            'JetMatching:jetAlgorithm = 2',
            'JetMatching:etaJetMax = 5.',
            'JetMatching:coneRadius = 1.',
            'JetMatching:slowJetPower = 1',
            'JetMatching:qCut = %.0f' % qcut,  #this is the actual merging scale
            'JetMatching:nQmatch = 5', #4 corresponds to 4-flavour scheme (no matching of b-quarks), 5 for 5-flavour scheme
            'JetMatching:nJetMax = 4', #number of partons in born matrix element for highest multiplicity
            'JetMatching:doShowerKt = off', #off for MLM matching, turn on for shower-kT matching
            '1000023:tau0 = {ctau_mm}',#THIS IS IN MM
            '23:onMode=off',
            '23:onIfAny=1 2 3 4 5 11 13 15'
            #'TimeShower:mMaxGamma = 4.0',
            #'BeamRemnants:primordialKThard = 2.48'
        ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'pythia8PSweightsSettings',
                                    'processParameters',
                                    )
    ),
    #RandomizedParameters = cms.VPSet()
)
'''

    return FRAGMENT


def getFragmentUL(EOS_gridpack, mglu, ctau):
    ctau_mm = str(ctau*1000.)
    FRAGMENT=f'''import FWCore.ParameterSet.Config as cms

Nevents = 100
externalLHEProducer = cms.EDProducer('ExternalLHEProducer',
    args = cms.vstring('{EOS_gridpack}'),
    nEvents = cms.untracked.uint32(Nevents),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_xrootd.sh'),
    generateConcurrently = cms.untracked.bool(False)
)


from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *


#params from T1qqqqVV
def matchParams(mass):
    if   mass<799: return 118., 0.235
    elif mass<999: return 128., 0.235
    elif mass<1199: return 140., 0.235
    elif mass<1399: return 143., 0.245
    elif mass<1499: return 147., 0.255
    elif mass<1799: return 150., 0.267
    elif mass<2099: return 156., 0.290 
    elif mass<2301: return 160., 0.315 
    elif mass<2601: return 162., 0.340
    elif mass<2851: return 168, 0.364
    else: return 160., 0.315
model="T1qqqqVV"
#mlsp=1.0
mglu={mglu}
qcut, tru_eff = matchParams(mglu)
mcm_eff = 0.258 #what is this??
wgt = Nevents*(mcm_eff/tru_eff)

generator = cms.EDFilter("Pythia8ConcurrentHadronizerFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8PSweightsSettingsBlock,
        processParameters = cms.vstring(                          
            'JetMatching:setMad = off',
            'JetMatching:scheme = 1',
            'JetMatching:merge = on',
            'JetMatching:jetAlgorithm = 2',
            'JetMatching:etaJetMax = 5.',
            'JetMatching:coneRadius = 1.',
            'JetMatching:slowJetPower = 1',
            'JetMatching:qCut = %.0f' % qcut,  #this is the actual merging scale
            'JetMatching:nQmatch = 5', #4 corresponds to 4-flavour scheme (no matching of b-quarks), 5 for 5-flavour scheme
            'JetMatching:nJetMax = 4', #number of partons in born matrix element for highest multiplicity
            'JetMatching:doShowerKt = off', #off for MLM matching, turn on for shower-kT matching
            '1000023:tau0 = {ctau_mm}',#THIS IS IN MM
            '23:onMode=off',
            '23:onIfAny=1 2 3 4 5 11 13 15'
            #'TimeShower:mMaxGamma = 4.0',
            #'BeamRemnants:primordialKThard = 2.48'
        ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'pythia8PSweightsSettings',
                                    'processParameters',
                                    )
    ),
    #RandomizedParameters = cms.VPSet()
)
'''
    return FRAGMENT
