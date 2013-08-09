import FWCore.ParameterSet.Config as cms

process = cms.Process("SingleTopSkimMerge")

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.source = cms.Source ("PoolSource",
                             fileNames = cms.untracked.vstring (
#'rfio:/castor/cern.ch/user/o/oiorio/SingleTop/SingleTop_tChan/TChanSampleTChanMu_9_1_S3X.root',
#    'file:/tmp/oiorio/00012F91-72E5-DF11-A763-00261834B5F1.root'

'file:/tmp/oiorio/FE4EF257-A3AB-E011-9698-00304867915A.root',
'file:/tmp/oiorio/50A31B1A-8AAB-E011-835B-0026189438F5.root'
#'file:/tmp/oiorio/WJetsSmallFile_1_1_nb1.root',
#'file:/tmp/oiorio/00012F91-72E5-DF11-A763-00261834B5F1.root',
),
eventsToProcess = cms.untracked.VEventRange('1:2807840-1:2807840'),
duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
#skipBadFiles = cms.untracked.bool(True),
)



## Load additional RECO config
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff") ### real data
process.GlobalTag.globaltag = cms.string('START42_V13::All')


process.skimwall = cms.OutputModule("PoolOutputModule",
                                    fileName = cms.untracked.string('OneEvent.root'),
                                    outputCommands = cms.untracked.vstring(    'keep *',   )
)
#process.source.fileNames = TChannel_ntuple
#process.skimwall.fileName = "/tmp/oiorio/TChannelMerged.root"
#process.skimwall.fileName = "/castor/cern.ch/user/o/oiorio/SingleTop/2011/MC2011/NewNtuples/Merged/TChannelMerged.root"

#Save the skims
#process.outpath = cms.EndPath( process.skimlight + process.skimwcc + process.skimwbb )
process.outpath = cms.EndPath( process.skimwall)
