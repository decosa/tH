import time



import sys
sys.argv.append('-b')
import ROOT
import commands, os

ROOT.gROOT.Reset();
ROOT.gROOT.SetStyle('Plain')
ROOT.gStyle.SetPalette(1)
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch()        # don't pop up canvases
ROOT.TH1.SetDefaultSumw2()
ROOT.TH1.AddDirectory(False)
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.AutoLibraryLoader.enable();
ROOT.gSystem.Load("libDataFormatsFWLite.so");

c = ROOT.TCanvas()

debug = False

elcuts = ["(nTightEl == 1 && tightElectronsMvaTrigV0 > 0.5)",
        "nVetoMu == 0 ",
        "nVetoEl == 1 ",
        "(nJets >= 1)",
        "(nJets >= 2)",
        "(nJets >= 3)",
        "(nJets >= 4)"
        ]


mucuts = ["(nTightMu == 1 )",
        "nVetoMu == 1 ",
        "nVetoEl == 0 ",
        "(nJets >= 1)",
        "(nJets >= 2)",
        "(nJets >= 3)",
        "(nJets >= 4)"
        ]


def _cutFlow(t,cuts):
    cut = "1 "
    
    #start = time.time()
    for i in range(len(cuts)):
        cut += " && "
        cut += cuts[i]
        if(debug): print "CUT ----- ", cut
        print "Step " + str(i+1) + ": " + str(t.GetEntries(cut) )
    #stop = time.time()
    #print "Time: ", stop - start



def setAliases(t):
    t.SetAlias("nTightEl","floats_nTupleElectrons_tightElectronsE_SingleTop.@obj.size()")
    t.SetAlias("nTightMu","floats_nTupleMuons_tightMuonsE_SingleTop.@obj.size()")
    t.SetAlias("nVetoEl","floats_nTupleVetoElectrons_vetoElectronsE_SingleTop.@obj.size()")
    t.SetAlias("nVetoMu","floats_nTupleVetoMuons_vetoMuonsE_SingleTop.@obj.size()")
    t.SetAlias("nJets","floats_nTupleTopJetsPF_topJetsPFE_SingleTop.@obj.size()")


def doCutFlow(filename, cuts):

    file = ROOT.TFile(filename)
    t = file.Get("Events")
    nStep0 = t.GetEntries()
    print 'Step 0: ', nStep0
    setAliases(t)
    _cutFlow(t, cuts)
    #t.Draw("nJets", "(nTightMu == 1 ) && nVetoMu == 1  && nVetoEl == 0  ")
    #c.Print("nJets_mu.pdf")


print "___MUON CHANNEL___"
doCutFlow("mutH_edmntuples.root", mucuts)

print "___ELECTRON CHANNEL___"
doCutFlow("eltH_edmntuples.root", elcuts)

