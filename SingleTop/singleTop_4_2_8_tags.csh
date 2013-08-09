cd ../../

cvs co -r V06-04-19-01 DataFormats/PatCandidates
cvs co -r V08-06-42 PhysicsTools/PatAlgos
cvs co -r V00-05-24 PhysicsTools/PatExamples
cvs co -r V00-03-24 PhysicsTools/SelectorUtils
cvs co -r V08-02-14 PhysicsTools/UtilAlgos
cvs co -r V08-03-10 PhysicsTools/Utilities
cvs co -r V00-04-11 RecoBTag/PerformanceDB
cvs co -r V00-03-31 RecoEgamma/ElectronIdentification
cvs co -r V03-03-05 RecoLuminosity/LumiDB
cvs co -r V04-05-07 JetMETCorrections/Type1MET
cvs co -r b4_2_X_cvMEtCorr_30Nov11 PhysicsTools/PatUtils
cvs co -r V03-03-07 DataFormats/METReco

cp ~oiorio/public/xMario/Lumi3DReWeighting.h PhysicsTools/Utilities/interface/Lumi3DReWeighting.h
cp ~oiorio/public/xMario/Lumi3DReWeighting.cc PhysicsTools/Utilities/src/Lumi3DReWeighting.cc

cp TopQuarkAnalysis/SingleTop/test/lhapdfwrapnew.xml $CMSSW_BASE/config/toolbox/$SCRAM_ARCH/tools/selected/lhapdfwrap.xml
cp TopQuarkAnalysis/SingleTop/test/lhapdfnew.xml $CMSSW_BASE/config/toolbox/$SCRAM_ARCH/tools/selected/lhapdf.xml
cp TopQuarkAnalysis/SingleTop/test/lhapdffullnew.xml $CMSSW_BASE/config/toolbox/$SCRAM_ARCH/tools/selected/lhapdffull.xml

cmsenv
scram setup lhapdffull
cmsenv

scram b -j 9 > & step1.log 

cvs co -r V02-03-00 JetMETCorrections/Algorithms
rm -f JetMETCorrections/Algorithms/interface/L1JPTOffsetCorrector.h
rm -f JetMETCorrections/Algorithms/src/L1JPTOffsetCorrector.cc
cvs co -r V03-01-00 JetMETCorrections/Objects
addpkg JetMETCorrections/Modules
cvs up -r 1.4 JetMETCorrections/Modules/plugins/JetCorrectorOnTheFly.cc
cvs up -r 1.6 JetMETCorrections/Modules/interface/JetCorrectionProducer.h
cvs co -r $CMSSW_VERSION PhysicsTools/PatAlgos
cvs up -r 1.64.2.4 PhysicsTools/PatAlgos/python/tools/jetTools.py


scram b -j 9 > & step2.log &

