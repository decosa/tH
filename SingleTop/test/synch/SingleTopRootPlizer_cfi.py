import FWCore.ParameterSet.Config as cms

TreesEle = cms.EDAnalyzer('SingleTopSystematicsTreesDumper',                              
#General Info
#systematics = cms.untracked.vstring("BTagUp","BTagDown","MisTagUp","MisTagDown","JESUp","JESDown","UnclusteredMETUp","UnclusteredMETDown","PUUp","PUDown"),
systematics = cms.untracked.vstring("JESUp","JESDown","UnclusteredMETUp","UnclusteredMETDown"),
#systematics = cms.untracked.vstring("JESUp","JESDown","UnclusteredMETUp","UnclusteredMETDown"),
#systematics = cms.untracked.vstring(""),
doBScan = cms.untracked.bool(True),
rateSystematics = cms.untracked.vstring("WLightRateUp",                                        "WLightRateDown",                                        "TTBarRateUp",                                        "Ttbarratedown ",                                        "WHFRateUp",                                        "WHFRateDown"),
#rateSystematics = cms.untracked.vstring(""),
doPU = cms.untracked.bool(True),
#doResol  = cms.untracked.bool(False),
doResol  = cms.untracked.bool(True),
#dataPUFile = cms.untracked.string("pileUpDistr.root"),
#mcPUFile = cms.untracked.string("pileupdistr_TChannel.root"),
#puHistoName = cms.untracked.string("pileUpDumper/PileUpTChannel"),
#mode = cms.untracked.string("pt"),
#maxPtCut = cms.untracked.double("45"),

#x1/x2
x1 = cms.InputTag("PDFInfo","x1"),
x2 = cms.InputTag("PDFInfo","x2"),
id1 = cms.InputTag("PDFInfo","id1"),
id2 = cms.InputTag("PDFInfo","id2"),
scalePDF = cms.InputTag("PDFInfo","scalePDF"),
doPDF =cms.untracked.bool(True),
takeBTagSFFromDB = cms.untracked.bool(False),

channelInfo = cms.PSet(
    crossSection = cms.untracked.double(20.93),
    channel = cms.untracked.string("TChannel"),
    originalEvents = cms.untracked.double(480000),
    finalLumi = cms.untracked.double(14.5),
    MTWCut = cms.untracked.double(50.0),#Default 50.0 GeV
    loosePtCut = cms.untracked.double(30.0),#Default 30.0 GeV
    RelIsoCut = cms.untracked.double(0.1),
    mcPUFile = cms.untracked.string("pileupdistr_TChannel.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpTChannel"),

    ),

#Leptons
leptonsEta = cms.InputTag("nTupleElectrons","tightElectronsEta"),  
leptonsPt = cms.InputTag("nTupleElectrons","tightElectronsPt"),  
leptonsPhi = cms.InputTag("nTupleElectrons","tightElectronsPhi"),  
leptonsEnergy = cms.InputTag("nTupleElectrons","tightElectronsE"),  
leptonsCharge = cms.InputTag("nTupleElectrons","tightElectronsCharge"),  
leptonsRelIso = cms.InputTag("nTupleElectrons","tightElectronsPFRelIso"),  
leptonsDB = cms.InputTag("nTupleElectrons","tightElectronsAbsoluteDB"),  
leptonsID = cms.InputTag("nTupleElectrons","tightElectronsSimpleEleId70cIso"),  

qcdLeptonsEta = cms.InputTag("nTupleElectrons","tightElectronsEta"),  
qcdLeptonsPt = cms.InputTag("nTupleElectrons","tightElectronsPt"),  
qcdLeptonsPhi = cms.InputTag("nTupleElectrons","tightElectronsPhi"),  
qcdLeptonsEnergy = cms.InputTag("nTupleElectrons","tightElectronsE"),  
qcdLeptonsCharge = cms.InputTag("nTupleElectrons","tightElectronsCharge"),  
qcdLeptonsRelIso = cms.InputTag("nTupleElectrons","tightElectronsPFRelIso"),  
qcdLeptonsDB = cms.InputTag("nTupleElectrons","tightElectronsAbsoluteDB"),  
qcdLeptonsID = cms.InputTag("nTupleElectrons","tightElectronsSimpleEleId70cIso"),  


looseElectronsRelIso = cms.InputTag("nTupleLooseElectrons","looseElectronsPFRelIso"),  
looseMuonsRelIso = cms.InputTag("nTupleLooseMuons","looseMuonsPFRelIso"),  

leptonsFlavour = cms.untracked.string("electron"),

#Jets

genJetsPt =cms.InputTag("genJetsPF","genJetsPt"),  
genJetsEta =cms.InputTag("genJetsPF","genJetsEta"),  
#genJetsPt =cms.InputTag("nTupleTopJetsPF","topJetsPFPt"),  
#genJetsEta =cms.InputTag("nTupleTopJetsPF","topJetsPFEta"),  

jetsPt = cms.InputTag("nTupleTopJetsPF","topJetsPFPt"),  
jetsPhi = cms.InputTag("nTupleTopJetsPF","topJetsPFPhi"),  
jetsEta = cms.InputTag("nTupleTopJetsPF","topJetsPFEta"),  
jetsEnergy = cms.InputTag("nTupleTopJetsPF","topJetsPFE"),  

jetsBTagAlgo = cms.InputTag("nTupleTopJetsPF","topJetsPFTrackCountingHighPur"),  
jetsAntiBTagAlgo =  cms.InputTag("nTupleTopJetsPF","topJetsPFTrackCountingHighEff"),  
jetsFlavour = cms.InputTag("nTupleTopJetsPF","topJetsPFFlavour"),   

jetsCorrTotal = cms.InputTag("nTupleTopJetsPF","topJetsPFJetCorrTotal"),   

#MET 

METPhi = cms.InputTag("nTuplePatMETsPF","patMETsPFPhi"),
METPt = cms.InputTag("nTuplePatMETsPF","patMETsPFPt"),

UnclusteredMETPx = cms.InputTag("UnclusteredMETPF","UnclusteredMETPx"),
UnclusteredMETPy = cms.InputTag("UnclusteredMETPF","UnclusteredMETPy"),

#Vertices

nVerticesPlus = cms.InputTag("NVertices","PileUpP1"),
nVerticesMinus = cms.InputTag("NVertices","PileUpM1"),
nVertices = cms.InputTag("NVertices","PileUp0"),

)


TreesMu = TreesEle.clone(

#Leptons
leptonsEta = cms.InputTag("nTupleMuons","tightMuonsEta"),  
leptonsPt = cms.InputTag("nTupleMuons","tightMuonsPt"),  
leptonsPhi = cms.InputTag("nTupleMuons","tightMuonsPhi"),  
leptonsEnergy = cms.InputTag("nTupleMuons","tightMuonsE"),  
leptonsCharge = cms.InputTag("nTupleMuons","tightMuonsCharge"),  
leptonsRelIso = cms.InputTag("nTupleMuons","tightMuonsPFRelIso"),  
leptonsDB = cms.InputTag("nTupleMuons","tightMuonsAbsoluteDB"),  
#leptonsID = cms.InputTag("nTupleMuons","tightMuonsSimpleEleId70cIso"),  

qcdLeptonsEta = cms.InputTag("nTupleMuons","tightMuonsEta"),  
qcdLeptonsPt = cms.InputTag("nTupleMuons","tightMuonsPt"),  
qcdLeptonsPhi = cms.InputTag("nTupleMuons","tightMuonsPhi"),  
qcdLeptonsEnergy = cms.InputTag("nTupleMuons","tightMuonsE"),  
qcdLeptonsCharge = cms.InputTag("nTupleMuons","tightMuonsCharge"),  
qcdLeptonsRelIso = cms.InputTag("nTupleMuons","tightMuonsPFRelIso"),  
qcdLeptonsDB = cms.InputTag("nTupleMuons","tightMuonsAbsoluteDB"),  
#qcdLeptonsID = cms.InputTag("nTupleMuons","tightMuonsSimpleEleId70cIso"),  

looseElectronsRelIso = cms.InputTag("nTupleLooseElectrons","looseElectronsPFRelIso"),  
looseMuonsRelIso = cms.InputTag("nTupleLooseMuons","looseMuonsPFRelIso"),  

leptonsFlavour = cms.untracked.string("muon"),

    channelInfo = cms.PSet(
        crossSection = cms.untracked.double(20.93),
        channel = cms.untracked.string("TChannel"),
        #    originalEvents = cms.untracked.double(14800000),
        originalEvents = cms.untracked.double(480000),
        finalLumi = cms.untracked.double(14.5),
        MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
        RelIsoCut = cms.untracked.double(0.05),
        ),

    
    )

