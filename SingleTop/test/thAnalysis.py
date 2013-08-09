import ROOT
import sys
from DataFormats.FWLite import Events, Handle


#from FWCore.ParameterSet.VarParsing import VarParsing
#options = VarParsing ('python')
#options.parseArguments()

#ROOT.gSystem.Load("libFWCoreFWLite.so");
#ROOT.AutoLibraryLoader.enable();
#ROOT.gSystem.Load("libDataFormatsFWLite.so");

events = Events("singleTopEdmNtuple_TChannel.root")

hAllmuPt  = Handle ("std::vector<float>")
labelAllmuPt = ("nTupleAllMuons","allMuonsPt")



for event in events:
    event.getByLabel(labelAllmuPt, hAllmuPt)



    
    if hAllmuPt.isValid():
        muonsPt = hAllmuPt.product()
        numMuons = len (muonsPt)
        print numMuons

    else:
        print "object ", labelAllmuPt, "not found!"
    # get the product
    

