import ROOT


#variable


treeVar = "elePt";

nBin = 24;
xMin = 25.;
xMax = 265.;

nBinS = "24";
xMinS = "25.";
xMaxS = "265.";

#color = [kBlue,kGreen,kRed,kRed]

treePath = '/scratch/decosa/tH/WjetsIncl/'
plotPath = '/shome/dpinna/tH_analysis'


histoName = ['ttbar','VJetsIncl','VJetspt','ZZ']
hName = ['ttbar','VJetsIncl','VJetspt','ZZ']

title = 'Histo'


fileNames = 'Wjets-mg_rev468_tkF.root'
xTitle = 'Cut Flow' 
yTitle = 'Events / bin ' 

cutSelection = ['elePt>50','eleEta<5','elePhi<5','elePt>70','eleEta<2','elePhi<3','elePt>100','elePhi<2']

cutName = ["Trigger_cut ","Isol.Lepton_cut","LooseElectron_veto","LooseMuon_veto","JetMultiplicity>=1","JetMultiplicity>=2","JetMultiplicity>=3", "JetMultiplicity>=4"]

#sigma = 234.


#Load tree from root file
#-----------------------------
def getTree(fileName): 
    
    #tree.Reset();
    tree = ROOT.TChain('eventContent/BasicInfo');
    tree.Add(treePath+fileName);
    tree.SetDirectory(0);
    nEntries = tree.GetEntries();
    
    return tree
    del tree


#Load histo from root file
#-----------------------------

def getHisto(fileName, histoName):
    
    fName = treePath
    fName += fileName
    
    file =  ROOT.TFile(fName)
    histo = file.Get(histoName)
    histo.SetDirectory(0)
    file.Close()
    
    return histo
    del histo

def getHistoFromTree(fileName, cut, k, flav):
    
    nEvents = 0
    
    ss = ROOT.TEventList();
    Tree = getTree(fileName)
    Tree.Scan()
    
    
    Tree.Draw(">>ss", cut)
    Tree.SetEventList(ss)
    Tree.Scan()
    
    print fileName
    print cut
    print sigma
    
    eventList = ROOT.gDirectory.Get("ss")
    eventList.SetDirectory(0)
    
    return eventList

    del eventList
    del Tree


def CutSelectionNTupleProva():

    #ROOT.gROOT.SetStyle("Plain")
    c = ROOT.TCanvas(title,title, 800, 600)
    
    file = ROOT.TFile(treePath+fileNames)
    #print treePath+fileNames
    tree = file.Get('eventContent/BasicInfo')
    nEntries = tree.GetEntries();
    #print 'number of entries in the original tree: ', nEntries
    tree.ls()
    #tree = getTree(fileNames)
    
    histoCutFlow = ROOT.TH1F("histoCutFlow","histoCutFlow",10,0,10)
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetOptStat(0)

    histoCutFlow.SetTitle('')
    
    histoCutFlow.GetXaxis().SetTitle(xTitle)
    histoCutFlow.GetXaxis().SetLabelOffset(0.01)
    #histoCutFlow.GetXaxis().SetTitleOffset(0.015)
    histoCutFlow.GetXaxis().SetTitleSize(0.03)
    histoCutFlow.GetXaxis().SetLabelSize(0.035)
    
    histoCutFlow.GetYaxis().SetTitle(yTitle)
    histoCutFlow.GetYaxis().SetTitleOffset(1.2)
    histoCutFlow.GetYaxis().SetTitleSize(0.03)
    histoCutFlow.GetYaxis().SetLabelSize(0.025)

    for i in range(0,len(cutName)):
        print ' i: %d' %i
        if i==0:
            tree.Draw(">>ss", cutSelection[i])
        else:
            cutSelectionSum =''
            for k in range(i):
                print 'k %d ' %(k)
                print 'Selection to add %s' %(cutSelection[k])
                if k==0: cutSelectionSum += cutSelection[k]
                else: cutSelectionSum += ' && ' + cutSelection[k]  
                print 'Selection Sum: %s ' %(cutSelectionSum)
            tree.Draw(">>ss", cutSelectionSum)
            
        list = ROOT.TEventList(ROOT.gDirectory.Get("ss"))

        list.ls()
        
        tree.SetEventList(list)

        print 'Entries from tree with pt cut %d' %(tree.GetEntries())
        print 'Entries from list with pt cut %d' %(list.GetN())

        histoCutFlow.Fill(i,list.GetN())
        
        x = histoCutFlow.GetXaxis().SetBinLabel(i+1, cutName[i])

   
    histoCutFlow.Draw()
    integral = '%s: %f' %("integral", histoCutFlow.Integral())
    name = '%s/%s.pdf' %(plotPath,title)
    c.Print('provaCutFlow.pdf')
    c.Print('provaCutFlow.png')
    print integral


CutSelectionNTupleProva()        
 
