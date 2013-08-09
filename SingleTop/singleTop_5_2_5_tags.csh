cd ../../
addpkg DataFormats/PatCandidates V06-05-01
addpkg PhysicsTools/PatAlgos V08-09-11-02
addpkg CommonTools/ParticleFlow V00-03-14
addpkg JetMETCorrections/Type1MET V04-06-05
addpkg PhysicsTools/PatUtils V03-09-22
addpkg CommonTools/RecoUtils V00-00-09
cvs co -r V00-00-08      -d EGamma/EGammaAnalysisTools UserCode/EGamma/EGammaAnalysisTools
cd EGamma/EGammaAnalysisTools/data
cat download.url | xargs wget                      

cd ../../../

cvs co -r V00-02-05 -d CMGTools/External UserCode/CMG/CMGTools/External

cp TopQuarkAnalysis/SingleTop/python/pfIsolation_fix.py CommonTools/ParticleFlow/python/Tools/pfIsolation.py



#cp TopQuarkAnalysis/SingleTop/test/lhapdfwrapnew.xml $CMSSW_BASE/config/toolbox/$SCRAM_ARCH/tools/selected/lhapdfwrap.xml
#cp TopQuarkAnalysis/SingleTop/test/lhapdfnew.xml $CMSSW_BASE/config/toolbox/$SCRAM_ARCH/tools/selected/lhapdf.xml
#cp TopQuarkAnalysis/SingleTop/test/lhapdffullnew.xml $CMSSW_BASE/config/toolbox/$SCRAM_ARCH/tools/selected/lhapdffull.xml

cmsenv
scram setup lhapdffull
cmsenv

scram b -j 9 > & step1.log &
