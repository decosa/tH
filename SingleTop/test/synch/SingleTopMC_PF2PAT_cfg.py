import FWCore.ParameterSet.Config as cms

process = cms.Process("SingleTop")



process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
    FailPath = cms.untracked.vstring('ProductNotFound','Type Mismatch')
    )

process.MessageLogger.cerr.FwkReport.reportEvery = 10

#from PhysicsTools.PatAlgos.tools.cmsswVersionTools import run36xOn35xInput


# conditions ------------------------------------------------------------------

print "test "

#process.load("Configuration.StandardSequences.MixingNoPileUp_cff")
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff") ### real data
process.GlobalTag.globaltag = cms.string('START42_V17::All')
#process.GlobalTag.globaltag = cms.string('START42_V13::All')
#process.GlobalTag.globaltag = cms.string('START311_V2::All')

#from Configuration.PyReleaseValidation.autoCond import autoCond
#process.GlobalTag.globaltag = autoCond['startup']
process.load("TopQuarkAnalysis.SingleTop.SingleTopSequences_cff") 

process.load("SelectionCuts_Skim_cff");################<----------

#From <<ysicsTools.PatAlgos.tools.cmsswVersionTools import *
#larlaun42xOn3yzMcInput(process)
#run36xOn35xInput(process)


# Get a list of good primary vertices, in 42x, these are DAF vertices
from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector
process.goodOfflinePrimaryVertices = cms.EDFilter(
    "PrimaryVertexObjectFilter",
    filterParams = pvSelector.clone( minNdof = cms.double(4.0), maxZ = cms.double(24.0) ),
    src=cms.InputTag('offlinePrimaryVertices')
    )

# require physics declared
process.load('HLTrigger.special.hltPhysicsDeclared_cfi')
process.hltPhysicsDeclared.L1GtReadoutRecordTag = 'gtDigis'

#dummy output

process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('dummy.root'),
                               outputCommands = cms.untracked.vstring(""),
                               )

#rocess.load("PhysicsTools.HepMCCandAlgos.flavorHistoryPaths_cfi")

#mytrigs=["HLT_Mu9"]
mytrigs=["*"]

from HLTrigger.HLTfilters.hltHighLevel_cfi import *
#if mytrigs is not None :
#    process.hltSelection = hltHighLevel.clone(TriggerResultsTag = 'TriggerResults::HLT', HLTPaths = mytrigs)
#    process.hltSelection.throw = False

#
#    getattr(process,"pfNoElectron"+postfix)*process.kt6PFJets 

                                 

# set the dB to the beamspot
process.patMuons.usePV = cms.bool(False)
process.patElectrons.usePV = cms.bool(False)

#inputJetCorrLabel = ('AK5PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'])

# Configure PAT to use PF2PAT instead of AOD sources
# this function will modify the PAT sequences. It is currently 
# not possible to run PF2PAT+PAT and standart PAT at the same time
from PhysicsTools.PatAlgos.tools.pfTools import *
postfix = ""
#usePF2PAT(process,runPF2PAT=True, jetAlgo='AK5', runOnMC=True, postfix=postfix, jetCorrections = inputJetCorrLabel)
usePF2PAT(process,runPF2PAT=True, jetAlgo='AK5', runOnMC=True, postfix=postfix)
process.pfPileUp.Enable = True
process.pfPileUp.checkClosestZVertex = cms.bool(False)
process.pfPileUp.Vertices = cms.InputTag('goodOfflinePrimaryVertices')
process.pfJets.doAreaFastjet = True
process.pfJets.doRhoFastjet = False
#process.pfJets.Rho_EtaMax =  cms.double(4.4)


#Compute the mean pt per unit area (rho) from the
#PFchs inputs
from RecoJets.JetProducers.kt4PFJets_cfi import kt4PFJets
process.kt6PFJets = kt4PFJets.clone(
    rParam = cms.double(0.6),
    src = cms.InputTag('pfNoElectron'+postfix),
    doAreaFastjet = cms.bool(True),
    doRhoFastjet = cms.bool(True),
#    voronoiRfact = cms.double(0.9),
#    Rho_EtaMax =  cms.double(4.4)
    )
process.patJetCorrFactors.rho = cms.InputTag("kt6PFJets", "rho")

coneOpening = cms.double(0.4)
defaultIsolationCut = cms.double(0.2)

#coneOpening = process.coneOpening
#defaultIsolationCut = process.coneOpening


#Muons
applyPostfix(process,"isoValMuonWithNeutral",postfix).deposits[0].deltaR = coneOpening
applyPostfix(process,"isoValMuonWithCharged",postfix).deposits[0].deltaR = coneOpening
applyPostfix(process,"isoValMuonWithPhotons",postfix).deposits[0].deltaR = coneOpening
#electrons
applyPostfix(process,"isoValElectronWithNeutral",postfix).deposits[0].deltaR = coneOpening
applyPostfix(process,"isoValElectronWithCharged",postfix).deposits[0].deltaR = coneOpening
applyPostfix(process,"isoValElectronWithPhotons",postfix).deposits[0].deltaR = coneOpening

applyPostfix(process,"pfIsolatedMuons",postfix).combinedIsolationCut = defaultIsolationCut
applyPostfix(process,"pfIsolatedElectrons",postfix).combinedIsolationCut = defaultIsolationCut

#applyPostfix(process,"pfIsolatedMuons",postfix).combinedIsolationCut = cms.double(0.125)
#applyPostfix(process,"pfIsolatedElectrons",postfix).combinedIsolationCut = cms.double(0.125)

#postfixQCD = "ZeroIso"



# Add the PV selector and KT6 producer to the sequence
getattr(process,"patPF2PATSequence"+postfix).replace(
    getattr(process,"pfNoElectron"+postfix),
    getattr(process,"pfNoElectron"+postfix)*process.kt6PFJets )

#Residuals (Data)
#process.patPFJetMETtype1p2Corr.jetCorrLabel = 'L2L3Residual'
process.patseq = cms.Sequence(
#   process.patElectronIDs +
    process.goodOfflinePrimaryVertices *
    process.patElectronIDs *
    getattr(process,"patPF2PATSequence"+postfix) #*
#   process.producePatPFMETCorrections
#   getattr(process,"patPF2PATSequence"+postfixQCD) 
    )





process.pfIsolatedMuonsZeroIso = process.pfIsolatedMuons.clone(combinedIsolationCut =  cms.double(float("inf")))
process.patMuonsZeroIso = process.patMuons.clone(pfMuonSource = cms.InputTag("pfIsolatedMuonsZeroIso"), genParticleMatch = cms.InputTag("muonMatchZeroIso"))
# use pf isolation, but do not change matching
tmp = process.muonMatch.src
adaptPFMuons(process, process.patMuonsZeroIso, "")
process.muonMatch.src = tmp
process.muonMatchZeroIso = process.muonMatch.clone(src = cms.InputTag("pfIsolatedMuonsZeroIso"))

process.pfIsolatedElectronsZeroIso = process.pfIsolatedElectrons.clone(combinedIsolationCut = cms.double(float("inf")))
process.patElectronsZeroIso = process.patElectrons.clone(pfElectronSource = cms.InputTag("pfIsolatedElectronsZeroIso"))

#####################
#Adaptpfelectrons (process, process.patElectronsZeroIso, "")

#Add the PF type 1 corrections to MET
process.load("PhysicsTools.PatUtils.patPFMETCorrections_cff")
process.selectedPatJetsForMETtype1p2Corr.src = cms.InputTag('selectedPatJets')
process.selectedPatJetsForMETtype2Corr.src = cms.InputTag('selectedPatJets')
process.patPFJetMETtype1p2Corr.type1JetPtThreshold = cms.double(10.0)
process.patPFJetMETtype1p2Corr.skipEM = cms.bool(False)
process.patPFJetMETtype1p2Corr.skipMuons = cms.bool(False)

#process.patPF2PATSequence.remove(process.patPF2PATSequence.FastjetJetProducer)

process.pathPreselection = cms.Path(
        process.patseq +  process.producePatPFMETCorrections
        )


process.ZeroIsoLeptonSequence = cms.Path(
         process.pfIsolatedMuonsZeroIso +
         process.muonMatchZeroIso +
         process.patMuonsZeroIso +
         process.pfIsolatedElectronsZeroIso +
         process.patElectronsZeroIso
         )


#process.looseLeptonSequence.remove(process.muonMatchLoose)


#getattr(process,"pfNoPileUp"+postfix).enable = True
#getattr(process,"pfNoMuon"+postfix).enable = True
#getattr(process,"pfNoElectron"+postfix).enable = True
#getattr(process,"pfNoTau"+postfix).enable = False
#Getattr (process,"pfNoJet"+postfix).enable = True 

process.pfNoTau.enable = False

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(502) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.source = cms.Source ("PoolSource",
                             fileNames = cms.untracked.vstring (
'file:/tmp/oiorio/FE4EF257-A3AB-E011-9698-00304867915A.root',
'file:/tmp/oiorio/50A31B1A-8AAB-E011-835B-0026189438F5.root'
#'file:/tmp/oiorio/TTJetsLocalFall11.root',
#'file:/tmp/oiorio/',
#'file:/tmp/oiorio/00012F91-72E5-DF11-A763-00261834B5F1.root',
),
#eventsToProcess = cms.untracked.VEventRange('1:2807840-1:2807840'),
duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
)

ChannelName = "SyncTest2";

#process.TFileService = cms.Service("TFileService", fileName = cms.string("/tmp/oiorio/"+ChannelName+"_pt_bmode.root"))
process.TFileService = cms.Service("TFileService", fileName = cms.string("pileupdistr_"+ChannelName+".root"))

process.pileUpDumper = cms.EDAnalyzer("SingleTopPileUpDumper",
                                      channel = cms.string(ChannelName),
                                      )

#process.WLightFilter = process.flavorHistoryFilter.clone(pathToSelect = cms.int32(11))
#process.WccFlter = process.flavorHistoryFilter.clone(pathToSelect = cms.int32(6))
#process.WbbFilter = process.flavorHistoryFilter.clone(pathToSelect = cms.int32(5))

#process.hltFilter.TriggerResultsTag = cms.InputTag("TriggerResults","","REDIGI38X")
#process.hltFilter.TriggerResultsTag = cms.InputTag("TriggerResults","","REDIGI37X")
#process.hltFilter.TriggerResultsTag = cms.InputTag("TriggerResults","","REDIGI")
#process.hltFilter.TriggerResultsTag = cms.InputTag("TriggerResults","","REDIGI311X")
#process.hltFilter.TriggerResultsTag = cms.InputTag("TriggerResults","","HLT")
process.hltFilter.TriggerResultsTag = cms.InputTag("TriggerResults","","HLT")
process.hltFilter.HLTPaths = mytrigs
    
    
#process.countLeptons.doQCD = cms.untracked.bool(False)

process.baseLeptonSequence = cms.Path(
#    process.pileUpDumper +
    process.basePath 
    )
    
process.selection = cms.Path (
    process.preselection +
    process.nTuplesSkim
    )
   
        
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import saveNTuplesSkimLoose
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import saveNTuplesSkimMu
    
savePatTupleSkimLoose = cms.untracked.vstring(
    'drop *',

    'keep patMuons_selectedPatMuons_*_*',
    'keep patElectrons_selectedPatElectrons_*_*',
    'keep patJets_selectedPatJets_*_*',
    'keep patMETs_patMETs_*_*',
    'keep *_patPFMet_*_*',
    'keep *_patType1CorrectedPFMet_*_*',
    'keep *_PVFilterProducer_*_*',

    'keep *_pfJets_*_*',
    'keep patJets_topJetsPF_*_*',
    'keep patMuons_looseMuons_*_*',
    'keep patElectrons_looseElectrons_*_*',
    'keep patMuons_tightMuons_*_*',
    'keep patElectrons_tightElectrons_*_*',

    'keep *_PDFInfo_*_*',

    'keep *_patElectronsZeroIso_*_*',
    'keep *_patMuonsZeroIso_*_*',
    'keep *_kt6PFJets_*_*',

    'keep *_PVFilterProducer_*_*',
    
    'keep *_cFlavorHistoryProducer_*_*',
    'keep *_bFlavorHistoryProducer_*_*',
    )

## Output module configuration
process.singleTopNTuple = cms.OutputModule("PoolOutputModule",
#                                fileName = cms.untracked.string('rfio:/CST/cern.ch/user/o/oiorio/SingleTop/SubSkims/WControlSamples1.root'),
#                   fileName = cms.untracked.Bstring('/tmp/oiorio/edmntuple_tchannel_big.root'),
                   fileName = cms.untracked.string('/tmp/oiorio/edmntuple_'+ChannelName+'.root'),
                   SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('selection')),
                   outputCommands = saveNTuplesSkimLoose,
)

process.singleTopPatTuple = cms.OutputModule("PoolOutputModule",
#                                fileName = cms.untracked.string('rfio:/CST/cern.ch/user/o/oiorio/SingleTop/SubSkims/WControlSamples1.root'),
                   fileName = cms.untracked.string('/tmp/oiorio/pattuple_'+ChannelName+'.root'),


#                   SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('selection')),
                   outputCommands = savePatTupleSkimLoose
)
process.singleTopNTuple.dropMetaData = cms.untracked.string("ALL")

process.outpath = cms.EndPath(
    process.singleTopNTuple +
    process.singleTopPatTuple 
    )

