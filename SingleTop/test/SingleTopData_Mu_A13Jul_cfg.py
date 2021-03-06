import FWCore.ParameterSet.Config as cms

#Process name:
process = cms.Process("SingleTop")

#Messagelogger options:
process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
    FailPath = cms.untracked.vstring('ProductNotFound','Type Mismatch')
    )

#Geometry:
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff") ### real data

#Name to be used in the output files:
ChannelName = "Mu_A13Jul"

#Data or MC:
#isData = False
isData = True

#Tag:
process.GlobalTag.globaltag = cms.string('FT_53_V6C_AN3::All')

#Single top and pat sequences:
process.load("tH.SingleTop.SingleTopSequences_cff") 
process.load("SelectionCuts_Skim_cff")################<----------Cuts file
process.load("PhysicsTools.PatAlgos.patSequences_cff") 

#Trigger filter to be eventually used:
import HLTrigger.HLTfilters.triggerResultsFilter_cfi as triggerFilter

process.HLTFilterMu2012  = triggerFilter.triggerResultsFilter.clone(
    hltResults = cms.InputTag( "TriggerResults","","HLT" ),
   triggerConditions = ["HLT_*"],#All trigger paths are included in the skim
#   triggerConditions = ["HLT_IsoMu24_eta2p1_v*"],
#   triggerConditions = ["HLT_Ele27_WP80_v*"],
    l1tResults = '',
    throw = False
    )

process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('dummy.root'),
                               outputCommands = cms.untracked.vstring(""),
                               )

process.goodOfflinePrimaryVertices = cms.EDFilter( "PrimaryVertexObjectFilter" ,
                                                   filterParams = cms.PSet( minNdof = cms.double( 4. ) , maxZ = cms.double( 24. ) , maxRho = cms.double( 2. ) ) ,
                                                   filter = cms.bool( True) , src = cms.InputTag( 'offlinePrimaryVertices' ) )

process.patElectrons.addElectronID = cms.bool(True)
process.patElectrons.electronIDSources = process.electronIDSources

postfix = ""

# Configure PAT to use PF2PAT instead of AOD sources:
from PhysicsTools.PatAlgos.tools.pfTools import *
from PhysicsTools.PatAlgos.tools.trigTools import *
from PhysicsTools.PatUtils.tools.metUncertaintyTools import *
Postfix = ""
runOnMC = (not isData)
jetAlgoName = "AK5"
usePF2PAT(process, runPF2PAT=True, jetAlgo=jetAlgoName, runOnMC=runOnMC, postfix=Postfix, jetCorrections=('AK5PFchs',['L1FastJet','L2Relative','L3Absolute','L2L3Residual']), pvCollection=cms.InputTag('goodOfflinePrimaryVertices'),  typeIMetCorrections=True, outputModules = None)

#Trigger matching:
switchOnTriggerMatchEmbedding(process,triggerMatchers = ['PatMuonTriggerMatchHLTIsoMu24','PatJetTriggerMatchHLTIsoMuBTagIP'])

#PF no Pileup:
process.pfPileUp.Enable = True
process.load("CMGTools.External.pujetidsequence_cff")

process.pfPileUp.checkClosestZVertex = cms.bool(False)

#Use DR = 0.3 for electrons:
process.pfIsolatedElectrons.isolationValueMapsCharged = cms.VInputTag(cms.InputTag("elPFIsoValueCharged03PFId"))
process.pfIsolatedElectrons.deltaBetaIsolationValueMap = cms.InputTag("elPFIsoValuePU03PFId")
process.pfIsolatedElectrons.isolationValueMapsNeutral = cms.VInputTag(cms.InputTag("elPFIsoValueNeutral03PFId"), cms.InputTag("elPFIsoValueGamma03PFId"))
process.patElectrons.isolationValues = cms.PSet( pfChargedHadrons = cms.InputTag("elPFIsoValueCharged03PFId"), pfChargedAll = cms.InputTag("elPFIsoValueChargedAll03PFId"), pfPUChargedHadrons = cms.InputTag("elPFIsoValuePU03PFId"), pfNeutralHadrons = cms.InputTag("elPFIsoValueNeutral03PFId"), pfPhotons = cms.InputTag("elPFIsoValueGamma03PFId") )

#Define the PAT sequences:
process.patseq = cms.Sequence(
    process.goodOfflinePrimaryVertices *
    process.patElectronIDs *
    getattr(process,"patPF2PATSequence"+postfix) #+process.triggerMatchingSequence
    )

process.topMETsPF.metsSrc = cms.InputTag("patMETs")
process.topMETsPF.isData = isData
process.topJetsPF.isData = isData

#Define anti-isolated muons/electrons:

#Muons:
process.pfIsolatedMuonsZeroIso = process.pfIsolatedMuons.clone(combinedIsolationCut =  cms.double(float("inf")),
                                                               isolationCut =  cms.double(float("inf")),
                                                               )
from tH.SingleTop.AdaptPFMuonsFix_cff import adaptPFMuonsAnd

process.patMuonsZeroIso = process.patMuons.clone(pfMuonSource = cms.InputTag("pfIsolatedMuonsZeroIso"))
process.patMuonsZeroIso.pfMuonSource = cms.InputTag("pfIsolatedMuonsZeroIso")

#Electrons
process.pfIsolatedElectronsZeroIso = process.pfIsolatedElectrons.clone(combinedIsolationCut = cms.double(float("inf")),
                                                                       isolationCut =  cms.double(float("inf")),
                                                                       )
process.patElectronsZeroIso = process.patElectrons.clone(pfElectronSource = cms.InputTag("pfIsolatedElectronsZeroIso"))

#Define anti-isolated leptons sequence:
process.ZeroIsoLeptonSequence = cms.Sequence(
         process.pfIsolatedMuonsZeroIso +
         process.patMuonsZeroIso +
         process.pfIsolatedElectronsZeroIso +
         process.patElectronsZeroIso
         )

#Set max number of events:
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(300) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

#Input file:
process.source = cms.Source ("PoolSource",
                             fileNames = cms.untracked.vstring (
    "file:/afs/cern.ch/work/o/oiorio/public/xFrancescoFab/DataReRecoA.root"
),
duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
)

# path for preselection:
process.pathPreselection = cms.Path (
    process.HLTFilterMu2012 *
    process.goodOfflinePrimaryVertices 
    )

#Path for the final skim selection:
process.pathSelection = cms.Path(
    process.HLTFilterMu2012 *
    process.patseq + process.puJetIdSqeuence + process.puJetIdSqeuenceChs *
    process.ZeroIsoLeptonSequence *
    process.basePathData +
    process.preselectionData + 
    process.nTuplesSkim 
    )

#Add MC Truth information: 
doMCTruth = True 
if isData: doMCTruth = False  

from tH.SingleTop.SingleTopNtuplizers_cff import saveNTuplesSkimLoose
from tH.SingleTop.SingleTopNtuplizers_cff import saveNTuplesSkimMu

#Objects included in the pat-tuples
savePatTupleSkimLoose = cms.untracked.vstring(
    'drop *',

    'keep patMuons_selectedPatMuons_*_*',
    'keep patMuons_selectedPatMuonsTriggerMatch_*_*',
    'keep patJets_selectedPatJetsTriggerMatch_*_*',

    'keep patElectrons_selectedPatElectrons_*_*',
    'keep patJets_selectedPatJets_*_*',
    'keep patMETs_patMETs_*_*',
#    'keep *_patPFMet_*_*',
#    'keep *_patType1CorrectedPFMet_*_*',
#    'keep *_PVFilterProducer_*_*',

#    'keep *_kt6PFJetsForIsolation_rho_*',
    'keep *_kt6PFJets_rho_*',

    'keep patJets_topJetsPF_*_*',
    'keep patMuons_vetoMuons_*_*',
    'keep *_vetoElectrons_*_*',
    'keep patMuons_tightMuons_*_*',
    'keep patMuons_tightMuonsTest_*_*',
    'keep *_tightElectrons_*_*',

    "keep *_TriggerResults_*_*",#Trigger results
    "keep *_PatMuonTriggerMatchHLTIsoMu24_*_*",#Trigger matches
#    "keep *_patTrigger_*_*",
#    "keep *_patTriggerEvent_*_*",

    'keep *_PDFInfo_*_*',

    'keep *_patElectronsZeroIso_*_*',
    'keep *_patMuonsZeroIso_*_*',
#    'keep *_kt6PFJetsCentral_*_*',
#    'keep *_PVFilterProducer_*_*',
    
#    "keep *_puJetId_*_*", # input variables
#    "keep *_puJetMva_*_*", # final MVAs and working point flags
#    "keep *_puJetIdChs_*_*", # input variables
#    "keep *_puJetMvaChs_*_*", # final MVAs and working point flags

#    'keep *_pfNoMuon_*_*',
#    'keep *_pfIsolatedElectrons_*_*',
#    'keep *_pfNoElectron_*_*',
#    'keep *_pfNoTau_*_*',
#    'keep *_pfTaus_*_*',
#    'keep *_pfNoTau_*_*',
#    'keep *_pfJets_*_*',

    )




#print " test 5 " 

#doMCTruth= False
if doMCTruth:
    process.MCTruth = cms.Path (
        process.HLTFilterMu2012 *
        process.MCTruthParticles
        + process.nTuplesSkimMCTruth
        )
    
    savePatTupleSkimLoose.append('keep *_MCTruthParticles_*_*')

    saveNTuplesSkimLoose.append('keep  floats_MCTruthParticles_*_*')
    saveNTuplesSkimLoose.append('keep  ints_MCTruthParticles_*_*')
    saveNTuplesSkimLoose.append('keep  floats_singleTopMCLeptons_*_*')
    saveNTuplesSkimLoose.append('keep  floats_singleTopMCQuarks_*_*')
    saveNTuplesSkimLoose.append('keep  floats_singleTopMCNeutrinos_*_*')
    saveNTuplesSkimLoose.append('keep  floats_singleTopMCBQuarks_*_*')
    saveNTuplesSkimLoose.append('keep  floats_singleTopMCTops_*_*')
    saveNTuplesSkimLoose.append('keep  floats_singleTopMCTopsW_*_*')
    saveNTuplesSkimLoose.append('keep  floats_singleTopMCTopsBQuark_*_*')
    saveNTuplesSkimLoose.append('keep  floats_singleTopMCTopsLepton_*_*')
    saveNTuplesSkimLoose.append('keep  floats_singleTopMCTopsNeutrino_*_*')
    saveNTuplesSkimLoose.append('keep  floats_singleTopMCTopsQuark_*_*')
    saveNTuplesSkimLoose.append('keep  floats_singleTopMCTopsQuarkBar_*_*')

## Output module configuration
process.singleTopNTuple = cms.OutputModule("PoolOutputModule",
                   fileName = cms.untracked.string('edmntuple_'+ChannelName+'.root'),
#                   fileName = cms.untracked.string('edmntuple_ele'+ChannelName+'.root'),
                   SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('pathSelection')),
#                   SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('pathPreselection')),
                   outputCommands = saveNTuplesSkimLoose,
)

process.singleTopPatTuple = cms.OutputModule("PoolOutputModule",
                   fileName = cms.untracked.string('pattuple_'+ChannelName+'.root'),

                   SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('pathSelection')),
                   outputCommands = savePatTupleSkimLoose
                                             )
process.singleTopNTuple.dropMetaData = cms.untracked.string("ALL")
process.singleTopPatTuple.dropMetaData = cms.untracked.string("ALL")

process.outpath = cms.EndPath(
    process.singleTopNTuple +
    process.singleTopPatTuple 
    )

