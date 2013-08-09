import FWCore.ParameterSet.Config as cms

import HLTrigger.HLTfilters.hltHighLevel_cfi


processNameData = "HLT";
processNameMC = "REDIGI311X"

HLTFilterMu = cms.EDFilter('SingleTopTriggers',
                           HLTriggerResults = cms.InputTag("TriggerResults","",processNameData),
                           isMC = cms.untracked.bool(False),
                           triggerList = cms.vstring("HLT_IsoMu17_v",
                                                     ),
                           runRangesList = cms.vint32(-1),
                           
                           channel = cms.untracked.int32(2),#Useless now
                           )                         

HLTFilterEle = cms.EDFilter('SingleTopTriggers',
                            HLTriggerResults = cms.InputTag("TriggerResults","",processNameData),
                            isMC = cms.untracked.bool(False),
                            triggerList = cms.vstring("HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v",
                                                      "HLT_Ele25_CaloIdVT_TrkIdT_CentralJet30_BTagIP_v",
                                                      "HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_CentralJet30_BTagIP_v",
                                                      ),
                            runRangesList = cms.vint32(160404,163869,165970),

                            channel = cms.untracked.int32(3),#Useless now
                            )

HLTFilterMuOrEleMC = cms.EDFilter('SingleTopTriggers',
                                  HLTriggerResults = cms.InputTag("TriggerResults","",processNameMC),
                                  isMC = cms.untracked.bool(False),
                                  triggerList = cms.vstring("HLT_Ele22_SW_TighterCaloIdIsol_L1R_v",
                                                            "HLT_Ele17_SW_TighterEleIdIsol_L1R_v",
                                                               "HLT_IsoMu17_v",),
                                  runRangesList = cms.vint32(-1,-1,-1),
                                  
                                  channel = cms.untracked.int32(1),#Useless now
                                  )                         

HLTFilterMuQCD = cms.EDFilter('SingleTopTriggers',
                           HLTriggerResults = cms.InputTag("TriggerResults","",processNameData),
                           isMC = cms.untracked.bool(False),
                           triggerList = cms.vstring("HLT_Mu15_v",
                                                     ),
                           runRangesList = cms.vint32(-1),

                           channel = cms.untracked.int32(4),#Useless now
                           )                         

HLTFilterEleQCD = cms.EDFilter('SingleTopTriggers',
                               HLTriggerResults = cms.InputTag("TriggerResults","",processNameData),
                               isMC = cms.untracked.bool(False),
                               triggerList = cms.vstring("HLT_Ele25_CaloIdVT_TrkIdT_CentralJet30_v",
                                                         ),
                               runRangesList = cms.vint32(-1),
                               channel = cms.untracked.int32(5),#Useless now
                            )

####################
HLTFilterMuOrEle = cms.EDFilter('SingleTopTriggers',
                                HLTriggerResults = cms.InputTag("TriggerResults","",processNameData),
                                isMC = cms.untracked.bool(False),
                                triggerList = cms.vstring("HLT_IsoMu17_v",   
                                                          "HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v"),    
                                runRangesList = cms.vint32(-1),
                                
                                channel = cms.untracked.int32(1),#Useless now
                                )                         



