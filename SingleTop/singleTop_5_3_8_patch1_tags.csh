cd ../../
cvs co -r V00-10-10-06   DPGAnalysis/SiStripTools                         
cvs co -r V01-00-11-01   DPGAnalysis/Skims                                
cvs co -r V06-05-06-07   DataFormats/PatCandidates                        
cvs co -r V00-02-14      DataFormats/StdDictionaries                      
cvs co -r V00-00-08      DataFormats/TrackerCommon                        
cvs co -r V00-00-70      FWCore/GuiBrowsers                               
cvs co -r V08-09-52      PhysicsTools/PatAlgos                            
cvs co -r V03-09-28      PhysicsTools/PatUtils                            
cvs co -r V01-09-05      RecoLocalTracker/SubCollectionProducers          
cvs co -r V00-00-08      RecoMET/METAnalyzers                             
cvs co -r V00-00-13      RecoMET/METFilters                               
cvs co -r V03-03-12-02   RecoMET/METProducers                             
cvs co -r V15-02-06      RecoParticleFlow/PFProducer     
cvs co -r V00-00-31-EA02   -d EGamma/EGammaAnalysisTools UserCode/EGamma/EGammaAnalysisTools
cd EGamma/EGammaAnalysisTools/data
cat download.url | xargs wget                      

cd ../../../

cvs co -r V00-02-05 -d CMGTools/External UserCode/CMG/CMGTools/External

#cp TopQuarkAnalysis/SingleTop/python/pfIsolation_fix.py CommonTools/ParticleFlow/python/Tools/pfIsolation.py

#cp TopQuarkAnalysis/SingleTop/test/lhapdfwrapnew.xml $CMSSW_BASE/config/toolbox/$SCRAM_ARCH/tools/selected/lhapdfwrap.xml
#cp TopQuarkAnalysis/SingleTop/test/lhapdfnew.xml $CMSSW_BASE/config/toolbox/$SCRAM_ARCH/tools/selected/lhapdf.xml
#cp TopQuarkAnalysis/SingleTop/test/lhapdffullnew.xml $CMSSW_BASE/config/toolbox/$SCRAM_ARCH/tools/selected/lhapdffull.xml

cmsenv
scram setup lhapdffull
cmsenv

scram b -j 9 > & step1.log &
