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

# ====================================================
# Class Histo: to manage histograms and setting style
# ====================================================

class Histo:

    def __init__(self, name="", title="", nBins=100, xmin=0, xmax=100):
        self._name = name
        self._title = title
        self._nBins = nBins
        self._xmin = xmin
        self._xmax = xmax
        self._h = ROOT.TH1F(self._title, self._name, self._nBins, self._xmin, self._xmax)
        self._h.GetXaxis().SetLabelFont(42);
        self._h.GetYaxis().SetLabelFont(42);
        self._h.GetXaxis().SetTitleFont(42);
        self._h.GetYaxis().SetTitleFont(42);
        self._h.GetXaxis().SetTitleOffset(1.2);
        self._h.GetYaxis().SetTitleOffset(1.2);
        self._h.SetTitleFont(42);

    def SetStyle(self, color, XaxisTitle):
        self._h.SetLineColor(color)
        self._h.SetFillColor(color)
        self._h.SetFillStyle(3004)
        self._h.GetXaxis().SetTitle(XaxisTitle)
        nEvts = (self._h.GetXaxis().GetXmax() - self._h.GetXaxis().GetXmin()) / self._h.GetNbinsX()
        self._h.GetYaxis().SetTitle("number of events/"+ str.format("{0:.2f}", nEvts) +" GeV");

    def GetHisto(self):
        return self._h


# ====================================================
# Class Tree: to manage trees
# ====================================================


class Tree:

    def __init__(self, filename, treename):
        self._filename = filename
        self._treename = treename
        self._tree = None
        self._file = None
        self._outfile = None
        self._newtree = None

        
    def _openFile(self, filename = '', option = ''):
        if filename == '': filename = self._filename
        file = ROOT.TFile.Open(filename, option)
        if not file.__nonzero__() or not file.IsOpen():
            raise NameError('File '+filename+' not open')
        return file
    
    def initTree(self):
        self._file = self._openFile()
        self._tree = self._file.Get(self._treename)

    def GetTree(self):
        return self._tree

    def GetEntries(self, cut = ''):
        return self._tree.GetEntries(cut)

    def disconnect(self):
        self._newtree.Write()
        self._outfile.Close()
        self._file.Close()
        
        self._file = None
        self._tree = None
        self._outfile = None
        self._newtree = None
        
    def cloneTree(self, outfilename, branches = []):



        self._tree.SetBranchStatus('*'  ,0)        
        for b in branches:
            print"Branch Alias:", b
            bName = self._tree.GetAlias(b)
            print "Branch Name", bName
            self._tree.SetBranchStatus(bName,1)
            print "brach turned on"

        self._outfile = self._openFile(outfilename, 'recreate')            
        self._newtree = self._tree.CloneTree()
        print "tree cloned"
            ## BUT keep all branches "active" in the old tree
        self._tree.SetBranchStatus('*'  ,1)

            
    def filterTree(self, cut):
        self._tree.Draw(">>elist", cut, "entrylist")
        self._list = ROOT.TEntryList(ROOT.gDirectory.Get("elist") )
        self._tree.SetEntryList(self._list)
        return self._list


    def pruneClonedTree(self):

        for i in xrange(self._list.GetN()):
            
            self._tree.GetEntry(self._list.GetEntry(i))
            
            self._newtree.Fill()

        self.disconnect()
            
                                                        
# ====================================================
# Code to create a cutFlow
# ====================================================

    
cutNames = ["Trigger", "OneTightLepton", "LooseMuonVeto", "LooseElectronVeto", "nJets#ge 1", "nJets#ge 2", "nJets#ge 3", "nJets#ge 4"]
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


def _cutFlow(tree,cuts):

    histo = Histo("CutFlow", "CutFlow", len(cutNames), 0., len(cutNames))
    histo.SetStyle(ROOT.kBlue, "")
    h = histo.GetHisto()
    h.SetBinContent(1, tree.GetEntries())
    h.GetXaxis().SetBinLabel(1, cutNames[0])
    print 'Step 0: ', h.GetBinContent(1)
    cut = ''
    strcut = ''
    for i in range(len(cuts)):
        cut = cuts[i]
        strcut += cuts[i]
        strcut += " && "
        if(debug): print "CUT ----- ", strcut
        print "Step " + str(i+1) + ": " + str(tree.GetEntries(cut) )
        list = tree.filterTree(cut)
        h.SetBinContent(i+2, list.GetN())
        h.GetXaxis().SetBinLabel(i+2, cutNames[i+1])

    h.Draw()
    c.Print("cutFlow.pdf")
    return cut



    
def setAliases(t):
    t.SetAlias("nTightEl","floats_nTupleElectrons_tightElectronsE_SingleTop.@obj.size()")
    t.SetAlias("nTightMu","floats_nTupleMuons_tightMuonsE_SingleTop.@obj.size()")
    t.SetAlias("nVetoEl","floats_nTupleVetoElectrons_vetoElectronsE_SingleTop.@obj.size()")
    t.SetAlias("nVetoMu","floats_nTupleVetoMuons_vetoMuonsE_SingleTop.@obj.size()")
    t.SetAlias("nJets","floats_nTupleTopJetsPF_topJetsPFE_SingleTop.@obj.size()")


def doCutFlow(filename, cuts):

    tree = Tree(filename, "Events")
    tree.initTree()
    t = tree.GetTree()

    ### CLONE DOES NOT WORK
    #    tree.cloneTree("newtree.root", ["vetoMuonsE"])    
    #    file = ROOT.TFile(filename)
    #   t = file.Get("Events")
    setAliases(t)
    t.Draw("nJets")
    c.Print("nJets.pdf")
    cut = _cutFlow(tree, cuts)
    #t.Draw("nJets", "(nTightMu == 1 ) && nVetoMu == 1  && nVetoEl == 0  ")
    #c.Print("nJets_mu.pdf")
#    tree.pruneClonedTree()
    #    t.Draw("nJets")
    t.ls()
    tp = ROOT.TTreePlayer()
    tp = t.GetPlayer()
    tp.SetScanRedirect(ROOT.kTRUE) # You may have to cast t.GetPlayer() to a TTreePlayer*
    tp.SetScanFileName("output.txt")
    t.Scan("topJetsPFEventNumber")

    #c.Print("nJetsEntryList.pdf")

    #list.Print("all")







print "___MUON CHANNEL___"
doCutFlow("../mutH_edmntuples.root", mucuts)

print "___ELECTRON CHANNEL___"
doCutFlow("../eltH_edmntuples.root", elcuts)

